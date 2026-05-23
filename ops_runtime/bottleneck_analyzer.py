def analyze_bottlenecks(metrics):
    bottlenecks = []

    if metrics.get("paid", 0) == 0 and metrics.get("proposal_sent", 0) > 0:
        bottlenecks.append({
            "area": "Revenue",
            "severity": "High",
            "issue": "Proposal sent but no payment recorded.",
            "recommendation": "Improve payment path, urgency, and follow-up.",
        })

    if metrics.get("contacted", 0) > 0 and metrics.get("replied", 0) == 0:
        bottlenecks.append({
            "area": "Outreach",
            "severity": "Medium",
            "issue": "Outreach has no replies.",
            "recommendation": "Rewrite hook / offer; tighten ICP.",
        })

    if metrics.get("replied", 0) > 0 and metrics.get("call_booked", 0) == 0:
        bottlenecks.append({
            "area": "Conversion",
            "severity": "Medium",
            "issue": "Replies are not converting to booked calls.",
            "recommendation": "Send calendar link earlier; pre-qualify in DM.",
        })

    if metrics.get("approvals_pending", 0) > 0:
        bottlenecks.append({
            "area": "Trust",
            "severity": "Medium",
            "issue": "Approvals are pending in the trust log.",
            "recommendation": "Clear approval queue before next external commitment.",
        })

    return bottlenecks
