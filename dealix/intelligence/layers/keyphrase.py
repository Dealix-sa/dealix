"""
Keyphrase extraction — RAKE-style, bilingual.
استخراج العبارات المفتاحية بأسلوب RAKE — يدعم العربية والإنجليزية.

No deps. Output is a ranked list of multi-word phrases with scores.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from dealix.intelligence.arabic_nlp import normalize_arabic

_STOP_AR = {
    "في", "على", "من", "الى", "إلى", "هو", "هي", "هذا", "هذه", "ذلك", "تلك",
    "ان", "أن", "إن", "كان", "كانت", "يكون", "تكون", "ما", "ماذا", "كيف",
    "متى", "اين", "أين", "لماذا", "هل", "نعم", "لا", "مع", "بعد", "قبل",
    "ايضا", "أيضا", "حتى", "لكن", "او", "أو", "و", "ثم", "كذلك", "غير",
    "بين", "خلال", "حول", "عن", "لدى", "عند", "كل", "بعض",
    "احنا", "احنه", "احنه", "نحن", "انا", "أنا", "انت", "أنت",
    "ال", "ها", "بال", "كال", "فال", "وال", "لل",
}
_STOP_EN = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "of", "in", "on", "at",
    "to", "for", "with", "by", "from", "as", "and", "or", "but", "if",
    "then", "than", "this", "that", "these", "those", "it", "its", "i",
    "you", "we", "they", "he", "she", "him", "her", "them", "us", "my",
    "your", "our", "their", "his", "hers", "ours", "what", "which", "who",
    "whom", "whose", "where", "when", "why", "how", "all", "any", "both",
    "each", "few", "more", "most", "some", "such", "no", "not", "only",
    "own", "same", "so", "too", "very", "can", "will", "just",
}
_PUNCT_SPLIT = re.compile(r"[\.,;:!\?\(\)\[\]\{\}\"'/\\\|\-—–\n\r\t،؛؟]+")
_WHITESPACE = re.compile(r"\s+")
_DIGIT_ONLY = re.compile(r"^\d+(\.\d+)?$")


@dataclass(frozen=True)
class Keyphrase:
    phrase: str
    score: float
    word_count: int
    frequency: int


class KeyphraseExtractor:
    """RAKE — Rapid Automatic Keyword Extraction (bilingual flavor)."""

    def __init__(
        self,
        *,
        min_word_chars: int = 2,
        max_phrase_words: int = 5,
        extra_stopwords: set[str] | None = None,
    ) -> None:
        self.min_word_chars = min_word_chars
        self.max_phrase_words = max_phrase_words
        self.stopwords = {normalize_arabic(s) for s in (_STOP_AR | _STOP_EN)}
        if extra_stopwords:
            self.stopwords |= {normalize_arabic(s) for s in extra_stopwords}

    def extract(self, text: str, *, top_k: int = 10) -> list[Keyphrase]:
        if not text or not text.strip():
            return []
        phrases = self._candidate_phrases(text)
        if not phrases:
            return []
        word_scores = self._score_words(phrases)
        # Phrase score = sum of word scores; frequency boost.
        phrase_freq: dict[str, int] = {}
        for p in phrases:
            phrase_freq[p] = phrase_freq.get(p, 0) + 1
        scored: list[Keyphrase] = []
        seen: set[str] = set()
        for p, freq in phrase_freq.items():
            words = p.split()
            score = sum(word_scores.get(w, 0.0) for w in words) * (1 + 0.1 * (freq - 1))
            key = " ".join(words)
            if key in seen:
                continue
            seen.add(key)
            scored.append(
                Keyphrase(
                    phrase=p, score=round(score, 4), word_count=len(words), frequency=freq
                )
            )
        scored.sort(key=lambda k: k.score, reverse=True)
        return scored[:top_k]

    # ── Internals ─────────────────────────────────────────────────
    def _candidate_phrases(self, text: str) -> list[str]:
        out: list[str] = []
        for segment in _PUNCT_SPLIT.split(text):
            seg = _WHITESPACE.sub(" ", segment).strip()
            if not seg:
                continue
            words = [normalize_arabic(w.lower()) for w in seg.split()]
            buf: list[str] = []
            for w in words:
                if (
                    not w
                    or len(w) < self.min_word_chars
                    or w in self.stopwords
                    or _DIGIT_ONLY.match(w)
                ):
                    if buf:
                        out.extend(self._window_phrase(buf))
                        buf = []
                    continue
                buf.append(w)
            if buf:
                out.extend(self._window_phrase(buf))
        return out

    def _window_phrase(self, words: list[str]) -> list[str]:
        if len(words) <= self.max_phrase_words:
            return [" ".join(words)]
        # Slide a window equal to max_phrase_words to avoid mega-phrases.
        out: list[str] = []
        for i in range(0, len(words) - self.max_phrase_words + 1):
            out.append(" ".join(words[i : i + self.max_phrase_words]))
        return out

    @staticmethod
    def _score_words(phrases: list[str]) -> dict[str, float]:
        word_freq: dict[str, int] = {}
        word_degree: dict[str, int] = {}
        for p in phrases:
            ws = p.split()
            degree = len(ws) - 1
            for w in ws:
                word_freq[w] = word_freq.get(w, 0) + 1
                word_degree[w] = word_degree.get(w, 0) + degree
        return {w: (word_degree[w] + word_freq[w]) / word_freq[w] for w in word_freq}
