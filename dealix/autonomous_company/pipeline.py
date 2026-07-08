"""Pipeline logic: derive a deal's true stage from its evidence events, and score
deals so the decision engine can prioritise the founder's limited time."""

from __future__ import annotations

from datetime import date

from .schemas import (
    STAGE_PROBABILITY,
    STAGE_STALE_DAYS,
    Deal,
    DealStage,
)

# Map an evidence event to the stage it proves. Highest-proven stage wins.
EVENT_TO_STAGE: dict[str, DealStage] = {
    "lead_identified": DealStage.NEW,
    "message_sent_manually": DealStage.CONTACTED,
    "call_booked": DealStage.ENGAGED,
    "invoice_sent": DealStage.PROPOSED,
    "payment_received": DealStage.WON,
    "work_delivered": DealStage.DELIVERED,
    "proof_pack_delivered": DealStage.PROOF,
    "follow_up_scheduled": DealStage.REFERRAL,
    "lost": DealStage.LOST,
}

_STAGE_RANK = {stage: i for i, stage in enumerate(
    [
        DealStage.NEW,
        DealStage.CONTACTED,
        DealStage.ENGAGED,
        DealStage.PROPOSED,
        DealStage.WON,
        DealStage.DELIVERED,
        DealStage.PROOF,
        DealStage.REFERRAL,
    ]
)}


def derive_stage(deal: Deal) -> DealStage:
    """The deal's real stage is the highest stage its events prove.

    A `lost` event is terminal and overrides everything.
    """

    if deal.has_event("lost"):
        return DealStage.LOST
    best = DealStage.NEW
    best_rank = -1
    for ev in deal.events:
        stage = EVENT_TO_STAGE.get(ev.event)
        if stage is None or stage is DealStage.LOST:
            continue
        rank = _STAGE_RANK.get(stage, -1)
        if rank > best_rank:
            best_rank = rank
            best = stage
    return best


def is_active(stage: DealStage) -> bool:
    return stage not in {DealStage.LOST, DealStage.REFERRAL}


def is_won(stage: DealStage) -> bool:
    return stage in {DealStage.WON, DealStage.DELIVERED, DealStage.PROOF, DealStage.REFERRAL}


def is_stalled(deal: Deal, today: date) -> bool:
    if deal.stage in {DealStage.LOST, DealStage.REFERRAL}:
        return False
    threshold = STAGE_STALE_DAYS.get(deal.stage, 7)
    return deal.days_since_touch(today) > threshold


def score(deal: Deal, today: date) -> float:
    """Higher score = more deserving of the founder's next hour.

    Rewards deals that are close to revenue and have been waiting, penalises
    not-opted-in leads (they should not be actioned until opted in).
    """

    prob = STAGE_PROBABILITY.get(deal.stage, 0.0)
    value_factor = deal.value_sar / 499.0  # normalise to entry offer
    waiting = deal.days_since_touch(today)
    urgency = min(waiting, 30) / 10.0
    base = (prob * 4.0) + (value_factor * 1.5) + urgency
    if is_stalled(deal, today):
        base += 2.0  # rescue stalled but valuable deals
    if not deal.opted_in and deal.stage == DealStage.NEW:
        base *= 0.35  # cannot be actioned until opted in
    if deal.stage == DealStage.LOST:
        return 0.0
    return round(base, 3)
