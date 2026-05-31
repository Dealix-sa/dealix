"""Revenue Share Calculator — deterministic split per commercial model."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class RevenueShareModel(StrEnum):
    REFERRAL_15 = "referral_15"  # one-time 15% on first invoice
    REFERRAL_25_RECURRING = "referral_25_recurring"  # 25% recurring for 12 months
    RESELLER_40 = "reseller_40"  # 40% margin, partner handles delivery
    WHITE_LABEL_50 = "white_label_50"  # 50/50 split, partner brands the work


@dataclass
class RevenueSplit:
    dealix_sar: int
    partner_sar: int
    model: RevenueShareModel
    note: str


class RevenueShareCalculator:
    def calculate(
        self,
        *,
        revenue_sar: int,
        model: RevenueShareModel,
        month_index: int = 1,
    ) -> RevenueSplit:
        if revenue_sar < 0:
            raise ValueError("revenue_sar must be >= 0")

        if model == RevenueShareModel.REFERRAL_15:
            partner = int(revenue_sar * 0.15) if month_index == 1 else 0
            note = "one-time 15% on first invoice"
        elif model == RevenueShareModel.REFERRAL_25_RECURRING:
            partner = int(revenue_sar * 0.25) if month_index <= 12 else 0
            note = f"25% recurring (month {month_index}/12)"
        elif model == RevenueShareModel.RESELLER_40:
            partner = int(revenue_sar * 0.40)
            note = "40% reseller margin"
        elif model == RevenueShareModel.WHITE_LABEL_50:
            partner = int(revenue_sar * 0.50)
            note = "50/50 white-label split"
        else:  # pragma: no cover — defensive
            raise ValueError(f"unknown model: {model}")

        return RevenueSplit(
            dealix_sar=revenue_sar - partner,
            partner_sar=partner,
            model=model,
            note=note,
        )


__all__ = ["RevenueShareCalculator", "RevenueShareModel", "RevenueSplit"]
