"""Full-Ops autonomous operating loop — the 7-step tick.

This module is **pure orchestration over existing primitives**. It adds no
new data model: it senses ``WorkItem`` objects into the existing
``WorkQueue``, prioritises them with the existing ``prioritizer``, routes
them to the existing ``agent_os`` agents (the Full-Ops roster), executes a
tactic that produces an **internal draft only**, gates every external
action through ``approval_center`` + the ``safe_send_gateway`` doctrine
check, and records the tick to a JSONL ledger.

The wall is step 5 (``gate``). Nothing crosses it without the founder's
click:

  - an internal-only WorkItem is recorded as a draft and stops there;
  - an external WorkItem becomes an ``approval_center.ApprovalRequest``
    with ``action_mode="approval_required"`` — never sent, never charged;
  - a WorkItem that trips the doctrine check becomes ``action_mode="blocked"``
    and the approval-center policy makes a blocked request impossible to
    approve.

The loop never calls a send/charge tool. The agents only hold internal
tools (``read``/``analyze``/``draft``/``recommend``/``queue_for_approval``).
"""
from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from auto_client_acquisition.approval_center import (
    ApprovalRequest,
    get_default_approval_store,
)
from auto_client_acquisition.full_ops.agent_roster import (
    agent_for_os,
    register_full_ops_agents,
)
from auto_client_acquisition.full_ops.prioritizer import prioritize
from auto_client_acquisition.full_ops.work_item import WorkItem
from auto_client_acquisition.full_ops.work_queue import WorkQueue, get_default_queue
from auto_client_acquisition.safe_send_gateway.doctrine import (
    enforce_doctrine_non_negotiables,
)

# OS layers whose work, by default, results in an external-facing action
# and therefore must be routed through the approval gate.
_EXTERNAL_OS = frozenset({"sales", "growth", "partnership"})

# Action modes that mean "this WorkItem reaches outside the platform".
_EXTERNAL_ACTION_MODES = frozenset({"approval_required", "approved_manual"})

# Risk-flag tokens that map to a hard doctrine violation. Any of these on a
# WorkItem forces the approval into ``blocked`` — it can never be approved.
_DOCTRINE_FLAG_MAP: dict[str, str] = {
    "cold_whatsapp": "request_cold_whatsapp",
    "whatsapp_automation": "request_cold_whatsapp",
    "linkedin_automation": "request_linkedin_automation",
    "scraping": "request_scraping",
    "web_scrape": "request_scraping",
    "bulk_outreach": "request_bulk_outreach",
    "guaranteed_sales": "request_guaranteed_sales_claim",
    "guaranteed_sales_claim": "request_guaranteed_sales_claim",
    "fake_proof": "request_fake_proof",
    "external_send_without_approval": "request_external_send_without_approval",
}


def _ledger_path() -> Path:
    """Resolve the Full-Ops tick ledger path (``DEALIX_FULL_OPS_LEDGER_PATH``).

    Follows the JSONL-store-with-env-override convention. Default is
    ``var/full_ops_tick_ledger.jsonl`` under the repo root.
    """
    raw = os.getenv("DEALIX_FULL_OPS_LEDGER_PATH", "var/full_ops_tick_ledger.jsonl")
    p = Path(raw)
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _is_external(item: WorkItem) -> bool:
    """Is this WorkItem an external-facing action that needs the gate?"""
    if item.action_mode in _EXTERNAL_ACTION_MODES:
        return True
    return item.os_type in _EXTERNAL_OS


def _doctrine_kwargs(item: WorkItem) -> dict[str, bool]:
    """Translate a WorkItem's ``risk_flags`` into doctrine-check kwargs."""
    kwargs: dict[str, bool] = {}
    for flag in item.risk_flags:
        key = _DOCTRINE_FLAG_MAP.get(flag.strip().lower())
        if key is not None:
            kwargs[key] = True
    return kwargs


# ── Step 1 — SENSE ─────────────────────────────────────────────────


def sense(
    *,
    queue: WorkQueue | None = None,
    seed_items: list[WorkItem] | None = None,
    tenant_id: str = "dealix",
) -> list[WorkItem]:
    """Collect WorkItems from the OS layers into the Full-Ops queue.

    The OS layers already publish into the shared ``WorkQueue`` (the
    Daily Command Center reads the same queue). ``sense`` therefore reads
    the live queue and, for deterministic ticks/tests, also accepts an
    explicit ``seed_items`` list which it inserts idempotently.
    """
    q = queue or get_default_queue()
    if seed_items:
        q.add_many(seed_items)
    return q.list_all(tenant_id=tenant_id)


# ── Step 3 — ASSIGN ────────────────────────────────────────────────


def assign(items: list[WorkItem]) -> list[dict[str, Any]]:
    """Route each WorkItem to a Full-Ops agent by capability tag.

    Returns a list of ``{work_item, agent_id}`` assignment records. Agents
    are registered (idempotently) before routing so the registry is always
    consistent with the roster.
    """
    register_full_ops_agents()
    assignments: list[dict[str, Any]] = []
    for item in items:
        assignments.append(
            {"work_item": item, "agent_id": agent_for_os(item.os_type)}
        )
    return assignments


# ── Step 4 — EXECUTE ───────────────────────────────────────────────


