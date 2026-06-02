"""WhatsApp Client OS — Support triage.

Classifies a support message into one of the canonical support categories and
flags whether it must reach a human directly (billing, urgent complaints, and
sensitive issues are never resolved by the bot alone).
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from auto_client_acquisition.whatsapp_client_os.schemas import SupportCategory

_CATEGORY_PATTERNS: tuple[tuple[SupportCategory, re.Pattern[str]], ...] = (
    (
        SupportCategory.BILLING,
        re.compile(
            r"فاتورة|دفع|سداد|اشتراك|استرجاع\s+مبلغ|billing|payment|invoice|refund|subscription",
            re.IGNORECASE,
        ),
    ),
    (
        SupportCategory.URGENT_COMPLAINT,
        re.compile(
            r"شكوى|عاجل\s+جدا|مشكلة\s+كبيرة|توقف\s+كل\s+شيء|urgent|complaint|escalat", re.IGNORECASE
        ),
    ),
    (
        SupportCategory.TECHNICAL,
        re.compile(
            r"لا\s+يعمل|ما\s+يشتغل|خطأ|عطل|توقف|not\s+working|error|down|crash|bug", re.IGNORECASE
        ),
    ),
    (
        SupportCategory.DATA,
        re.compile(
            r"بيانات\s+ناقصة|ناقص|مفقود|غير\s+صحيح(?:ة)?|data\s+missing|incorrect\s+data|wrong\s+data",
            re.IGNORECASE,
        ),
    ),
    (
        SupportCategory.REPORT,
        re.compile(
            r"التقرير|تقرير\s+غير\s+واضح|الأرقام\s+غلط|report|dashboard\s+wrong", re.IGNORECASE
        ),
    ),
    (
        SupportCategory.DRAFT_QUALITY,
        re.compile(
            r"الرسالة\s+(?:غير|مو)|عدّل\s+المسودة|صيغة\s+الرسالة|draft\s+(?:wrong|bad)|reword|rewrite",
            re.IGNORECASE,
        ),
    ),
    (
        SupportCategory.PERMISSION,
        re.compile(r"صلاحي|وصول|ربط|permission|access|connect", re.IGNORECASE),
    ),
)

# Categories the bot must hand to a human rather than resolve alone.
_HUMAN_ONLY = frozenset({SupportCategory.BILLING.value, SupportCategory.URGENT_COMPLAINT.value})


@dataclass(frozen=True, slots=True)
class SupportTriageResult:
    category: str
    needs_human: bool


def triage(text: str) -> SupportTriageResult:
    """Classify a support message; default to GENERAL."""
    raw = text or ""
    for category, pattern in _CATEGORY_PATTERNS:
        if pattern.search(raw):
            return SupportTriageResult(
                category=category.value,
                needs_human=category.value in _HUMAN_ONLY,
            )
    return SupportTriageResult(category=SupportCategory.GENERAL.value, needs_human=False)


__all__ = ["SupportTriageResult", "triage"]
