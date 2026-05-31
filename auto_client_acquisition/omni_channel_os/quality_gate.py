"""Scores outreach assets on specificity, length, tone, CTA presence, and language quality."""
from __future__ import annotations

import logging

from auto_client_acquisition.omni_channel_os.schemas import (
    AssetType,
    ChannelAsset,
    Company,
    Language,
)

log = logging.getLogger(__name__)

_NO_AUTO_SEND = True

_PERSONALIZATION_TOKENS = (
    "{company}",
    "{name}",
    "{sector}",
    "{country}",
    "{pain}",
    "{offer}",
)

_CTA_MARKERS_EN = (
    "book",
    "schedule",
    "click",
    "reply",
    "contact",
    "get",
    "start",
    "try",
    "see",
    "learn",
    "download",
    "sign up",
    "register",
    "free",
)

_CTA_MARKERS_AR = (
    "احصل",
    "ابدأ",
    "سجل",
    "تواصل",
    "جرب",
    "شوف",
    "تحميل",
    "اكتشف",
    "تسجيل",
    "مجاني",
    "مجانا",
)

_QUALITY_PENALTY_PATTERNS = (
    "lorem ipsum",
    "placeholder",
    "todo",
    "fill in",
    "insert here",
    "guaranteed roi",
    "guaranteed results",
    "guaranteed sales",
    "نضمن لك نتائج",
    "نضمن الربح",
)


class QualityGate:
    _NO_AUTO_SEND = True

    MIN_WORD_COUNT: dict[AssetType, int] = {
        AssetType.email_draft: 60,
        AssetType.linkedin_connection_note: 20,
        AssetType.linkedin_dm: 40,
        AssetType.linkedin_followup_1: 30,
        AssetType.linkedin_followup_2: 30,
        AssetType.linkedin_comment_idea: 15,
        AssetType.linkedin_post_ar: 50,
        AssetType.linkedin_post_en: 50,
        AssetType.website_form_message: 60,
        AssetType.whatsapp_optin_reply: 20,
        AssetType.whatsapp_qualification: 25,
        AssetType.call_script: 50,
        AssetType.partner_intro: 40,
        AssetType.webinar_invite: 40,
        AssetType.lead_ad_followup: 20,
        AssetType.content_post_ar: 80,
        AssetType.content_post_en: 80,
        AssetType.proposal_seed: 100,
    }

    def score(self, asset: ChannelAsset, company: Company) -> float:
        s_length = self._score_length(asset)
        s_personal = self._score_personalization(asset, company)
        s_cta = self._score_cta_presence(asset)
        s_forbidden = self._score_forbidden_patterns(asset)

        raw = (
            s_length * 0.30
            + s_personal * 0.25
            + s_cta * 0.20
            + s_forbidden * 0.25
        )
        result = max(0.0, min(100.0, round(raw, 1)))
        log.debug(
            "quality_gate.score asset_id=%s score=%.1f length=%.1f personal=%.1f cta=%.1f forbidden=%.1f",
            asset.asset_id,
            result,
            s_length,
            s_personal,
            s_cta,
            s_forbidden,
        )
        return result

    def _score_length(self, asset: ChannelAsset) -> float:
        word_count = len(asset.body.split())
        minimum = self.MIN_WORD_COUNT.get(asset.asset_type, 40)
        if word_count == 0:
            return 0.0
        if word_count < minimum:
            return round(word_count / minimum * 70.0, 1)
        # Bonus for richness, capped at 100
        bonus = min(30.0, (word_count - minimum) / max(minimum, 1) * 20.0)
        return min(100.0, 70.0 + bonus)

    def _score_personalization(self, asset: ChannelAsset, company: Company) -> float:
        text = asset.body.lower()
        score = 40.0  # baseline for having a body

        # Company name present
        if company.name.lower() in text:
            score += 20.0

        # Sector or country mentioned
        if company.sector.value.lower().replace("_", " ") in text:
            score += 15.0
        if company.country.value.lower() in text:
            score += 10.0

        # Template tokens replaced (not still literal placeholders)
        raw_tokens_remaining = sum(1 for t in _PERSONALIZATION_TOKENS if t in text)
        if raw_tokens_remaining > 0:
            score -= raw_tokens_remaining * 15.0

        return max(0.0, min(100.0, score))

    def _score_cta_presence(self, asset: ChannelAsset) -> float:
        combined = (asset.cta + " " + asset.body).lower()
        if asset.language == Language.arabic:
            markers = _CTA_MARKERS_AR
        else:
            markers = _CTA_MARKERS_EN

        hits = sum(1 for m in markers if m in combined)
        if hits == 0:
            return 20.0
        if hits == 1:
            return 70.0
        return min(100.0, 70.0 + (hits - 1) * 10.0)

    def _score_forbidden_patterns(self, asset: ChannelAsset) -> float:
        text = (asset.body + " " + (asset.subject_or_hook or "") + " " + asset.cta).lower()
        hits = sum(1 for p in _QUALITY_PENALTY_PATTERNS if p in text)
        if hits == 0:
            return 100.0
        return max(0.0, 100.0 - hits * 40.0)

    def passes(self, asset: ChannelAsset, company: Company, min_score: float = 65.0) -> bool:
        return self.score(asset, company) >= min_score


__all__ = ["QualityGate"]
