"""Deterministic risk engine (authoritative — docs/04-risk-engine.md).

This module is the single source of truth for CyberQuant AI risk
calculations. It is pure/deterministic: identical inputs always produce
identical outputs, and every intermediate value is retained for
explainability.

Modeling decisions (documented, so numbers are auditable):

* One canonical modeled risk item is produced per **open finding**. This
  avoids double-counting: an asset's financial impact is *partitioned*
  across its open findings by each finding's (cvss x likelihood) weight,
  so summing finding-level EAL yields the asset EAL, and summing asset
  EAL yields enterprise exposure.
* Financial impact for an asset is decomposed into the five components
  named by the spec (downtime, data breach, recovery, regulatory,
  reputation), derived deterministically from the asset's supplied
  financial value, downtime cost, and data sensitivity.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.config import settings

# --- Normalization tables (docs/04 section 2) -----------------------------
DATA_SENSITIVITY_FACTOR = {
    "PUBLIC": 0.0,
    "INTERNAL": 0.33,
    "CONFIDENTIAL": 0.66,
    "RESTRICTED": 1.0,
    # DB enum aliases
    "LOW": 0.0,
    "MEDIUM": 0.5,
    "HIGH": 1.0,
}

CRITICALITY_LEVEL = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 5}

CONTROL_STATUS_FACTOR = {
    "IMPLEMENTED": 1.0,
    "PARTIAL": 0.5,
    "PLANNED": 0.0,
    "FAILED": 0.0,
}


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


@dataclass
class FindingRisk:
    vuln_ref: str
    vuln_name: str
    cvss: float
    severity: str
    # normalized factors
    cvss_norm: float
    criticality_factor: float
    exposure_factor: float
    exploitability: float
    threat_activity: float
    data_sensitivity_factor: float
    control_effectiveness: float
    # intermediate probability values
    base_probability: float
    multiplier: float
    pre_control_probability: float
    incident_probability: float
    # financials
    financial_impact: float
    eal: float
    drivers: list[str]


@dataclass
class AssetRisk:
    probability: float  # blended (eal / financial_impact)
    financial_impact: float
    financial_components: dict
    eal: float
    risk_score: float
    confidence: float
    explanation: str
    findings: list[FindingRisk] = field(default_factory=list)
    detail: dict = field(default_factory=dict)


def compute_control_effectiveness(controls: list) -> float:
    """Combine an asset's controls into a single effectiveness K in [0,1].

    Uses a complementary-product combination so multiple partial controls
    contribute without exceeding 1.0::

        K = 1 - product(1 - eff_i * status_factor_i)
    """
    remaining = 1.0
    for c in controls:
        factor = CONTROL_STATUS_FACTOR.get(c.status.upper(), 0.0)
        remaining *= 1.0 - clamp(c.effectiveness * factor)
    return clamp(1.0 - remaining)


def _base_probability(cvss: float) -> float:
    cvss_clamped = clamp(cvss, 0.0, 10.0)
    return settings.base_probability_floor + (cvss_clamped / 10.0) * settings.base_probability_cvss_weight


def _multiplier(c: float, e: float, x: float, t: float, d: float) -> float:
    return (
        1.0
        + settings.multiplier_criticality * c
        + settings.multiplier_exposure * e
        + settings.multiplier_exploitability * x
        + settings.multiplier_threat * t
        + settings.multiplier_data_sensitivity * d
    )


def _financial_components(asset) -> dict:
    """Deterministic decomposition of an asset's incident financial impact.

    All values in INR. Derived from supplied asset inputs so they remain
    reproducible and clearly *simulated*.
    """
    fv = max(0.0, asset.financial_value)
    downtime = max(0.0, asset.downtime_cost_per_hour)
    sens = DATA_SENSITIVITY_FACTOR.get(asset.data_sensitivity.upper(), 0.5)
    data_breach = fv * sens * 0.40
    recovery = fv * 0.05
    regulatory = fv * sens * 0.10
    reputation = fv * 0.10
    total = downtime + data_breach + recovery + regulatory + reputation
    return {
        "downtime_cost": round(downtime, 2),
        "data_breach_cost": round(data_breach, 2),
        "recovery_cost": round(recovery, 2),
        "regulatory_cost": round(regulatory, 2),
        "reputation_business_impact": round(reputation, 2),
        "total": round(total, 2),
    }


def _drivers(cvss: float, exposure: float, criticality_level: int, k: float) -> list[str]:
    drivers: list[str] = []
    if cvss >= 9.0:
        drivers.append(f"CVSS {cvss}")
    elif cvss >= 7.0:
        drivers.append(f"High CVSS {cvss}")
    if exposure >= 1.0:
        drivers.append("HIGH internet exposure")
    if criticality_level >= 5:
        drivers.append("Asset criticality 5/5")
    elif criticality_level >= 3:
        drivers.append(f"Asset criticality {criticality_level}/5")
    if k < 0.4:
        drivers.append("Low control effectiveness")
    return drivers


def compute_asset_risk(asset, vulnerabilities: list, controls: list) -> AssetRisk:
    """Run the full deterministic pipeline for one asset."""
    k = compute_control_effectiveness(controls)
    components = _financial_components(asset)
    asset_impact = components["total"]

    crit_level = CRITICALITY_LEVEL.get(asset.criticality.upper(), 1)
    c = clamp((crit_level - 1) / 4.0)
    e = 1.0 if asset.internet_exposure else 0.0
    d = clamp(DATA_SENSITIVITY_FACTOR.get(asset.data_sensitivity.upper(), 0.5))

    open_vulns = [v for v in vulnerabilities if v.status.upper() == "OPEN"]

    # Partition asset financial impact across open findings by weight.
    weights = {v.ref: max(0.0, v.cvss_score) * clamp(v.threat_activity) for v in open_vulns}
    weight_total = sum(weights.values()) or 1.0

    findings: list[FindingRisk] = []
    asset_eal = 0.0
    for v in open_vulns:
        x = clamp(v.exploitability)
        t = clamp(v.threat_activity)
        base = _base_probability(v.cvss_score)
        mult = _multiplier(c, e, x, t, d)
        pre = clamp(base * mult)
        incident = clamp(pre * (1.0 - k))
        share = weights[v.ref] / weight_total
        f_impact = round(asset_impact * share, 2)
        f_eal = round(incident * f_impact, 2)
        asset_eal += f_eal
        findings.append(
            FindingRisk(
                vuln_ref=v.ref,
                vuln_name=v.name,
                cvss=v.cvss_score,
                severity=v.severity,
                cvss_norm=round(clamp(v.cvss_score / 10.0), 4),
                criticality_factor=round(c, 4),
                exposure_factor=e,
                exploitability=round(x, 4),
                threat_activity=round(t, 4),
                data_sensitivity_factor=round(d, 4),
                control_effectiveness=round(k, 4),
                base_probability=round(base, 4),
                multiplier=round(mult, 4),
                pre_control_probability=round(pre, 4),
                incident_probability=round(incident, 4),
                financial_impact=f_impact,
                eal=f_eal,
                drivers=_drivers(v.cvss_score, e, crit_level, k),
            )
        )

    asset_eal = round(asset_eal, 2)
    blended_probability = round(asset_eal / asset_impact, 4) if asset_impact > 0 else 0.0
    risk_score = _asset_risk_score(asset_eal)
    confidence = _confidence(asset, open_vulns, k)
    explanation = _asset_explanation(asset, findings, asset_eal, blended_probability, k)

    return AssetRisk(
        probability=blended_probability,
        financial_impact=asset_impact,
        financial_components=components,
        eal=asset_eal,
        risk_score=risk_score,
        confidence=confidence,
        explanation=explanation,
        findings=findings,
        detail={
            "control_effectiveness": round(k, 4),
            "criticality_factor": round(c, 4),
            "exposure_factor": e,
            "data_sensitivity_factor": round(d, 4),
            "financial_components": components,
            "open_finding_count": len(open_vulns),
            "assumptions": [
                "Annualized MVP probability model; not statistically calibrated.",
                "Financial values are simulated demo inputs, not measured losses.",
                "Asset financial impact is partitioned across open findings to avoid double-counting.",
            ],
        },
    )


def _asset_risk_score(asset_eal: float) -> float:
    """Per-asset 0-100 score, normalized against a per-asset reference.

    Uses one tenth of the enterprise reference exposure as the per-asset
    reference so individual critical assets can reach the upper bands.
    """
    per_asset_reference = settings.reference_exposure / 10.0
    return round(min(100.0, 100.0 * asset_eal / per_asset_reference), 1)


def enterprise_risk_score(exposure: float) -> float:
    """0-100 enterprise risk score (docs/04 section 8)."""
    reference = settings.reference_exposure
    if reference <= 0:
        raise ValueError("reference_exposure must be greater than 0")
    return round(min(100.0, 100.0 * exposure / reference), 1)


def risk_level(score: float) -> str:
    if score >= 75:
        return "CRITICAL"
    if score >= 50:
        return "HIGH"
    if score >= 25:
        return "MODERATE"
    return "LOW"


def _confidence(asset, open_vulns: list, k: float) -> float:
    """Data-completeness confidence in [0,1] (docs/04 section 10)."""
    present = 0
    total = 9
    # asset-level required inputs
    present += 1 if asset.financial_value is not None else 0
    present += 1 if asset.downtime_cost_per_hour is not None else 0
    present += 1 if asset.internet_exposure is not None else 0
    present += 1 if asset.data_sensitivity else 0
    present += 1 if asset.criticality else 0
    present += 1 if k is not None else 0
    # finding-level required inputs (present if any open finding carries them)
    if open_vulns:
        present += 1 if all(v.cvss_score is not None for v in open_vulns) else 0
        present += 1 if all(v.exploitability is not None for v in open_vulns) else 0
        present += 1 if all(v.threat_activity is not None for v in open_vulns) else 0
    return round(present / total, 2)


def _asset_explanation(asset, findings: list, asset_eal: float, prob: float, k: float) -> str:
    if not findings:
        return f"{asset.name} has no open findings in the current modeled dataset."
    top = max(findings, key=lambda f: f.eal)
    driver_text = ", ".join(top.drivers) if top.drivers else "the modeled risk factors"
    return (
        f"{asset.name} carries a modeled Expected Annual Loss of the aggregated open findings. "
        f"The largest contributor is '{top.vuln_name}' (CVSS {top.cvss}) with an estimated "
        f"incident probability of {round(top.incident_probability * 100)}%. "
        f"Key risk drivers: {driver_text}. "
        f"Aggregate control effectiveness on this asset is {round(k * 100)}%."
    )
