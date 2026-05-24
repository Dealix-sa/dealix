"""Evidence Pack Builder — bundles every artifact behind a high-stakes action."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from dealix.hermes.core.schemas import (
    Asset,
    Decision,
    Execution,
    Opportunity,
    Outcome,
    Signal,
)


@dataclass
class EvidencePack:
    pack_id: str
    title: str
    created_at: datetime
    signal: dict[str, Any] | None = None
    opportunity: dict[str, Any] | None = None
    decision: dict[str, Any] | None = None
    execution: dict[str, Any] | None = None
    outcome: dict[str, Any] | None = None
    asset: dict[str, Any] | None = None
    audit_event_ids: list[str] = field(default_factory=list)
    approval_id: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "pack_id": self.pack_id,
            "title": self.title,
            "created_at": self.created_at.isoformat(),
            "signal": self.signal,
            "opportunity": self.opportunity,
            "decision": self.decision,
            "execution": self.execution,
            "outcome": self.outcome,
            "asset": self.asset,
            "audit_event_ids": self.audit_event_ids,
            "approval_id": self.approval_id,
        }


class EvidencePackBuilder:
    """Builds evidence packs by composing kernel objects."""

    @staticmethod
    def build(
        *,
        title: str,
        signal: Signal | None = None,
        opportunity: Opportunity | None = None,
        decision: Decision | None = None,
        execution: Execution | None = None,
        outcome: Outcome | None = None,
        asset: Asset | None = None,
        audit_event_ids: list[str] | None = None,
        approval_id: str | None = None,
    ) -> EvidencePack:
        from uuid import uuid4

        return EvidencePack(
            pack_id=f"evd_{uuid4().hex[:12]}",
            title=title,
            created_at=datetime.now(timezone.utc),
            signal=signal.model_dump(mode="json") if signal else None,
            opportunity=opportunity.model_dump(mode="json") if opportunity else None,
            decision=decision.model_dump(mode="json") if decision else None,
            execution=execution.model_dump(mode="json") if execution else None,
            outcome=outcome.model_dump(mode="json") if outcome else None,
            asset=asset.model_dump(mode="json") if asset else None,
            audit_event_ids=audit_event_ids or [],
            approval_id=approval_id,
        )
