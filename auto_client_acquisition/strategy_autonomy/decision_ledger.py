"""Strategic decision ledger — code-backed CEO/board decision record.

Replaces a free-text ``DECISION_LEDGER.md`` with an append-only JSONL
store. Mirrors the ``capital_os.capital_ledger`` pattern: a frozen
dataclass row, a JSONL append guarded by a process lock, and an
environment-overridable path.

A decision classified as irreversible (KILL / HIRE / RAISE_PRICE /
CREATE_BUSINESS_UNIT / CREATE_VENTURE_CANDIDATE) is refused if it carries
no evidence — irreversible moves must always be grounded.
"""

from __future__ import annotations

import json
import os
import threading
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from auto_client_acquisition.strategy_autonomy.decision_types import (
    StrategicDecisionType,
    is_irreversible,
)

_DEFAULT_PATH = "var/strategic-decision-ledger.jsonl"
_lock = threading.Lock()

# Recognized lifecycle states for a strategic decision row.
_VALID_STATUSES: frozenset[str] = frozenset(
    {"recommended", "pending_approval", "approved", "rejected", "delegated"}
)


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_STRATEGIC_DECISION_LEDGER_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True, slots=True)
class StrategicDecision:
    """One CEO/board-tier strategic decision recorded to the ledger."""

    decision_id: str
    cycle_id: str
    decision_type: str
    target: str
    rationale_ar: str
    rationale_en: str
    score: float
    decision_band: str
    gate_ref: str
    evidence: tuple[str, ...] = field(default_factory=tuple)
    irreversible: bool = False
    requires_approval: bool = False
    approval_id: str = ""
    status: str = "recommended"
    customer_id: str = "dealix_strategic"
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["evidence"] = list(self.evidence)
        return data


def _decision_type_value(t: str | StrategicDecisionType) -> str:
    return t.value if isinstance(t, StrategicDecisionType) else str(t)


def record_decision(
    *,
    cycle_id: str,
    decision_type: str | StrategicDecisionType,
    target: str,
    rationale_ar: str,
    rationale_en: str,
    score: float,
    decision_band: str,
    gate_ref: str = "",
    evidence: list[str] | tuple[str, ...] | None = None,
    customer_id: str = "dealix_strategic",
    status: str = "recommended",
    approval_id: str = "",
) -> StrategicDecision:
    """Append a strategic decision to the tenant-scoped decision ledger.

    Irreversible decisions are refused when ``evidence`` is empty — an
    irreversible move must always be grounded in recorded evidence.
    """
    if not cycle_id:
        raise ValueError("cycle_id is required")
    type_str = _decision_type_value(decision_type)
    if not type_str.strip():
        raise ValueError("decision_type is required")
    if not target.strip():
        raise ValueError("target is required")
    if status not in _VALID_STATUSES:
        raise ValueError(f"invalid status: {status}")

    evidence_tuple = tuple(str(e) for e in (evidence or []) if str(e).strip())
    irreversible = is_irreversible(type_str)
    if irreversible and not evidence_tuple:
        raise ValueError(
            f"irreversible decision {type_str} requires non-empty evidence"
        )

    decision = StrategicDecision(
        decision_id=f"sd_{uuid.uuid4().hex[:12]}",
        cycle_id=cycle_id,
        decision_type=type_str,
        target=target.strip(),
        rationale_ar=rationale_ar,
        rationale_en=rationale_en,
        score=float(score),
        decision_band=decision_band,
        gate_ref=gate_ref,
        evidence=evidence_tuple,
        irreversible=irreversible,
        requires_approval=irreversible,
        approval_id=approval_id,
        status=status,
        customer_id=customer_id,
        created_at=_now_iso(),
    )
    path = _path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(decision.to_dict(), ensure_ascii=False) + "\n")
    return decision


def _read_all() -> list[StrategicDecision]:
    path = _path()
    if not path.exists():
        return []
    out: list[StrategicDecision] = []
    with _lock:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    data["evidence"] = tuple(data.get("evidence", []))
                    out.append(StrategicDecision(**data))
                except Exception:  # noqa: BLE001
                    continue
    return out


def _latest_rows() -> list[StrategicDecision]:
    """All decisions collapsed to the latest row per ``decision_id``.

    The ledger is append-only; a status transition is a new row carrying
    the same ``decision_id``. The read API therefore reflects the most
    recent row per decision (insertion order preserved, newest last).
    """
    latest: dict[str, StrategicDecision] = {}
    for row in _read_all():
        latest[row.decision_id] = row
    return list(latest.values())


def update_decision_status(
    decision_id: str,
    *,
    status: str,
    approval_id: str | None = None,
) -> StrategicDecision | None:
    """Append a status-transition row for an existing decision.

    Used to close the strategic loop: a decision recorded as
    ``pending_approval`` is advanced to ``approved`` / ``rejected`` once
    the founder acts in the Approval Center. Returns the updated row, or
    ``None`` when the decision id is unknown.
    """
    if status not in _VALID_STATUSES:
        raise ValueError(f"invalid status: {status}")
    current = get_decision(decision_id)
    if current is None:
        return None
    data = current.to_dict()
    data["status"] = status
    if approval_id is not None:
        data["approval_id"] = approval_id
    data["evidence"] = tuple(data.get("evidence", []))
    updated = StrategicDecision(**data)
    path = _path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(updated.to_dict(), ensure_ascii=False) + "\n")
    return updated


def query_decisions(
    *,
    decision_type: str | StrategicDecisionType | None = None,
    status: str | None = None,
    customer_id: str | None = None,
    cycle_id: str | None = None,
    limit: int = 200,
) -> list[StrategicDecision]:
    """Query the decision ledger with optional filters."""
    rows = _latest_rows()
    if decision_type is not None:
        type_str = _decision_type_value(decision_type)
        rows = [r for r in rows if r.decision_type == type_str]
    if status is not None:
        rows = [r for r in rows if r.status == status]
    if customer_id is not None:
        rows = [r for r in rows if r.customer_id == customer_id]
    if cycle_id is not None:
        rows = [r for r in rows if r.cycle_id == cycle_id]
    return rows[-limit:] if limit else rows


def latest_decisions(limit: int = 20) -> list[StrategicDecision]:
    """Return the most recent strategic decisions, newest last."""
    rows = _latest_rows()
    return rows[-limit:] if limit else rows


def get_decision(decision_id: str) -> StrategicDecision | None:
    """Return a single decision by id (latest status row), or None."""
    found: StrategicDecision | None = None
    for row in _read_all():
        if row.decision_id == decision_id:
            found = row
    return found


def clear_for_test() -> None:
    path = _path()
    if path.exists():
        with _lock:
            path.write_text("", encoding="utf-8")


__all__ = [
    "StrategicDecision",
    "clear_for_test",
    "get_decision",
    "latest_decisions",
    "query_decisions",
    "record_decision",
    "update_decision_status",
]
