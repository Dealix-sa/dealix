def recommend_strategic_decision(score: dict) -> dict:
    metrics = score.get("metrics", {})
    total = score.get("total_score", 0)
    if metrics.get("lead_count", 0) < 25:
        return {
            "decision": "FIX",
            "area": "Pipeline",
            "reason": "Pipeline is below minimum viable execution level.",
            "action": "Add 25 qualified leads before building anything else."
        }
    if metrics.get("contacted", 0) < 25:
        return {
            "decision": "FIX",
            "area": "Outbound",
            "reason": "Leads exist but outreach execution is incomplete.",
            "action": "Send 25 founder-led DMs."
        }
    if metrics.get("proposal_sent", 0) < 1:
        return {
            "decision": "FIX",
            "area": "Sales Conversion",
            "reason": "No proposal means no near-term payment path.",
            "action": "Convert best reply or sample into proposal."
        }
    if metrics.get("cash_collected", 0) <= 0 and metrics.get("proposal_sent", 0) >= 1:
        return {
            "decision": "FIX",
            "area": "Payment Path",
            "reason": "Proposal exists but cash is not collected.",
            "action": "Pursue payment, PO, or written approval."
        }
    if metrics.get("paid", 0) >= 1 and metrics.get("delivered", 0) < 1:
        return {
            "decision": "BUILD",
            "area": "Delivery Proof",
            "reason": "Paid work must become delivery proof.",
            "action": "Deliver with QA and request feedback."
        }
    if metrics.get("delivered", 0) >= 1 and metrics.get("retainer", 0) < 1:
        return {
            "decision": "BUILD",
            "area": "Retention",
            "reason": "Delivery should convert into recurring revenue.",
            "action": "Ask for retainer or next sprint."
        }
    if total >= 90:
        return {
            "decision": "CONTINUE",
            "area": "Operating System",
            "reason": "Company system is operating.",
            "action": "Continue cadence and productize repeated workflows."
        }
    return {
        "decision": "DEFER",
        "area": "Product Expansion",
        "reason": "Evidence is not strong enough for expansion.",
        "action": "Keep focus on revenue, delivery, and learning."
    }
