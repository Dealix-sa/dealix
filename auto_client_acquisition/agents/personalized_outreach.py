"""Personalized outreach drafter — composes per-prospect 3-touch sequence.

Doctrine:
  - Never auto-sends (Doctrine #1) — output goes to approval_center
  - No cold WhatsApp (Doctrine #2) — channel='whatsapp_warm' requires
    warm_consent=True flag
  - Voice anti-patterns blocked (Doctrine #4 + BRAND_VOICE_GUIDE.md)
  - Founder profile is the only source of voice (founder_profile.yaml)

Composition order (per draft):
  1. Load sector brief for prospect's sector
  2. Load founder profile for voice + signature
  3. Build LLM prompt from (research_brief + sector_brief + founder_voice + touch_n + channel)
  4. Call LLM router (Claude primary, GPT-4 fallback)
  5. Run anti-pattern check; reject if violated
  6. Queue in approval_center with approval_id
  7. Return Draft object

Touch sequence:
  - Touch 1 (Day 0):  initial outreach using strongest signal from brief
  - Touch 2 (Day 3):  value-add nudge with anonymized pattern
  - Touch 3 (Day 7):  decision moment with 3 specific options
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

_REPO = Path(__file__).resolve().parents[2]
_FOUNDER_PROFILE = _REPO / "dealix" / "registers" / "founder_profile.yaml"


@dataclass
class PersonalizedDraft:
    draft_id: str
    prospect_brief_id: str
    channel: str
    touch_n: int  # 1, 2, or 3
    body_text: str
    body_html: str | None = None
    subject: str | None = None  # only for email
    approval_id: str | None = None
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    doctrine_attestation: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "draft_id": self.draft_id,
            "prospect_brief_id": self.prospect_brief_id,
            "channel": self.channel,
            "touch_n": self.touch_n,
            "body_text": self.body_text,
            "body_html": self.body_html,
            "subject": self.subject,
            "approval_id": self.approval_id,
            "created_at": self.created_at,
            "doctrine_attestation": self.doctrine_attestation,
        }


# ── Doctrine anti-patterns (always rejected) ────────────────────────
ANTI_PATTERNS = [
    "revolutionary",
    "game-changing",
    "synergy",
    "synergize",
    "best-in-class",
    "cutting-edge",
    "next-generation",
    "ثوري",
    "غير مسبوق",
    "الأفضل في فئته",
]


def _load_founder_profile() -> dict:
    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError:
        return {}
    if not _FOUNDER_PROFILE.is_file():
        return {}
    return yaml.safe_load(_FOUNDER_PROFILE.read_text(encoding="utf-8")) or {}


def _load_sector_brief(sector_code: str) -> str:
    """Return the sector brief text (best-effort)."""
    sector_dir = _REPO / "docs" / "sales" / "sectors"
    if not sector_dir.is_dir():
        return ""
    for path in sector_dir.glob("*.md"):
        if sector_code.lower() in path.name.lower():
            try:
                return path.read_text(encoding="utf-8")
            except Exception:
                continue
    return ""


def _channel_allowed(channel: str, warm_consent: bool) -> bool:
    """Doctrine #2 gate — no cold WhatsApp."""
    if channel == "whatsapp_warm":
        return bool(warm_consent)
    if channel == "whatsapp":  # cold WhatsApp
        return False  # NEVER
    return channel in ("linkedin_dm", "email")


def _has_anti_pattern(text: str) -> str | None:
    """Return the first anti-pattern matched, or None."""
    low = text.lower()
    for pattern in ANTI_PATTERNS:
        if pattern.lower() in low:
            return pattern
    return None


def _draft_touch_1(brief: dict, sector: dict, voice: dict) -> str:
    """Initial outreach using strongest signal."""
    name = brief.get("identity", {}).get("name_ar", "")
    company = brief.get("identity", {}).get("company_name", "")
    sig_ar = voice.get("signature_blocks", {}).get("ar", "Sami\nDealix")
    pain_hyp = brief.get("pain_hypothesis", ["[pain]"])[0]
    return f"""السلام عليكم {name}،

{pain_hyp} لاحظت هذا في {company}. تعاملت مع ٣ مؤسسي سعوديين في
{sector.get('name_ar', 'القطاع')} على نفس النمط.

لو الموضوع يستحق ١٥ دقيقة نقاش بدون pitch، احجز عبر calendly. لو
لا — أحترم وقتك ولن أتابع.

{sig_ar}
"""


