"""Social content drafting engine — deterministic, internal-inputs-only.

Produces bilingual (Arabic-primary) LinkedIn / X post drafts from internal
sources only: the content cadence (``cadence.py``) and the static offer
ladder (``finance_os/pricing_catalog.py``). No external data is fetched —
this engine cannot trip the no-scraping guard.

Every assembled draft is run through ``governance_os.policy_check_draft``;
any draft that fails the automated check is dropped, never returned.
"""
from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass
from typing import Any

from auto_client_acquisition.content_os.cadence import ContentPillar, theme_for
from auto_client_acquisition.finance_os.pricing_catalog import pricing_catalog
from auto_client_acquisition.governance_os.policy_check import policy_check_draft

SUPPORTED_PLATFORMS: tuple[str, ...] = ("linkedin", "x")


@dataclass(frozen=True, slots=True)
class SocialPostDraft:
    """A single bilingual social post awaiting founder approval."""

    platform: str  # "linkedin" | "x"
    locale_primary: str
    theme: str  # pillar_id
    body_ar: str
    body_en: str
    internal_sources: tuple[str, ...]
    proof_impact: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "platform": self.platform,
            "locale_primary": self.locale_primary,
            "theme": self.theme,
            "body_ar": self.body_ar,
            "body_en": self.body_en,
            "internal_sources": list(self.internal_sources),
            "proof_impact": self.proof_impact,
        }


def _entry_offer() -> dict[str, Any]:
    """The free diagnostic — the funnel entry point used in every CTA."""
    catalog = pricing_catalog()
    for tier in catalog:
        if tier["tier_id"] == "diagnostic":
            return tier
    return catalog[0]


def _linkedin_body(pillar: ContentPillar, offer: dict[str, Any]) -> tuple[str, str]:
    """Assemble the bilingual LinkedIn post body for one pillar."""
    body_ar = (
        f"{pillar.name_ar}\n\n"
        f"{pillar.message_ar}\n\n"
        f"في Dealix نشتغل بطريقة محكومة: كل مسوّدة تواصل، كل تقرير، وكل قرار "
        f"استهداف يصل لك جاهزاً — وأنت من يوافق قبل أي إرسال.\n\n"
        f"ابدأ بـ«{offer['name_ar']}»: {offer['description_ar']}\n\n"
        f"نساعدك على وضوح الإيراد — والنتائج تقديرية، نوثّقها ولا نَعِد بها."
    )
    body_en = (
        f"{pillar.name_en}\n\n"
        f"{pillar.message_en}\n\n"
        f"At Dealix we work the governed way: every outreach draft, every "
        f"report, and every targeting decision reaches you ready — and you "
        f"approve before anything is sent.\n\n"
        f"Start with \"{offer['name_en']}\": {offer['description_en']}\n\n"
        f"We help you reach revenue clarity — outcomes are estimated and "
        f"documented, never promised."
    )
    return body_ar, body_en


def _x_body(pillar: ContentPillar, offer: dict[str, Any]) -> tuple[str, str]:
    """Assemble the bilingual X (Twitter) post body — short form."""
    body_ar = (
        f"{pillar.message_ar}\n\n"
        f"ابدأ بـ«{offer['name_ar']}» — مراجعتك تسبق أي إرسال. #الإيراد #الحوكمة"
    )
    body_en = (
        f"{pillar.message_en}\n\n"
        f"Start with \"{offer['name_en']}\" — your review precedes every send."
    )
    return body_ar, body_en


def _build_draft(platform: str, pillar: ContentPillar, offer: dict[str, Any]) -> SocialPostDraft | None:
    """Build one draft and gate it through the governance pre-check."""
    if platform == "linkedin":
        body_ar, body_en = _linkedin_body(pillar, offer)
    else:
        body_ar, body_en = _x_body(pillar, offer)

    # Governance pre-check on the full bilingual text. A failing draft is
    # dropped — never returned, never queued.
    if not policy_check_draft(f"{body_ar}\n{body_en}").allowed:
        return None

    return SocialPostDraft(
        platform=platform,
        locale_primary="ar",
        theme=pillar.pillar_id,
        body_ar=body_ar,
        body_en=body_en,
        internal_sources=("content_cadence", "pricing_catalog"),
        proof_impact="content_os:authority",
    )


def draft_daily_social_posts(
    *,
    date: _dt.date | None = None,
    count: int = 1,
    platforms: tuple[str, ...] = SUPPORTED_PLATFORMS,
) -> list[SocialPostDraft]:
    """Draft today's social posts — ``count`` per platform (default 1 each).

    Deterministic: the same ``date`` always yields the same drafts.
    """
    day = date or _dt.datetime.now(_dt.UTC).date()
    offer = _entry_offer()
    drafts: list[SocialPostDraft] = []
    for i in range(max(1, count)):
        # Successive posts on the same day step through following pillars.
        pillar = theme_for(day + _dt.timedelta(days=i))
        for platform in platforms:
            if platform not in SUPPORTED_PLATFORMS:
                continue
            draft = _build_draft(platform, pillar, offer)
            if draft is not None:
                drafts.append(draft)
    return drafts


__all__ = ["SUPPORTED_PLATFORMS", "SocialPostDraft", "draft_daily_social_posts"]
