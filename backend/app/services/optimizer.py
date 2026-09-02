"""Deterministic greedy investment optimizer (docs/08-investment-optimizer.md).

Given a fixed budget and a set of candidate investments, select the set
that maximizes expected financial risk reduction without exceeding the
budget. Greedy by risk-reduction-per-rupee, with documented deterministic
tie-breaking. No randomness, no LLM.
"""

from __future__ import annotations

from dataclasses import dataclass

PRIORITY_RANK = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}


@dataclass
class Investment:
    ref: str
    mitigation_id: int
    name: str
    cost: float
    expected_risk_reduction: float  # INR absolute
    priority: str
    implementation_time: int


@dataclass
class OptimizationResult:
    budget: float
    selected: list[dict]
    recommendations: list[dict]
    total_investment: float
    expected_risk_reduction: float
    remaining_budget: float
    before_exposure: float
    after_exposure: float
    percentage_reduction: float
    rosi: float | None


def _efficiency(inv: Investment) -> float:
    if inv.cost <= 0:
        return 0.0
    return inv.expected_risk_reduction / inv.cost


def _rosi(reduction: float, cost: float) -> float | None:
    if cost <= 0:
        return None
    return round((reduction - cost) / cost * 100.0, 2)


def optimize(
    investments: list[Investment],
    budget: float,
    before_exposure: float,
    max_recommendations: int | None = None,
) -> OptimizationResult:
    if budget < 0:
        raise ValueError("Budget must be greater than or equal to 0")

    # Deterministic sort: efficiency desc, priority desc, reduction desc, ref asc.
    ordered = sorted(
        investments,
        key=lambda i: (
            -_efficiency(i),
            -PRIORITY_RANK.get(i.priority.upper(), 0),
            -i.expected_risk_reduction,
            i.ref,
        ),
    )

    selected: list[Investment] = []
    recommendations: list[dict] = []
    remaining = budget

    for inv in ordered:
        eff = round(_efficiency(inv), 4)
        if inv.cost <= remaining and inv.cost > 0:
            selected.append(inv)
            remaining -= inv.cost
            decision, reason = "selected", (
                f"Selected: {eff} of expected risk reduction per rupee, "
                f"and its cost fits the remaining budget."
            )
        elif inv.cost > budget:
            decision, reason = "not_selected", "Investment cost exceeds the available budget."
        else:
            decision, reason = "not_selected", "Cost exceeds the remaining budget after higher-priority selections."
        recommendations.append(
            {
                "mitigation_id": inv.mitigation_id,
                "investment_id": inv.ref,
                "action_name": inv.name,
                "decision": decision,
                "reason": reason,
                "cost": inv.cost,
                "expected_risk_reduction": inv.expected_risk_reduction,
                "risk_reduction_per_rupee": eff,
                "rosi": _rosi(inv.expected_risk_reduction, inv.cost),
                "priority": inv.priority,
            }
        )

    total_investment = round(sum(i.cost for i in selected), 2)
    total_reduction = round(sum(i.expected_risk_reduction for i in selected), 2)
    after_exposure = round(max(0.0, before_exposure - total_reduction), 2)
    percentage_reduction = (
        round(total_reduction / before_exposure * 100.0, 2) if before_exposure > 0 else 0.0
    )

    selected_payload = [
        {
            "mitigation_id": i.mitigation_id,
            "investment_id": i.ref,
            "action_name": i.name,
            "cost": i.cost,
            "expected_risk_reduction": i.expected_risk_reduction,
            "rosi": _rosi(i.expected_risk_reduction, i.cost),
            "priority": i.priority,
        }
        for i in selected
    ]

    if max_recommendations is not None:
        recommendations = recommendations[:max_recommendations]

    return OptimizationResult(
        budget=round(budget, 2),
        selected=selected_payload,
        recommendations=recommendations,
        total_investment=total_investment,
        expected_risk_reduction=total_reduction,
        remaining_budget=round(remaining, 2),
        before_exposure=round(before_exposure, 2),
        after_exposure=after_exposure,
        percentage_reduction=percentage_reduction,
        rosi=_rosi(total_reduction, total_investment),
    )
