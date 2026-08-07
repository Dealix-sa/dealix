#!/usr/bin/env python3
"""Generate Dealix Growth/Sales/Partnership action cards.

This generator is intentionally safe-by-default:
- It never sends messages.
- It creates review cards and draft messages only.
- It requires source_url and verification_status fields.
- WhatsApp cards are marked approval_required and draft_only.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SAMPLE_INPUT = ROOT / "data" / "commercial" / "growth_accounts.sample.json"
REPORT_DIR = ROOT / "reports" / "commercial" / "growth_cards"
LATEST_JSON = REPORT_DIR / "latest.json"
LATEST_MD = REPORT_DIR / "latest.md"

ALLOWED_MOTIONS = {
    "sales",
    "partnership",
    "proposal_push",
    "revival",
    "upsell",
    "retention",
    "referral",
}

SAFE_DEFAULTS = {
    "external_send_enabled": False,
    "outbound_mode": "draft_only",
    "approval_required": True,
    "whatsapp_live_send": False,
}


@dataclass(frozen=True)
class GrowthCard:
    card_id: str
    company_name: str
    sector: str
    city: str
    motion: str
    recommended_channel: str
    risk_level: str
    approval_required: bool
    send_status: str
    source_url: str
    verification_status: str
    pain_hypothesis: str
    dealix_angle: str
    recommended_product: str
    draft_message_ar: str
    draft_message_en: str
    buttons: list[dict[str, str]]
    owner_decision: str
    next_action: str


def load_accounts() -> list[dict[str, Any]]:
    if SAMPLE_INPUT.exists():
        return json.loads(SAMPLE_INPUT.read_text(encoding="utf-8"))
    return [
        {
            "company_name": "شركة خدمات لوجستية تجريبية",
            "sector": "logistics",
            "city": "Riyadh",
            "website": "https://example.com",
            "source_url": "https://example.com/contact",
            "verification_status": "ready_for_review",
            "motion": "partnership",
            "recommended_channel": "email",
            "pain_hypothesis": "متابعات B2B كثيرة وعروض تحتاج دفع ومتابعة منظمة.",
            "dealix_angle": "Revenue Command Room + Partnership follow-up queue.",
            "recommended_product": "Revenue Command Room OS",
        }
    ]


def normalize_motion(value: str | None) -> str:
    motion = (value or "sales").strip().lower()
    return motion if motion in ALLOWED_MOTIONS else "sales"


def risk_for_channel(channel: str, verification_status: str) -> str:
    channel = channel.lower()
    if channel == "whatsapp":
        return "high"
    if verification_status not in {"ready_for_review", "approved_to_send", "email_found", "contact_page_found"}:
        return "medium"
    return "low"


def channel_for(account: dict[str, Any]) -> str:
    channel = str(account.get("recommended_channel", "email")).strip().lower()
    if channel in {"whatsapp", "email", "linkedin_manual", "phone", "partner_referral", "website_form"}:
        return channel
    return "email"


def buttons_for(card_id: str, channel: str) -> list[dict[str, str]]:
    if channel == "whatsapp":
        return [
            {"id": f"card:{card_id}:approve", "title": "اعتماد"},
            {"id": f"card:{card_id}:edit", "title": "تعديل"},
            {"id": f"card:{card_id}:skip", "title": "تخطي"},
        ]
    return [
        {"id": f"card:{card_id}:review", "title": "مراجعة"},
        {"id": f"card:{card_id}:call", "title": "اتصال"},
        {"id": f"card:{card_id}:hold", "title": "تأجيل"},
    ]


def arabic_message(account: dict[str, Any], motion: str) -> str:
    company = account.get("company_name", "الشركة")
    angle = account.get("dealix_angle", "تنظيم المتابعة والمبيعات اليومية")
    if motion == "partnership":
        return (
            f"مرحبًا فريق {company}،\n\n"
            f"أتابع معكم بخصوص فرصة تعاون محتملة. Dealix يساعد الشركات في تحويل المتابعات والمبيعات والشراكات إلى غرفة قيادة يومية واضحة: فرص، مسودات، عروض، وقرارات متابعة.\n\n"
            f"زاوية التعاون المقترحة: {angle}.\n\n"
            "إذا مناسب، نرتب مكالمة قصيرة هذا الأسبوع ونوضح نموذج شراكة عملي بدون تغيير أنظمتكم الحالية.\n\n"
            "لإيقاف التواصل، يمكنكم الرد بـ إيقاف."
        )
    if motion == "proposal_push":
        return (
            f"مرحبًا فريق {company}،\n\n"
            "أحب أتابع معكم بخصوص العرض السابق. جهزنا طريقة أبسط لتحويل المتابعة إلى خطوات يومية واضحة ومقاسة بدل بقاء الفرصة معلقة.\n\n"
            "هل يناسبكم نراجع العرض في مكالمة قصيرة ونحدد أول خطوة تشغيلية؟\n\n"
            "لإيقاف التواصل، يمكنكم الرد بـ إيقاف."
        )
    if motion == "retention":
        return (
            f"مرحبًا فريق {company}،\n\n"
            "جهزنا مراجعة قيمة مختصرة توضّح أين تحسنت المتابعة وما الخطوة التالية التي تستحق التنفيذ.\n\n"
            "هل يناسبكم نرسل لكم ملخصًا تنفيذيًا ونقترح خطة الأسبوع القادم؟"
        )
    return (
        f"مرحبًا فريق {company}،\n\n"
        "لاحظنا أن كثيرًا من الشركات تضيع عليها فرص بين واتساب، الإيميل، والعروض غير المتابعة. Dealix يبني غرفة قيادة للمبيعات والمتابعة تعرض: من نكلم، ماذا نرسل، وما القرار التالي.\n\n"
        f"الزاوية المقترحة لكم: {angle}.\n\n"
        "هل يناسبكم موعد قصير هذا الأسبوع لعرض نموذج عملي؟\n\n"
        "لإيقاف التواصل، يمكنكم الرد بـ إيقاف."
    )


def english_message(account: dict[str, Any], motion: str) -> str:
    company = account.get("company_name", "your team")
    angle = account.get("dealix_angle", "daily sales and follow-up execution")
    return (
        f"Hello {company},\n\n"
        "Dealix helps B2B teams turn scattered sales, follow-ups, proposals, and partnerships into a daily command room with clear next actions.\n\n"
        f"Suggested angle: {angle}.\n\n"
        "Would a short call this week be useful to review a practical 7-day sprint?\n\n"
        "Reply STOP if you prefer not to receive follow-ups."
    )


def build_card(index: int, account: dict[str, Any]) -> GrowthCard:
    source_url = str(account.get("source_url", "")).strip()
    verification_status = str(account.get("verification_status", "unverified")).strip() or "unverified"
    motion = normalize_motion(account.get("motion"))
    channel = channel_for(account)
    card_id = f"growth-{index:04d}"

    return GrowthCard(
        card_id=card_id,
        company_name=str(account.get("company_name", "Unknown company")),
        sector=str(account.get("sector", "unknown")),
        city=str(account.get("city", "unknown")),
        motion=motion,
        recommended_channel=channel,
        risk_level=risk_for_channel(channel, verification_status),
        approval_required=True,
        send_status="draft_only",
        source_url=source_url or "MISSING_SOURCE_URL",
        verification_status=verification_status,
        pain_hypothesis=str(account.get("pain_hypothesis", "Needs verified pain hypothesis before outreach.")),
        dealix_angle=str(account.get("dealix_angle", "Growth Card OS + Commercial Command Room")),
        recommended_product=str(account.get("recommended_product", "Growth Card OS")),
        draft_message_ar=arabic_message(account, motion),
        draft_message_en=english_message(account, motion),
        buttons=buttons_for(card_id, channel),
        owner_decision="review",
        next_action="Founder/client reviews the card, edits draft if needed, then chooses approve/call/hold/discard.",
    )


def validate_card(card: GrowthCard) -> list[str]:
    errors: list[str] = []
    if card.source_url == "MISSING_SOURCE_URL":
        errors.append(f"{card.card_id}: source_url is required")
    if len(card.buttons) > 3:
        errors.append(f"{card.card_id}: WhatsApp/action cards allow at most 3 buttons")
    if card.send_status != "draft_only":
        errors.append(f"{card.card_id}: send_status must remain draft_only")
    if not card.approval_required:
        errors.append(f"{card.card_id}: approval_required must be true")
    return errors


def write_reports(cards: list[GrowthCard], errors: list[str]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "safe_defaults": SAFE_DEFAULTS,
        "summary": {
            "cards": len(cards),
            "errors": len(errors),
            "draft_only": True,
            "live_send": False,
        },
        "cards": [asdict(card) for card in cards],
        "errors": errors,
    }
    LATEST_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Dealix Growth Cards Report",
        "",
        f"Generated at: `{payload['generated_at']}`",
        "",
        "## Safety",
        "",
        "- External send: **disabled**",
        "- WhatsApp live send: **disabled**",
        "- Status: **draft_only**",
        "- Approval required: **true**",
        "",
        "## Cards",
        "",
    ]
    for card in cards:
        lines.extend(
            [
                f"### {card.company_name}",
                "",
                f"- Card: `{card.card_id}`",
                f"- Motion: `{card.motion}`",
                f"- Channel: `{card.recommended_channel}`",
                f"- Product: {card.recommended_product}",
                f"- Decision: `{card.owner_decision}`",
                f"- Next action: {card.next_action}",
                "",
            ]
        )
    if errors:
        lines.extend(["## Validation Errors", ""] + [f"- {err}" for err in errors])
    LATEST_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    accounts = load_accounts()
    cards = [build_card(i + 1, account) for i, account in enumerate(accounts)]
    errors: list[str] = []
    for card in cards:
        errors.extend(validate_card(card))
    write_reports(cards, errors)
    print(f"GROWTH_CARDS_GENERATED={len(cards)}")
    print(f"GROWTH_CARD_ERRORS={len(errors)}")
    print(f"REPORT_JSON={LATEST_JSON}")
    print(f"REPORT_MD={LATEST_MD}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
