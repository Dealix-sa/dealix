"""Money dashboard — the founder-facing rollup of the money engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from dealix.hermes.core.schemas import MoneyAction
from dealix.hermes.core.scoring import (
    KillScaleRecommendation,
    kill_or_scale,
    rank_money_actions,
)


@dataclass
class MoneyDashboard:
    fastest_cash_actions: list[MoneyAction] = field(default_factory=list)
    highest_strategic_actions: list[MoneyAction] = field(default_factory=list)
    pipeline_value_sar: float = 0.0
    weighted_pipeline_sar: float = 0.0
    kill_scale: KillScaleRecommendation = field(
        default_factory=lambda: KillScaleRecommendation([], [], {})
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "fastest_cash_actions": [
                a.model_dump(mode="json") for a in self.fastest_cash_actions
            ],
            "highest_strategic_actions": [
                a.model_dump(mode="json") for a in self.highest_strategic_actions
            ],
            "pipeline_value_sar": round(self.pipeline_value_sar, 2),
            "weighted_pipeline_sar": round(self.weighted_pipeline_sar, 2),
            "kill_scale": {
                "scale": list(self.kill_scale.scale),
                "pause_or_kill": list(self.kill_scale.pause_or_kill),
                "reasoning": dict(self.kill_scale.reasoning),
            },
        }


def build_dashboard(
    actions: list[MoneyAction], top_n: int = 5
) -> MoneyDashboard:
    """Compose the money dashboard from a list of money actions."""
    ranked = rank_money_actions(list(actions))
    fastest = sorted(ranked, key=lambda a: a.cash_speed_score, reverse=True)[:top_n]
    strategic = sorted(
        ranked, key=lambda a: a.strategic_value_score, reverse=True
    )[:top_n]
    pipeline = sum((a.estimated_value_sar or 0.0) for a in ranked)
    weighted = sum(
        (a.estimated_value_sar or 0.0) * a.close_probability for a in ranked
    )

    return MoneyDashboard(
        fastest_cash_actions=fastest,
        highest_strategic_actions=strategic,
        pipeline_value_sar=pipeline,
        weighted_pipeline_sar=weighted,
        kill_scale=kill_or_scale(ranked),
    )
