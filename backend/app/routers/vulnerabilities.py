"""Vulnerabilities endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.errors import APIError
from app.models import Vulnerability
from app.schemas import VulnerabilityListResponse, VulnerabilityResponse

router = APIRouter()

VALID_SEVERITY = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
VALID_STATUS = {"OPEN", "MITIGATED", "ACCEPTED", "CLOSED"}


@router.get("/vulnerabilities", response_model=VulnerabilityListResponse)
def list_vulnerabilities(
    asset_id: int | None = Query(default=None, gt=0),
    severity: str | None = Query(default=None),
    status: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> VulnerabilityListResponse:
    if severity and severity.upper() not in VALID_SEVERITY:
        raise APIError("VALIDATION_ERROR", "Invalid severity filter")
    if status and status.upper() not in VALID_STATUS:
        raise APIError("VALIDATION_ERROR", "Invalid status filter")

    stmt = select(Vulnerability)
    count_stmt = select(func.count()).select_from(Vulnerability)
    if asset_id:
        stmt = stmt.where(Vulnerability.asset_id == asset_id)
        count_stmt = count_stmt.where(Vulnerability.asset_id == asset_id)
    if severity:
        stmt = stmt.where(Vulnerability.severity == severity.upper())
        count_stmt = count_stmt.where(Vulnerability.severity == severity.upper())
    if status:
        stmt = stmt.where(Vulnerability.status == status.upper())
        count_stmt = count_stmt.where(Vulnerability.status == status.upper())

    total = db.execute(count_stmt).scalar_one()
    items = db.execute(
        stmt.order_by(Vulnerability.cvss_score.desc(), Vulnerability.ref).limit(limit).offset(offset)
    ).scalars().all()
    return VulnerabilityListResponse(items=items, total=total, limit=limit, offset=offset)


@router.get("/vulnerabilities/{vuln_id}", response_model=VulnerabilityResponse)
def get_vulnerability(vuln_id: int, db: Session = Depends(get_db)) -> VulnerabilityResponse:
    vuln = db.get(Vulnerability, vuln_id)
    if vuln is None:
        raise APIError("NOT_FOUND", f"Vulnerability {vuln_id} not found")
    return vuln
