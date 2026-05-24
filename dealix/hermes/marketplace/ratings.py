"""Ratings + reviews for listings."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Rating:
    listing_id: str
    rater: str
    stars: int   # 1..5
    comment: str = ""


@dataclass
class RatingBoard:
    _ratings: list[Rating] = field(default_factory=list)

    def add(self, *, listing_id: str, rater: str, stars: int, comment: str = "") -> Rating:
        if not 1 <= stars <= 5:
            raise ValueError("stars must be in [1,5].")
        r = Rating(listing_id=listing_id, rater=rater, stars=stars, comment=comment)
        self._ratings.append(r)
        return r

    def average(self, listing_id: str) -> float:
        items = [r.stars for r in self._ratings if r.listing_id == listing_id]
        return sum(items) / len(items) if items else 0.0


__all__ = ["Rating", "RatingBoard"]
