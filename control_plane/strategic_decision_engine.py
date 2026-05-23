"""Strategic decision engine.

Maps the CEO business score into a Build / Fix / Kill / Defer / Continue
recommendation so the founder always knows the next strategic move.
"""

from __future__ import annotations


def recommend_strategic_decision(score: dict) -> dict:
    metrics = score.get("metrics", {})
    total_score = int(score.get("total_score", 0))

    leads = int(metrics.get("lead_count", 0) or 0)
    proposals = int(metrics.get("proposal_sent", 0) or 0)
    paid = int(metrics.get("paid", 0) or 0)
    delivered = int(metrics.get("delivered", 0) or 0)
    retainer = int(metrics.get("retainer", 0) or 0)

    if leads < 25:
        return {
            "decision": "FIX",
            "area": "Revenue / pipeline",
            "action": "Build pipeline to 25 qualified leads before any new investment.",
        }
    if proposals >= 1 and paid < 1:
        return {
            "decision": "FIX",
            "area": "Sales conversion",
            "action": "Close the open proposal: clarify scope, decision-maker, and payment terms.",
        }
    if paid >= 1 and delivered < 1:
        return {
            "decision": "BUILD",
            "area": "Delivery",
            "action": "Execute the paid engagement with QA-controlled delivery and proof.",
        }
    if delivered >= 1 and retainer < 1:
        return {
            "decision": "BUILD",
            "area": "Retention",
            "action": "Ask for feedback and convert the delivered client into a retainer.",
        }
    if total_score >= 80:
        return {
            "decision": "BUILD",
            "area": "Productization",
            "action": "Promote the most repeated workflow to template or SaaS candidate.",
        }
    return {
        "decision": "CONTINUE",
        "area": "Operating loop",
        "action": "Run the daily revenue and delivery loop; review weekly.",
    }
