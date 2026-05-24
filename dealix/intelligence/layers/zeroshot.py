"""
Zero-shot classifier — cosine similarity between text & label embeddings.
تصنيف بدون أمثلة — يحسب التشابه بين النص ومسميات الفئات.

No training data needed. Bilingual (uses the shared embedding model).
Useful for intent classification, lead routing, content tagging.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from dealix.intelligence.layers.embeddings import EmbeddingModel, cosine_similarity


@dataclass(frozen=True)
class ZeroShotResult:
    label: str
    score: float
    ranking: tuple[tuple[str, float], ...]
    multi_label: bool
    backend: str


class ZeroShotClassifier:
    """Single + multi-label zero-shot classifier."""

    def __init__(
        self,
        labels: Sequence[str],
        *,
        embedder: EmbeddingModel | None = None,
        hypothesis_template: str = "هذا النص عن {label} | this text is about {label}",
    ) -> None:
        if not labels:
            raise ValueError("at least one label is required")
        self._embedder = embedder or EmbeddingModel()
        self._labels = list(labels)
        self._hypotheses = [hypothesis_template.format(label=lbl) for lbl in self._labels]
        self._label_vecs = [self._embedder.embed(h).vector for h in self._hypotheses]

    def classify(
        self,
        text: str,
        *,
        multi_label: bool = False,
        threshold: float = 0.35,
    ) -> ZeroShotResult:
        if not text or not text.strip():
            return ZeroShotResult("unknown", 0.0, tuple(), multi_label, self._embedder.backend)
        qvec = self._embedder.embed(text).vector
        scored: list[tuple[str, float]] = []
        for label, lvec in zip(self._labels, self._label_vecs):
            scored.append((label, max(0.0, cosine_similarity(qvec, lvec))))
        scored.sort(key=lambda x: x[1], reverse=True)
        if multi_label:
            top = [(lbl, s) for lbl, s in scored if s >= threshold] or [scored[0]]
            label = ",".join(lbl for lbl, _ in top)
            score = max(s for _, s in top)
        else:
            label, score = scored[0]
        return ZeroShotResult(
            label=label,
            score=round(score, 4),
            ranking=tuple((lbl, round(s, 4)) for lbl, s in scored),
            multi_label=multi_label,
            backend=self._embedder.backend,
        )

    def add_label(self, label: str) -> None:
        if label in self._labels:
            return
        self._labels.append(label)
        hyp = f"هذا النص عن {label} | this text is about {label}"
        self._hypotheses.append(hyp)
        self._label_vecs.append(self._embedder.embed(hyp).vector)
