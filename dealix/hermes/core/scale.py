"""Scale / Kill Engine — runs over outcomes + assets to decide what to
double down on and what to retire.

Rules (initial, deliberately conservative):
    * SCALE   — three or more paid outcomes within 30 days, no risk flags
    * HOLD    — at least one paid outcome but mixed signals
    * KILL    — no paid outcome after a meaningful sample, or risk > value
"""

from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime, timedelta

from dealix.hermes.core.schemas import (
    Outcome,
    OutcomeKind,
    ScaleDecision,
    ScaleVerdict,
)


class ScaleEngine:
    def __init__(self) -> None:
        self._decisions: dict[str, ScaleDecision] = {}

    def evaluate_offer(
        self,
        *,
        offer_id: str,
        outcomes: list[Outcome],
        decided_by: str = "hermes.scale_engine",
        window_days: int = 30,
        min_paid_for_scale: int = 3,
        min_sample: int = 5,
    ) -> ScaleDecision:
        cutoff = datetime.now(UTC) - timedelta(days=window_days)
        recent = [o for o in outcomes if o.recorded_at >= cutoff]
        kinds = Counter(o.kind for o in recent)
        paid = kinds[OutcomeKind.PAID]
        blocked = kinds[OutcomeKind.RISK_BLOCKED]
        ignored = kinds[OutcomeKind.IGNORED]
        sample = len(recent)

        revenue = sum(
            o.realised_value_sar for o in recent if o.kind is OutcomeKind.PAID
        )

        snapshot = {
            "paid": float(paid),
            "blocked": float(blocked),
            "ignored": float(ignored),
            "sample": float(sample),
            "revenue_sar": float(revenue),
        }

        if paid >= min_paid_for_scale and blocked == 0:
            verdict = ScaleVerdict.SCALE
            reason = f"{paid} paid in {window_days}d, no trust blocks."
        elif paid >= 1 and (blocked > 0 or ignored >= paid * 2):
            verdict = ScaleVerdict.HOLD
            reason = "Mixed signals — hold until trust + reply rate clear."
        elif sample >= min_sample and paid == 0:
            verdict = ScaleVerdict.KILL
            reason = (
                f"{sample} attempts without a paid outcome; cost > learning."
            )
        else:
            verdict = ScaleVerdict.HOLD
            reason = "Sample not yet decisive."

        d = ScaleDecision(
            target=offer_id,
            target_kind="offer",
            verdict=verdict,
            reason=reason,
            metrics_snapshot=snapshot,
            decided_by=decided_by,
        )
        self._decisions[d.decision_id] = d
        return d

    def get(self, decision_id: str) -> ScaleDecision | None:
        return self._decisions.get(decision_id)

    def all(self) -> list[ScaleDecision]:
        return list(self._decisions.values())


__all__ = ["ScaleEngine"]
