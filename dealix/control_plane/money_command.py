"""
Section 66 — Money Command System.

The Money Command is *not* a dashboard. It is "CFO + Head of Sales" in
one surface. It tracks Deal Rooms, computes probability-weighted revenue,
and surfaces the *best next action* — never just numbers.
"""

from __future__ import annotations

import uuid
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass
class DealRoom:
    deal_id: str
    target: str
    offer: str
    deal_value_sar: float
    floor_price_sar: float
    target_price_sar: float
    pain: str
    workspace_id: str
    objections: list[str] = field(default_factory=list)
    next_step: str = ""
    walkaway_conditions: list[str] = field(default_factory=list)
    close_probability: float = 0.2
    stage: str = "qualifying"
    last_touch_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @property
    def expected_revenue_sar(self) -> float:
        return round(self.deal_value_sar * max(0.0, min(1.0, self.close_probability)), 2)

    def to_dict(self) -> dict[str, Any]:
        return {
            "deal_id": self.deal_id,
            "target": self.target,
            "offer": self.offer,
            "deal_value_sar": self.deal_value_sar,
            "floor_price_sar": self.floor_price_sar,
            "target_price_sar": self.target_price_sar,
            "pain": self.pain,
            "workspace_id": self.workspace_id,
            "objections": list(self.objections),
            "next_step": self.next_step,
            "walkaway_conditions": list(self.walkaway_conditions),
            "close_probability": self.close_probability,
            "stage": self.stage,
            "expected_revenue_sar": self.expected_revenue_sar,
            "last_touch_at": self.last_touch_at.isoformat() if self.last_touch_at else None,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class MoneySnapshot:
    cash_now_sar: float
    pipeline_sar: float
    expected_revenue_sar: float
    probability_weighted_revenue_sar: float
    open_proposals: int
    stuck_deals: int
    pending_payments_sar: float
    upsells_sar: float
    partner_revenue_sar: float
    best_next_action: str
    generated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, Any]:
        return {
            "cash_now_sar": self.cash_now_sar,
            "pipeline_sar": self.pipeline_sar,
            "expected_revenue_sar": self.expected_revenue_sar,
            "probability_weighted_revenue_sar": self.probability_weighted_revenue_sar,
            "open_proposals": self.open_proposals,
            "stuck_deals": self.stuck_deals,
            "pending_payments_sar": self.pending_payments_sar,
            "upsells_sar": self.upsells_sar,
            "partner_revenue_sar": self.partner_revenue_sar,
            "best_next_action": self.best_next_action,
            "generated_at": self.generated_at.isoformat(),
        }


class MoneyCommand:
    """Deal book + snapshot generator."""

    def __init__(self, *, stuck_after_days: int = 7) -> None:
        self._deals: dict[str, DealRoom] = {}
        self._cash_sar: float = 0.0
        self._pending_payments_sar: float = 0.0
        self._partner_revenue_sar: float = 0.0
        self._upsell_pipeline_sar: float = 0.0
        self._stuck_after_days = stuck_after_days

    def open_deal(
        self,
        *,
        target: str,
        offer: str,
        deal_value_sar: float,
        floor_price_sar: float,
        target_price_sar: float,
        pain: str,
        workspace_id: str,
        objections: Iterable[str] = (),
        next_step: str = "",
        walkaway_conditions: Iterable[str] = (),
        close_probability: float = 0.2,
    ) -> DealRoom:
        if deal_value_sar < 0 or floor_price_sar < 0 or target_price_sar < 0:
            raise ValueError("monetary values must be non-negative")
        if floor_price_sar > target_price_sar:
            raise ValueError("floor_price_sar cannot exceed target_price_sar")
        deal = DealRoom(
            deal_id=f"deal_{uuid.uuid4().hex[:12]}",
            target=target,
            offer=offer,
            deal_value_sar=deal_value_sar,
            floor_price_sar=floor_price_sar,
            target_price_sar=target_price_sar,
            pain=pain,
            workspace_id=workspace_id,
            objections=list(objections),
            next_step=next_step,
            walkaway_conditions=list(walkaway_conditions),
            close_probability=close_probability,
        )
        self._deals[deal.deal_id] = deal
        return deal

    def touch_deal(self, deal_id: str, *, next_step: str | None = None) -> DealRoom:
        deal = self.get_deal(deal_id)
        deal.last_touch_at = datetime.now(UTC)
        if next_step is not None:
            deal.next_step = next_step
        return deal

    def update_probability(self, deal_id: str, *, probability: float) -> DealRoom:
        if not 0.0 <= probability <= 1.0:
            raise ValueError("probability must be in [0.0, 1.0]")
        deal = self.get_deal(deal_id)
        deal.close_probability = probability
        return deal

    def get_deal(self, deal_id: str) -> DealRoom:
        try:
            return self._deals[deal_id]
        except KeyError as exc:
            raise KeyError(f"unknown deal: {deal_id}") from exc

    def deals(self) -> list[DealRoom]:
        return list(self._deals.values())

    def add_cash(self, sar: float) -> None:
        if sar < 0:
            raise ValueError("cash addition must be non-negative")
        self._cash_sar += sar

    def add_pending_payment(self, sar: float) -> None:
        self._pending_payments_sar += sar

    def add_partner_revenue(self, sar: float) -> None:
        self._partner_revenue_sar += sar

    def add_upsell_pipeline(self, sar: float) -> None:
        self._upsell_pipeline_sar += sar

    def snapshot(self) -> MoneySnapshot:
        now = datetime.now(UTC)
        deals = list(self._deals.values())
        open_proposals = sum(1 for d in deals if d.stage in ("proposal", "negotiation"))
        stuck = 0
        pipeline = 0.0
        weighted = 0.0
        for deal in deals:
            pipeline += deal.deal_value_sar
            weighted += deal.expected_revenue_sar
            if deal.last_touch_at is None:
                age_days = (now - deal.created_at).days
            else:
                age_days = (now - deal.last_touch_at).days
            if age_days >= self._stuck_after_days:
                stuck += 1
        best_action = self._best_next_action(deals)
        return MoneySnapshot(
            cash_now_sar=round(self._cash_sar, 2),
            pipeline_sar=round(pipeline, 2),
            expected_revenue_sar=round(weighted, 2),
            probability_weighted_revenue_sar=round(weighted, 2),
            open_proposals=open_proposals,
            stuck_deals=stuck,
            pending_payments_sar=round(self._pending_payments_sar, 2),
            upsells_sar=round(self._upsell_pipeline_sar, 2),
            partner_revenue_sar=round(self._partner_revenue_sar, 2),
            best_next_action=best_action,
        )

    def _best_next_action(self, deals: list[DealRoom]) -> str:
        if not deals:
            return "open the first Deal Room — no pipeline exists yet"
        ranked = sorted(deals, key=lambda d: d.expected_revenue_sar, reverse=True)
        top = ranked[0]
        if top.next_step:
            return f"work {top.target}: {top.next_step}"
        return f"define the next step for {top.target} ({top.offer})"
