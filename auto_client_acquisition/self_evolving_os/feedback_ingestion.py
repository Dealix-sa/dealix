"""Feedback ingestion — translate ledger outcomes into FeedbackEvents.

The self-evolving layer (L11) listens to three signals from the rest of the
AI Stack:

* **Value OS** — confirmed monetary outcomes (``ValueEvent``).
* **Adoption OS** — adoption / friction signals on a retainer.
* **Customer feedback** — explicit thumbs-up/down events the client surfaces.

Each signal is normalized into a :class:`FeedbackEvent` with a discrete
:class:`OutcomeKind` so the learning store can attribute the outcome back to
a specific decision passport, agent, and model task.

This module is **shadow-mode only**: it records observations, never reaches
back into the router or mesh to mutate behavior. Any mutation requires an
approved :class:`ImprovementProposal`.
"""

from __future__ import annotations

import uuid
from collections.abc import Mapping
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timezone
from enum import StrEnum
from typing import Any


class OutcomeKind(StrEnum):
    """Discrete outcome categories the learning store understands."""

    SUCCESS = "success"
    PARTIAL = "partial"
    FAILURE = "failure"
    BLOCKED_BY_GOVERNANCE = "blocked_by_governance"
    BLOCKED_BY_DOCTRINE = "blocked_by_doctrine"
    CUSTOMER_CONFIRMED = "customer_confirmed"
    CUSTOMER_REJECTED = "customer_rejected"
    NO_SIGNAL = "no_signal"


_VALID_LAYERS: frozenset[str] = frozenset(
    {
        "L1_source_passport",
        "L2_data_quality",
        "L3_intelligence",
        "L4_model_router",
        "L5_agent_mesh",
        "L6_governance",
        "L7_proof_pack",
        "L8_value_ledger",
        "L9_capital_ledger",
        "L10_adoption",
        "L11_self_evolving",
    }
)


@dataclass(frozen=True, slots=True)
class FeedbackEvent:
    """A normalized ledger observation ready for shadow-mode learning."""

    event_id: str
    tenant_id: str
    run_id: str
    layer: str
    outcome_kind: str
    outcome_value: float | None
    doctrine_clean: bool
    decision_id: str | None = None
    agent_name: str | None = None
    model_task: str | None = None
    learnings: Mapping[str, Any] = field(default_factory=dict)
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["learnings"] = dict(self.learnings)
        return data


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _validate_layer(layer: str) -> None:
    if layer not in _VALID_LAYERS:
        raise ValueError(
            f"unknown layer: {layer!r} (allowed: {sorted(_VALID_LAYERS)})"
        )


def make_feedback_event(
    *,
    tenant_id: str,
    run_id: str,
    layer: str,
    outcome_kind: OutcomeKind | str,
    outcome_value: float | None = None,
    doctrine_clean: bool = True,
    decision_id: str | None = None,
    agent_name: str | None = None,
    model_task: str | None = None,
    learnings: Mapping[str, Any] | None = None,
) -> FeedbackEvent:
    """Construct a validated feedback event ready for the learning store."""
    if not tenant_id or not tenant_id.strip():
        raise ValueError("tenant_id is required")
    if not run_id or not run_id.strip():
        raise ValueError("run_id is required")
    _validate_layer(layer)
    kind_value = outcome_kind.value if isinstance(outcome_kind, OutcomeKind) else str(outcome_kind)
    try:
        OutcomeKind(kind_value)
    except ValueError as exc:
        raise ValueError(
            f"unknown outcome_kind: {kind_value!r} (allowed: {[k.value for k in OutcomeKind]})"
        ) from exc
    return FeedbackEvent(
        event_id=f"fb_{uuid.uuid4().hex[:16]}",
        tenant_id=tenant_id.strip(),
        run_id=run_id.strip(),
        layer=layer,
        outcome_kind=kind_value,
        outcome_value=float(outcome_value) if outcome_value is not None else None,
        doctrine_clean=bool(doctrine_clean),
        decision_id=decision_id,
        agent_name=agent_name,
        model_task=model_task,
        learnings=dict(learnings or {}),
        created_at=_now_iso(),
    )


