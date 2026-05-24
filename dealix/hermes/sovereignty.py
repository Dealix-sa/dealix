"""
Sovereignty Gate — the only path through which an action may execute.

Sovereignty levels
------------------
S0  AUTONOMOUS         — fully automated, internal, reversible
S1  INTERNAL           — internal action, audited, no external recipient
S2  SAMI_APPROVAL      — Sami must explicitly approve before execute
S3  SOVEREIGN_MEMO     — Sami approves a written memo (commercial / partner)
S4  SOVEREIGN_RESERVED — only Sami may initiate (public API, marketplace,
                          white-label commercials, venture spin-out, M&A)

Every `Action` MUST carry a `sovereignty_level`. The gate evaluates whether
the action can proceed automatically, must queue for approval, or is blocked
outright. The gate is the *only* path to execution: agents do not call tools
directly — they propose actions which the gate adjudicates.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4


class SovereigntyLevel(StrEnum):
    S0_AUTONOMOUS = "S0_AUTONOMOUS"
    S1_INTERNAL = "S1_INTERNAL"
    S2_SAMI_APPROVAL = "S2_SAMI_APPROVAL"
    S3_SOVEREIGN_MEMO = "S3_SOVEREIGN_MEMO"
    S4_SOVEREIGN_RESERVED = "S4_SOVEREIGN_RESERVED"

    @property
    def requires_approval(self) -> bool:
        return self in {
            SovereigntyLevel.S2_SAMI_APPROVAL,
            SovereigntyLevel.S3_SOVEREIGN_MEMO,
            SovereigntyLevel.S4_SOVEREIGN_RESERVED,
        }

    @property
    def requires_written_memo(self) -> bool:
        return self in {
            SovereigntyLevel.S3_SOVEREIGN_MEMO,
            SovereigntyLevel.S4_SOVEREIGN_RESERVED,
        }


class GateVerdict(StrEnum):
    ALLOW = "allow"
    QUEUE_APPROVAL = "queue_approval"
    BLOCK = "block"


# Actions that are *always* blocked unless executed under explicit S3+ memo,
# even if the proposing agent claims a lower level. The gate enforces the
# floor — agents cannot downgrade these.
SOVEREIGN_FLOOR_ACTIONS: frozenset[str] = frozenset(
    {
        "send_external_message",
        "publish_public_api",
        "publish_marketplace_listing",
        "sign_partnership_agreement",
        "claim_partnership",
        "execute_payment",
        "issue_refund",
        "change_pricing_published",
        "export_customer_data",
        "delete_customer_data",
        "white_label_terms_change",
        "venture_spin_out",
        "acquire_entity",
    }
)


SOVEREIGN_RESERVED_ACTIONS: frozenset[str] = frozenset(
    {
        "publish_public_api",
        "publish_marketplace_listing",
        "white_label_terms_change",
        "venture_spin_out",
        "acquire_entity",
    }
)


@dataclass(slots=True)
class Action:
    """A proposed action awaiting gate adjudication."""

    action_type: str
    payload: dict[str, Any]
    proposed_by: str
    sovereignty_level: SovereigntyLevel
    risk_level: float = 0.0  # 0.0–1.0
    expected_value_sar: float = 0.0
    expected_outcome: str = ""
    outcome_required: bool = True
    action_id: str = field(default_factory=lambda: str(uuid4()))
    proposed_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        if not 0.0 <= self.risk_level <= 1.0:
            raise ValueError("risk_level must be between 0.0 and 1.0")
        if not self.action_type:
            raise ValueError("action_type is required")
        if not self.proposed_by:
            raise ValueError("proposed_by is required")


@dataclass(slots=True)
class GateDecision:
    """Verdict returned by the sovereignty gate."""

    action_id: str
    verdict: GateVerdict
    enforced_level: SovereigntyLevel
    reason: str
    approval_required: bool
    memo_required: bool
    decided_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class SovereigntyGate:
    """Single chokepoint that decides whether an `Action` may execute.

    The gate is deterministic and side-effect-free: it returns a `GateDecision`.
    Persisting the decision and enqueueing approvals is the orchestrator's job.
    """

    def evaluate(self, action: Action) -> GateDecision:
        floor = self._floor_level(action)
        enforced = max((action.sovereignty_level, floor), key=self._level_order)

        if enforced is SovereigntyLevel.S4_SOVEREIGN_RESERVED:
            return GateDecision(
                action_id=action.action_id,
                verdict=GateVerdict.QUEUE_APPROVAL,
                enforced_level=enforced,
                reason="S4 sovereign-reserved: only Sami may initiate.",
                approval_required=True,
                memo_required=True,
            )

        if enforced is SovereigntyLevel.S3_SOVEREIGN_MEMO:
            return GateDecision(
                action_id=action.action_id,
                verdict=GateVerdict.QUEUE_APPROVAL,
                enforced_level=enforced,
                reason="Commercial / partner action requires written memo.",
                approval_required=True,
                memo_required=True,
            )

        if enforced is SovereigntyLevel.S2_SAMI_APPROVAL:
            return GateDecision(
                action_id=action.action_id,
                verdict=GateVerdict.QUEUE_APPROVAL,
                enforced_level=enforced,
                reason="Sami approval required before execute.",
                approval_required=True,
                memo_required=False,
            )

        # S0 / S1 — allow but still audited
        return GateDecision(
            action_id=action.action_id,
            verdict=GateVerdict.ALLOW,
            enforced_level=enforced,
            reason="Internal action permitted under sovereign floor.",
            approval_required=False,
            memo_required=False,
        )

    @staticmethod
    def _level_order(level: SovereigntyLevel) -> int:
        return [
            SovereigntyLevel.S0_AUTONOMOUS,
            SovereigntyLevel.S1_INTERNAL,
            SovereigntyLevel.S2_SAMI_APPROVAL,
            SovereigntyLevel.S3_SOVEREIGN_MEMO,
            SovereigntyLevel.S4_SOVEREIGN_RESERVED,
        ].index(level)

    @staticmethod
    def _floor_level(action: Action) -> SovereigntyLevel:
        if action.action_type in SOVEREIGN_RESERVED_ACTIONS:
            return SovereigntyLevel.S4_SOVEREIGN_RESERVED
        if action.action_type in SOVEREIGN_FLOOR_ACTIONS:
            return SovereigntyLevel.S3_SOVEREIGN_MEMO
        if action.risk_level >= 0.8:
            return SovereigntyLevel.S2_SAMI_APPROVAL
        if action.risk_level >= 0.5:
            return SovereigntyLevel.S1_INTERNAL
        return SovereigntyLevel.S0_AUTONOMOUS


__all__ = [
    "SovereigntyLevel",
    "GateVerdict",
    "Action",
    "GateDecision",
    "SovereigntyGate",
    "SOVEREIGN_FLOOR_ACTIONS",
    "SOVEREIGN_RESERVED_ACTIONS",
]
