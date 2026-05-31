"""
Money Command — §98.

A small Deal Room that powers the "cash now / pipeline / next best
action" view at the top of the Sovereign UI.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any


@dataclass
class Deal:
    deal_id: str
    customer: str
    stage: str
    value_sar: float
    close_probability: float
    next_step: str
    last_activity_at: str
    owner_id: str
    blockers: list[str] = field(default_factory=list)
    upsell_ready: bool = False
    partner_id: str | None = None
    paid: bool = False
    payment_due_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "deal_id": self.deal_id,
            "customer": self.customer,
            "stage": self.stage,
            "value_sar": self.value_sar,
            "close_probability": self.close_probability,
            "next_step": self.next_step,
            "last_activity_at": self.last_activity_at,
            "owner_id": self.owner_id,
            "blockers": list(self.blockers),
            "upsell_ready": self.upsell_ready,
            "partner_id": self.partner_id,
            "paid": self.paid,
            "payment_due_at": self.payment_due_at,
        }


class MoneyCommand:
    def __init__(self) -> None:
        self._deals: dict[str, Deal] = {}
        self._lock = threading.Lock()

    def register_deal(self, deal: Deal) -> Deal:
        with self._lock:
            self._deals[deal.deal_id] = deal
            return deal

    def all_deals(self) -> list[Deal]:
        return list(self._deals.values())

    def expected_revenue(self) -> float:
        return round(sum(d.value_sar * d.close_probability for d in self._deals.values()), 2)

    def cash_now(self) -> float:
        return round(sum(d.value_sar for d in self._deals.values() if d.paid), 2)

    def pipeline(self) -> float:
        return round(sum(d.value_sar for d in self._deals.values() if not d.paid), 2)

    def open_proposals(self) -> list[Deal]:
        return [d for d in self._deals.values() if d.stage == "proposal"]

    def stuck_deals(self, threshold_days: int = 14) -> list[Deal]:
        cutoff = datetime.now(UTC) - timedelta(days=threshold_days)
        out: list[Deal] = []
        for d in self._deals.values():
            if d.paid:
                continue
            try:
                ts = datetime.fromisoformat(d.last_activity_at)
            except ValueError:
                continue
            if ts < cutoff:
                out.append(d)
        return out

    def pending_payments(self) -> list[Deal]:
        return [d for d in self._deals.values() if not d.paid and d.payment_due_at]

    def upsells(self) -> list[Deal]:
        return [d for d in self._deals.values() if d.upsell_ready]

    def partner_revenue(self) -> dict[str, float]:
        out: dict[str, float] = {}
        for d in self._deals.values():
            if d.partner_id and d.paid:
                out[d.partner_id] = out.get(d.partner_id, 0.0) + d.value_sar
        return {k: round(v, 2) for k, v in out.items()}

    def best_next_action(self) -> dict[str, Any] | None:
        ranked: list[tuple[float, Deal]] = []
        for d in self._deals.values():
            if d.paid:
                continue
            blockers = max(1, len(d.blockers))
            score = (d.value_sar * d.close_probability) / blockers
            ranked.append((score, d))
        if not ranked:
            return None
        ranked.sort(key=lambda x: -x[0])
        best_score, best_deal = ranked[0]
        return {
            "deal_id": best_deal.deal_id,
            "customer": best_deal.customer,
            "score": round(best_score, 2),
            "next_step": best_deal.next_step,
        }

    def snapshot(self) -> dict[str, Any]:
        return {
            "expected_revenue": self.expected_revenue(),
            "cash_now": self.cash_now(),
            "pipeline": self.pipeline(),
            "open_proposals": len(self.open_proposals()),
            "stuck_deals": len(self.stuck_deals()),
            "pending_payments": len(self.pending_payments()),
            "upsells": len(self.upsells()),
            "partner_revenue": self.partner_revenue(),
        }
