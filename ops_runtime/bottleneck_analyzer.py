def analyze_bottlenecks(metrics):
    bottlenecks = []

    if metrics.get("lead_count", 0) < 25:
        bottlenecks.append({
            "area": "Sales",
            "severity": "High",
            "issue": "Lead volume below weekly target.",
            "recommendation": "Add at least 25 qualified leads to pipeline."
        })

    if metrics.get("contacted", 0) < 25:
        bottlenecks.append({
            "area": "Acquisition",
            "severity": "High",
            "issue": "Outbound volume below weekly target.",
            "recommendation": "Send first 25 founder-led DMs."
        })

    if metrics.get("proposal_sent", 0) == 0 and metrics.get("replied", 0) > 0:
        bottlenecks.append({
            "area": "Sales",
            "severity": "Medium",
            "issue": "Replies exist but no proposals sent.",
            "recommendation": "Qualify replies and send at least one proposal."
        })

    if metrics.get("paid", 0) == 0 and metrics.get("proposal_sent", 0) > 0:
        bottlenecks.append({
            "area": "Revenue",
            "severity": "High",
            "issue": "Proposals sent but no payments recorded.",
            "recommendation": "Improve payment path, urgency, and follow-up."
        })

    if metrics.get("approvals_pending", 0) > 5:
        bottlenecks.append({
            "area": "Founder",
            "severity": "Medium",
            "issue": "Too many approvals waiting.",
            "recommendation": "Batch approvals daily and clarify approval matrix."
        })

    return bottlenecks
