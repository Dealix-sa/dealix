"""Private-runtime reader for the Founder Console internal API.

The Founder Console runs against a small **private** runtime store on
disk (CSV + JSON) that lives **outside** the repo. Default location is
``/opt/dealix-ops-private``; override via ``DEALIX_PRIVATE_OPS``.

Every helper here is read-mostly. Missing files return safe empty
structures and a ``source: "fallback"`` marker so the console can
render an "unwired" state without lying about production.

The append helpers are write-side primitives used by approval and
audit endpoints; both rely on the same CSV layout produced by
``scripts/bootstrap_private_ops_runtime.py``.
"""

from __future__ import annotations

import csv
import datetime as _dt
import json
import os
import uuid
from pathlib import Path
from typing import Any, Iterable

_DEFAULT_ROOT = "/opt/dealix-ops-private"
_FALLBACK = {"source": "fallback", "note": "private runtime not bootstrapped"}


def private_ops_root() -> Path:
    """Return the configured private-ops root directory."""
    root = os.environ.get("DEALIX_PRIVATE_OPS", _DEFAULT_ROOT)
    return Path(root)


def now_iso() -> str:
    """UTC ISO-8601 timestamp used by every write helper."""
    return _dt.datetime.now(_dt.UTC).replace(microsecond=0).isoformat()


# ── primitive IO ───────────────────────────────────────────────────────────

def read_csv(rel_path: str) -> list[dict[str, str]]:
    """Read a CSV under the private-ops root. Missing → empty list."""
    path = private_ops_root() / rel_path
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8", newline="") as fh:
            return list(csv.DictReader(fh))
    except Exception:
        return []


def append_csv(rel_path: str, row: dict[str, Any], header: list[str]) -> bool:
    """Append a row to a CSV. Creates the file (with header) if missing.

    Returns True on success, False on any IO error. Never raises.
    """
    path = private_ops_root() / rel_path
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        is_new = not path.exists()
        with path.open("a", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=header)
            if is_new:
                writer.writeheader()
            # Drop unknown keys defensively rather than blowing up.
            safe_row = {k: row.get(k, "") for k in header}
            writer.writerow(safe_row)
        return True
    except Exception:
        return False


def read_json(rel_path: str) -> Any:
    """Read a JSON file under the private-ops root. Missing → None."""
    path = private_ops_root() / rel_path
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def write_json(rel_path: str, data: Any) -> bool:
    """Write a JSON file under the private-ops root. Best effort."""
    path = private_ops_root() / rel_path
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return True
    except Exception:
        return False


def count_where(rows: Iterable[dict[str, Any]], **filters: Any) -> int:
    """Count rows matching every key=value filter."""
    n = 0
    for r in rows:
        if all(str(r.get(k, "")) == str(v) for k, v in filters.items()):
            n += 1
    return n


# ── high-level views consumed by the internal API ──────────────────────────

def ceo_summary() -> dict[str, Any]:
    """Top-of-funnel CEO snapshot."""
    leads = read_csv("intelligence/lead_intelligence_base.csv")
    approvals = read_csv("approvals/approval_queue.csv")
    cash = read_csv("finance/cash_collected.csv")
    incidents = read_csv("trust/incidents.csv")
    if not (leads or approvals or cash):
        return {
            **_FALLBACK,
            "leads_total": 0,
            "approvals_open": 0,
            "cash_total_sar": 0,
            "incidents_open": 0,
            "generated_at": now_iso(),
        }
    return {
        "leads_total": len(leads),
        "approvals_open": count_where(approvals, status="pending"),
        "cash_total_sar": _sum_numeric(cash, "amount_sar"),
        "incidents_open": count_where(incidents, status="open"),
        "generated_at": now_iso(),
        "source": "private_runtime",
    }


def sales_funnel_summary() -> dict[str, Any]:
    """Funnel counts by stage."""
    leads = read_csv("intelligence/lead_intelligence_base.csv")
    outreach = read_csv("outreach/outreach_queue.csv")
    convo = read_csv("outreach/conversation_log.csv")
    proposals = read_csv("sales/proposal_queue.csv")
    cash = read_csv("finance/cash_collected.csv")
    if not (leads or outreach or convo or proposals or cash):
        return {**_FALLBACK, "stages": []}
    return {
        "source": "private_runtime",
        "stages": [
            {"name": "leads", "count": len(leads)},
            {"name": "outreach_queued", "count": count_where(outreach, status="queued")},
            {"name": "replied", "count": count_where(convo, direction="inbound")},
            {"name": "proposals_open", "count": count_where(proposals, status="open")},
            {"name": "cash_collected", "count": len(cash)},
        ],
        "generated_at": now_iso(),
    }


