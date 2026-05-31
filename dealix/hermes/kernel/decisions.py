"""Phase 3: structured Decision memos with approval routing."""

from __future__ import annotations

from dataclasses import dataclass, field

from dealix.hermes.kernel.schemas import (
    Decision,
    LifecycleEvent,
    Opportunity,
    RecommendedAction,
    SovereigntyLevel,
)


# Sovereignty levels that always require human approval before the
# Execution Plane is allowed to dispatch.
_APPROVAL_REQUIRED = {
    SovereigntyLevel.S2_SAMI_APPROVAL,
    SovereigntyLevel.S3_SOVEREIGN_MEMO,
    SovereigntyLevel.S4_SOVEREIGN_ONLY,
    SovereigntyLevel.S5_NEVER_AUTONOMOUS,
}


@dataclass
class DecisionStore:
    _decisions: dict[str, Decision] = field(default_factory=dict)
    _events: list[LifecycleEvent] = field(default_factory=list)

    def create_memo(
        self,
        opp: Opportunity,
        *,
        memo: str,
        recommendation: RecommendedAction | None = None,
        rationale: str = "",
        risks: list[str] | None = None,
        evidence_refs: list[str] | None = None,
        expected_outcome: str = "",
    ) -> Decision:
        rec = recommendation or opp.recommended_action
        requires_approval = opp.sovereignty_level in _APPROVAL_REQUIRED
        decision = Decision(
            opportunity_id=opp.opportunity_id,
            title=opp.title,
            memo=memo,
            recommendation=rec,
            sovereignty_level=opp.sovereignty_level,
            requires_approval=requires_approval,
            rationale=rationale,
            risks=risks or [],
            evidence_refs=evidence_refs or [],
            expected_outcome=expected_outcome,
        )
        self._decisions[decision.decision_id] = decision
        self._events.append(LifecycleEvent(
            event_type="decision.created",
            entity_id=decision.decision_id,
            sovereignty_level=decision.sovereignty_level,
            payload={"requires_approval": requires_approval, "recommendation": rec.value},
        ))
        return decision

    def attach_approval(self, decision_id: str, approval_id: str) -> Decision:
        d = self._decisions[decision_id]
        updated = d.model_copy(update={"approval_id": approval_id})
        self._decisions[decision_id] = updated
        return updated

    def mark_approved(self, decision_id: str) -> Decision:
        d = self._decisions[decision_id]
        self._events.append(LifecycleEvent(
            event_type="decision.approved",
            entity_id=decision_id,
            sovereignty_level=d.sovereignty_level,
        ))
        return d

    def mark_denied(self, decision_id: str, reason: str = "") -> Decision:
        d = self._decisions[decision_id]
        self._events.append(LifecycleEvent(
            event_type="decision.denied",
            entity_id=decision_id,
            sovereignty_level=d.sovereignty_level,
            payload={"reason": reason},
        ))
        return d

    def get(self, decision_id: str) -> Decision:
        return self._decisions[decision_id]

    def list(self) -> list[Decision]:
        return list(self._decisions.values())

    def events(self) -> list[LifecycleEvent]:
        return list(self._events)
