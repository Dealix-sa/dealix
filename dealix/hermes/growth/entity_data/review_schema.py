from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ReviewEntity:
    author: str
    rating: float
    body: str
    item_reviewed: str
    rating_max: float = 5.0
    rating_min: float = 1.0


def review_jsonld(r: ReviewEntity) -> dict[str, object]:
    if not (r.rating_min <= r.rating <= r.rating_max):
        raise ValueError(
            f"rating {r.rating} outside [{r.rating_min},{r.rating_max}]"
        )
    return {
        "@context": "https://schema.org",
        "@type": "Review",
        "author": {"@type": "Person", "name": r.author},
        "reviewRating": {
            "@type": "Rating",
            "ratingValue": r.rating,
            "bestRating": r.rating_max,
            "worstRating": r.rating_min,
        },
        "reviewBody": r.body,
        "itemReviewed": {"@type": "Product", "name": r.item_reviewed},
    }
