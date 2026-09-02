"""Pydantic request/response contracts (docs/05-api-specification.md)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# --- Assets ---------------------------------------------------------------
class AssetResponse(ORMModel):
    id: int
    ref: str
    name: str
    type: str
    business_unit: str
    criticality: str
    financial_value: float
    downtime_cost_per_hour: float
    internet_exposure: bool
    data_sensitivity: str
    description: str | None = None


class AssetListResponse(BaseModel):
    items: list[AssetResponse]
    total: int
    limit: int
    offset: int


class VulnerabilitySummary(BaseModel):
    id: int
    ref: str
    name: str
    severity: str
    cvss_score: float
    status: str


class ControlSummary(BaseModel):
    id: int
    ref: str
    control_name: str
    effectiveness: float
    status: str


class LatestRisk(BaseModel):
    risk_score: float
    eal: float
    confidence: float
    financial_impact: float
    probability: float


class AssetDetailResponse(AssetResponse):
    vulnerabilities: list[VulnerabilitySummary] = []
    controls: list[ControlSummary] = []
    control_effectiveness: float | None = None
    latest_risk: LatestRisk | None = None
    risk_drivers: list[str] = []


# --- Vulnerabilities ------------------------------------------------------
class VulnerabilityResponse(ORMModel):
    id: int
    ref: str
    asset_id: int
    name: str
    cve: str | None = None
    cvss_score: float
    severity: str
    exploitability: float
    threat_activity: float
    status: str
    nist_category: str | None = None


class VulnerabilityListResponse(BaseModel):
    items: list[VulnerabilityResponse]
    total: int
    limit: int
    offset: int


# --- Risks ----------------------------------------------------------------
class RiskResponse(ORMModel):
    id: int
    asset_id: int
    probability: float
    financial_impact: float
    eal: float
    risk_score: float
    confidence: float
    calculation_timestamp: datetime
    explanation: str


class MitigationSummary(BaseModel):
    id: int
    action_name: str
    cost: float
    expected_risk_reduction: float
    rosi: float
    priority: str


class RiskDetailResponse(RiskResponse):
    detail: dict = {}
    mitigations: list[MitigationSummary] = []


class RiskListResponse(BaseModel):
    items: list[RiskResponse]
    total: int
    limit: int
    offset: int


# --- Findings (risk analysis per-finding view) ----------------------------
class FindingResponse(BaseModel):
    vuln_ref: str
    vuln_name: str
    asset_id: int
    asset_name: str
    business_unit: str
    cvss: float
    severity: str
    incident_probability: float
    financial_impact: float
    eal: float
    control_effectiveness: float
    drivers: list[str]


class FindingListResponse(BaseModel):
    items: list[FindingResponse]
    total: int


# --- Recommendations ------------------------------------------------------
class RecommendationResponse(ORMModel):
    id: int
    ref: str
    risk_id: int
    action_name: str
    description: str
    cost: float
    expected_risk_reduction: float
    rosi: float
    priority: str
    implementation_time: int
    nist_category: str | None = None


class RecommendationListResponse(BaseModel):
    items: list[RecommendationResponse]
    total: int
    limit: int
    offset: int


# --- Dashboard ------------------------------------------------------------
class TrendPoint(BaseModel):
    date: str
    risk_score: float
    eal: float


class Contributor(BaseModel):
    asset_id: int
    asset_ref: str
    asset_name: str
    business_unit: str
    risk_level: str
    risk_score: float
    financial_exposure: float
    primary_driver: str
    vulnerability_count: int


class DashboardAction(BaseModel):
    recommendation_id: int
    action_name: str
    priority: str
    cost: float
    expected_risk_reduction: float
    rosi: float


class DashboardResponse(BaseModel):
    enterprise_risk_score: float
    enterprise_risk_level: str
    total_financial_exposure: float
    enterprise_eal: float
    critical_assets: int
    critical_vulnerabilities: int
    risk_trend: list[TrendPoint]
    top_contributors: list[Contributor]
    recommended_actions: list[DashboardAction]
    data_status: str
    last_updated: datetime


# --- Optimize -------------------------------------------------------------
class OptimizeRequest(BaseModel):
    budget: float = Field(ge=0)
    risk_ids: list[int] | None = None
    max_recommendations: int = Field(default=10, ge=1, le=50)


class OptimizeRecommendation(BaseModel):
    mitigation_id: int
    investment_id: str
    action_name: str
    decision: str
    reason: str
    cost: float
    expected_risk_reduction: float
    risk_reduction_per_rupee: float
    rosi: float | None
    priority: str


class SelectedInvestment(BaseModel):
    mitigation_id: int
    investment_id: str
    action_name: str
    cost: float
    expected_risk_reduction: float
    rosi: float | None
    priority: str


class OptimizeResponse(BaseModel):
    budget: float
    allocated: float
    remaining: float
    baseline_eal: float
    projected_eal: float
    expected_loss_reduction: float
    risk_reduction: float
    selected_investments: list[SelectedInvestment]
    recommendations: list[OptimizeRecommendation]
    rosi: float | None


# --- Simulate -------------------------------------------------------------
class SimulateRequest(BaseModel):
    budget: float = Field(ge=0)
    mitigation_ids: list[int] = Field(default_factory=list)
    risk_ids: list[int] | None = None


class SelectedMitigation(BaseModel):
    mitigation_id: int
    action_name: str
    cost: float


class SimulateResponse(BaseModel):
    simulation_id: int
    baseline_exposure: float
    selected_mitigations: list[SelectedMitigation]
    resulting_exposure: float
    risk_reduction: float
    budget: float
    timestamp: datetime


# --- AI -------------------------------------------------------------------
class AIQueryRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2000)
    context: dict[str, Any] | None = None


# --- Compliance -----------------------------------------------------------
class FrameworkResponse(ORMModel):
    id: int
    name: str
    slug: str
    version: str | None = None
    description: str | None = None


class FrameworkListResponse(BaseModel):
    items: list[FrameworkResponse]


class FrameworkControlResponse(ORMModel):
    id: int
    framework_id: int
    control_name: str
    control_id: str
    description: str | None = None
    mapping_status: str


class ComplianceResponse(BaseModel):
    framework: FrameworkResponse
    controls: list[FrameworkControlResponse]
