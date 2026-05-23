def build_risk_alerts(score: dict) -> list[dict]:
    metrics = score.get("metrics", {})
    alerts = []
    if metrics.get("lead_count", 0) < 25:
        alerts.append({
            "level": "red",
            "risk": "Pipeline starvation",
            "action": "Add 25 qualified leads."
        })
    if metrics.get("proposal_sent", 0) >= 1 and metrics.get("cash_collected", 0) <= 0:
        alerts.append({
            "level": "red",
            "risk": "Proposal not converting to cash",
            "action": "Pursue payment, PO, or written approval."
        })
    if metrics.get("paid", 0) >= 1 and metrics.get("delivered", 0) < 1:
        alerts.append({
            "level": "yellow",
            "risk": "Delivery proof missing",
            "action": "Complete delivery with QA."
        })
    if metrics.get("delivered", 0) >= 1 and metrics.get("retainer", 0) < 1:
        alerts.append({
            "level": "yellow",
            "risk": "Retention not captured",
            "action": "Ask for feedback and retainer."
        })
    return alerts
