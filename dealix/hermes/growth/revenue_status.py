"""
Revenue lifecycle — encodes the legal transitions between statuses so
the pipeline can never "jump" from influenced straight to retainer.
"""

from __future__ import annotations

from dealix.hermes.money.verified_revenue import RevenueStatus


class RevenueLifecycle:
    """Forward-only state machine."""

    _ORDER: tuple[RevenueStatus, ...] = (
        RevenueStatus.INFLUENCED,
        RevenueStatus.QUALIFIED_PIPELINE,
        RevenueStatus.PROPOSAL_SENT,
        RevenueStatus.COMMITTED,
        RevenueStatus.INVOICED,
        RevenueStatus.PAID,
    )

    @classmethod
    def allowed_next(cls, current: RevenueStatus) -> set[RevenueStatus]:
        if current == RevenueStatus.PAID:
            return {
                RevenueStatus.RETAINER_ACTIVE,
                RevenueStatus.EXPANDED,
                RevenueStatus.RENEWED,
            }
        if current == RevenueStatus.RETAINER_ACTIVE:
            return {RevenueStatus.EXPANDED, RevenueStatus.RENEWED}
        if current == RevenueStatus.EXPANDED:
            return {RevenueStatus.RENEWED}
        if current == RevenueStatus.RENEWED:
            return {RevenueStatus.RETAINER_ACTIVE, RevenueStatus.EXPANDED}
        if current in cls._ORDER:
            idx = cls._ORDER.index(current)
            if idx + 1 < len(cls._ORDER):
                return {cls._ORDER[idx + 1]}
            return set()
        return set()


def advance_revenue_status(
    current: RevenueStatus, target: RevenueStatus
) -> RevenueStatus:
    if target == current:
        return current
    if target not in RevenueLifecycle.allowed_next(current):
        raise ValueError(
            f"illegal revenue transition: {current.value} → {target.value}"
        )
    return target
