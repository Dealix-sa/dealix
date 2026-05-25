from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FAQItem:
    question: str
    answer: str


def faq_jsonld(items: list[FAQItem]) -> dict[str, object]:
    if not items:
        raise ValueError("at least one FAQItem required")
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item.question,
                "acceptedAnswer": {"@type": "Answer", "text": item.answer},
            }
            for item in items
        ],
    }
