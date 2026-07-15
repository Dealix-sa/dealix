"""
Extractive summarization — TextRank-lite.
تلخيص استخراجي — يختار أهم الجمل بدون نماذج توليدية.

Algorithm:
1. Sentence-split.
2. Compute sentence similarity via cosine over hashed-trigram embeddings.
3. Run power-iteration PageRank on the similarity graph.
4. Return top-K sentences in original order (no rewriting → low risk).
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from dealix.intelligence.layers.embeddings import cosine_similarity, embed

_SENT_SPLIT = re.compile(r"(?<=[\.\?!؟])\s+|\n+")
_DEFAULT_TOP_K = 3
_MAX_ITER = 30
_DAMPING = 0.85
_TOLERANCE = 1e-4


@dataclass(frozen=True)
class SentenceScore:
    sentence: str
    score: float
    original_index: int


@dataclass(frozen=True)
class SummaryResult:
    summary: str
    sentences: tuple[SentenceScore, ...]
    coverage_ratio: float  # selected_chars / total_chars
    backend: str = "textrank-lite"


class ExtractiveSummarizer:
    def __init__(self, top_k: int = _DEFAULT_TOP_K, *, min_sentence_chars: int = 12) -> None:
        self.top_k = max(1, int(top_k))
        self.min_sentence_chars = min_sentence_chars

    def summarize(self, text: str, *, top_k: int | None = None) -> SummaryResult:
        if not text or not text.strip():
            return SummaryResult("", tuple(), 0.0)
        sentences = self._split(text)
        if not sentences:
            return SummaryResult("", tuple(), 0.0)
        if len(sentences) == 1:
            s = sentences[0]
            return SummaryResult(
                s,
                (SentenceScore(s, 1.0, 0),),
                1.0,
            )
        embeddings = [embed(s) for s in sentences]
        scores = self._textrank(embeddings)
        ranked = sorted(
            (
                SentenceScore(s, scores[i], i)
                for i, s in enumerate(sentences)
            ),
            key=lambda x: x.score,
            reverse=True,
        )
        k = max(1, top_k or self.top_k)
        selected = sorted(ranked[:k], key=lambda x: x.original_index)
        summary = " ".join(s.sentence for s in selected)
        total_chars = sum(len(s) for s in sentences) or 1
        sel_chars = sum(len(s.sentence) for s in selected)
        return SummaryResult(
            summary=summary,
            sentences=tuple(selected),
            coverage_ratio=round(sel_chars / total_chars, 3),
        )

    # ── Internals ─────────────────────────────────────────────────
    def _split(self, text: str) -> list[str]:
        out: list[str] = []
        for raw in _SENT_SPLIT.split(text):
            s = raw.strip()
            if len(s) >= self.min_sentence_chars:
                out.append(s)
        return out

    @staticmethod
    def _textrank(embeddings: list[list[float]]) -> list[float]:
        n = len(embeddings)
        # Build similarity matrix (zero diagonal).
        sims = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                sij = max(0.0, cosine_similarity(embeddings[i], embeddings[j]))
                sims[i][j] = sij
                sims[j][i] = sij
        # Row-normalize.
        for i in range(n):
            total = sum(sims[i])
            if total > 0:
                sims[i] = [v / total for v in sims[i]]
        # Power iteration.
        scores = [1.0 / n] * n
        for _ in range(_MAX_ITER):
            new_scores = [(1 - _DAMPING) / n] * n
            for j in range(n):
                contrib = 0.0
                for i in range(n):
                    contrib += sims[i][j] * scores[i]
                new_scores[j] += _DAMPING * contrib
            delta = sum(abs(new_scores[i] - scores[i]) for i in range(n))
            scores = new_scores
            if delta < _TOLERANCE:
                break
        return scores
