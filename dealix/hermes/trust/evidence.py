"""Evidence Pack builder.

An evidence pack is the externally-presentable record of one or more
outcomes: it is what we hand to a customer, auditor, or partner to prove
"this work happened, here is what it produced, here is the audit trail."
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from dealix.hermes.core.schemas import Outcome


class EvidenceItem(BaseModel):
    kind: str  # outcome | memo | proposal | audit_log | screenshot
    title: str
    summary: str
    body: str
    captured_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class EvidencePack(BaseModel):
    pack_id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    purpose: str  # "customer proof" | "audit" | "investor update"
    items: list[EvidenceItem] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    created_by: str
    completeness: float = 0.0  # 0..1


class EvidencePackBuilder:
    def from_outcomes(
        self,
        *,
        title: str,
        purpose: str,
        outcomes: list[Outcome],
        created_by: str,
        extra_items: list[EvidenceItem] | None = None,
    ) -> EvidencePack:
        items: list[EvidenceItem] = []
        for o in outcomes:
            items.append(
                EvidenceItem(
                    kind="outcome",
                    title=f"Outcome — {o.kind.value}",
                    summary=o.summary[:160],
                    body=o.model_dump_json(indent=2),
                )
            )
        items.extend(extra_items or [])

        completeness = self._completeness(outcomes, items)
        return EvidencePack(
            title=title,
            purpose=purpose,
            items=items,
            created_by=created_by,
            completeness=completeness,
        )

    @staticmethod
    def _completeness(outcomes: list[Outcome], items: list[EvidenceItem]) -> float:
        if not outcomes:
            return 0.0
        # Heuristic: at least one item per outcome, plus an audit/memo item.
        has_per_outcome = sum(1 for o in outcomes if any(o.outcome_id in i.body for i in items))
        coverage = has_per_outcome / len(outcomes)
        has_audit = any(i.kind in {"audit_log", "memo"} for i in items)
        return round(min(1.0, coverage * 0.8 + (0.2 if has_audit else 0.0)), 3)


__all__ = ["EvidencePack", "EvidenceItem", "EvidencePackBuilder"]
