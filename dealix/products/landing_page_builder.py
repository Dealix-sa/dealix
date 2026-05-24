"""خادم المنتج — LandingPageBuilder.

Produces a structured landing-page draft (hero, pain bullets,
deliverable bullets, CTA, trust badges) from an Offer. Pure data —
templating into HTML is the caller's job.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from dealix.money.offer_matcher import Offer


class LandingPageDraft(BaseModel):
    """Structured landing-page content (no HTML rendering)."""

    model_config = ConfigDict(extra="forbid")

    hero_title: str = Field(..., min_length=1, max_length=160)
    hero_subtitle: str = Field(..., min_length=1, max_length=300)
    pain_bullets: list[str] = Field(..., min_length=1, max_length=8)
    deliverable_bullets: list[str] = Field(..., min_length=1, max_length=12)
    cta_primary: str = Field(..., min_length=1, max_length=80)
    cta_secondary: str = Field(default="View pricing", max_length=80)
    trust_badges: list[str] = Field(default_factory=list, max_length=10)
    price_band_label: str = Field(..., min_length=1, max_length=160)
    success_metric: str = Field(..., min_length=1, max_length=300)
    arabic_title: str | None = None


_DEFAULT_BADGES: tuple[str, ...] = (
    "PDPL-aware",
    "ZATCA-aware",
    "Sami-reviewed",
    "Evidence-pack backed",
)


class LandingPageBuilder:
    """Turn an Offer into a structured landing-page draft."""

    def draft(self, offer: Offer, *, arabic_title: str | None = None) -> LandingPageDraft:
        hero_title = offer.name
        hero_subtitle = f"For {offer.buyer.lower()} who need {offer.pain.lower()}."
        pain_bullets = _split_into_bullets(offer.pain)
        deliverable_bullets = _split_into_bullets(offer.deliverable)
        low, high = offer.price_band
        price_label = (
            f"{low.amount:.0f}–{high.amount:.0f} {low.currency}"
        )
        return LandingPageDraft(
            hero_title=hero_title,
            hero_subtitle=hero_subtitle,
            pain_bullets=pain_bullets,
            deliverable_bullets=deliverable_bullets,
            cta_primary="Book a 20-minute scoping call",
            cta_secondary="View pricing",
            trust_badges=list(_DEFAULT_BADGES),
            price_band_label=price_label,
            success_metric=offer.success_metric,
            arabic_title=arabic_title,
        )


def _split_into_bullets(text: str) -> list[str]:
    bullets: list[str] = []
    for chunk in text.replace("\n", ";").split(";"):
        for line in chunk.split(","):
            cleaned = line.strip(" .;")
            if cleaned and cleaned not in bullets:
                bullets.append(cleaned)
    if not bullets:
        bullets.append(text.strip())
    return bullets[:8]


__all__ = ["LandingPageBuilder", "LandingPageDraft"]
