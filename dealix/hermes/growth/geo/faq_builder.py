"""
FAQ builder — structured Q&A pairs for FAQPage schema emission.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FAQEntry:
    question: str
    answer: str


def build_faq(entries: list[FAQEntry]) -> dict[str, object]:
    if not entries:
        raise ValueError("at least one FAQ entry required")
    payload = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": e.question,
                "acceptedAnswer": {"@type": "Answer", "text": e.answer},
            }
            for e in entries
        ],
    }
    return payload
