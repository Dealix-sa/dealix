"""Revenue Share Calculator — splits a deal across partner roles."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RevenueShare:
    total_sar: float
    dealix_sar: float
    partner_sar: float
    note: str


class RevenueShareCalculator:
    def split(self, total_sar: float, *, partner_share_pct: float = 0.25) -> RevenueShare:
        partner_share_pct = max(0.0, min(partner_share_pct, 0.5))
        partner_sar = round(total_sar * partner_share_pct, 2)
        dealix_sar = round(total_sar - partner_sar, 2)
        return RevenueShare(
            total_sar=total_sar,
            dealix_sar=dealix_sar,
            partner_sar=partner_sar,
            note=f"Partner share capped at 50%; current split {partner_share_pct:.0%}.",
        )
