"""Deterministic AI decision engine (docs/07-ai-decision-engine.md).

The MVP works WITHOUT an external LLM. This module classifies a question
into a deterministic intent, retrieves structured backend data, applies
deterministic decision logic, and returns a grounded, auditable answer.

Every number returned exists in the retrieved source data; no CVEs,
losses, or facts are invented.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field

from app.config import settings

# --- Intents --------------------------------------------------------------
HIGHEST_FINANCIAL_RISK = "HIGHEST_FINANCIAL_RISK"
TOP_VULNERABILITY = "TOP_VULNERABILITY"
MOST_EXPOSED_ASSET = "MOST_EXPOSED_ASSET"
RECOMMENDED_PRIORITY = "RECOMMENDED_PRIORITY"
BUDGET_RISK_REDUCTION = "BUDGET_RISK_REDUCTION"
UNSUPPORTED = "UNSUPPORTED"


@dataclass
class Evidence:
    label: str
    value: str
    sourceId: str


@dataclass
class AIResponse:
    answer: str
    keyEvidence: list[dict] = field(default_factory=list)
    riskDrivers: list[str] = field(default_factory=list)
    recommendation: str | None = None
    estimatedImpact: dict | None = None
    confidence: float | None = None
    limitations: list[str] = field(default_factory=list)
    dataStatus: str = settings.data_status
    sourceIds: list[str] = field(default_factory=list)
    sources: list[dict] = field(default_factory=list)
    ai_available: bool = False


def format_inr(value: float | None) -> str:
    if value is None:
        return "unavailable"
    # Indian grouping (lakh/crore) for display.
    n = int(round(value))
    s = str(abs(n))
    if len(s) > 3:
        last3 = s[-3:]
        rest = s[:-3]
        parts = []
        while len(rest) > 2:
            parts.insert(0, rest[-2:])
            rest = rest[:-2]
        if rest:
            parts.insert(0, rest)
        s = ",".join(parts) + "," + last3
    sign = "-" if n < 0 else ""
    return f"₹{sign}{s}"


def detect_intent(question: str) -> str:
    q = question.lower().strip()
    if re.search(r"\b(budget|lakh|crore|spend|₹|\brs\b|rupee)\b", q) and re.search(
        r"\b(reduce|reduc|invest|spend|budget)\b", q
    ):
        return BUDGET_RISK_REDUCTION
    if "vulnerab" in q or "finding" in q or "cve" in q:
        return TOP_VULNERABILITY
    if ("fix" in q and "first" in q) or "prioritize" in q or "priority" in q or "what should we" in q:
        return RECOMMENDED_PRIORITY
    if "exposed" in q or "exposure" in q:
        return MOST_EXPOSED_ASSET
    if "risk" in q or "loss" in q or "eal" in q or "biggest" in q or "highest" in q:
        return HIGHEST_FINANCIAL_RISK
    return UNSUPPORTED


def extract_budget(question: str) -> float | None:
    q = question.lower()
    m = re.search(r"(\d+(?:\.\d+)?)\s*(crore|cr)\b", q)
    if m:
        return float(m.group(1)) * 10_000_000
    m = re.search(r"(\d+(?:\.\d+)?)\s*(lakh|lac|l)\b", q)
    if m:
        return float(m.group(1)) * 100_000
    m = re.search(r"₹?\s*([\d,]{4,})", q)
    if m:
        return float(m.group(1).replace(",", ""))
    return None


_LIMITATIONS = [
    "Risk values are modeled estimates, not guaranteed outcomes.",
    "The demo dataset is simulated.",
]


def _unsupported() -> AIResponse:
    return AIResponse(
        answer=(
            "I can answer questions about CyberQuant AI's modeled cyber risk, financial "
            "exposure, vulnerabilities, assets, investments, and scenarios. I don't have "
            "enough structured data to answer that question reliably."
        ),
        limitations=_LIMITATIONS,
    )


def answer_question(question: str, context: dict | None, data: dict) -> AIResponse:
    """Produce a grounded answer.

    ``data`` is the structured backend context assembled by the router:
        {
          "assets": [{ref,name,eal,risk_score,...}],          # sorted desc by eal
          "findings": [{vuln_ref,vuln_name,asset_name,eal,incident_probability,cvss,drivers}],
          "recommendations": [{action_name,cost,expected_risk_reduction,priority,rosi}],
          "enterprise": {exposure, risk_score, risk_level},
          "optimize": callable(budget) -> optimization dict,
        }
    """
    intent = detect_intent(question)

    if intent == HIGHEST_FINANCIAL_RISK or intent == MOST_EXPOSED_ASSET:
        assets = data.get("assets") or []
        if not assets:
            return _unsupported()
        top = assets[0]
        return AIResponse(
            answer=(
                f"The simulated dataset indicates {top['name']} currently carries the highest "
                f"modeled financial cyber risk, with an Expected Annual Loss of "
                f"{format_inr(top['eal'])}."
            ),
            keyEvidence=[
                {"label": "Expected Annual Loss", "value": format_inr(top["eal"]), "sourceId": f"asset:{top['ref']}"},
                {"label": "Risk Score", "value": f"{top['risk_score']}/100", "sourceId": f"asset:{top['ref']}"},
                {"label": "Financial Impact", "value": format_inr(top.get("financial_impact")), "sourceId": f"asset:{top['ref']}"},
            ],
            riskDrivers=top.get("drivers", []),
            recommendation=(
                f"Prioritize the critical findings and control gaps on {top['name']} to reduce its modeled EAL."
            ),
            confidence=top.get("confidence"),
            limitations=_LIMITATIONS,
            sourceIds=[f"asset:{top['ref']}"],
            sources=[{"type": "asset", "id": top["ref"], "name": top["name"]}],
        )

    if intent == TOP_VULNERABILITY:
        findings = data.get("findings") or []
        if not findings:
            return _unsupported()
        top = findings[0]
        return AIResponse(
            answer=(
                f"The finding contributing most to expected loss is '{top['vuln_name']}' on "
                f"{top['asset_name']}, with a modeled EAL of {format_inr(top['eal'])}."
            ),
            keyEvidence=[
                {"label": "EAL", "value": format_inr(top["eal"]), "sourceId": f"vulnerability:{top['vuln_ref']}"},
                {"label": "Incident Probability", "value": f"{round(top['incident_probability'] * 100)}%", "sourceId": f"vulnerability:{top['vuln_ref']}"},
                {"label": "CVSS", "value": str(top["cvss"]), "sourceId": f"vulnerability:{top['vuln_ref']}"},
            ],
            riskDrivers=top.get("drivers", []),
            recommendation="Remediate this finding first; it produces the largest modeled loss reduction.",
            limitations=_LIMITATIONS,
            sourceIds=[f"vulnerability:{top['vuln_ref']}"],
            sources=[{"type": "vulnerability", "id": top["vuln_ref"], "name": top["vuln_name"]}],
        )

    if intent == RECOMMENDED_PRIORITY:
        recs = data.get("recommendations") or []
        if not recs:
            return _unsupported()
        top = recs[0]
        return AIResponse(
            answer=(
                f"Based on the current modeled risk and investment efficiency, the highest-priority "
                f"action is '{top['action_name']}'."
            ),
            keyEvidence=[
                {"label": "Cost", "value": format_inr(top["cost"]), "sourceId": f"investment:{top['action_name']}"},
                {"label": "Expected Risk Reduction", "value": format_inr(top["expected_risk_reduction"]), "sourceId": f"investment:{top['action_name']}"},
                {"label": "ROSI", "value": f"{top['rosi']}%" if top.get("rosi") is not None else "n/a", "sourceId": f"investment:{top['action_name']}"},
            ],
            riskDrivers=[f"Priority: {top['priority']}"],
            recommendation=f"Implement '{top['action_name']}' as the first remediation step.",
            limitations=_LIMITATIONS,
            sources=[{"type": "recommendation", "id": str(top.get("mitigation_id", "")), "name": top["action_name"]}],
        )

    if intent == BUDGET_RISK_REDUCTION:
        budget = extract_budget(question)
        optimize = data.get("optimize")
        if budget is None or optimize is None:
            return _unsupported()
        result = optimize(budget)
        actions = ", ".join(s["action_name"] for s in result["selected_investments"]) or "no affordable initiatives"
        return AIResponse(
            answer=(
                f"With a {format_inr(budget)} budget, the optimizer recommends: {actions}."
            ),
            keyEvidence=[
                {"label": "Total Spend", "value": format_inr(result["total_investment"]), "sourceId": "optimize"},
                {"label": "Expected Risk Reduction", "value": format_inr(result["expected_risk_reduction"]), "sourceId": "optimize"},
                {"label": "Remaining Budget", "value": format_inr(result["remaining_budget"]), "sourceId": "optimize"},
            ],
            riskDrivers=["Highest risk-reduction-per-rupee within the budget constraint"],
            recommendation="Prioritize the optimizer's recommended control set.",
            estimatedImpact={
                "before_exposure": result["before_exposure"],
                "after_exposure": result["after_exposure"],
                "percentage_reduction": result["percentage_reduction"],
            },
            limitations=_LIMITATIONS,
            sourceIds=["optimize"],
            sources=[{"type": "optimization", "id": "optimize", "name": "Investment Optimizer"}],
        )

    return _unsupported()


def to_dict(resp: AIResponse) -> dict:
    return asdict(resp)
