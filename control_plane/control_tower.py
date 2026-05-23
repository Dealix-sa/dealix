from __future__ import annotations


def build_control_tower_signal(score: dict) -> dict:
    metrics = score.get("metrics", {})
    total_score = score.get("total_score", 0)
    signals = []
    if metrics.get("lead_count", 0) < 25:
        signals.append({
            "area": "Revenue",
            "level": "red",
            "message": "Pipeline is below minimum threshold.",
            "action": "Add 25 qualified leads.",
        })
    if metrics.get("contacted", 0) < 25:
        signals.append({
            "area": "Sales",
            "level": "red",
            "message": "Outbound execution is below target.",
            "action": "Send 25 founder-led DMs.",
        })
    if metrics.get("proposal_sent", 0) < 1 and metrics.get("replied", 0) > 0:
        signals.append({
            "area": "Revenue",
            "level": "yellow",
            "message": "Replies exist but no proposal is recorded.",
            "action": "Convert best reply into a proposal.",
        })
    if metrics.get("proposal_sent", 0) >= 1 and metrics.get("cash_collected", 0) <= 0:
        signals.append({
            "area": "Finance",
            "level": "red",
            "message": "Proposal exists but no cash is collected.",
            "action": "Pursue payment, PO, or written approval.",
        })
    if metrics.get("paid", 0) >= 1 and metrics.get("delivered", 0) < 1:
        signals.append({
            "area": "Delivery",
            "level": "yellow",
            "message": "Paid work exists but delivery is not completed.",
            "action": "Run delivery report and QA checklist.",
        })
    if total_score < 50:
        posture = "SETUP_INCOMPLETE"
    elif total_score < 75:
        posture = "FIX_BEFORE_SCALE"
    elif total_score < 90:
        posture = "READY_INTERNAL"
    else:
        posture = "OPERATING"
    top_action = signals[0]["action"] if signals else "Run weekly learning review and update one system."
    return {
        "posture": posture,
        "top_action": top_action,
        "signals": signals,
    }
