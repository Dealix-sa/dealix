def generate_alerts(metrics, bottlenecks):
    alerts = []

    if metrics.get("paid", 0) == 0 and metrics.get("proposal_sent", 0) > 0:
        alerts.append({
            "level": "red",
            "area": "Revenue",
            "message": "Proposal sent but no payment recorded.",
            "action": "Follow up and offer bank transfer / PO fallback."
        })

    if metrics.get("contacted", 0) < 25:
        alerts.append({
            "level": "yellow",
            "area": "Sales",
            "message": "Weekly outbound target not reached.",
            "action": "Send more founder-led DMs."
        })

    if metrics.get("approvals_pending", 0) > 0:
        alerts.append({
            "level": "yellow",
            "area": "Trust",
            "message": "Approvals are waiting.",
            "action": "Review approvals before sending external commitments."
        })

    if metrics.get("contacted", 0) >= 25:
        alerts.append({
            "level": "green",
            "area": "Sales",
            "message": "Weekly outbound target reached.",
            "action": "Focus on replies, calls, and proposals."
        })

    for b in bottlenecks:
        if b.get("severity") == "High":
            alerts.append({
                "level": "red",
                "area": b.get("area", "Unknown"),
                "message": b.get("issue", ""),
                "action": b.get("recommendation", "")
            })

    return alerts
