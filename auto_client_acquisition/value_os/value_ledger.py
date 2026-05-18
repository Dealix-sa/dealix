"""Value ledger events (cross-package stable import path: ``value_os``)."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

from auto_client_acquisition.proof_architecture_os.value_ledger import (
    ValueLedgerEvent,
    value_ledger_event_valid,
)

_VALID_TIERS = frozenset({"estimated", "observed", "verified", "client_confirmed"})
_STORE: dict[str, list["ValueEvent"]] = {}


class ValueDisciplineError(ValueError):
    """Tier discipline violation (missing source_ref / confirmation_ref)."""


@dataclass(frozen=True, slots=True)
class ValueEvent:
    """Customer value event for monthly reports."""

    tier: str
    occurred_at: str
    kind: str = ""
    amount: float = 0.0
    source_ref: str = ""
    confirmation_ref: str = ""
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return dict(asdict(self))


def _validate_tier(*, tier: str, source_ref: str, confirmation_ref: str) -> None:
    if tier not in _VALID_TIERS:
        raise ValueDisciplineError(f"invalid_tier:{tier}")
    if tier in ("verified", "client_confirmed") and not source_ref.strip():
        raise ValueDisciplineError("verified_and_client_confirmed_require_source_ref")
    if tier == "client_confirmed" and not confirmation_ref.strip():
        raise ValueDisciplineError("client_confirmed_requires_confirmation_ref")


def add_event(
    *,
    customer_id: str,
    kind: str,
    amount: float,
    tier: str,
    source_ref: str = "",
    confirmation_ref: str = "",
    notes: str = "",
) -> ValueEvent:
    _validate_tier(tier=tier, source_ref=source_ref, confirmation_ref=confirmation_ref)
    event = ValueEvent(
        tier=tier,
        occurred_at=datetime.now(timezone.utc).isoformat(),
        kind=kind,
        amount=amount,
        source_ref=source_ref,
        confirmation_ref=confirmation_ref,
        notes=notes,
    )
    _STORE.setdefault(customer_id, []).append(event)
    return event


def list_events(*, customer_id: str) -> list[ValueEvent]:
    return list(_STORE.get(customer_id, []))


__all__ = [
    "ValueLedgerEvent",
    "ValueEvent",
    "ValueDisciplineError",
    "add_event",
    "list_events",
    "value_ledger_event_valid",
]
