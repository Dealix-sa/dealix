"""ABM pipeline stages — the ordered funnel from target to outcome."""

from __future__ import annotations

from typing import Final

from pydantic import BaseModel, ConfigDict

from dealix.growth_os.abm.account_card import AccountCard

ABM_STAGES: Final[tuple[str, ...]] = (
    "target",
    "research",
    "pain_hypothesis",
    "stakeholder_map",
    "personalized_offer",
    "message",
    "followup",
    "proposal",
    "deal_room",
    "outcome",
)


class ABMPipeline(BaseModel):
    """Read-only view of the pipeline definition + the accounts in it."""

    model_config = ConfigDict(extra="forbid")

    stages: tuple[str, ...] = ABM_STAGES
    accounts: list[AccountCard]

    def count_by_stage(self) -> dict[str, int]:
        out = dict.fromkeys(self.stages, 0)
        for a in self.accounts:
            if a.stage in out:
                out[a.stage] += 1
        return out


def advance_stage(card: AccountCard) -> AccountCard:
    """Return a new card advanced to the next stage. Last stage is idempotent."""
    if card.stage not in ABM_STAGES:
        raise ValueError(f"unknown stage: {card.stage!r}")
    idx = ABM_STAGES.index(card.stage)
    next_idx = min(idx + 1, len(ABM_STAGES) - 1)
    data = card.model_dump()
    data["stage"] = ABM_STAGES[next_idx]
    return AccountCard.model_validate(data)


__all__ = ["ABM_STAGES", "ABMPipeline", "advance_stage"]
