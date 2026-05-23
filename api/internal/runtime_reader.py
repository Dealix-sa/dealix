"""Read private operating CSVs for the Founder Console internal API.

The private ops root defaults to /opt/dealix-ops-private and is overridable
via the DEALIX_PRIVATE_OPS env var. Missing files return safe empty
structures with `source: "fallback"` so the Founder Console always renders.
"""

from __future__ import annotations

import csv
import os
from collections.abc import Iterable
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PRIVATE_OPS_ENV = "DEALIX_PRIVATE_OPS"
DEFAULT_PRIVATE_OPS = "/opt/dealix-ops-private"

# All CSVs the runtime reader expects to find. Keep in sync with
# scripts/bootstrap_private_ops_runtime.py.
RUNTIME_FILES: dict[str, list[str]] = {
    "lead_intelligence": [
        "lead_id", "company", "sector", "score", "intent",
        "last_signal", "owner", "status", "updated_at",
    ],
    "outreach_queue": [
        "outreach_id", "lead_id", "channel", "approval_class",
        "state", "scheduled_at", "approved_by", "updated_at",
    ],
    "conversation_log": [
        "conversation_id", "lead_id", "direction", "channel",
        "sentiment", "summary", "occurred_at",
    ],
    "suppression_list": [
        "identifier", "channel", "reason", "added_at",
    ],
    "approval_queue": [
        "approval_id", "type", "approval_class", "risk_level",
        "summary", "evidence", "recommended_action", "created_at",
    ],
    "approval_decisions": [
        "approval_id", "type", "actor", "decision", "reason",
        "approval_class", "risk_level", "policy_result", "evidence",
        "source_endpoint", "timestamp", "external_action_allowed",
    ],
    "trust_flags": [
        "flag_id", "category", "severity", "summary", "evidence",
        "status", "created_at",
    ],
    "proposal_queue": [
        "proposal_id", "lead_id", "stage", "value_sar",
        "expected_close", "owner", "updated_at",
    ],
    "payment_capture_queue": [
        "invoice_id", "customer", "amount_sar", "due_date",
        "stage", "last_followup_at", "updated_at",
    ],
    "cash_collected": [
        "invoice_id", "customer", "amount_sar", "collected_at",
        "method",
    ],
    "worker_state": [
        "worker", "last_run", "status", "failures_24h",
        "next_run", "notes",
    ],
    "channel_scorecard": [
        "channel", "sent", "replies", "positive_replies",
        "samples", "proposals", "payments",
    ],
    "sector_scorecard": [
        "sector", "pipeline_sar", "wins", "win_rate",
        "avg_cycle_days", "samples",
    ],
    "eval_status": [
        "suite", "passed", "failed", "warn", "last_run",
        "blocking",
    ],
    "productization_candidates": [
        "candidate_id", "name", "stage", "evidence", "next_step",
        "updated_at",
    ],
    "security_status": [
        "control", "status", "last_checked", "owner", "evidence",
    ],
}

RUNTIME_PATHS: dict[str, str] = {
    "lead_intelligence": "intelligence/lead_intelligence_base.csv",
    "outreach_queue": "outreach/outreach_queue.csv",
    "conversation_log": "outreach/conversation_log.csv",
    "suppression_list": "outreach/suppression_list.csv",
    "approval_queue": "approvals/approval_queue.csv",
    "approval_decisions": "trust/approval_decisions.csv",
    "trust_flags": "trust/trust_flags.csv",
    "proposal_queue": "sales/proposal_queue.csv",
    "payment_capture_queue": "finance/payment_capture_queue.csv",
    "cash_collected": "finance/cash_collected.csv",
    "worker_state": "runtime/worker_state.csv",
    "channel_scorecard": "distribution/channel_scorecard.csv",
    "sector_scorecard": "distribution/sector_scorecard.csv",
    "eval_status": "evals/eval_status.csv",
    "productization_candidates": "product/productization_candidates.csv",
    "security_status": "security/security_status.csv",
}


def private_ops_root() -> Path:
    return Path(os.environ.get(PRIVATE_OPS_ENV, DEFAULT_PRIVATE_OPS))


