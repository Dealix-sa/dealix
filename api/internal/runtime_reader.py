"""Founder Console v4 — live runtime reader over Private Ops CSVs.

The base path is configurable via the DEALIX_PRIVATE_OPS environment
variable. Missing files return empty lists, so the API stays callable
during bootstrap.
"""

from __future__ import annotations

import csv
import os
from datetime import datetime
from pathlib import Path
from typing import Any

PRIVATE_OPS = Path(os.getenv("DEALIX_PRIVATE_OPS", "/opt/dealix-ops-private"))


def read_csv(rel_path: str) -> list[dict[str, Any]]:
    path = PRIVATE_OPS / rel_path
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def append_csv(rel_path: str, row: dict[str, Any], headers: list[str]) -> None:
    path = PRIVATE_OPS / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists() and path.stat().st_size > 0
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def count_where(rows: list[dict[str, Any]], field: str, values: set[str]) -> int:
    needles = {v.lower() for v in values}
    return sum(1 for r in rows if str(r.get(field, "")).strip().lower() in needles)


def now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"


def sales_funnel_summary() -> dict[str, Any]:
    intel = read_csv("intelligence/lead_intelligence_base.csv")
    outreach = read_csv("outreach/outreach_queue.csv")
    conversations = read_csv("outreach/conversation_log.csv")
    proposals = read_csv("sales/proposal_queue.csv")
    payments = read_csv("finance/payment_capture_queue.csv")

    a_leads = count_where(intel, "priority", {"A"})
    pending_approval = count_where(outreach, "approval_status", {"Pending", "Needs Edit"})
    approved_outreach = count_where(outreach, "approval_status", {"Approved"})
    sent = count_where(outreach, "send_status", {"Sent"})
    positive = count_where(conversations, "reply_type", {"positive", "interested", "yes"})

    return {
        "lead_intelligence": len(intel),
        "a_leads": a_leads,
        "pending_approval": pending_approval,
        "approved_outreach": approved_outreach,
        "sent": sent,
        "replies": len(conversations),
        "positive_replies": positive,
        "samples": 0,
        "proposals": len(proposals),
        "payment_capture": len(payments),
        "source": "private_ops_csv",
        "last_updated": now_iso(),
    }


def approvals_list() -> list[dict[str, Any]]:
    rows = read_csv("approvals/approval_queue.csv")
    return [
        {
            "id": r.get("approval_id", ""),
            "type": r.get("type", ""),
            "company": r.get("company", ""),
            "approval_class": r.get("approval_class", "A1"),
            "risk_level": r.get("risk_level", "Low"),
            "summary": r.get("summary", ""),
            "evidence": r.get("evidence", ""),
            "recommended_action": r.get("recommended_action", ""),
            "status": r.get("status", "Pending"),
        }
        for r in rows
        if str(r.get("status", "")).lower() in {"pending", "needs edit", ""}
    ]


def finance_summary() -> dict[str, Any]:
    cash = read_csv("finance/cash_collected.csv")
    payments = read_csv("finance/payment_capture_queue.csv")
    collected = 0.0
    for r in cash:
        if str(r.get("status", "")).lower() in {"paid", "collected", "done"}:
            try:
                collected += float(r.get("amount_sar") or 0)
            except ValueError:
                pass
    return {
        "cash_collected_sar": collected,
        "mrr_sar": 0,
        "pipeline_sar": 0,
        "weighted_pipeline_sar": 0,
        "payment_followups_due": len(payments),
        "source": "private_ops_csv",
        "last_updated": now_iso(),
    }


def ceo_summary() -> dict[str, Any]:
    funnel = sales_funnel_summary()
    approvals = approvals_list()
    finance = finance_summary()

    if funnel["lead_intelligence"] < 100:
        top_action = "Build lead intelligence base to 100 records"
        status = "C3 Revenue Not Ready"
    elif len(approvals) > 0:
        top_action = "Review approval queue"
        status = "C3 Approval Ready"
    elif funnel["approved_outreach"] > funnel["sent"]:
        top_action = "Create/send approved drafts"
        status = "C3 Outreach Ready"
    elif funnel["positive_replies"] > funnel["proposals"]:
        top_action = "Create sample/proposal for positive replies"
        status = "C3 Conversion Ready"
    elif funnel["proposals"] > 0 and funnel["payment_capture"] == 0:
        top_action = "Create payment capture follow-up"
        status = "C3 Proposal Follow-up Needed"
    else:
        top_action = "Run distribution review and build next sector batch"
        status = "C4 Operational"

    return {
        "top_action": top_action,
        "status": status,
        "risk_flags": 0,
        "cash_collected_sar": finance["cash_collected_sar"],
        "approved_outreach": funnel["approved_outreach"],
        "positive_replies": funnel["positive_replies"],
        "proposals_due": funnel["proposals"],
        "payment_followups_due": funnel["payment_capture"],
        "last_updated": now_iso(),
        "source": "private_ops_csv",
    }
