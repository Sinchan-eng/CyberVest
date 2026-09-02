"""Enterprise aggregation helpers shared across routers.

Enterprise exposure = Σ canonical asset EAL (one canonical Risk per asset),
which prevents double-counting (docs/04 section 7).
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Asset, Mitigation, Risk, Vulnerability
from app.services import risk_engine
from app.services.optimizer import Investment, optimize


def enterprise_exposure(db: Session) -> float:
    risks = db.execute(select(Risk)).scalars().all()
    return round(sum(r.eal for r in risks), 2)


def asset_contributors(db: Session) -> list[dict]:
    """Assets ranked by canonical EAL, with primary driver + vuln count."""
    rows = db.execute(select(Risk)).scalars().all()
    result = []
    for r in rows:
        asset = r.asset
        findings = r.detail.get("findings", []) if isinstance(r.detail, dict) else []
        top = max(findings, key=lambda f: f["eal"], default=None)
        drivers = top["drivers"] if top else []
        vuln_count = db.execute(
            select(Vulnerability).where(Vulnerability.asset_id == asset.id)
        ).scalars().all()
        result.append(
            {
                "asset_id": asset.id,
                "asset_ref": asset.ref,
                "asset_name": asset.name,
                "business_unit": asset.business_unit,
                "risk_level": risk_engine.risk_level(r.risk_score),
                "risk_score": r.risk_score,
                "financial_exposure": r.eal,
                "financial_impact": r.financial_impact,
                "probability": r.probability,
                "confidence": r.confidence,
                "primary_driver": (top["vuln_name"] if top else "None"),
                "drivers": drivers,
                "vulnerability_count": len(vuln_count),
            }
        )
    result.sort(key=lambda x: x["financial_exposure"], reverse=True)
    return result


def all_findings(db: Session) -> list[dict]:
    """Flattened per-finding modeled risks across all assets, ranked by EAL."""
    rows = db.execute(select(Risk)).scalars().all()
    findings: list[dict] = []
    for r in rows:
        asset = r.asset
        for f in (r.detail.get("findings", []) if isinstance(r.detail, dict) else []):
            findings.append(
                {
                    "vuln_ref": f["vuln_ref"],
                    "vuln_name": f["vuln_name"],
                    "asset_id": asset.id,
                    "asset_name": asset.name,
                    "business_unit": asset.business_unit,
                    "cvss": f["cvss"],
                    "severity": f["severity"],
                    "incident_probability": f["incident_probability"],
                    "financial_impact": f["financial_impact"],
                    "eal": f["eal"],
                    "control_effectiveness": f["control_effectiveness"],
                    "drivers": f["drivers"],
                }
            )
    findings.sort(key=lambda x: x["eal"], reverse=True)
    return findings


def candidate_investments(db: Session, risk_ids: list[int] | None = None) -> list[Investment]:
    stmt = select(Mitigation)
    mitigations = db.execute(stmt).scalars().all()
    if risk_ids:
        mitigations = [m for m in mitigations if m.risk_id in set(risk_ids)]
    return [
        Investment(
            ref=m.ref,
            mitigation_id=m.id,
            name=m.action_name,
            cost=m.cost,
            expected_risk_reduction=m.expected_risk_reduction,
            priority=m.priority,
            implementation_time=m.implementation_time,
        )
        for m in mitigations
    ]


def run_optimizer(db: Session, budget: float, risk_ids: list[int] | None = None,
                  max_recommendations: int | None = None) -> dict:
    before = enterprise_exposure(db)
    investments = candidate_investments(db, risk_ids)
    result = optimize(investments, budget, before, max_recommendations)
    return {
        "budget": result.budget,
        "selected_investments": result.selected,
        "recommendations": result.recommendations,
        "total_investment": result.total_investment,
        "expected_risk_reduction": result.expected_risk_reduction,
        "remaining_budget": result.remaining_budget,
        "before_exposure": result.before_exposure,
        "after_exposure": result.after_exposure,
        "percentage_reduction": result.percentage_reduction,
        "rosi": result.rosi,
    }