def runtime_file(name: str) -> Path:
    rel = RUNTIME_PATHS.get(name)
    if rel is None:
        raise KeyError(f"unknown runtime file: {name}")
    return private_ops_root() / rel


def _read_csv(path: Path) -> tuple[list[dict[str, Any]], str]:
    if not path.exists():
        return [], "fallback"
    try:
        with path.open("r", newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            rows = [dict(row) for row in reader]
        return rows, "runtime"
    except OSError:
        return [], "fallback"


def read_runtime(name: str) -> dict[str, Any]:
    """Read a known runtime file; return rows + source tag."""
    path = runtime_file(name)
    rows, source = _read_csv(path)
    return {
        "name": name,
        "path": str(path),
        "rows": rows,
        "count": len(rows),
        "source": source,
    }


def append_runtime(name: str, row: dict[str, Any]) -> Path:
    """Append a row to a runtime CSV, creating headers if needed."""
    path = runtime_file(name)
    headers = RUNTIME_FILES[name]
    path.parent.mkdir(parents=True, exist_ok=True)
    new_file = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=headers)
        if new_file:
            writer.writeheader()
        writer.writerow({h: row.get(h, "") for h in headers})
    return path


def _sum(rows: Iterable[dict[str, Any]], field: str) -> float:
    total = 0.0
    for row in rows:
        raw = (row.get(field) or "").strip()
        if not raw:
            continue
        try:
            total += float(raw)
        except ValueError:
            continue
    return total


def _count(rows: Iterable[dict[str, Any]], field: str, value: str) -> int:
    return sum(1 for row in rows if (row.get(field) or "").strip() == value)


