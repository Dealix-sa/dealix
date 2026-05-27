"""DecisionLog — every sovereign choice is recorded here.

A decision is the *only* doorway between an opportunity and an execution.
The decision log mirrors entries to the sovereignty journal so both views
stay consistent.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable

from dealix.hermes.core.schemas import Decision, DecisionStatus
from dealix.hermes.sovereignty.approval_rules import ApprovalRules
from dealix.hermes.sovereignty.decision_journal import DecisionJournal


class DecisionLog:
    def __init__(
        self,
        approval_rules: ApprovalRules | None = None,
        journal: DecisionJournal | None = None,
    ) -> None:
        self._by_id: dict[str, Decision] = {}
        self._rules = approval_rules or ApprovalRules()
        self._journal = journal or DecisionJournal()

    @property
    def journal(self) -> DecisionJournal:
        return self._journal

    def file(self, decision: Decision, *, domain: str = "core") -> Decision:
        """Record a new decision and immediately run sovereignty rules."""
        if decision.id in self._by_id:
            raise ValueError(f"Duplicate decision id: {decision.id}")
        verdict = self._rules.evaluate(
            action=decision.action,
            level=decision.sovereignty_level,
            domain=domain,
        )
        if not verdict.allowed:
            decision.status = DecisionStatus.BLOCKED
            decision.rejection_reason = verdict.reason
        elif verdict.auto:
            decision.status = DecisionStatus.AUTO_APPROVED
            decision.approver = "system"
            decision.approved_at = datetime.now(timezone.utc)
        else:
            decision.status = DecisionStatus.PENDING_APPROVAL
        self._by_id[decision.id] = decision
        self._journal.append(
            actor=decision.owner,
            action=decision.action,
            level=decision.sovereignty_level.label,
            outcome=decision.status.value,
            rationale=verdict.reason,
            refs=[decision.id, decision.opportunity_id],
        )
        return decision

    def approve(self, decision_id: str, *, by: str = "sami", note: str = "") -> Decision:
        dec = self._by_id[decision_id]
        if dec.status != DecisionStatus.PENDING_APPROVAL:
            raise ValueError(f"Decision {decision_id} is not pending approval.")
        dec.status = DecisionStatus.APPROVED
        dec.approver = by
        dec.approved_at = datetime.now(timezone.utc)
        if note:
            dec.payload["approval_note"] = note
        self._journal.append(
            actor=by,
            action=dec.action,
            level=dec.sovereignty_level.label,
            outcome="approved",
            rationale=note or "Approved by sovereign.",
            refs=[dec.id, dec.opportunity_id],
        )
        return dec

    def reject(self, decision_id: str, *, by: str = "sami", reason: str) -> Decision:
        dec = self._by_id[decision_id]
        dec.status = DecisionStatus.REJECTED
        dec.approver = by
        dec.approved_at = datetime.now(timezone.utc)
        dec.rejection_reason = reason
        self._journal.append(
            actor=by,
            action=dec.action,
            level=dec.sovereignty_level.label,
            outcome="rejected",
            rationale=reason,
            refs=[dec.id, dec.opportunity_id],
        )
        return dec

    def all(self) -> list[Decision]:
        return list(self._by_id.values())

    def pending(self) -> list[Decision]:
        return [d for d in self._by_id.values() if d.status == DecisionStatus.PENDING_APPROVAL]

    def executable(self) -> list[Decision]:
        return [d for d in self._by_id.values() if d.is_executable]

    def get(self, decision_id: str) -> Decision:
        return self._by_id[decision_id]

    def by_opportunity(self, opportunity_id: str) -> Iterable[Decision]:
        return (d for d in self._by_id.values() if d.opportunity_id == opportunity_id)


__all__ = ["DecisionLog"]
