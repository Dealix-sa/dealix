"""Deal Room — a per-opportunity bundle for the founder.

The Deal Room collects: the opportunity, the latest proposal, the
follow-up plan, the price band, and the trust checks. It's the unit
of work the founder reviews before approving an external send.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from dealix.hermes.core.schemas import Opportunity
from dealix.hermes.money.followup import FollowUpPlan
from dealix.hermes.money.pricing import PriceBand
from dealix.hermes.money.proposal_factory import Proposal


@dataclass
class DealRoom:
    opportunity: Opportunity
    proposal: Proposal | None = None
    followup_plan: FollowUpPlan | None = None
    price_band: PriceBand | None = None
    artifacts: list[dict[str, Any]] = field(default_factory=list)

    def add_artifact(self, kind: str, payload: dict[str, Any]) -> None:
        self.artifacts.append({"kind": kind, "payload": payload})

    def to_dict(self) -> dict[str, Any]:
        return {
            "opportunity": self.opportunity.model_dump(mode="json"),
            "proposal": self.proposal.to_dict() if self.proposal else None,
            "followup_plan": (
                {
                    "opportunity_id": self.followup_plan.opportunity_id,
                    "client_name": self.followup_plan.client_name,
                    "steps": [
                        {
                            "day_offset": s.day_offset,
                            "scheduled_at": s.scheduled_at.isoformat(),
                            "channel": s.channel,
                            "draft": s.draft,
                            "sovereignty_level": s.sovereignty_level.name,
                            "requires_approval": s.requires_approval,
                            "blocked_reason": s.blocked_reason,
                        }
                        for s in self.followup_plan.steps
                    ],
                }
                if self.followup_plan
                else None
            ),
            "price_band": (
                {
                    "low_sar": self.price_band.low_sar,
                    "target_sar": self.price_band.target_sar,
                    "high_sar": self.price_band.high_sar,
                    "rationale": self.price_band.rationale,
                    "requires_approval": self.price_band.requires_approval,
                }
                if self.price_band
                else None
            ),
            "artifacts": list(self.artifacts),
        }
