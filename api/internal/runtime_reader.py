"""Read-only / append-only access to the private ops runtime tree.

The Dealix Operating Layer keeps its operational CSV state outside the
public repo at ``$DEALIX_PRIVATE_OPS`` (default ``/opt/dealix-ops-private``).
All Founder Console endpoints read from here. Missing files return safe
empty structures with ``source: "fallback"`` so the UI never crashes.

See docs/runtime/PRIVATE_OPS_RUNTIME_CONTRACT.md.
"""

from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

PRIVATE_OPS_ENV = "DEALIX_PRIVATE_OPS"
DEFAULT_PRIVATE_OPS = "/opt/dealix-ops-private"


# ── Path helpers ──────────────────────────────────────────────────


def private_ops_root() -> Path:
    return Path(os.environ.get(PRIVATE_OPS_ENV, DEFAULT_PRIVATE_OPS))


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── Generic CSV helpers ───────────────────────────────────────────


def read_csv(rel_path: str) -> list[dict[str, str]]:
    path = private_ops_root() / rel_path
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            return [dict(row) for row in reader]
    except Exception:
        return []


def append_csv(rel_path: str, fieldnames: list[str], row: dict[str, Any]) -> bool:
    path = private_ops_root() / rel_path
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        is_new = not path.exists()
        with path.open("a", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            if is_new:
                writer.writeheader()
            writer.writerow({k: row.get(k, "") for k in fieldnames})
        return True
    except Exception:
        return False


def count_where(rows: Iterable[dict[str, str]], **filters: str) -> int:
    n = 0
    for row in rows:
        ok = True
        for key, value in filters.items():
            if row.get(key) != value:
                ok = False
                break
        if ok:
            n += 1
    return n


# ── Domain summaries ──────────────────────────────────────────────


def _envelope(payload: dict[str, Any], source: str) -> dict[str, Any]:
    return {"source": source, "as_of": now_iso(), **payload}


def ceo_summary() -> dict[str, Any]:
    intel = read_csv("intelligence/lead_intelligence_base.csv")
    outreach = read_csv("outreach/outreach_queue.csv")
    replies = read_csv("outreach/conversation_log.csv")
    proposals = read_csv("sales/proposal_queue.csv")
    cash = read_csv("finance/cash_collected.csv")
    workers = read_csv("runtime/worker_state.csv")

    if not (intel or outreach or replies or proposals or cash or workers):
        return _envelope(
            {
                "top_action": "Bootstrap private ops runtime: make bootstrap-runtime",
                "status": "fallback",
                "leads": 0,
                "approved_outreach": 0,
                "positive_replies": 0,
                "proposals_due": 0,
                "payment_followups": 0,
                "worker_failures": 0,
                "cash_collected": 0,
                "risk_flags": ["private_ops_empty"],
            },
            source="fallback",
        )

    cash_total = 0.0
    for row in cash:
        try:
            cash_total += float(row.get("amount", 0) or 0)
        except ValueError:
            continue

    return _envelope(
        {
            "top_action": "Review pending approvals",
            "status": "operational",
            "leads": len(intel),
            "approved_outreach": count_where(outreach, status="approved"),
            "positive_replies": count_where(replies, classification="positive"),
            "proposals_due": count_where(proposals, status="due"),
            "payment_followups": count_where(read_csv("finance/payment_capture_queue.csv"), status="due"),
            "worker_failures": sum(int(r.get("failures_24h", 0) or 0) for r in workers),
            "cash_collected": cash_total,
            "risk_flags": [],
        },
        source="private_ops",
    )


def sales_funnel_summary() -> dict[str, Any]:
    intel = read_csv("intelligence/lead_intelligence_base.csv")
    outreach = read_csv("outreach/outreach_queue.csv")
    replies = read_csv("outreach/conversation_log.csv")
    proposals = read_csv("sales/proposal_queue.csv")
    if not (intel or outreach or replies or proposals):
        return _envelope({"stages": [], "note": "no data yet"}, source="fallback")
    return _envelope(
        {
            "stages": [
                {"name": "leads", "count": len(intel)},
                {"name": "outreach_drafts", "count": count_where(outreach, status="draft")},
                {"name": "outreach_approved", "count": count_where(outreach, status="approved")},
                {"name": "positive_replies", "count": count_where(replies, classification="positive")},
                {"name": "proposals_open", "count": count_where(proposals, status="open")},
                {"name": "proposals_won", "count": count_where(proposals, status="won")},
            ]
        },
        source="private_ops",
    )


def approvals_list() -> dict[str, Any]:
    rows = read_csv("approvals/approval_queue.csv")
    if not rows:
        return _envelope({"items": []}, source="fallback")
    pending = [r for r in rows if r.get("status") in {"", "pending", None}]
    return _envelope({"items": pending}, source="private_ops")


def finance_summary() -> dict[str, Any]:
    cash = read_csv("finance/cash_collected.csv")
    payments = read_csv("finance/payment_capture_queue.csv")
    proposals = read_csv("sales/proposal_queue.csv")
    if not (cash or payments or proposals):
        return _envelope({"cash_total": 0, "mrr": 0, "pipeline": 0, "weighted_pipeline": 0, "payment_followups": 0}, source="fallback")
    cash_total = sum(float(r.get("amount", 0) or 0) for r in cash if r.get("amount"))
    mrr = sum(float(r.get("mrr", 0) or 0) for r in cash if r.get("mrr"))
    pipeline = sum(float(r.get("value", 0) or 0) for r in proposals if r.get("value"))
    weighted = sum(float(r.get("value", 0) or 0) * float(r.get("probability", 0) or 0) for r in proposals if r.get("value"))
    return _envelope(
        {
            "cash_total": cash_total,
            "mrr": mrr,
            "pipeline": pipeline,
            "weighted_pipeline": weighted,
            "payment_followups": count_where(payments, status="due"),
        },
        source="private_ops",
    )


def worker_health() -> dict[str, Any]:
    rows = read_csv("runtime/worker_state.csv")
    if not rows:
        return _envelope({"workers": []}, source="fallback")
    return _envelope({"workers": rows}, source="private_ops")


def trust_flags() -> dict[str, Any]:
    rows = read_csv("trust/trust_flags.csv")
    if not rows:
        return _envelope({"flags": []}, source="fallback")
    return _envelope({"flags": rows}, source="private_ops")


def distribution_summary() -> dict[str, Any]:
    channels = read_csv("distribution/channel_scorecard.csv")
    sectors = read_csv("distribution/sector_scorecard.csv")
    if not (channels or sectors):
        return _envelope({"channels": [], "sectors": [], "double_down": None}, source="fallback")
    return _envelope(
        {"channels": channels, "sectors": sectors, "double_down": _pick_double_down(channels)},
        source="private_ops",
    )


def _pick_double_down(channels: list[dict[str, str]]) -> str | None:
    best: tuple[float, str] | None = None
    for row in channels:
        try:
            roi = float(row.get("roi", 0) or 0)
        except ValueError:
            continue
        name = row.get("channel", "")
        if name and (best is None or roi > best[0]):
            best = (roi, name)
    return best[1] if best else None


def delivery_queue() -> dict[str, Any]:
    rows = read_csv("delivery/delivery_queue.csv")
    if not rows:
        return _envelope({"items": []}, source="fallback")
    return _envelope({"items": rows}, source="private_ops")


def retention_queue() -> dict[str, Any]:
    rows = read_csv("retention/retention_queue.csv")
    if not rows:
        return _envelope({"items": []}, source="fallback")
    return _envelope({"items": rows}, source="private_ops")


def proof_library() -> dict[str, Any]:
    rows = read_csv("proof/proof_library.csv")
    if not rows:
        return _envelope({"items": []}, source="fallback")
    return _envelope({"items": rows}, source="private_ops")


def audit_events() -> dict[str, Any]:
    rows = read_csv("trust/approval_decisions.csv")
    if not rows:
        return _envelope({"events": []}, source="fallback")
    return _envelope({"events": rows[-200:]}, source="private_ops")


def control_summary() -> dict[str, Any]:
    from api.internal.policy_adapter import load_policy, load_agents, load_eval_gate

    policy = load_policy()
    agents = load_agents()
    eval_gate = load_eval_gate()
    scorecard = operating_scorecard()
    return _envelope(
        {
            "policies": len(policy.get("rules", [])) if policy else 0,
            "agents": len(agents.get("agents", [])) if agents else 0,
            "eval_suites": len(eval_gate.get("suites", [])) if eval_gate else 0,
            "scorecard": scorecard,
        },
        source="config",
    )


def policies_summary() -> dict[str, Any]:
    from api.internal.policy_adapter import load_policy

    policy = load_policy() or {}
    return _envelope(
        {
            "version": policy.get("version"),
            "classes": policy.get("approval_classes", []),
            "rules": policy.get("rules", []),
            "trust_gates": policy.get("trust_gates", []),
        },
        source="config",
    )


def agent_registry() -> dict[str, Any]:
    from api.internal.policy_adapter import load_agents

    agents = (load_agents() or {}).get("agents", [])
    return _envelope({"agents": agents}, source="config")


def eval_status() -> dict[str, Any]:
    rows = read_csv("evals/eval_status.csv")
    from api.internal.policy_adapter import load_eval_gate

    gate = (load_eval_gate() or {}).get("suites", [])
    return _envelope(
        {"suites": gate, "results": rows},
        source="config+private_ops" if rows else "config",
    )


def productization() -> dict[str, Any]:
    rows = read_csv("product/productization_candidates.csv")
    if not rows:
        return _envelope({"candidates": []}, source="fallback")
    return _envelope({"candidates": rows}, source="private_ops")


def security_status() -> dict[str, Any]:
    rows = read_csv("security/security_status.csv")
    env_token_set = bool(os.environ.get("DEALIX_INTERNAL_TOKEN"))
    private_ops_set = bool(os.environ.get(PRIVATE_OPS_ENV))
    payload = {
        "internal_token_set": env_token_set,
        "private_ops_env_set": private_ops_set,
        "private_ops_path": str(private_ops_root()),
        "checks": rows,
    }
    return _envelope(payload, source="env+private_ops" if rows else "env")


def operating_scorecard() -> dict[str, Any]:
    path = private_ops_root() / "founder" / "operating_scorecard.md"
    if not path.exists():
        return {
            "revenue_score": None,
            "trust_score": None,
            "runtime_score": None,
            "founder_leverage_score": None,
            "productization_score": None,
            "top_bottleneck": "operating_scorecard.md missing — run make operating-scorecard",
            "next_best_action": "make operating-scorecard PRIVATE_OPS=$DEALIX_PRIVATE_OPS",
            "source": "fallback",
        }
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        text = ""
    return {"markdown": text, "source": "private_ops"}
