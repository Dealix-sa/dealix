"""
Moderation layer — toxicity + content category for user/agent text.
طبقة الإشراف على المحتوى — تصنيف السمّية والفئات الحساسة.

Bilingual lexicon-based. Output is a per-category score in [0,1].
Categories: toxicity, harassment, hate, sexual, violence, self_harm.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Literal

from dealix.intelligence.arabic_nlp import normalize_arabic, segment_arabic

Category = Literal["toxicity", "harassment", "hate", "sexual", "violence", "self_harm"]

# Conservative bilingual lexicons. Weights in [0,1].
_TOXIC = {
    "غبي": 0.7, "حقير": 0.9, "تافه": 0.6, "زبالة": 0.9, "حمار": 0.7, "كلب": 0.7,
    "stupid": 0.6, "idiot": 0.8, "trash": 0.7, "loser": 0.6, "moron": 0.8,
}
_HARASSMENT = {
    "اكرهك": 0.8, "اقتلك": 1.0, "اضربك": 0.9, "اطردك": 0.6,
    "i hate you": 0.7, "kill you": 1.0, "fight you": 0.8,
}
_HATE = {
    "كافر": 0.9, "ملحد": 0.6, "زنديق": 0.9, "اجنبي حقير": 0.9,
    "racist": 0.7, "infidel": 0.7,
}
_SEXUAL = {
    "بورنو": 1.0, "اباحه": 0.8, "اباحة": 0.8, "جنس": 0.5,
    "porn": 1.0, "nude": 0.7, "nudes": 0.7, "sex": 0.5,
}
_VIOLENCE = {
    "اقتل": 0.9, "اضرب": 0.6, "تفجير": 0.9, "سلاح": 0.6, "ارهاب": 1.0,
    "kill": 0.8, "shoot": 0.8, "bomb": 0.9, "terror": 1.0,
}
_SELF_HARM = {
    "انتحار": 1.0, "اقتل نفسي": 1.0, "اذي نفسي": 0.9,
    "suicide": 1.0, "kill myself": 1.0, "self harm": 0.9,
}


def _norm_dict(d: dict[str, float]) -> dict[str, float]:
    return {normalize_arabic(k.lower()): v for k, v in d.items()}


_CATEGORIES: dict[Category, dict[str, float]] = {
    "toxicity": _norm_dict(_TOXIC),
    "harassment": _norm_dict(_HARASSMENT),
    "hate": _norm_dict(_HATE),
    "sexual": _norm_dict(_SEXUAL),
    "violence": _norm_dict(_VIOLENCE),
    "self_harm": _norm_dict(_SELF_HARM),
}


@dataclass(frozen=True)
class ModerationResult:
    flagged: bool
    categories: dict[Category, float] = field(default_factory=dict)  # type: ignore[arg-type]
    highest_category: Category | None = None
    highest_score: float = 0.0
    matched_terms: tuple[str, ...] = field(default_factory=tuple)


class Moderator:
    def __init__(self, *, threshold: float = 0.5) -> None:
        self.threshold = threshold

    def evaluate(self, text: str) -> ModerationResult:
        if not text or not text.strip():
            return ModerationResult(False, {}, None, 0.0, tuple())
        norm = normalize_arabic(text.lower())
        tokens = set(segment_arabic(norm))
        scores: dict[Category, float] = {}
        matched: list[str] = []
        for cat, lex in _CATEGORIES.items():
            best = 0.0
            for term, weight in lex.items():
                if " " in term:
                    if term in norm:
                        matched.append(term)
                        best = max(best, weight)
                elif term in tokens:
                    matched.append(term)
                    best = max(best, weight)
            scores[cat] = round(best, 3)
        highest_cat = max(scores, key=lambda k: scores[k]) if scores else None
        highest = scores.get(highest_cat, 0.0) if highest_cat else 0.0  # type: ignore[arg-type]
        return ModerationResult(
            flagged=highest >= self.threshold,
            categories=scores,
            highest_category=highest_cat,
            highest_score=highest,
            matched_terms=tuple(sorted(set(matched))),
        )

    def filter(self, texts: Iterable[str]) -> list[tuple[str, ModerationResult]]:
        return [(t, self.evaluate(t)) for t in texts]