def approvals_list() -> dict[str, Any]:
    """All rows from the approval queue. Pending first."""
    rows = read_csv("approvals/approval_queue.csv")
    if not rows:
        return {**_FALLBACK, "approvals": []}
    rows.sort(key=lambda r: (r.get("status", "") != "pending", r.get("created_at", "")))
    return {"source": "private_runtime", "approvals": rows, "generated_at": now_iso()}


def worker_health() -> dict[str, Any]:
    rows = read_csv("runtime/worker_state.csv")
    if not rows:
        return {**_FALLBACK, "workers": []}
    return {"source": "private_runtime", "workers": rows, "generated_at": now_iso()}


def trust_flags() -> dict[str, Any]:
    rows = read_csv("trust/trust_flags.csv")
    if not rows:
        return {**_FALLBACK, "flags": []}
    return {"source": "private_runtime", "flags": rows, "generated_at": now_iso()}


def finance_summary() -> dict[str, Any]:
    cash = read_csv("finance/cash_collected.csv")
    capture = read_csv("finance/payment_capture_queue.csv")
    econ = read_csv("finance/ai_unit_economics.csv")
    if not (cash or capture or econ):
        return {**_FALLBACK, "cash_total_sar": 0, "capture_open": 0}
    return {
        "source": "private_runtime",
        "cash_total_sar": _sum_numeric(cash, "amount_sar"),
        "capture_open": count_where(capture, status="open"),
        "ai_unit_economics_rows": len(econ),
        "generated_at": now_iso(),
    }


def distribution_summary() -> dict[str, Any]:
    by_channel = read_csv("distribution/channel_scorecard.csv")
    by_sector = read_csv("distribution/sector_scorecard.csv")
    if not (by_channel or by_sector):
        return {**_FALLBACK, "by_channel": [], "by_sector": []}
    return {
        "source": "private_runtime",
        "by_channel": by_channel,
        "by_sector": by_sector,
        "generated_at": now_iso(),
    }


def delivery_queue() -> dict[str, Any]:
    rows = read_csv("sales/proposal_queue.csv")
    if not rows:
        return {**_FALLBACK, "items": []}
    return {"source": "private_runtime", "items": rows, "generated_at": now_iso()}


def retention_queue() -> dict[str, Any]:
    rows = read_csv("trust/trust_flags.csv")
    rows = [r for r in rows if r.get("category", "") == "retention"]
    if not rows:
        return {**_FALLBACK, "items": []}
    return {"source": "private_runtime", "items": rows, "generated_at": now_iso()}


def proof_library() -> dict[str, Any]:
    incidents = read_csv("trust/incidents.csv")
    return {
        "source": "private_runtime" if incidents else "fallback",
        "items": [],
        "note": "proof library deliberately empty until founder approves publishing",
        "generated_at": now_iso(),
    }


def audit_events(limit: int = 200) -> dict[str, Any]:
    rows = read_csv("trust/approval_decisions.csv")
    rows.sort(key=lambda r: r.get("decided_at", ""), reverse=True)
    return {
        "source": "private_runtime" if rows else "fallback",
        "events": rows[:limit],
        "generated_at": now_iso(),
    }


def control_summary() -> dict[str, Any]:
    return {
        "source": "computed",
        "policies": policies_summary(),
        "agents": agent_registry(),
        "evals": eval_status(),
        "scorecard": operating_scorecard(),
        "sovereign": sovereign_readiness(),
        "generated_at": now_iso(),
    }


def policies_summary() -> dict[str, Any]:
    path = Path("policies/dealix_control_policy.yaml")
    if not path.exists():
        return {**_FALLBACK, "classes": [], "rules": []}
    text = path.read_text(encoding="utf-8")
    # Lightweight parse — we don't want a hard PyYAML dep just for counts.
    classes = [ln.split(":")[0].strip(" -") for ln in text.splitlines()
               if ln.lstrip().startswith("- id:")]
    rules = [ln.split(":")[0].strip(" -") for ln in text.splitlines()
             if ln.lstrip().startswith("- name:")]
    return {
        "source": "policy_yaml",
        "classes_count": len([c for c in classes if c]),
        "rules_count": len([r for r in rules if r]),
    }


