"""
Recommendation Engine — يجاوب سؤالًا واحدًا: "ما الفعل التالي الأقوى الآن؟"
يأخذ snapshot من باقي الـ graphs ويرتّب أفعالًا قابلة للتنفيذ في الـ
Sovereign Console.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .learning_engine import InsightKind, LearningEngine


@dataclass
class Recommendation:
    title: str
    rationale: str
    score: float  # 0..1
    suggested_intent: str
    payload: dict[str, Any] = field(default_factory=dict)


class RecommendationEngine:
    def __init__(self, *, learning: LearningEngine) -> None:
        self._learning = learning

    def best_next_actions(self, n: int = 5) -> list[Recommendation]:
        recs: list[Recommendation] = []
        for ins in self._learning.insights_by_channel():
            if ins.kind == InsightKind.EXPAND:
                recs.append(
                    Recommendation(
                        title=f"وسّع قناة `{ins.dimension_value}`",
                        rationale=(
                            f"الـ revenue المنسوب لها = "
                            f"{ins.evidence.get('attributed_revenue_sar', 0):.0f} ريال"
                        ),
                        score=ins.confidence,
                        suggested_intent="growth.campaign.scale",
                        payload={"channel": ins.dimension_value},
                    )
                )
            elif ins.kind == InsightKind.KILL:
                recs.append(
                    Recommendation(
                        title=f"جمّد قناة `{ins.dimension_value}`",
                        rationale="نسبة الدخل المُتحقَّق منها أقل من الحد الأدنى.",
                        score=ins.confidence,
                        suggested_intent="growth.campaign.freeze",
                        payload={"channel": ins.dimension_value},
                    )
                )
        return sorted(recs, key=lambda r: r.score, reverse=True)[:n]


__all__ = ["Recommendation", "RecommendationEngine"]
