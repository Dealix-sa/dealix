"""
Content-based recommender — cosine over the vector store.
محرّك توصية مبني على المحتوى — تشابه كوساين على متجر المتجهات.

Recommends similar items given a seed item id (item-item) or a free-text
query (text-item). Composable with the RAG store. Includes optional
diversity (MMR) re-ranking.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence

from dealix.intelligence.layers.embeddings import cosine_similarity
from dealix.intelligence.layers.vector_store import VectorRecord, VectorStore


@dataclass(frozen=True)
class Recommendation:
    id: str
    score: float
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)


class ContentRecommender:
    """Cosine recommender with optional MMR diversification."""

    def __init__(
        self,
        store: VectorStore,
        *,
        diversify_lambda: float = 0.5,
    ) -> None:
        if not 0.0 <= diversify_lambda <= 1.0:
            raise ValueError("diversify_lambda in [0,1]")
        self._store = store
        self._lambda = diversify_lambda

    def by_id(
        self,
        record_id: str,
        *,
        top_k: int = 5,
        metadata_filter: dict[str, Any] | None = None,
        diversify: bool = True,
        exclude_self: bool = True,
    ) -> list[Recommendation]:
        rec = self._store.get(record_id)
        if rec is None:
            return []
        return self._search_with_vector(
            rec.vector,
            top_k=top_k,
            metadata_filter=metadata_filter,
            diversify=diversify,
            exclude_ids={record_id} if exclude_self else set(),
        )

    def by_text(
        self,
        text: str,
        *,
        top_k: int = 5,
        metadata_filter: dict[str, Any] | None = None,
        diversify: bool = True,
    ) -> list[Recommendation]:
        # Use store's embedder for parity.
        embed_vec = self._store._embedder.embed(text).vector  # type: ignore[attr-defined]
        return self._search_with_vector(
            embed_vec, top_k=top_k, metadata_filter=metadata_filter, diversify=diversify
        )

    # ── Internals ─────────────────────────────────────────────────
    def _search_with_vector(
        self,
        vector: Sequence[float],
        *,
        top_k: int,
        metadata_filter: dict[str, Any] | None,
        diversify: bool,
        exclude_ids: set[str] | None = None,
    ) -> list[Recommendation]:
        exclude_ids = exclude_ids or set()
        # Pull a deeper pool then rerank.
        pool_size = max(top_k * 4, 20)
        candidates = self._store.search_by_vector(
            vector, top_k=pool_size, metadata_filter=metadata_filter
        )
        candidates = [(r, s) for r, s in candidates if r.id not in exclude_ids]
        if not candidates:
            return []
        if not diversify or len(candidates) <= top_k:
            return [
                Recommendation(r.id, round(s, 4), r.text, dict(r.metadata or {}))
                for r, s in candidates[:top_k]
            ]
        return self._mmr(vector, candidates, top_k)

    def _mmr(
        self,
        query_vec: Sequence[float],
        candidates: list[tuple[VectorRecord, float]],
        top_k: int,
    ) -> list[Recommendation]:
        selected: list[tuple[VectorRecord, float]] = []
        remaining = list(candidates)
        while remaining and len(selected) < top_k:
            best_idx = 0
            best_score = -float("inf")
            for i, (rec, base_score) in enumerate(remaining):
                if not selected:
                    score = base_score
                else:
                    max_sim = max(
                        cosine_similarity(rec.vector, s_rec.vector) for s_rec, _ in selected
                    )
                    score = self._lambda * base_score - (1 - self._lambda) * max_sim
                if score > best_score:
                    best_score = score
                    best_idx = i
            pick = remaining.pop(best_idx)
            selected.append(pick)
        return [
            Recommendation(r.id, round(s, 4), r.text, dict(r.metadata or {}))
            for r, s in selected
        ]
