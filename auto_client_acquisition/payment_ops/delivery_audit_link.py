"""Payment to delivery audit link — the traceable chain for a paid pilot.

A pilot's revenue truth must be auditable end to end:

    invoice.paid  ->  delivery started  ->  proof.pack_delivered

This module records each link as a typed ``RevenueEvent`` (taxonomy in
``auto_client_acquisition/revenue_memory/events.py``) into an append-only
JSONL ledger. Events in one chain share a ``correlation_id`` so the whole
pilot can be read back in order.

This is a recording layer only. It never charges, never sends, never runs
the Sprint. It exists so that, after a pilot, the founder can answer
"which payment produced which Proof Pack" from the ledger alone.

Storage: ``$DEALIX_DELIVERY_AUDIT_PATH`` (default ``var/delivery-audit-link.jsonl``).
Same JSONL pattern as value_ledger + friction_log + renewal_scheduler.
"""

from __future__ import annotations

import json
import os
import threading
from pathlib import Path
from typing import Any

from auto_client_acquisition.revenue_memory.events import (
    EVENT_TYPES,
    RevenueEvent,
    event_to_dict,
    make_event,
)

# The three links of the audit chain — each is a member of the canonical
# event taxonomy. ``proof.pack_requested`` marks the intermediate delivery
# step (Sprint started for this payment) so the chain has no gap.
_INVOICE_PAID = "invoice.paid"
_DELIVERY_STARTED = "proof.pack_requested"
_PROOF_DELIVERED = "proof.pack_delivered"

_DEFAULT_PATH = "var/delivery-audit-link.jsonl"
_lock = threading.Lock()


def _audit_path() -> Path:
    """Resolve the ledger path, honouring the env override."""
    p = Path(os.environ.get("DEALIX_DELIVERY_AUDIT_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parents[2] / p
    return p


def _append(event: RevenueEvent) -> None:
    """Append one event to the JSONL ledger (thread-safe, append-only)."""
    path = _audit_path()
    with _lock:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event_to_dict(event), ensure_ascii=False) + "\n")


def record_invoice_paid(
    *,
    customer_id: str,
    payment_id: str,
    amount_sar: float,
    correlation_id: str,
    evidence_reference: str = "",
    actor: str = "founder",
) -> RevenueEvent:
    """Record that a payment was confirmed — the first link of the chain.

    ``correlation_id`` ties this event to every later delivery event for the
    same pilot. ``evidence_reference`` carries the Moyasar txn id / bank ref
    so the row is auditable, never a bare "yes".
    """
    if not customer_id:
        raise ValueError("customer_id is required")
    if not payment_id:
        raise ValueError("payment_id is required")
    if not correlation_id:
        raise ValueError("correlation_id is required to keep the chain joinable")
    event = make_event(
        event_type=_INVOICE_PAID,
        customer_id=customer_id,
        subject_type="deal",
        subject_id=payment_id,
        payload={
            "payment_id": payment_id,
            "amount_sar": amount_sar,
            "evidence_reference": evidence_reference,
        },
        correlation_id=correlation_id,
        actor=actor,
    )
    _append(event)
    return event


def record_delivery_started(
    *,
    customer_id: str,
    payment_id: str,
    delivery_kickoff_id: str,
    correlation_id: str,
    causation_event_id: str | None = None,
    actor: str = "founder",
) -> RevenueEvent:
    """Record that delivery started for a confirmed payment — the middle link.

    ``delivery_kickoff_id`` is the audit handle the founder reuses as the
    Sprint ``engagement_id``. ``causation_event_id`` should be the
    ``invoice.paid`` event id so the chain is causally linked.
    """
    if not delivery_kickoff_id:
        raise ValueError("delivery_kickoff_id is required")
    if not correlation_id:
        raise ValueError("correlation_id is required to keep the chain joinable")
    event = make_event(
        event_type=_DELIVERY_STARTED,
        customer_id=customer_id,
        subject_type="deal",
        subject_id=payment_id,
        payload={
            "payment_id": payment_id,
            "delivery_kickoff_id": delivery_kickoff_id,
        },
        causation_id=causation_event_id,
        correlation_id=correlation_id,
        actor=actor,
    )
    _append(event)
    return event


def record_proof_pack_delivered(
    *,
    customer_id: str,
    payment_id: str,
    delivery_kickoff_id: str,
    correlation_id: str,
    proof_score: int | None = None,
    proof_tier: str = "",
    causation_event_id: str | None = None,
    actor: str = "founder",
) -> RevenueEvent:
    """Record that the Proof Pack was delivered — the final link of the chain.

    Completes the ``invoice.paid -> delivery -> proof`` audit trail. The
    Proof Pack content is not duplicated here; only the score/tier and the
    handles needed to locate it.
    """
    if not correlation_id:
        raise ValueError("correlation_id is required to keep the chain joinable")
    event = make_event(
        event_type=_PROOF_DELIVERED,
        customer_id=customer_id,
        subject_type="deal",
        subject_id=payment_id,
        payload={
            "payment_id": payment_id,
            "delivery_kickoff_id": delivery_kickoff_id,
            "proof_score": proof_score,
            "proof_tier": proof_tier,
        },
        causation_id=causation_event_id,
        correlation_id=correlation_id,
        actor=actor,
    )
    _append(event)
    return event


def read_chain(correlation_id: str) -> list[dict[str, Any]]:
    """Read back one pilot's audit chain, ordered by occurrence.

    Returns the events sharing ``correlation_id`` as dicts. An empty list
    means no chain has been recorded for that id yet.
    """
    if not correlation_id:
        return []
    path = _audit_path()
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get("correlation_id") == correlation_id:
                rows.append(row)
    rows.sort(key=lambda r: (r.get("occurred_at", ""), r.get("event_id", "")))
    return rows


def chain_is_complete(correlation_id: str) -> bool:
    """True when all three links (paid, delivery, proof) are recorded."""
    types = {row.get("event_type") for row in read_chain(correlation_id)}
    return {_INVOICE_PAID, _DELIVERY_STARTED, _PROOF_DELIVERED}.issubset(types)


# Fail fast at import time if the taxonomy ever drifts out from under us.
for _t in (_INVOICE_PAID, _DELIVERY_STARTED, _PROOF_DELIVERED):
    if _t not in EVENT_TYPES:  # pragma: no cover - defensive
        raise RuntimeError(f"audit-link event type not in taxonomy: {_t}")


__all__ = [
    "chain_is_complete",
    "read_chain",
    "record_delivery_started",
    "record_invoice_paid",
    "record_proof_pack_delivered",
]
