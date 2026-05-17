"""Content cadence — the 6 LinkedIn content pillars and a deterministic
weekly schedule.

Mirrors ``docs/MARKETING_AND_CONTENT_SYSTEM.md`` §2 (أعمدة محتوى LinkedIn).
Pure data + a deterministic ``theme_for(date)`` — no I/O, no randomness, so
the same date always produces the same theme.
"""
from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ContentPillar:
    """One content pillar from the marketing system."""

    pillar_id: str
    name_ar: str
    name_en: str
    message_ar: str
    message_en: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "pillar_id": self.pillar_id,
            "name_ar": self.name_ar,
            "name_en": self.name_en,
            "message_ar": self.message_ar,
            "message_en": self.message_en,
        }


# The 6 canonical pillars (docs/MARKETING_AND_CONTENT_SYSTEM.md §2).
CADENCE_THEMES: tuple[ContentPillar, ...] = (
    ContentPillar(
        pillar_id="ai_under_control",
        name_ar="AI تحت السيطرة",
        name_en="AI Under Control",
        message_ar="الذكاء الاصطناعي مفيد حين تتحكم فيه — كل إجراء خارجي يمرّ بموافقتك.",
        message_en="AI helps when you control it — every external action waits for your approval.",
    ),
    ContentPillar(
        pillar_id="revenue_clarity",
        name_ar="وضوح الإيرادات",
        name_en="Revenue Clarity",
        message_ar="المشكلة ليست عدد الصفقات — المشكلة غياب الوضوح في القمع.",
        message_en="The problem is not deal count — it is the missing clarity in the pipeline.",
    ),
    ContentPillar(
        pillar_id="proof_not_promises",
        name_ar="إثبات لا وعود",
        name_en="Proof Not Promises",
        message_ar="نتيجة موثّقة في Proof Pack أقوى من أي وعد.",
        message_en="A documented result in a Proof Pack beats any promise.",
    ),
    ContentPillar(
        pillar_id="saudi_safe_gtm",
        name_ar="نمو آمن سعودياً",
        name_en="Saudi-Safe GTM",
        message_ar="النمو في السوق السعودي يحتاج حوكمة وامتثال PDPL، لا أتمتة عمياء.",
        message_en="Growth in the Saudi market needs governance and PDPL compliance, not blind automation.",
    ),
    ContentPillar(
        pillar_id="agency_growth_desk",
        name_ar="مكتب نمو الوكالات",
        name_en="Agency Growth Desk",
        message_ar="الوكالة التي تثبت نتائجها بالأرقام تكسب العقود.",
        message_en="The agency that proves its results with numbers wins the contracts.",
    ),
    ContentPillar(
        pillar_id="executive_radar",
        name_ar="رادار التنفيذي",
        name_en="Executive Radar",
        message_ar="ثلاثة قرارات واضحة أفضل من ثلاثين لوحة معلومات.",
        message_en="Three clear decisions beat thirty dashboards.",
    ),
)


def theme_for(date: _dt.date | None = None) -> ContentPillar:
    """Return the content pillar for ``date`` (deterministic).

    Cycles through all 6 pillars by ordinal day so every pillar is used
    roughly evenly regardless of weekday.
    """
    day = date or _dt.datetime.now(_dt.UTC).date()
    index = day.toordinal() % len(CADENCE_THEMES)
    return CADENCE_THEMES[index]


__all__ = ["CADENCE_THEMES", "ContentPillar", "theme_for"]