def execute(assignments: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Each assigned agent runs its tactic, producing a DRAFT artifact.

    INTERNAL ONLY. ``execute`` never performs an external send or charge —
    it builds an in-memory draft dict describing what *would* be proposed.
    The actual outside action, if any, is created by ``gate``.
    """
    drafts: list[dict[str, Any]] = []
    for record in assignments:
        item: WorkItem = record["work_item"]
        agent_id: str = record["agent_id"]
        drafts.append(
            {
                "work_item": item,
                "agent_id": agent_id,
                "artifact": {
                    "kind": "draft",
                    "os_type": item.os_type,
                    "title_ar": item.title_ar,
                    "title_en": item.title_en,
                    "summary_ar": item.description_ar or item.title_ar,
                    "summary_en": item.description_en or item.title_en,
                    "produced_by": agent_id,
                    "internal_only": True,
                },
            }
        )
    return drafts


# ── Step 5 — GATE ──────────────────────────────────────────────────


def gate(drafts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Funnel every external action through the approval gate.

    For each draft whose WorkItem is external-facing:
      1. run ``enforce_doctrine_non_negotiables`` over its risk flags;
      2. on a doctrine violation create the ApprovalRequest with
         ``action_mode="blocked"`` (approval-center policy makes a blocked
         request impossible to approve);
      3. otherwise create it with ``action_mode="approval_required"``.

    Internal-only drafts are passed through untouched — they never create
    an approval and never reach a customer.
    """
    store = get_default_approval_store()
    gated: list[dict[str, Any]] = []
    for draft in drafts:
        item: WorkItem = draft["work_item"]
        if not _is_external(item):
            gated.append({**draft, "gate": "internal_only", "approval": None})
            continue

        doctrine_kwargs = _doctrine_kwargs(item)
        blocked = False
        violation_detail = ""
        try:
            enforce_doctrine_non_negotiables(**doctrine_kwargs)
        except ValueError as exc:
            blocked = True
            violation_detail = str(exc)

        action_mode = "blocked" if blocked else "approval_required"
        req = ApprovalRequest(
            object_type="work_item",
            object_id=item.id,
            action_type="follow_up_task",
            action_mode=action_mode,
            channel=None,
            summary_ar=item.title_ar,
            summary_en=item.title_en,
            risk_level="blocked" if blocked else "low",
            proof_impact=violation_detail
            or "Records 1 governed action in the Full-Ops ledger.",
            customer_id=item.customer_id,
        )
        created = store.create(req)
        gated.append(
            {
                **draft,
                "gate": "blocked" if blocked else "approval_required",
                "approval": created.model_dump(mode="json"),
                "doctrine_violation": violation_detail or None,
            }
        )
    return gated


# ── Step 6 — RECORD ────────────────────────────────────────────────


def record(summary: dict[str, Any]) -> Path:
    """Append the tick summary to the Full-Ops JSONL tick ledger.

    One JSON line per tick. The ledger is the audit trail consulted by the
    Daily Command Center and the verifier. Returns the ledger path.
    """
    path = _ledger_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(summary, ensure_ascii=False) + "\n")
    return path


def read_tick_ledger(*, limit: int = 50) -> list[dict[str, Any]]:
    """Return the most recent recorded ticks, newest first."""
    path = _ledger_path()
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    rows.reverse()
    return rows[: max(1, int(limit))]


# ── Step 7 — RUN_TICK ──────────────────────────────────────────────


def run_tick(
    *,
    queue: WorkQueue | None = None,
    seed_items: list[WorkItem] | None = None,
    tenant_id: str = "dealix",
    record_ledger: bool = True,
) -> dict[str, Any]:
    """Run one full operating cycle and return a structured summary.

    Pipeline: sense → prioritize → assign → execute → gate → record.

    The returned dict reports WorkItems sensed, agents assigned, drafts
    produced, approvals created (``approval_required`` vs ``blocked``) and
    asserts ``sends=0`` / ``charges=0`` — the loop never performs either.
    """
    tick_id = f"tick_{datetime.now(UTC).strftime('%Y%m%dT%H%M%S%f')}"

    sensed = sense(queue=queue, seed_items=seed_items, tenant_id=tenant_id)
    prioritized = prioritize(sensed)
    assignments = assign(prioritized)
    drafts = execute(assignments)
    gated = gate(drafts)

    approvals_required = [g for g in gated if g["gate"] == "approval_required"]
    approvals_blocked = [g for g in gated if g["gate"] == "blocked"]
    internal_only = [g for g in gated if g["gate"] == "internal_only"]

    summary: dict[str, Any] = {
        "tick_id": tick_id,
        "generated_at": datetime.now(UTC).isoformat(),
        "tenant_id": tenant_id,
        "work_items_sensed": len(sensed),
        "work_items": [it.model_dump(mode="json") for it in prioritized],
        "assignments": [
            {"work_item_id": a["work_item"].id, "agent_id": a["agent_id"]}
            for a in assignments
        ],
        "drafts_produced": len(drafts),
        "approvals_created": len(approvals_required) + len(approvals_blocked),
        "approvals_required": [g["approval"] for g in approvals_required],
        "approvals_blocked": [g["approval"] for g in approvals_blocked],
        "internal_only_count": len(internal_only),
        "doctrine_violations": [
            {"work_item_id": g["work_item"].id, "detail": g["doctrine_violation"]}
            for g in gated
            if g.get("doctrine_violation")
        ],
        # The loop is internal-only by construction. These counters exist
        # so callers and tests can assert the wall held.
        "sends": 0,
        "charges": 0,
        "internal_only": True,
        "hard_gates": {
            "no_live_send": True,
            "no_live_charge": True,
            "approval_required_for_external_actions": True,
            "blocked_cannot_be_approved": True,
            "max_autonomy_level": 4,
            "l5_forbidden": True,
        },
    }

    if record_ledger:
        summary["ledger_path"] = str(record(summary))

    return summary


__all__ = [
    "assign",
    "execute",
    "gate",
    "read_tick_ledger",
    "record",
    "run_tick",
    "sense",
]