def from_value_event(
    *,
    tenant_id: str,
    run_id: str,
    value_event: Mapping[str, Any],
) -> FeedbackEvent:
    """Translate a value_ledger event into a feedback event.

    Mapping:

    * ``tier == 'client_confirmed'`` → ``CUSTOMER_CONFIRMED``
    * ``tier == 'verified'`` → ``SUCCESS``
    * ``tier == 'observed'`` → ``PARTIAL``
    * else → ``NO_SIGNAL``
    """
    tier = str(value_event.get("tier", "")).strip().lower()
    amount = float(value_event.get("amount", 0.0))
    mapping = {
        "client_confirmed": OutcomeKind.CUSTOMER_CONFIRMED,
        "verified": OutcomeKind.SUCCESS,
        "observed": OutcomeKind.PARTIAL,
    }
    kind = mapping.get(tier, OutcomeKind.NO_SIGNAL)
    return make_feedback_event(
        tenant_id=tenant_id,
        run_id=run_id,
        layer="L8_value_ledger",
        outcome_kind=kind,
        outcome_value=amount,
        doctrine_clean=True,
        learnings={
            "tier": tier,
            "kind": str(value_event.get("kind", "")),
            "source_ref": str(value_event.get("source_ref", "")),
        },
    )


def from_friction_log(
    *,
    tenant_id: str,
    run_id: str,
    friction_event: Mapping[str, Any],
) -> FeedbackEvent:
    """Friction log entries are partial-success or failure signals.

    ``impact`` field determines the kind:
        * ``high`` / ``blocker`` → FAILURE
        * ``medium`` → PARTIAL
        * anything else → NO_SIGNAL
    """
    impact = str(friction_event.get("impact", "")).strip().lower()
    mapping = {
        "high": OutcomeKind.FAILURE,
        "blocker": OutcomeKind.FAILURE,
        "medium": OutcomeKind.PARTIAL,
    }
    kind = mapping.get(impact, OutcomeKind.NO_SIGNAL)
    return make_feedback_event(
        tenant_id=tenant_id,
        run_id=run_id,
        layer="L10_adoption",
        outcome_kind=kind,
        outcome_value=None,
        doctrine_clean=True,
        learnings={
            "friction_type": str(friction_event.get("friction_type", "")),
            "description": str(friction_event.get("description", ""))[:200],
            "product_signal": str(friction_event.get("product_signal", "")),
        },
    )


def from_governance_block(
    *,
    tenant_id: str,
    run_id: str,
    layer: str,
    reason: str,
    decision_id: str | None = None,
) -> FeedbackEvent:
    """A governance block is always a failure attributed to the offending layer."""
    _validate_layer(layer)
    return make_feedback_event(
        tenant_id=tenant_id,
        run_id=run_id,
        layer=layer,
        outcome_kind=OutcomeKind.BLOCKED_BY_GOVERNANCE,
        outcome_value=0.0,
        doctrine_clean=False,
        decision_id=decision_id,
        learnings={"reason": reason},
    )


def from_doctrine_violation(
    *,
    tenant_id: str,
    run_id: str,
    layer: str,
    violation: str,
    decision_id: str | None = None,
) -> FeedbackEvent:
    """A doctrine violation is always a failure with ``doctrine_clean=False``."""
    _validate_layer(layer)
    return make_feedback_event(
        tenant_id=tenant_id,
        run_id=run_id,
        layer=layer,
        outcome_kind=OutcomeKind.BLOCKED_BY_DOCTRINE,
        outcome_value=0.0,
        doctrine_clean=False,
        decision_id=decision_id,
        learnings={"violation": violation},
    )


__all__ = [
    "FeedbackEvent",
    "OutcomeKind",
    "from_doctrine_violation",
    "from_friction_log",
    "from_governance_block",
    "from_value_event",
    "make_feedback_event",
]
