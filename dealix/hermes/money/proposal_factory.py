"""ProposalFactory — assembles proposals as drafts only.

Section 137 default: every proposal is draft-only. Nothing leaves the
system until the Trust layer approves the corresponding S2 decision.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

from dealix.hermes.core.schemas import Opportunity


@dataclass
class Proposal:
    id: str
    opportunity_id: str
    title: str
    buyer: str
    summary: str
    deliverables: list[str]
    price_sar: float
    timeline_weeks: int
    metric: str
    upsell: str
    risks: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = "draft"   # draft | approved_to_send | sent | accepted | rejected


@dataclass
class ProposalFactory:
    _by_id: dict[str, Proposal] = field(default_factory=dict)

    def draft(
        self,
        opp: Opportunity,
        *,
        buyer: str,
        deliverables: list[str],
        price_sar: float,
        timeline_weeks: int,
        metric: str,
        upsell: str = "",
        risks: list[str] | None = None,
    ) -> Proposal:
        missing = []
        if not buyer:
            missing.append("buyer")
        if not deliverables:
            missing.append("deliverables")
        if price_sar <= 0:
            missing.append("price_sar")
        if not metric:
            missing.append("metric")
        if missing:
            raise ValueError(f"Proposal cannot be drafted; missing: {', '.join(missing)}")

        proposal = Proposal(
            id=f"prp_{uuid.uuid4().hex[:10]}",
            opportunity_id=opp.id,
            title=opp.title,
            buyer=buyer,
            summary=opp.payload.get("summary", opp.title),
            deliverables=list(deliverables),
            price_sar=float(price_sar),
            timeline_weeks=int(timeline_weeks),
            metric=metric,
            upsell=upsell,
            risks=list(risks or []),
        )
        self._by_id[proposal.id] = proposal
        return proposal

    def approve_to_send(self, proposal_id: str) -> Proposal:
        p = self._by_id[proposal_id]
        if p.status != "draft":
            raise ValueError(f"Proposal {proposal_id} is {p.status}, not draft.")
        p.status = "approved_to_send"
        return p

    def mark_sent(self, proposal_id: str) -> Proposal:
        p = self._by_id[proposal_id]
        if p.status != "approved_to_send":
            raise ValueError("Proposal must be approved_to_send before mark_sent.")
        p.status = "sent"
        return p

    def get(self, proposal_id: str) -> Proposal:
        return self._by_id[proposal_id]

    def all(self) -> list[Proposal]:
        return list(self._by_id.values())

    def open(self) -> list[Proposal]:
        return [p for p in self._by_id.values() if p.status in {"draft", "approved_to_send", "sent"}]


__all__ = ["Proposal", "ProposalFactory"]
