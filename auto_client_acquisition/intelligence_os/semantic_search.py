"""Hybrid semantic search — BM25-style sparse retrieval blended with dense cosine.

Dense-only retrieval is fast and bilingual but blind to rare terms and
exact-match phrases (company names, SKU numbers, dates). BM25-style sparse
retrieval catches those but misses semantic paraphrase. The hybrid blend
combines both with a weighted score and a configurable cap on each branch.

The implementation is deliberately self-contained (no external BM25 lib);
the term-frequency / inverse-document-frequency stats are computed at query
time over the candidate set returned by the dense branch — good enough for
modest corpora and trivial to swap for a production-grade index later.
"""

from __future__ import annotations

import math
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from auto_client_acquisition.intelligence_os.embedder import Embedder
from auto_client_acquisition.intelligence_os.vector_store import (
    InMemoryVectorStore,
    SearchHit,
    VectorRecord,
)

_WORD_RE = re.compile(r"[\w؀-ۿ]+", re.UNICODE)

# BM25 hyper-parameters with sensible defaults for short business documents.
_BM25_K1: float = 1.5
_BM25_B: float = 0.75


def _tokenize(text: str) -> list[str]:
    return [t.lower() for t in _WORD_RE.findall(text or "")]


def _bm25_score(
    *,
    query_terms: Sequence[str],
    doc_terms: Sequence[str],
    corpus_term_freq: Mapping[str, int],
    corpus_size: int,
    avg_doc_len: float,
) -> float:
    """Lightweight BM25 score for one document against one query."""
    if not doc_terms or not query_terms:
        return 0.0
    doc_len = len(doc_terms)
    tf: dict[str, int] = {}
    for term in doc_terms:
        tf[term] = tf.get(term, 0) + 1
    score = 0.0
    for term in query_terms:
        if term not in tf:
            continue
        n_q = corpus_term_freq.get(term, 0)
        if n_q == 0:
            continue
        idf = math.log(((corpus_size - n_q + 0.5) / (n_q + 0.5)) + 1.0)
        freq = tf[term]
        norm = 1.0 - _BM25_B + _BM25_B * (doc_len / max(avg_doc_len, 1.0))
        score += idf * (freq * (_BM25_K1 + 1.0)) / (freq + _BM25_K1 * norm)
    return score


@dataclass(frozen=True, slots=True)
class HybridHit:
    """One hit from hybrid search with both branches' scores exposed."""

    record_id: str
    text: str
    dense_score: float
    sparse_score: float
    blended_score: float
    namespace: str
    metadata: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_id": self.record_id,
            "text": self.text,
            "dense_score": self.dense_score,
            "sparse_score": self.sparse_score,
            "blended_score": self.blended_score,
            "namespace": self.namespace,
            "metadata": dict(self.metadata),
        }


def _build_corpus_stats(records: Sequence[VectorRecord]) -> tuple[dict[str, int], float]:
    """Compute term doc-frequencies and average doc length over a candidate set."""
    term_doc_freq: dict[str, int] = {}
    total_len = 0
    for r in records:
        terms = _tokenize(r.text)
        total_len += len(terms)
        for term in set(terms):
            term_doc_freq[term] = term_doc_freq.get(term, 0) + 1
    avg = total_len / len(records) if records else 0.0
    return term_doc_freq, avg


def hybrid_search(
    *,
    embedder: Embedder,
    store: InMemoryVectorStore,
    query: str,
    tenant_id: str = "",
    namespace: str | None = None,
    top_k: int = 5,
    dense_weight: float = 0.7,
    sparse_weight: float = 0.3,
    metadata_filter: Mapping[str, Any] | None = None,
    candidate_multiplier: int = 4,
) -> list[HybridHit]:
    """Run hybrid (dense cosine + BM25 sparse) retrieval and return top_k blended hits.

    The dense branch fetches up to ``top_k * candidate_multiplier`` candidates
    from the vector store; BM25 is computed over those candidates only. This
    keeps the cost proportional to the answer size and avoids scanning the
    whole corpus twice.
    """
    if top_k <= 0:
        return []
    if dense_weight < 0 or sparse_weight < 0:
        raise ValueError("weights must be non-negative")
    weight_sum = dense_weight + sparse_weight
    if weight_sum <= 0:
        raise ValueError("at least one of dense_weight / sparse_weight must be > 0")
    dw = dense_weight / weight_sum
    sw = sparse_weight / weight_sum

    query_vector = embedder.embed(query).vector
    candidates = store.search(
        query_vector=query_vector,
        tenant_id=tenant_id,
        namespace=namespace,
        top_k=top_k * max(candidate_multiplier, 1),
        metadata_filter=metadata_filter,
    )
    if not candidates:
        return []

    candidate_records = [c.record for c in candidates]
    term_doc_freq, avg_len = _build_corpus_stats(candidate_records)
    query_terms = _tokenize(query)

    sparse_scores = {
        c.record.record_id: _bm25_score(
            query_terms=query_terms,
            doc_terms=_tokenize(c.record.text),
            corpus_term_freq=term_doc_freq,
            corpus_size=len(candidate_records),
            avg_doc_len=avg_len,
        )
        for c in candidates
    }
    max_sparse = max(sparse_scores.values(), default=0.0)
    norm_sparse = {
        rid: (score / max_sparse if max_sparse > 0 else 0.0)
        for rid, score in sparse_scores.items()
    }
    # Cosine is already in [-1, 1]; clip negatives to 0 for blending sanity.
    dense_normalized = {c.record.record_id: max(0.0, c.score) for c in candidates}

    hits: list[HybridHit] = []
    for c in candidates:
        rid = c.record.record_id
        ds = dense_normalized.get(rid, 0.0)
        ss = norm_sparse.get(rid, 0.0)
        hits.append(
            HybridHit(
                record_id=rid,
                text=c.record.text,
                dense_score=ds,
                sparse_score=ss,
                blended_score=dw * ds + sw * ss,
                namespace=c.record.namespace,
                metadata=dict(c.record.metadata),
            )
        )
    hits.sort(key=lambda h: h.blended_score, reverse=True)
    return hits[:top_k]


def hits_as_search_hits(hits: Sequence[HybridHit]) -> list[SearchHit]:
    """Convert hybrid hits to ``SearchHit`` for downstream code that expects it."""
    out: list[SearchHit] = []
    for h in hits:
        out.append(
            SearchHit(
                record=VectorRecord(
                    record_id=h.record_id,
                    text=h.text,
                    vector=(),
                    metadata=h.metadata,
                    tenant_id="",
                    namespace=h.namespace,
                ),
                score=h.blended_score,
            )
        )
    return out


__all__ = [
    "HybridHit",
    "hits_as_search_hits",
    "hybrid_search",
]
