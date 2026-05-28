"""Hermes audit ledger — append-only JSONL log of every dispatch.

Also bridges into the existing friction_log for refusals and high-severity
events so that operators see them in their normal dashboards.
"""

from __future__ import annotations

import json
import os
import threading
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .governance_gate import Decision, GovernanceDecision

# String constants mirrored from auto_client_acquisition.friction_log.schemas.
# Kept here so audit.py stays dependency-light; the actual friction_log import
# happens lazily inside bridge_to_friction_log so the heavy dep tree is only
# loaded when a customer-scoped event actually needs to be written.
_FRICTION_KIND_GOVERNANCE_BLOCK = "governance_block"
_FRICTION_KIND_APPROVAL_DELAY = "approval_delay"
_FRICTION_KIND_MANUAL_OVERRIDE = "manual_override"
_FRICTION_SEVERITY_HIGH = "high"
_FRICTION_SEVERITY_MED = "med"


_DEFAULT_PATH = "var/hermes-runs.jsonl"
_lock = threading.Lock()


def _path() -> Path:
    p = Path(os.environ.get("HERMES_AUDIT_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


@dataclass
class HermesAuditRecord:
    run_id: str
    agent_id: str
    task_class: str
    customer_id: str
    intent_summary: str
    governance_decision: dict[str, Any]
    sub_agent: str = ""
    provider: str = ""
    model_id: str = ""
    occurred_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    success: bool = False
    error: str = ""
    output_ref: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def write(record: HermesAuditRecord) -> Path:
    path = _path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock, path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record.to_dict(), ensure_ascii=False) + "\n")
    return path


def bridge_to_friction_log(
    record: HermesAuditRecord, decision: GovernanceDecision
) -> None:
    """Mirror refusals and approval-required events into friction_log.

    Lazy-imports the heavy `auto_client_acquisition.friction_log.store` only
    when there is actually a customer-scoped event to write. Failures here
    must not crash the orchestrator (audit is best-effort beyond the JSONL
    write which is already done by the caller).
    """
    if not record.customer_id:
        return

    mapping = {
        Decision.REJECTED.value: (_FRICTION_KIND_GOVERNANCE_BLOCK, _FRICTION_SEVERITY_HIGH),
        Decision.NEEDS_APPROVAL.value: (_FRICTION_KIND_APPROVAL_DELAY, _FRICTION_SEVERITY_MED),
        Decision.KILL_SWITCHED.value: (_FRICTION_KIND_MANUAL_OVERRIDE, _FRICTION_SEVERITY_HIGH),
    }
    pair = mapping.get(decision.decision)
    if pair is None:
        return
    kind, severity = pair
    try:
        from auto_client_acquisition.friction_log import store as friction_store
    except ImportError:
        return
    try:
        friction_store.emit(
            customer_id=record.customer_id,
            kind=kind,
            severity=severity,
            workflow_id=record.run_id,
            evidence_ref=str(_path()),
            notes=decision.reason,
        )
    except Exception:
        # Friction bridge is best-effort; never break the orchestrator.
        return
