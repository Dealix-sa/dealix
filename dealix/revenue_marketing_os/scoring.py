"""
Scoring primitives for Revenue Marketing OS.

Two scoring laws govern this module:

    Lead Score =
        0.25 ICP fit + 0.20 pain likelihood + 0.20 ability to pay +
        0.15 urgency + 0.10 partner potential + 0.10 trust fit

    Revenue Quality =
        0.25 margin + 0.20 repeatability + 0.20 retainer potential +
        0.15 data moat + 0.10 partner potential - 0.10 delivery burden

Both produce a 0-100 score (Revenue Quality clipped to [0, 100]).
"""

from __future__ import annotations

from typing import Any

_LEAD_WEIGHTS = {
    "icp_fit": 0.25,
    "pain_likelihood": 0.20,
    "ability_to_pay": 0.20,
    "urgency": 0.15,
    "partner_potential": 0.10,
    "trust_fit": 0.10,
}

_REVENUE_WEIGHTS = {
    "margin": 0.25,
    "repeatability": 0.20,
    "retainer_potential": 0.20,
    "data_moat": 0.15,
    "partner_potential": 0.10,
    "delivery_burden": -0.10,
}


def _clip01(x: float) -> float:
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x


def compute_lead_score(fields: dict[str, Any]) -> tuple[int, dict[str, int]]:
    """
    Compute a 0-100 lead fit score and per-component breakdown.

    Inputs are expected as 0.0..1.0 floats; ints/strings are coerced
    safely. Missing keys default to 0.0.
    """
    breakdown: dict[str, int] = {}
    score = 0.0
    for key, weight in _LEAD_WEIGHTS.items():
        raw = fields.get(key, 0.0)
        try:
            val = _clip01(float(raw))
        except (TypeError, ValueError):
            val = 0.0
        component = val * weight * 100.0
        breakdown[key] = round(component)
        score += component
    return round(score), breakdown


def compute_revenue_quality_score(fields: dict[str, Any]) -> tuple[int, dict[str, int]]:
    """
    Compute a 0-100 revenue-quality score. Delivery burden lowers the
    score so a heavy one-off ranks below a small recurring contract.
    """
    breakdown: dict[str, int] = {}
    score = 0.0
    for key, weight in _REVENUE_WEIGHTS.items():
        raw = fields.get(key, 0.0)
        try:
            val = _clip01(float(raw))
        except (TypeError, ValueError):
            val = 0.0
        component = val * weight * 100.0
        breakdown[key] = round(component)
        score += component
    score = max(0.0, min(100.0, score))
    return round(score), breakdown


def revenue_is_real(record: dict[str, Any]) -> bool:
    """
    Revenue Assurance gate. We refuse to count anything that is not
    backed by a payment / agreement / invoice flag.
    """
    status = record.get("status") or ""
    if status in ("paid", "retainer_active", "renewed", "expanded"):
        return bool(record.get("payment_verified") or record.get("invoice_verified"))
    if status == "invoiced":
        return bool(record.get("invoice_verified"))
    if status == "committed":
        return bool(record.get("agreement_signed"))
    return False


def funnel_metrics(events: dict[str, int]) -> dict[str, float]:
    """
    Compute conversion ratios for the B2B funnel. ``events`` must
    contain integer counts for at least ``visitor``, ``lead``,
    ``mql``, ``sql``, ``call``, ``proposal``, ``win``, ``payment``,
    ``retainer``, ``expansion``.
    """

    def ratio(a: str, b: str) -> float:
        denom = events.get(b, 0)
        if denom <= 0:
            return 0.0
        return round(events.get(a, 0) / denom, 4)

    return {
        "visitor_to_lead": ratio("lead", "visitor"),
        "lead_to_mql": ratio("mql", "lead"),
        "mql_to_sql": ratio("sql", "mql"),
        "sql_to_call": ratio("call", "sql"),
        "call_to_proposal": ratio("proposal", "call"),
        "proposal_to_win": ratio("win", "proposal"),
        "win_to_payment": ratio("payment", "win"),
        "payment_to_retainer": ratio("retainer", "payment"),
        "retainer_to_expansion": ratio("expansion", "retainer"),
    }
