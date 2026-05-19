"""Deterministic pain-signal extraction (Stage 4).

No LLM: scans the lead's request text for known post-lead pain signals,
in Arabic and English. Feeds the ``pain_clear`` flag into qualification.
See ``docs/distribution_os/BUYER_PSYCHOLOGY.md``.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# signal label -> trigger phrases (lowercased, ar + en).
_PAIN_SIGNALS: dict[str, tuple[str, ...]] = {
    "leads_lost_after_campaign": (
        "leads lost", "lose leads", "losing leads", "leads go cold",
        "تضيع", "نخسر العملاء", "ضياع",
    ),
    "no_followup_owner": (
        "no follow-up", "no follow up", "nobody follows up", "no owner",
        "لا متابعة", "ما في متابعة", "لا أحد يتابع", "ما حد مسؤول",
    ),
    "cannot_prove_outcome": (
        "can't prove", "cannot prove", "no proof", "no evidence",
        "ما نقدر نثبت", "لا دليل", "إثبات",
    ),
    "dead_crm": (
        "crm is dead", "crm not used", "crm does nothing",
        "crm ميت", "ما نستخدم crm", "crm ما يحرك",
    ),
    "messy_followup": (
        "messy", "scattered", "disorganized", "chaos",
        "فوضى", "متناثرة", "غير منظم",
    ),
    "no_visibility": (
        "no visibility", "no clarity", "don't know where", "blind",
        "ما نعرف وين", "غياب الوضوح", "تقارير شكلية",
    ),
}


@dataclass(frozen=True, slots=True)
class PainResult:
    """Outcome of pain extraction."""

    pain_clear: bool
    signals: tuple[str, ...] = ()
    signal_count: int = 0

    def to_dict(self) -> dict[str, object]:
        return {
            "pain_clear": self.pain_clear,
            "signals": list(self.signals),
            "signal_count": self.signal_count,
        }


def extract_pain(request_text: str) -> PainResult:
    """Extract post-lead pain signals from a lead's request text."""
    lowered = (request_text or "").lower()
    found: list[str] = []
    for label, triggers in _PAIN_SIGNALS.items():
        if any(trigger in lowered for trigger in triggers):
            found.append(label)
    return PainResult(
        pain_clear=bool(found),
        signals=tuple(found),
        signal_count=len(found),
    )


__all__ = ["PainResult", "extract_pain"]
