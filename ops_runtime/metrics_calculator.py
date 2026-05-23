def _to_int(value):
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def _count_stage(rows, stage_values):
    stage_values = {value.lower() for value in stage_values}
    count = 0
    for row in rows:
        stage = (row.get("stage") or row.get("status") or "").strip().lower()
        if stage in stage_values:
            count += 1
    return count


def calculate_pipeline_metrics(pipeline_rows):
    rows = list(pipeline_rows)
    return {
        "lead_count": len(rows),
        "new": _count_stage(rows, {"new"}),
        "contacted": _count_stage(rows, {"contacted", "outreach", "dm"}),
        "replied": _count_stage(rows, {"replied", "reply"}),
        "sample_sent": _count_stage(rows, {"sample_sent", "sample"}),
        "call_booked": _count_stage(rows, {"call_booked", "call"}),
        "proposal_sent": _count_stage(rows, {"proposal_sent", "proposal"}),
        "paid": _count_stage(rows, {"paid", "won"}),
        "delivered": _count_stage(rows, {"delivered"}),
        "retainer": _count_stage(rows, {"retainer"}),
    }


def calculate_mrr_metrics(mrr_rows):
    rows = list(mrr_rows)
    mrr_total = 0
    active = 0
    for row in rows:
        amount = _to_int(row.get("amount") or row.get("mrr") or 0)
        status = (row.get("status") or "").strip().lower()
        if status in {"active", "live"}:
            active += 1
            mrr_total += amount
    return {
        "mrr": mrr_total,
        "active_retainers": active,
    }


def calculate_approval_metrics(approval_rows):
    rows = list(approval_rows)
    pending = 0
    high_risk = 0
    for row in rows:
        status = (row.get("status") or "").strip().lower()
        risk = (row.get("risk") or "").strip().lower()
        if status in {"pending", "open"}:
            pending += 1
        if risk in {"high", "high_risk"}:
            high_risk += 1
    return {
        "approvals_total": len(rows),
        "approvals_pending": pending,
        "high_risk_approvals": high_risk,
    }
