"""Client permission ladder L0–L5 for the WhatsApp Client OS.

Rules (non-negotiable):
- Default is L0/L1 (questions, files the client sends).
- Any L2+ (read access into client systems) requires explanation + consent.
- Any L4+ (send-after-approval) requires an explicit approval step.
- L5 (payments, contracts, sensitive data) is NEVER completed in WhatsApp
  alone — it routes to a secure portal and/or a human.
"""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.whatsapp_client_os.schemas import PermissionLevel, RiskLevel

_ORDER: tuple[PermissionLevel, ...] = ("L0", "L1", "L2", "L3", "L4", "L5")


@dataclass(frozen=True, slots=True)
class LevelSpec:
    level: PermissionLevel
    meaning_ar: str
    example_ar: str
    risk: RiskLevel
    requires_explanation: bool
    requires_explicit_approval: bool
    whatsapp_only_allowed: bool  # may the level be completed inside WhatsApp alone?


_SPECS: dict[PermissionLevel, LevelSpec] = {
    "L0": LevelSpec("L0", "بدون صلاحيات", "أسئلة واستبيان الجاهزية", "low", False, False, True),
    "L1": LevelSpec(
        "L1", "ملفات/روابط يرسلها العميل", "يرسل CSV أو رابط", "low", False, False, True
    ),
    "L2": LevelSpec(
        "L2", "قراءة فقط من أنظمة العميل", "قراءة leads من CRM", "medium", True, False, True
    ),
    "L3": LevelSpec(
        "L3", "كتابة داخل نظام Dealix", "إنشاء drafts أو مهام", "medium", True, False, True
    ),
    "L4": LevelSpec("L4", "إرسال بعد موافقة صريحة", "إرسال إيميل معتمد", "high", True, True, True),
    "L5": LevelSpec("L5", "عمليات حسّاسة", "دفع، عقود، بيانات حسّاسة", "high", True, True, False),
}


def level_index(level: PermissionLevel) -> int:
    return _ORDER.index(level)


def spec(level: PermissionLevel) -> LevelSpec:
    return _SPECS[level]


def all_specs() -> list[LevelSpec]:
    return [_SPECS[lvl] for lvl in _ORDER]


def is_default_allowed(level: PermissionLevel) -> bool:
    """L0/L1 are allowed by default (no consent gate)."""
    return level_index(level) <= level_index("L1")


def requires_explanation(level: PermissionLevel) -> bool:
    return _SPECS[level].requires_explanation


def requires_explicit_approval(level: PermissionLevel) -> bool:
    return _SPECS[level].requires_explicit_approval


def can_complete_in_whatsapp(level: PermissionLevel) -> bool:
    """L5 can never be completed inside WhatsApp alone."""
    return _SPECS[level].whatsapp_only_allowed


def escalate_needed(level: PermissionLevel) -> bool:
    """True when the level demands a human / secure-portal route (L5)."""
    return not _SPECS[level].whatsapp_only_allowed


__all__ = [
    "LevelSpec",
    "all_specs",
    "can_complete_in_whatsapp",
    "escalate_needed",
    "is_default_allowed",
    "level_index",
    "requires_explanation",
    "requires_explicit_approval",
    "spec",
]
