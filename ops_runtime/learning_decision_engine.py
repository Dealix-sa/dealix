def recommend_learning_decision(metrics, bottlenecks, comparison):
    if metrics.get("paid", 0) == 0 and metrics.get("proposal_sent", 0) > 0:
        return {
            "decision": "Fix payment conversion",
            "type": "Fix",
            "reason": "Proposal exists but no payment recorded.",
            "recommended_file": "docs/revenue/CASH_RULES.md",
            "update": "Add stronger payment follow-up and fallback payment path.",
        }

    if metrics.get("replied", 0) < 5 and metrics.get("contacted", 0) >= 25:
        return {
            "decision": "Improve outbound messaging",
            "type": "Fix",
            "reason": "Outbound target reached but reply target missed.",
            "recommended_file": "docs/acquisition/MESSAGE_QUALITY_STANDARD.md",
            "update": "Refine founder DM and test a new message angle.",
        }

    if metrics.get("sample_sent", 0) < 3:
        return {
            "decision": "Improve sample production",
            "type": "Build",
            "reason": "Sample target not reached.",
            "recommended_file": "docs/acquisition/SAMPLE_GENERATION_SYSTEM.md",
            "update": "Create faster sample generation checklist.",
        }

    if metrics.get("approvals_pending", 0) > 5:
        return {
            "decision": "Reduce approval bottleneck",
            "type": "Fix",
            "reason": "Too many approvals waiting.",
            "recommended_file": "docs/trust/APPROVAL_MATRIX.md",
            "update": "Clarify A0/A1/A2 routing to reduce founder bottleneck.",
        }

    if comparison.get("has_comparison") and comparison.get("biggest_drop"):
        return {
            "decision": f"Investigate drop in {comparison['biggest_drop']}",
            "type": "Fix",
            "reason": comparison.get("summary", ""),
            "recommended_file": "docs/learning/WEEKLY_INTELLIGENCE_REVIEW.md",
            "update": "Document cause of weekly drop and next experiment.",
        }

    return {
        "decision": "Continue operating cadence",
        "type": "Continue",
        "reason": "No critical bottleneck detected.",
        "recommended_file": "docs/ops/OPERATING_CADENCE.md",
        "update": "Keep weekly cadence and document next learning.",
    }
