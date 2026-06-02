"""Read-only accessor for the canonical offers catalog (os/03_OFFERS.yml).

The distribution layer never invents prices. Proposals and renewals pull
pricing, duration, and the natural next offer from this single source of truth.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any

import yaml

from dealix.distribution.paths import OFFERS_YAML


@lru_cache(maxsize=1)
def load_offers() -> dict[str, Any]:
    if not OFFERS_YAML.is_file():
        return {}
    data = yaml.safe_load(OFFERS_YAML.read_text(encoding="utf-8")) or {}
    offers = data.get("offers") if isinstance(data, dict) else None
    return offers if isinstance(offers, dict) else {}


def get_offer(offer_ref: str) -> dict[str, Any] | None:
    return load_offers().get(offer_ref)


def _fmt(n: Any) -> str:
    try:
        return f"{int(n):,}"
    except (TypeError, ValueError):
        return str(n)


def price_range_sar(offer: dict[str, Any]) -> str:
    """Human-readable SAR price range from an offer (handles monthly retainers)."""
    block = offer.get("price_sar") or offer.get("price_sar_monthly") or {}
    suffix = "/شهر" if "price_sar_monthly" in offer else ""
    lo, hi = block.get("min"), block.get("max")
    if lo is None and hi is None:
        return "حسب النطاق"
    if hi is None:
        return f"يبدأ من {_fmt(lo)} SAR{suffix}"
    return f"{_fmt(lo)}–{_fmt(hi)} SAR{suffix}"


def duration_days(offer: dict[str, Any]) -> int | None:
    block = offer.get("duration_days") or {}
    val = block.get("typical") or block.get("max") or block.get("min")
    try:
        return int(val) if val is not None else None
    except (TypeError, ValueError):
        return None


def next_offer_ref(offer_ref: str) -> str | None:
    """The natural next rung on the upsell ladder for an offer."""
    offer = get_offer(offer_ref) or {}
    return offer.get("natural_next_offer") or offer.get("natural_upsell")


def upsell_ladder(start_ref: str, *, max_len: int = 6) -> list[str]:
    """Follow ``natural_next_offer`` from a starting offer (cycle-safe)."""
    ladder: list[str] = []
    seen: set[str] = set()
    ref: str | None = start_ref
    while ref and ref not in seen and len(ladder) < max_len:
        ladder.append(ref)
        seen.add(ref)
        ref = next_offer_ref(ref)
    return ladder


__all__ = [
    "duration_days",
    "get_offer",
    "load_offers",
    "next_offer_ref",
    "price_range_sar",
    "upsell_ladder",
]
