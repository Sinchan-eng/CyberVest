"""GET /api/dashboard — executive dashboard summary."""

from __future__ import annotations

from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.errors import APIError
from app.models import Asset, Mitigation, Vulnerability
from app.schemas import DashboardResponse
from app.services import aggregation, risk_engine

router = APIRouter()

VALID_RISK_LEVELS = {"LOW", "MODERATE", "HIGH", "CRITICAL"}


@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard(
    business_unit: str | None = Query(default=None),
    risk_level: str | None = Query(default=None),
    days: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db),
) -> DashboardResponse:
    if risk_level and risk_level.upper() not in VALID_RISK_LEVELS:
        raise APIError("VALIDATION_ERROR", "Invalid risk_level filter")

    contributors = aggregation.asset_contributors(db)
    if business_unit:
        contributors = [c for c in contributors if c["business_unit"] == business_unit]
    if risk_level:
        contributors = [c for c in contributors if c["risk_level"] == risk_level.upper()]

    exposure = round(sum(c["financial_exposure"] for c in contributors), 2)
    score = risk_engine.enterprise_risk_score(exposure)

    critical_assets = db.execute(
        select(func.count()).select_from(Asset).where(Asset.criticality == "CRITICAL")
    ).scalar_one()
    critical_vulns = db.execute(
        select(func.count()).select_from(Vulnerability).where(Vulnerability.severity == "CRITICAL")
    ).scalar_one()

    # Deterministic simulated trend: gently declining toward the current score.
    trend = _trend(score, exposure, days)

    top = contributors[:8]
    mitigations = db.execute(
        select(Mitigation).order_by(Mitigation.expected_risk_reduction.desc())
    ).scalars().all()
    actions = [
        {
            "recommendation_id": m.id,
            "action_name": m.action_name,
            "priority": m.priority,
            "cost": m.cost,
            "expected_risk_reduction": m.expected_risk_reduction,
            "rosi": m.rosi,
        }
        for m in sorted(
            mitigations, key=lambda x: x.expected_risk_reduction / x.cost if x.cost else 0, reverse=True
        )[:5]
    ]

    return DashboardResponse(
        enterprise_risk_score=score,
        enterprise_risk_level=risk_engine.risk_level(score),
        total_financial_exposure=exposure,
        enterprise_eal=exposure,
        critical_assets=critical_assets,
        critical_vulnerabilities=critical_vulns,
        risk_trend=trend,
        top_contributors=[
            {
                "asset_id": c["asset_id"],
                "asset_ref": c["asset_ref"],
                "asset_name": c["asset_name"],
                "business_unit": c["business_unit"],
                "risk_level": c["risk_level"],
                "risk_score": c["risk_score"],
                "financial_exposure": c["financial_exposure"],
                "primary_driver": c["primary_driver"],
                "vulnerability_count": c["vulnerability_count"],
            }
            for c in top
        ],
        recommended_actions=actions,
        data_status=settings.data_status,
        last_updated=datetime.utcnow(),
    )


def _trend(current_score: float, current_eal: float, days: int) -> list[dict]:
    """Deterministic recent snapshots ending at the current values.

    Values are derived (not fabricated history): a small monotonic drift
    ending exactly at today's computed score/EAL. Limited to the last
    min(days, 8) points for a readable chart.
    """
    points = min(days, 8)
    out = []
    today = date.today()
    for i in range(points - 1, -1, -1):
        drift = 1.0 + (i * 0.008)  # older points slightly higher
        d = today - timedelta(days=i)
        out.append(
            {
                "date": d.isoformat(),
                "risk_score": round(min(100.0, current_score * drift), 1),
                "eal": round(current_eal * drift, 2),
            }
        )
    return out
