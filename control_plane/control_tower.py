"""Control Tower posture builder.

Reads the CEO business score and emits the single highest-priority action plus
the company posture string that mission control consumes.
"""

from __future__ import annotations


def build_control_tower_signal(score: dict) -> dict:
    metrics = score.get("metrics", {})
    total_score = int(score.get("total_score", 0))

    if total_score >= 80:
        posture = "SCALING"
    elif total_score >= 50:
        posture = "OPERATING"
    elif total_score >= 20:
        posture = "EXECUTING"
    else:
        posture = "SETUP"

    top_action = _top_action(metrics)

    return {
        "posture": posture,
        "top_action": top_action,
    }


def _top_action(metrics: dict) -> str:
    leads = int(metrics.get("lead_count", 0) or 0)
    contacted = int(metrics.get("contacted", 0) or 0)
    replied = int(metrics.get("replied", 0) or 0)
    samples = int(metrics.get("sample_sent", 0) or 0)
    proposals = int(metrics.get("proposal_sent", 0) or 0)
    paid = int(metrics.get("paid", 0) or 0)
    delivered = int(metrics.get("delivered", 0) or 0)
    retainer = int(metrics.get("retainer", 0) or 0)
    cash = int(metrics.get("cash_collected", 0) or 0)

    if leads < 25:
        return "Add qualified leads until you have at least 25."
    if contacted < 25:
        return "Send 25 DMs to qualified leads today."
    if replied < 3:
        return "Follow up to convert outreach into replies."
    if samples < 3:
        return "Send 3 tailored sample packs to replying leads."
    if proposals < 1:
        return "Convert a replying lead into a written proposal."
    if paid < 1 or cash <= 0:
        return "Pursue payment, PO, or written approval on the open proposal."
    if delivered < 1:
        return "Complete the paid engagement with QA-controlled delivery."
    if retainer < 1:
        return "Ask the delivered client for feedback and a retainer."
    return "Productize the repeating workflow into a template."
