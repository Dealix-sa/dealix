"""CEO business audit runtime.

Calculates the Dealix CEO Business Score from evidence stored in the
private ops repository. The score covers eight areas (revenue execution,
sales pipeline, financial control, delivery readiness, trust, learning,
CEO cadence, product discipline) and yields a 0–100 score plus a single
recommended next action.

This module is intentionally I/O-light: it only reads files inside the
provided private-ops root. It performs no network calls and writes no
state on its own. Callers (the generator script, CLI, or workflows)
decide where to persist the result.
"""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path


def read_csv(path: Path):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def to_float(value):
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def file_has_content(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 0


def dir_has_files(path: Path) -> bool:
    return path.exists() and path.is_dir() and any(p.is_file() for p in path.iterdir())


def calculate_business_score(private_ops_root: str) -> dict:
    root = Path(private_ops_root)

    pipeline = read_csv(root / "pipeline/pipeline_tracker.csv")
    revenue_actions = read_csv(root / "revenue/revenue_action_log.csv")
    cash = read_csv(root / "revenue/cash_collected.csv")
    pipeline_value = read_csv(root / "revenue/pipeline_value.csv")
    mrr = read_csv(root / "revenue/mrr_tracker.csv")
    expenses = read_csv(root / "finance/expenses.csv")
    approvals = read_csv(root / "trust/approval_log.csv")

    stages = {}
    for row in pipeline:
        stage = (row.get("stage") or "Unknown").strip()
        stages[stage] = stages.get(stage, 0) + 1

    lead_count = len(pipeline)
    contacted = stages.get("Contacted", 0)
    replied = stages.get("Replied", 0)
    sample_sent = stages.get("Sample Sent", 0)
    proposal_sent = stages.get("Proposal Sent", 0)
    paid = stages.get("Paid", 0)
    delivered = stages.get("Delivered", 0)
    retainer = stages.get("Retainer", 0)

    cash_collected = sum(
        to_float(r.get("amount_sar"))
        for r in cash
        if (r.get("status") or "").lower() in {"paid", "collected", "done"}
    )
    total_pipeline_value = sum(to_float(r.get("deal_value_sar")) for r in pipeline_value)
    active_mrr = sum(
        to_float(r.get("monthly_amount_sar"))
        for r in mrr
        if (r.get("status") or "").lower() in {"active", "paid", "current"}
    )
    monthly_expenses = sum(
        to_float(r.get("amount_sar"))
        for r in expenses
        if (r.get("recurring") or "").lower() in {"yes", "true", "1"}
    )

    # 01 Revenue Execution — 20
    revenue_score = 0
    if len(revenue_actions) >= 1:
        revenue_score += 4
    if contacted >= 25 or sum(
        1 for r in revenue_actions if (r.get("type") or "").lower() == "outbound"
    ) >= 25:
        revenue_score += 4
    if sample_sent >= 3 or dir_has_files(root / "delivery/samples"):
        revenue_score += 4
    if proposal_sent >= 1 or sum(
        1 for r in revenue_actions if (r.get("type") or "").lower() == "proposal"
    ) >= 1:
        revenue_score += 4
    if (
        paid >= 1
        or cash_collected > 0
        or sum(1 for r in revenue_actions if "payment" in (r.get("type") or "").lower()) >= 1
    ):
        revenue_score += 4

    # 02 Sales Pipeline — 15
    pipeline_score = 0
    if lead_count >= 25:
        pipeline_score += 5
    if lead_count > 0 and all((row.get("next_action") or "").strip() for row in pipeline):
        pipeline_score += 4
    if any((row.get("priority") or "").strip() in {"A", "B", "C"} for row in pipeline):
        pipeline_score += 2
    if replied >= 1:
        pipeline_score += 2
    if proposal_sent >= 1:
        pipeline_score += 2

    # 03 Financial Control — 15
    finance_score = 0
    if file_has_content(root / "finance/expenses.csv"):
        finance_score += 3
    if file_has_content(root / "revenue/cash_collected.csv"):
        finance_score += 3
    if file_has_content(root / "revenue/pipeline_value.csv"):
        finance_score += 3
    if file_has_content(root / "revenue/mrr_tracker.csv"):
        finance_score += 3
    if file_has_content(root / "finance/runway_estimate.md"):
        finance_score += 3

    # 04 Delivery Readiness — 15
    delivery_score = 0
    if file_has_content(root / "offers/revenue_sprint/client_intake.md"):
        delivery_score += 3
    if file_has_content(root / "offers/revenue_sprint/delivery_report_template.md"):
        delivery_score += 3
    if file_has_content(root / "offers/revenue_sprint/qa_checklist.md"):
        delivery_score += 3
    if file_has_content(root / "offers/revenue_sprint/handoff_template.md"):
        delivery_score += 3
    if dir_has_files(root / "delivery/samples") or dir_has_files(root / "delivery/reports"):
        delivery_score += 3

    # 05 Trust — 10
    trust_score = 0
    if file_has_content(root / "trust/approval_log.csv"):
        trust_score += 3
    if file_has_content(root / "founder/approvals_waiting.md"):
        trust_score += 2
    if len(approvals) >= 1:
        trust_score += 2
    if file_has_content(root / "trust/suppression_list.csv"):
        trust_score += 1
    if file_has_content(root / "trust/data_incidents.md"):
        trust_score += 2

    # 06 Learning — 10
    learning_score = 0
    if file_has_content(root / "learning/weekly_intelligence_review.md"):
        learning_score += 4
    if dir_has_files(root / "weekly_reviews"):
        learning_score += 2
    if file_has_content(root / "metrics_history/weekly_metrics.csv"):
        learning_score += 2
    if file_has_content(root / "learning/experiment_log.md"):
        learning_score += 2

    # 07 CEO Cadence — 10
    ceo_score = 0
    if file_has_content(root / "founder/daily_brief.md"):
        ceo_score += 3
    if file_has_content(root / "founder/decision_queue.md"):
        ceo_score += 2
    if file_has_content(root / "founder/weekly_ceo_review.md"):
        ceo_score += 2
    if file_has_content(root / "stage/evidence_report.md"):
        ceo_score += 2
    if file_has_content(root / "sprint/daily_execution_log.md"):
        ceo_score += 1

    # 08 Product Discipline — 5
    product_score = 0
    if file_has_content(root / "learning/productization_candidates.md"):
        product_score += 2
    if file_has_content(root / "stage/current_stage.md"):
        product_score += 2
    if file_has_content(root / "stage/blockers.md"):
        product_score += 1

    total_score = (
        revenue_score
        + pipeline_score
        + finance_score
        + delivery_score
        + trust_score
        + learning_score
        + ceo_score
        + product_score
    )

    # Enforce hard ceilings: score cannot exceed certain levels without
    # market evidence. These mirror the CEO_BUSINESS_AUDIT rules.
    if proposal_sent < 1 and total_score > 80:
        total_score = 80
    if (paid < 1 and cash_collected == 0 and delivered < 1 and retainer < 1) and total_score > 90:
        total_score = 90
    if lead_count < 1 and total_score > 70:
        total_score = 70

    if total_score >= 90:
        status = "OPERATING"
    elif total_score >= 75:
        status = "READY_INTERNAL"
    elif total_score >= 50:
        status = "FIX_BEFORE_SCALE"
    else:
        status = "SETUP_INCOMPLETE"

    next_action = "Add 25 leads and record revenue actions."
    if lead_count >= 25 and contacted < 25:
        next_action = "Send 25 founder-led DMs."
    elif contacted >= 25 and sample_sent < 3:
        next_action = "Prepare and send 3 sample packs."
    elif sample_sent >= 3 and proposal_sent < 1:
        next_action = "Convert best reply/sample into proposal."
    elif proposal_sent >= 1 and paid < 1 and cash_collected == 0:
        next_action = "Pursue payment, PO, or written approval."
    elif paid >= 1 or cash_collected > 0:
        next_action = "Deliver with QA and request feedback."

    return {
        "date": date.today().isoformat(),
        "total_score": total_score,
        "revenue_score": revenue_score,
        "pipeline_score": pipeline_score,
        "finance_score": finance_score,
        "delivery_score": delivery_score,
        "trust_score": trust_score,
        "learning_score": learning_score,
        "ceo_score": ceo_score,
        "product_score": product_score,
        "status": status,
        "next_action": next_action,
        "metrics": {
            "lead_count": lead_count,
            "contacted": contacted,
            "replied": replied,
            "sample_sent": sample_sent,
            "proposal_sent": proposal_sent,
            "paid": paid,
            "delivered": delivered,
            "retainer": retainer,
            "cash_collected": cash_collected,
            "pipeline_value": total_pipeline_value,
            "mrr": active_mrr,
            "monthly_expenses": monthly_expenses,
        },
    }
