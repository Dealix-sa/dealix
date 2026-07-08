"""Offer memory and safe offer ladder for Dealix."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(slots=True)
class Offer:
    name: str
    target: str
    price_note: str
    proof_required: str
    safe_cta: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def default_offer_ladder() -> list[Offer]:
    return [
        Offer("Saudi Opportunity Snapshot", "early interest", "499-1500 SAR", "source-backed one-page snapshot", "Would a one-page snapshot help?"),
        Offer("Revenue Proof Sprint", "fast first revenue", "499-2500 SAR", "manual payment evidence + proof pack", "Want a small proof sprint first?"),
        Offer("Revenue Command Pilot", "Saudi B2B operations", "2500-7500 SAR / 14 days", "daily report + drafts + approvals + proof pack", "Can we run a 14-day pilot?"),
        Offer("Saudi Market Access Sprint", "foreign B2B/SaaS entering KSA", "8000-35000 SAR", "qualified accounts + partner map + entry memo", "Should we test Saudi demand before setup?"),
        Offer("B2G Readiness Sprint", "enterprise/B2G readiness", "10000-50000 SAR", "readiness checklist + capability materials", "Would a readiness checklist be useful?"),
    ]
