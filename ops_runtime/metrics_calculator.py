from collections import Counter


def calculate_pipeline_metrics(pipeline_rows):
    stages = Counter((row.get("stage") or "Unknown").strip() for row in pipeline_rows)

    return {
        "lead_count": len(pipeline_rows),
        "new": stages.get("New", 0),
        "qualified": stages.get("Qualified", 0),
        "contacted": stages.get("Contacted", 0),
        "replied": stages.get("Replied", 0),
        "sample_sent": stages.get("Sample Sent", 0),
        "call_booked": stages.get("Call Booked", 0),
        "proposal_sent": stages.get("Proposal Sent", 0),
        "paid": stages.get("Paid", 0),
        "delivered": stages.get("Delivered", 0),
        "retainer": stages.get("Retainer", 0),
        "lost": stages.get("Lost", 0),
    }


def calculate_mrr_metrics(mrr_rows):
    active = [
        row for row in mrr_rows
        if (row.get("status") or "").strip().lower() in {"active", "paid", "current"}
    ]

    total_mrr = 0.0
    for row in active:
        try:
            total_mrr += float(row.get("monthly_amount") or 0)
        except ValueError:
            pass

    return {
        "active_retainers": len(active),
        "mrr": total_mrr,
    }


def calculate_approval_metrics(approval_rows):
    pending = [
        row for row in approval_rows
        if (row.get("decision") or "").strip().lower() in {"pending", ""}
    ]

    high_risk = [
        row for row in approval_rows
        if (row.get("risk_level") or "").strip().lower() in {"high", "critical"}
    ]

    return {
        "approvals_total": len(approval_rows),
        "approvals_pending": len(pending),
        "high_risk_approvals": len(high_risk),
    }
