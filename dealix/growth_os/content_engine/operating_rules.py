"""Nine marketing operating rules from section 49 of the spec.

These rules are enforced as pure functions; violations are returned as
structured records so the caller can decide to block, escalate, or warn.
"""

from __future__ import annotations

from typing import Any, Final

from pydantic import BaseModel, ConfigDict, Field


class MarketingRule(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str = Field(..., min_length=1)
    title_ar: str
    title_en: str
    description_ar: str
    description_en: str


class RuleViolation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    rule_key: str
    severity: str = "blocking"
    reason_ar: str
    reason_en: str


MARKETING_OPERATING_RULES: Final[tuple[MarketingRule, ...]] = (
    MarketingRule(
        key="every_campaign_has_offer",
        title_ar="كل حملة لها عرض",
        title_en="Every campaign has an offer",
        description_ar="لا حملة بدون عرض موجّه",
        description_en="No campaign ships without an attached offer",
    ),
    MarketingRule(
        key="every_offer_has_proof",
        title_ar="كل عرض له إثبات",
        title_en="Every offer has proof",
        description_ar="لا عرض بدون proof_pack أو case أو policy_map",
        description_en="No offer without a linked proof asset",
    ),
    MarketingRule(
        key="every_content_has_cta",
        title_ar="كل محتوى له CTA",
        title_en="Every content asset has a CTA",
        description_ar="لا محتوى ينشر بدون دعوة لاتخاذ إجراء",
        description_en="No asset published without a CTA",
    ),
    MarketingRule(
        key="every_cta_maps_to_paid_offer",
        title_ar="كل CTA يربط لعرض مدفوع",
        title_en="Every CTA maps to a paid offer",
        description_ar="CTA يجب أن ينتهي إلى عرض في خطة الإيراد",
        description_en="CTA must end at an offer in the revenue plan",
    ),
    MarketingRule(
        key="every_lead_has_owner",
        title_ar="كل ليد له مالك",
        title_en="Every lead has an owner",
        description_ar="لا ليد بلا مالك مسؤول عن المتابعة",
        description_en="No lead without an accountable owner",
    ),
    MarketingRule(
        key="every_deal_has_proof_pack",
        title_ar="كل صفقة لها ProofPack",
        title_en="Every deal has a ProofPack",
        description_ar="لا صفقة تصدر دون ProofPack مرفق",
        description_en="No deal ships without an attached ProofPack",
    ),
    MarketingRule(
        key="every_revenue_record_verified",
        title_ar="كل سجل إيراد موثّق",
        title_en="Every revenue record is verified",
        description_ar="لا تُحتسب إيرادات بلا verification (دفع/فاتورة/عقد)",
        description_en="No revenue counted without payment/invoice/agreement",
    ),
    MarketingRule(
        key="no_external_send_without_approval",
        title_ar="لا إرسال خارجي بلا موافقة",
        title_en="No external send without approval",
        description_ar="جميع الإرسالات الخارجية تحتاج موافقة بشرية",
        description_en="All external sends require explicit human approval",
    ),
    MarketingRule(
        key="no_vanity_metric_reporting",
        title_ar="لا تقارير بمقاييس فارغة",
        title_en="No vanity-metric reporting",
        description_ar="ممنوع الاعتماد على likes/views/replies بديلاً عن الإيراد",
        description_en="Likes/views/replies are not a substitute for revenue",
    ),
)


def _has(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, set, dict)):
        return len(value) > 0
    return True


def _check_campaign(asset: dict[str, Any]) -> list[RuleViolation]:
    out: list[RuleViolation] = []
    if not _has(asset.get("offer_key")):
        out.append(
            RuleViolation(
                rule_key="every_campaign_has_offer",
                reason_ar="حملة بدون عرض مرتبط",
                reason_en="Campaign has no attached offer",
            )
        )
    return out


def _check_offer(asset: dict[str, Any]) -> list[RuleViolation]:
    out: list[RuleViolation] = []
    if not _has(asset.get("proof_assets")):
        out.append(
            RuleViolation(
                rule_key="every_offer_has_proof",
                reason_ar="عرض بدون إثبات",
                reason_en="Offer has no proof asset",
            )
        )
    return out


def _check_content(asset: dict[str, Any]) -> list[RuleViolation]:
    out: list[RuleViolation] = []
    if not _has(asset.get("cta_label")) and not _has(asset.get("cta")):
        out.append(
            RuleViolation(
                rule_key="every_content_has_cta",
                reason_ar="محتوى بدون CTA",
                reason_en="Content asset has no CTA",
            )
        )
    if not _has(asset.get("offer_key")):
        out.append(
            RuleViolation(
                rule_key="every_cta_maps_to_paid_offer",
                reason_ar="CTA لا يربط لعرض مدفوع",
                reason_en="CTA does not map to a paid offer",
            )
        )
    return out


def _check_lead(asset: dict[str, Any]) -> list[RuleViolation]:
    out: list[RuleViolation] = []
    if not _has(asset.get("owner")):
        out.append(
            RuleViolation(
                rule_key="every_lead_has_owner",
                reason_ar="ليد بدون مالك",
                reason_en="Lead has no owner",
            )
        )
    return out


def _check_deal(asset: dict[str, Any]) -> list[RuleViolation]:
    out: list[RuleViolation] = []
    if not _has(asset.get("proof_pack_id")) and not _has(asset.get("proof_pack")):
        out.append(
            RuleViolation(
                rule_key="every_deal_has_proof_pack",
                reason_ar="صفقة بدون ProofPack",
                reason_en="Deal has no ProofPack",
            )
        )
    return out


def _check_revenue(asset: dict[str, Any]) -> list[RuleViolation]:
    out: list[RuleViolation] = []
    if not _has(asset.get("verification")):
        out.append(
            RuleViolation(
                rule_key="every_revenue_record_verified",
                reason_ar="سجل إيراد بدون توثيق",
                reason_en="Revenue record has no verification",
            )
        )
    return out


_CHECKERS = {
    "campaign": _check_campaign,
    "offer": _check_offer,
    "content": _check_content,
    "lead": _check_lead,
    "deal": _check_deal,
    "revenue": _check_revenue,
}


def check_asset(kind: str, asset: dict[str, Any]) -> list[RuleViolation]:
    """Run the operating rules against an asset of the given kind."""
    if kind not in _CHECKERS:
        raise ValueError(f"unknown asset kind: {kind!r}")
    return _CHECKERS[kind](asset)


def enforce_marketing_rules(content_asset: dict[str, Any]) -> list[RuleViolation]:
    """Run the content-specific rules. Shortcut for ``check_asset('content', ...)``."""
    return check_asset("content", content_asset)


def list_rules() -> list[MarketingRule]:
    return list(MARKETING_OPERATING_RULES)


__all__ = [
    "MARKETING_OPERATING_RULES",
    "MarketingRule",
    "RuleViolation",
    "check_asset",
    "enforce_marketing_rules",
    "list_rules",
]
