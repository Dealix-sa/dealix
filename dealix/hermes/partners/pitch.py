"""Builds a partner pitch (draft only)."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from dealix.hermes.partners.scout import Partner


@dataclass
class PartnerPitch:
    id: str
    partner_id: str
    headline: str
    why_us: list[str]
    offer_ids: list[str]
    revenue_share_pct: float


@dataclass
class PartnerPitchBuilder:
    _by_id: dict[str, PartnerPitch] = field(default_factory=dict)

    def build(
        self,
        partner: Partner,
        *,
        offer_ids: list[str],
        revenue_share_pct: float,
        why_us: list[str] | None = None,
    ) -> PartnerPitch:
        if not 0.0 <= revenue_share_pct <= 100.0:
            raise ValueError("revenue_share_pct must be in [0,100].")
        pitch = PartnerPitch(
            id=f"ptc_{uuid.uuid4().hex[:10]}",
            partner_id=partner.id,
            headline=f"Sell AI revenue services to {partner.sector}",
            why_us=list(why_us or ["Sovereign trust kit", "Saudi-first delivery", "Asset library"]),
            offer_ids=list(offer_ids),
            revenue_share_pct=revenue_share_pct,
        )
        self._by_id[pitch.id] = pitch
        return pitch


__all__ = ["PartnerPitch", "PartnerPitchBuilder"]
