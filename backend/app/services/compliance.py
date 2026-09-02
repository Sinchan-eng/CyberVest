"""Framework-mapping layer (docs/09-compliance-mapping.md).

Kept behind a framework-independent interface so ISO 27001, CIS, RBI CSF,
and SEBI CSCRF can be added later without touching the risk engine.
Evidence-based: a control's mapping status is derived from the actual
seeded controls that map to each NIST CSF category, never asserted.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Framework, FrameworkControl, SecurityControl


def derive_mapping_status(effectiveness_statuses: list[str]) -> str:
    """MAPPED if any implemented control maps to the category, PARTIAL if
    only partial controls exist, UNMAPPED if none."""
    if not effectiveness_statuses:
        return "UNMAPPED"
    normalized = [s.upper() for s in effectiveness_statuses]
    if "IMPLEMENTED" in normalized:
        return "MAPPED"
    if "PARTIAL" in normalized:
        return "PARTIAL"
    return "UNMAPPED"


def refresh_mapping_status(db: Session) -> None:
    """Recompute each NIST control's mapping status from seeded controls."""
    # Group seeded security controls by their NIST framework_mapping category.
    controls = db.execute(select(SecurityControl)).scalars().all()
    by_category: dict[str, list[str]] = {}
    for c in controls:
        if c.framework_mapping:
            by_category.setdefault(c.framework_mapping, []).append(c.status)

    for fc in db.execute(select(FrameworkControl)).scalars().all():
        statuses = by_category.get(fc.control_id, [])
        fc.mapping_status = derive_mapping_status(statuses)
    db.commit()


def get_framework(db: Session, slug: str) -> Framework | None:
    normalized = slug.strip().lower().replace(" ", "-").replace("%20", "-")
    return db.execute(
        select(Framework).where(Framework.slug == normalized)
    ).scalar_one_or_none()


def mapped_evidence(db: Session, category: str) -> list[dict]:
    """Return the seeded security controls that provide evidence for a
    NIST category (used in the control detail drawer)."""
    controls = db.execute(
        select(SecurityControl).where(SecurityControl.framework_mapping == category)
    ).scalars().all()
    return [
        {
            "control_ref": c.ref,
            "control_name": c.control_name,
            "asset_id": c.asset_id,
            "effectiveness": c.effectiveness,
            "status": c.status,
        }
        for c in controls
    ]
