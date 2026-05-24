"""Decision Memo — written record produced before execution.

A memo is mandatory for sovereignty levels S3+. The memo is the artifact a
human reviewer reads when adjudicating an approval, and it is the audit
record consulted when an outcome is reviewed later.
"""

from __future__ import annotations

from dealix.hermes.core.schemas import DecisionMemo, Opportunity
from dealix.hermes.sovereignty import SovereigntyLevel


class DecisionJournal:
    def __init__(self) -> None:
        self._memos: dict[str, DecisionMemo] = {}

    def draft(
        self,
        *,
        opportunity: Opportunity,
        recommendation: str,
        rationale: str,
        sovereignty_level: SovereigntyLevel,
        written_by: str,
        alternatives: list[str] | None = None,
    ) -> DecisionMemo:
        memo = DecisionMemo(
            opportunity_id=opportunity.opportunity_id,
            recommendation=recommendation,
            rationale=rationale,
            alternatives=list(alternatives or []),
            sovereignty_level=sovereignty_level,
            approval_required=sovereignty_level.requires_approval,
            written_by=written_by,
        )
        self._memos[memo.memo_id] = memo
        return memo

    def approve(self, memo_id: str, approver: str) -> DecisionMemo:
        memo = self._memos.get(memo_id)
        if memo is None:
            raise KeyError(memo_id)
        if not memo.approval_required:
            return memo
        from datetime import UTC, datetime

        memo = memo.model_copy(
            update={"approved_by": approver, "approved_at": datetime.now(UTC)}
        )
        self._memos[memo_id] = memo
        return memo

    def get(self, memo_id: str) -> DecisionMemo | None:
        return self._memos.get(memo_id)

    def pending(self) -> list[DecisionMemo]:
        return [
            m
            for m in self._memos.values()
            if m.approval_required and m.approved_at is None
        ]

    def by_opportunity(self, opportunity_id: str) -> list[DecisionMemo]:
        return [
            m for m in self._memos.values() if m.opportunity_id == opportunity_id
        ]


__all__ = ["DecisionJournal"]
