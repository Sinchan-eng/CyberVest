"""Deterministic database seeding + risk precomputation.

Running this loads the demo dataset (docs/10), runs the authoritative risk
engine over every asset, stores one canonical Risk row per asset, links
the 20 mitigation actions to the relevant asset risks, and seeds the NIST
CSF framework with derived mapping status.
"""

from __future__ import annotations

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine
from app.models import (
    Asset,
    Framework,
    FrameworkControl,
    Mitigation,
    Risk,
    SecurityControl,
    Vulnerability,
)
from app.services import compliance, risk_engine
from app.services.optimizer import _rosi
from app import seed_data


def reset_schema() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def _clear(db: Session) -> None:
    for model in (Mitigation, Risk, SecurityControl, Vulnerability, Asset, FrameworkControl, Framework):
        db.execute(delete(model))
    db.commit()


def seed(db: Session) -> None:
    _clear(db)

    # --- Assets ---
    asset_by_ref: dict[str, Asset] = {}
    for (ref, name, type_, bu, crit, fv, dt, ie, ds) in seed_data.ASSETS:
        asset = Asset(
            ref=ref, name=name, type=type_, business_unit=bu, criticality=crit,
            financial_value=fv, downtime_cost_per_hour=dt, internet_exposure=ie,
            data_sensitivity=ds, description=f"Simulated demo asset: {name}.",
        )
        db.add(asset)
        asset_by_ref[ref] = asset
    db.flush()

    # --- Vulnerabilities ---
    for (ref, asset_ref, name, cvss, sev, likelihood, status) in seed_data.VULNERABILITIES:
        db.add(
            Vulnerability(
                ref=ref, asset_id=asset_by_ref[asset_ref].id, name=name,
                cve=None, cvss_score=cvss, severity=sev,
                exploitability=likelihood, threat_activity=likelihood, status=status,
                nist_category=seed_data.VULN_NIST.get(ref),
            )
        )

    # --- Security controls ---
    for (ref, asset_ref, cname, eff, status, nist) in seed_data.CONTROLS:
        db.add(
            SecurityControl(
                ref=ref, asset_id=asset_by_ref[asset_ref].id, control_name=cname,
                effectiveness=eff, status=status, framework_mapping=nist,
            )
        )
    db.flush()

    # --- Compute risks (authoritative engine) ---
    risk_by_asset_ref: dict[str, Risk] = {}
    for ref, asset in asset_by_ref.items():
        vulns = db.execute(
            select(Vulnerability).where(Vulnerability.asset_id == asset.id)
        ).scalars().all()
        controls = db.execute(
            select(SecurityControl).where(SecurityControl.asset_id == asset.id)
        ).scalars().all()
        result = risk_engine.compute_asset_risk(asset, vulns, controls)
        risk = Risk(
            asset_id=asset.id,
            probability=result.probability,
            financial_impact=result.financial_impact,
            eal=result.eal,
            risk_score=result.risk_score,
            confidence=result.confidence,
            explanation=result.explanation,
            detail={
                **result.detail,
                "findings": [
                    {
                        "vuln_ref": f.vuln_ref,
                        "vuln_name": f.vuln_name,
                        "cvss": f.cvss,
                        "severity": f.severity,
                        "cvss_norm": f.cvss_norm,
                        "criticality_factor": f.criticality_factor,
                        "exposure_factor": f.exposure_factor,
                        "exploitability": f.exploitability,
                        "threat_activity": f.threat_activity,
                        "data_sensitivity_factor": f.data_sensitivity_factor,
                        "control_effectiveness": f.control_effectiveness,
                        "base_probability": f.base_probability,
                        "multiplier": f.multiplier,
                        "pre_control_probability": f.pre_control_probability,
                        "incident_probability": f.incident_probability,
                        "financial_impact": f.financial_impact,
                        "eal": f.eal,
                        "drivers": f.drivers,
                    }
                    for f in result.findings
                ],
            },
        )
        db.add(risk)
        risk_by_asset_ref[ref] = risk
    db.flush()

    # --- Mitigations (linked to target asset's risk) ---
    for (ref, target_ref, action, cost, reduction, days, priority, nist) in seed_data.MITIGATIONS:
        risk = risk_by_asset_ref[target_ref]
        db.add(
            Mitigation(
                ref=ref, risk_id=risk.id, action_name=action,
                description=f"{action} targeting {risk.asset.name}. Simulated candidate investment.",
                cost=cost, expected_risk_reduction=reduction,
                rosi=_rosi(reduction, cost) or 0.0, priority=priority,
                implementation_time=days, nist_category=nist,
            )
        )

    # --- NIST CSF framework ---
    fw = Framework(
        name=seed_data.NIST_FRAMEWORK["name"],
        slug=seed_data.NIST_FRAMEWORK["slug"],
        version=seed_data.NIST_FRAMEWORK["version"],
        description=seed_data.NIST_FRAMEWORK["description"],
    )
    db.add(fw)
    db.flush()
    for ctl in seed_data.NIST_CONTROLS:
        db.add(
            FrameworkControl(
                framework_id=fw.id,
                control_name=ctl["control_name"],
                control_id=ctl["control_id"],
                description=ctl["description"],
                mapping_status="UNMAPPED",
            )
        )
    db.commit()

    compliance.refresh_mapping_status(db)


def run() -> None:
    reset_schema()
    db = SessionLocal()
    try:
        seed(db)
        print("Seeded CyberQuant AI demo dataset.")
    finally:
        db.close()


if __name__ == "__main__":
    run()
