"""SQLAlchemy ORM models mirroring docs/03-database-schema.md."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Stable demo identifier, e.g. "AST-001".
    ref: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    business_unit: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    criticality: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    financial_value: Mapped[float] = mapped_column(Float, nullable=False)
    downtime_cost_per_hour: Mapped[float] = mapped_column(Float, nullable=False)
    internet_exposure: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    data_sensitivity: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    vulnerabilities: Mapped[list["Vulnerability"]] = relationship(
        back_populates="asset", cascade="all, delete-orphan"
    )
    controls: Mapped[list["SecurityControl"]] = relationship(
        back_populates="asset", cascade="all, delete-orphan"
    )
    risks: Mapped[list["Risk"]] = relationship(
        back_populates="asset", cascade="all, delete-orphan"
    )


class Vulnerability(Base):
    __tablename__ = "vulnerabilities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ref: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    cve: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    cvss_score: Mapped[float] = mapped_column(Float, nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    exploitability: Mapped[float] = mapped_column(Float, nullable=False)
    threat_activity: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    nist_category: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    asset: Mapped["Asset"] = relationship(back_populates="vulnerabilities")


class SecurityControl(Base):
    __tablename__ = "security_controls"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ref: Mapped[str] = mapped_column(String(20), index=True)
    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id"), nullable=False, index=True
    )
    control_name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    effectiveness: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    framework_mapping: Mapped[str | None] = mapped_column(String(200), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    asset: Mapped["Asset"] = relationship(back_populates="controls")


class Risk(Base):
    __tablename__ = "risks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id"), nullable=False, index=True
    )
    probability: Mapped[float] = mapped_column(Float, nullable=False)
    financial_impact: Mapped[float] = mapped_column(Float, nullable=False)
    eal: Mapped[float] = mapped_column(Float, nullable=False)
    risk_score: Mapped[float] = mapped_column(Float, nullable=False, index=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    calculation_timestamp: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), index=True
    )
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    # Retained intermediate values (JSON) for explainability.
    detail: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

    asset: Mapped["Asset"] = relationship(back_populates="risks")
    mitigations: Mapped[list["Mitigation"]] = relationship(
        back_populates="risk", cascade="all, delete-orphan"
    )


class Mitigation(Base):
    __tablename__ = "mitigations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ref: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    risk_id: Mapped[int] = mapped_column(
        ForeignKey("risks.id"), nullable=False, index=True
    )
    action_name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    cost: Mapped[float] = mapped_column(Float, nullable=False, index=True)
    # Absolute expected risk reduction in INR (per docs/08 + docs/10).
    expected_risk_reduction: Mapped[float] = mapped_column(Float, nullable=False)
    rosi: Mapped[float] = mapped_column(Float, nullable=False)
    priority: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    implementation_time: Mapped[int] = mapped_column(Integer, nullable=False)
    nist_category: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    risk: Mapped["Risk"] = relationship(back_populates="mitigations")


class Simulation(Base):
    __tablename__ = "simulations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    baseline_exposure: Mapped[float] = mapped_column(Float, nullable=False)
    selected_mitigations: Mapped[list] = mapped_column(JSON, nullable=False)
    resulting_exposure: Mapped[float] = mapped_column(Float, nullable=False)
    risk_reduction: Mapped[float] = mapped_column(Float, nullable=False)
    budget: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), index=True
    )


class Framework(Base):
    __tablename__ = "frameworks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    controls: Mapped[list["FrameworkControl"]] = relationship(
        back_populates="framework", cascade="all, delete-orphan"
    )


class FrameworkControl(Base):
    __tablename__ = "framework_controls"
    __table_args__ = (
        UniqueConstraint("framework_id", "control_id", name="uq_framework_control"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    framework_id: Mapped[int] = mapped_column(
        ForeignKey("frameworks.id"), nullable=False, index=True
    )
    control_name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    control_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Derived mapping status: MAPPED | PARTIAL | UNMAPPED
    mapping_status: Mapped[str] = mapped_column(String(20), default="UNMAPPED")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    framework: Mapped["Framework"] = relationship(back_populates="controls")