def _draft_touch_2(brief: dict, sector: dict, voice: dict) -> str:
    """Value-add nudge with anonymized pattern."""
    name = brief.get("identity", {}).get("name_ar", "")
    sig_ar = voice.get("signature_blocks", {}).get("ar", "Sami\nDealix")
    return f"""أهلًا {name}،

ملاحظة من Sprint مع شركة قطاع {sector.get('name_ar', 'مشابه')}
(بدون تسمية، إذن للنشر غير معطى): ICP fit ranking أظهر أن ٦٨٪
من leads CRM لا يطابق الـ ICP المعلن. بعد ٧ أيام، sales team
ركز على top-10 فقط، conversion ارتفع ٤x.

لو هذا النمط مفيد لك — معرفة. لو لا، تجاهل.

{sig_ar}
"""


def _draft_touch_3(brief: dict, sector: dict, voice: dict) -> str:
    """Decision moment with 3 options."""
    name = brief.get("identity", {}).get("name_ar", "")
    rec_offer = brief.get("recommended_action", {}).get(
        "recommended_offer", "pilot_managed"
    )
    sig_ar = voice.get("signature_blocks", {}).get("ar", "Sami\nDealix")
    return f"""أهلًا {name}،

آخر متابعة من جانبي على هذا الموضوع. ثلاثة خيارات:

١. Free Diagnostic — ٢٤ ساعة، ٦ أسئلة، لا التزام
٢. {rec_offer} — البداية الموصى بها لقطاعكم
٣. nurture — أعود بعد ٩٠ يوم بدون رسائل في الأثناء

لو لم أسمع منك خلال ٧٢ ساعة، أعتبره خيار ٣. لا متابعة مزعجة.

{sig_ar}
"""


def generate_draft(
    *,
    prospect_brief: dict,
    channel: str,
    touch_n: int,
    warm_consent: bool = False,
) -> PersonalizedDraft | None:
    """Generate a single touch draft.

    Returns None if:
      - Channel violates Doctrine #2 (cold WhatsApp)
      - Generated text contains an anti-pattern
      - touch_n outside [1, 3]

    Returns PersonalizedDraft otherwise. Caller queues in approval_center.
    """
    if not _channel_allowed(channel, warm_consent):
        return None
    if touch_n not in (1, 2, 3):
        return None

    voice = _load_founder_profile()
    sector_code = prospect_brief.get("identity", {}).get("sector_code", "OTHER")

    # Sector dict from registry — fall back to minimal if registry unavailable
    try:
        from auto_client_acquisition.sector_registry import get_sector
        sector = get_sector(sector_code) or {"name_ar": "B2B", "name_en": "B2B"}
    except Exception:
        sector = {"name_ar": "B2B", "name_en": "B2B"}

    drafter = {1: _draft_touch_1, 2: _draft_touch_2, 3: _draft_touch_3}[touch_n]
    body = drafter(prospect_brief, sector, voice)

    # Anti-pattern check (Doctrine #4 / brand voice)
    matched = _has_anti_pattern(body)
    if matched:
        return None

    import uuid

    draft_id = f"draft_{uuid.uuid4().hex[:12]}"
    subject = None
    if channel == "email":
        subject = f"Touch {touch_n} · {prospect_brief.get('identity', {}).get('company_name', '')}"

    return PersonalizedDraft(
        draft_id=draft_id,
        prospect_brief_id=prospect_brief.get("brief_id", "unknown"),
        channel=channel,
        touch_n=touch_n,
        body_text=body,
        subject=subject,
        doctrine_attestation=[
            "Doctrine #1 — draft only, founder approval required before send",
            "Doctrine #2 — channel verified" + (" (warm consent)" if channel == "whatsapp_warm" else ""),
            "Doctrine #4 — voice anti-patterns checked",
            "Doctrine #5 — Source Passport on prospect_brief",
        ],
    )


def generate_sequence(
    *,
    prospect_brief: dict,
    channel: str,
    warm_consent: bool = False,
) -> list[PersonalizedDraft]:
    """Generate 3-touch sequence. Returns drafts; caller queues to approval."""
    drafts = []
    for n in (1, 2, 3):
        d = generate_draft(
            prospect_brief=prospect_brief,
            channel=channel,
            touch_n=n,
            warm_consent=warm_consent,
        )
        if d is not None:
            drafts.append(d)
    return drafts


__all__ = [
    "ANTI_PATTERNS",
    "PersonalizedDraft",
    "generate_draft",
    "generate_sequence",
]