def ceo_summary() -> dict[str, Any]:
    approvals = read_runtime("approval_queue")
    outreach = read_runtime("outreach_queue")
    conversations = read_runtime("conversation_log")
    proposals = read_runtime("proposal_queue")
    payments = read_runtime("payment_capture_queue")
    trust = read_runtime("trust_flags")
    cash = read_runtime("cash_collected")

    positive_replies = _count(conversations["rows"], "sentiment", "positive")
    sent = _count(outreach["rows"], "state", "sent")
    approved = _count(outreach["rows"], "state", "approved")
    risk_open = sum(
        1 for r in trust["rows"]
        if (r.get("status") or "").strip() == "open"
    )

    top_action = (
        f"Review {approvals['count']} pending approval(s)"
        if approvals["count"] > 0
        else "No pending approvals — focus on positive replies and proposals."
    )

    source = "runtime"
    for child in (approvals, outreach, conversations, proposals, payments, trust, cash):
        if child["source"] == "fallback":
            source = "fallback"
            break

    return {
        "top_action": top_action,
        "status": "ok" if risk_open == 0 else "needs_attention",
        "risk_flags": risk_open,
        "cash_collected_sar": _sum(cash["rows"], "amount_sar"),
        "approved_outreach": approved,
        "sent_outreach": sent,
        "positive_replies": positive_replies,
        "proposals_due": proposals["count"],
        "payment_follow_ups": payments["count"],
        "source": source,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def sales_funnel() -> dict[str, Any]:
    leads = read_runtime("lead_intelligence")
    outreach = read_runtime("outreach_queue")
    conversations = read_runtime("conversation_log")
    proposals = read_runtime("proposal_queue")
    payments = read_runtime("payment_capture_queue")

    a_leads = _count(leads["rows"], "score", "A")
    pending = _count(outreach["rows"], "state", "pending")
    approved = _count(outreach["rows"], "state", "approved")
    sent = _count(outreach["rows"], "state", "sent")
    replies = sum(
        1 for r in conversations["rows"]
        if (r.get("direction") or "").strip() == "inbound"
    )
    positive = _count(conversations["rows"], "sentiment", "positive")

    source = "runtime"
    for child in (leads, outreach, conversations, proposals, payments):
        if child["source"] == "fallback":
            source = "fallback"
            break

    return {
        "lead_intelligence_count": leads["count"],
        "a_leads": a_leads,
        "pending_approval": pending,
        "approved_outreach": approved,
        "sent": sent,
        "replies": replies,
        "positive_replies": positive,
        "samples": _count(proposals["rows"], "stage", "sample"),
        "proposals": _count(proposals["rows"], "stage", "proposal"),
        "payment_capture": payments["count"],
        "source": source,
    }


def approvals_list() -> dict[str, Any]:
    data = read_runtime("approval_queue")
    return {"items": data["rows"], "count": data["count"], "source": data["source"]}


def workers_health() -> dict[str, Any]:
    data = read_runtime("worker_state")
    return {"workers": data["rows"], "count": data["count"], "source": data["source"]}


def trust_flags() -> dict[str, Any]:
    data = read_runtime("trust_flags")
    suppression = read_runtime("suppression_list")
    a3_attempts = sum(
        1 for r in data["rows"]
        if (r.get("category") or "").strip() == "a3_attempt"
    )
    return {
        "flags": data["rows"],
        "count": data["count"],
        "suppression_count": suppression["count"],
        "a3_attempts": a3_attempts,
        "source": data["source"],
    }


def finance_summary() -> dict[str, Any]:
    cash = read_runtime("cash_collected")
    payments = read_runtime("payment_capture_queue")
    proposals = read_runtime("proposal_queue")
    pipeline = _sum(proposals["rows"], "value_sar")
    return {
        "cash_collected_sar": _sum(cash["rows"], "amount_sar"),
        "pipeline_sar": pipeline,
        "weighted_pipeline_sar": pipeline * 0.5,
        "payment_follow_ups": payments["count"],
        "mrr_sar": 0.0,  # populated once retention CSVs are wired
        "source": (
            "fallback" if any(
                d["source"] == "fallback" for d in (cash, payments, proposals)
            ) else "runtime"
        ),
    }


def distribution_summary() -> dict[str, Any]:
    sectors = read_runtime("sector_scorecard")
    channels = read_runtime("channel_scorecard")
    best_sector = None
    best_sector_pipeline = -1.0
    for row in sectors["rows"]:
        try:
            value = float(row.get("pipeline_sar") or 0)
        except ValueError:
            value = 0.0
        if value > best_sector_pipeline:
            best_sector_pipeline = value
            best_sector = row.get("sector")

    return {
        "sectors": sectors["rows"],
        "channels": channels["rows"],
        "experiments": [],
        "double_down": best_sector,
        "source": (
            "fallback" if any(
                d["source"] == "fallback" for d in (sectors, channels)
            ) else "runtime"
        ),
    }


def delivery_queue() -> dict[str, Any]:
    proposals = read_runtime("proposal_queue")
    in_delivery = [
        r for r in proposals["rows"]
        if (r.get("stage") or "").strip() in {"delivery", "kickoff"}
    ]
    return {
        "items": in_delivery,
        "count": len(in_delivery),
        "source": proposals["source"],
    }


def retention_queue() -> dict[str, Any]:
    proposals = read_runtime("proposal_queue")
    won = [r for r in proposals["rows"] if (r.get("stage") or "").strip() == "won"]
    return {"items": won, "count": len(won), "source": proposals["source"]}


def proof_library() -> dict[str, Any]:
    return {"items": [], "count": 0, "source": "fallback"}


def audit_events() -> dict[str, Any]:
    data = read_runtime("approval_decisions")
    return {"events": data["rows"], "count": data["count"], "source": data["source"]}


def eval_status() -> dict[str, Any]:
    data = read_runtime("eval_status")
    blocking = sum(
        1 for r in data["rows"] if (r.get("blocking") or "").strip().lower() == "true"
    )
    return {
        "suites": data["rows"],
        "blocking_failures": blocking,
        "source": data["source"],
    }


def productization() -> dict[str, Any]:
    data = read_runtime("productization_candidates")
    return {
        "candidates": data["rows"],
        "count": data["count"],
        "source": data["source"],
    }


def security_status() -> dict[str, Any]:
    data = read_runtime("security_status")
    return {"controls": data["rows"], "count": data["count"], "source": data["source"]}