def agent_registry() -> dict[str, Any]:
    path = Path("registries/agent_registry.yaml")
    if not path.exists():
        return {**_FALLBACK, "agents": []}
    text = path.read_text(encoding="utf-8")
    agents = [ln.split(":", 1)[1].strip() for ln in text.splitlines()
              if ln.lstrip().startswith("- id:")]
    return {"source": "registry_yaml", "agents": agents, "count": len(agents)}


def eval_status() -> dict[str, Any]:
    path = Path("evals/gates/dealix_agent_eval_gate.yaml")
    if not path.exists():
        return {**_FALLBACK, "suites": []}
    text = path.read_text(encoding="utf-8")
    suites = [ln.split(":", 1)[1].strip() for ln in text.splitlines()
              if ln.lstrip().startswith("- name:")]
    return {"source": "eval_yaml", "suites": suites, "count": len(suites)}


def productization() -> dict[str, Any]:
    rows = read_csv("product/productization_candidates.csv")
    if not rows:
        return {**_FALLBACK, "candidates": []}
    return {"source": "private_runtime", "candidates": rows, "generated_at": now_iso()}


def security_status() -> dict[str, Any]:
    rows = read_csv("security/security_status.csv")
    if not rows:
        return {
            **_FALLBACK,
            "items": [],
            "auth_mode_hint": "Set DEALIX_INTERNAL_TOKEN to enforce internal API auth.",
        }
    return {"source": "private_runtime", "items": rows, "generated_at": now_iso()}


def operating_scorecard() -> dict[str, Any]:
    md = (private_ops_root() / "founder/operating_scorecard.md")
    if not md.exists():
        return {**_FALLBACK, "scorecard_md": None}
    try:
        return {
            "source": "private_runtime",
            "scorecard_md": md.read_text(encoding="utf-8"),
            "generated_at": now_iso(),
        }
    except Exception:
        return {**_FALLBACK, "scorecard_md": None}


def sovereign_readiness() -> dict[str, Any]:
    md = (private_ops_root() / "founder/sovereign_readiness.md")
    if not md.exists():
        return {**_FALLBACK, "readiness_md": None}
    try:
        return {
            "source": "private_runtime",
            "readiness_md": md.read_text(encoding="utf-8"),
            "generated_at": now_iso(),
        }
    except Exception:
        return {**_FALLBACK, "readiness_md": None}


# ── write-side helpers for approval flow ───────────────────────────────────

_APPROVAL_DECISION_HEADER = [
    "id",
    "approval_id",
    "decision",
    "reason",
    "decided_by",
    "decided_at",
    "policy_class",
]


def record_approval_decision(
    approval_id: str,
    decision: str,
    reason: str | None,
    decided_by: str,
    policy_class: str = "A2",
) -> dict[str, Any]:
    """Append an approval decision to the audit log."""
    row = {
        "id": uuid.uuid4().hex,
        "approval_id": approval_id,
        "decision": decision,
        "reason": (reason or "").strip(),
        "decided_by": decided_by,
        "decided_at": now_iso(),
        "policy_class": policy_class,
    }
    ok = append_csv("trust/approval_decisions.csv", row, _APPROVAL_DECISION_HEADER)
    return {"ok": ok, "decision": row}


_INCIDENT_HEADER = ["id", "kind", "target", "reason", "opened_at", "opened_by", "status"]


def record_incident(kind: str, target: str, reason: str, opened_by: str = "founder") -> dict[str, Any]:
    row = {
        "id": uuid.uuid4().hex,
        "kind": kind,
        "target": target,
        "reason": reason,
        "opened_at": now_iso(),
        "opened_by": opened_by,
        "status": "open",
    }
    ok = append_csv("trust/incidents.csv", row, _INCIDENT_HEADER)
    return {"ok": ok, "incident": row}


# ── small helpers ──────────────────────────────────────────────────────────

def _sum_numeric(rows: Iterable[dict[str, Any]], key: str) -> float:
    total = 0.0
    for r in rows:
        raw = (r.get(key, "") or "0").strip()
        try:
            total += float(raw)
        except (TypeError, ValueError):
            continue
    return round(total, 2)
