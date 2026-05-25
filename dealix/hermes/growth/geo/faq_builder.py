"""
FaqBuilder — emit Schema.org FAQPage JSON-LD blocks for GEO pages.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FaqEntry:
    question: str
    answer: str


def build_faq(topic: str, entries: list[FaqEntry]) -> dict[str, object]:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "name": f"{topic} — FAQ",
        "mainEntity": [
            {
                "@type": "Question",
                "name": e.question,
                "acceptedAnswer": {"@type": "Answer", "text": e.answer},
            }
            for e in entries
        ],
    }
