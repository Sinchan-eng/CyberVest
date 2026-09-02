"""Assets endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.errors import APIError
from app.models import Asset, Risk
from app.schemas import AssetDetailResponse, AssetListResponse
from app.services import risk_engine

router = APIRouter()


@router.get("/assets", response_model=AssetListResponse)
def list_assets(
    business_unit: str | None = Query(default=None),
    criticality: str | None = Query(default=None),
    search: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> AssetListResponse:
    stmt = select(Asset)
    count_stmt = select(func.count()).select_from(Asset)
    if business_unit:
        stmt = stmt.where(Asset.business_unit == business_unit)
        count_stmt = count_stmt.where(Asset.business_unit == business_unit)
    if criticality:
        stmt = stmt.where(Asset.criticality == criticality.upper())
        count_stmt = count_stmt.where(Asset.criticality == criticality.upper())
    if search:
        like = f"%{search}%"
        stmt = stmt.where(Asset.name.ilike(like))
        count_stmt = count_stmt.where(Asset.name.ilike(like))

    total = db.execute(count_stmt).scalar_one()
    items = db.execute(stmt.order_by(Asset.ref).limit(limit).offset(offset)).scalars().all()
    return AssetListResponse(items=items, total=total, limit=limit, offset=offset)


@router.get("/assets/{asset_id}", response_model=AssetDetailResponse)
def get_asset(asset_id: int, db: Session = Depends(get_db)) -> AssetDetailResponse:
    asset = db.get(Asset, asset_id)
    if asset is None:
        raise APIError("NOT_FOUND", f"Asset {asset_id} not found")

    control_effectiveness = risk_engine.compute_control_effectiveness(asset.controls)
    latest = db.execute(
        select(Risk).where(Risk.asset_id == asset.id).order_by(Risk.calculation_timestamp.desc())
    ).scalars().first()

    drivers: list[str] = []
    latest_payload = None
    if latest is not None:
        findings = latest.detail.get("findings", []) if isinstance(latest.detail, dict) else []
        top = max(findings, key=lambda f: f["eal"], default=None)
        drivers = top["drivers"] if top else []
        latest_payload = {
            "risk_score": latest.risk_score,
            "eal": latest.eal,
            "confidence": latest.confidence,
            "financial_impact": latest.financial_impact,
            "probability": latest.probability,
        }

    return AssetDetailResponse(
        id=asset.id, ref=asset.ref, name=asset.name, type=asset.type,
        business_unit=asset.business_unit, criticality=asset.criticality,
        financial_value=asset.financial_value,
        downtime_cost_per_hour=asset.downtime_cost_per_hour,
        internet_exposure=asset.internet_exposure,
        data_sensitivity=asset.data_sensitivity, description=asset.description,
        vulnerabilities=[
            {"id": v.id, "ref": v.ref, "name": v.name, "severity": v.severity,
             "cvss_score": v.cvss_score, "status": v.status}
            for v in sorted(asset.vulnerabilities, key=lambda x: x.cvss_score, reverse=True)
        ],
        controls=[
            {"id": c.id, "ref": c.ref, "control_name": c.control_name,
             "effectiveness": c.effectiveness, "status": c.status}
            for c in asset.controls
        ],
        control_effectiveness=round(control_effectiveness, 4),
        latest_risk=latest_payload,
        risk_drivers=drivers,
    )
