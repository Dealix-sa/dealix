"""
Vector store — in-memory cosine-similarity index with optional JSON persistence.
متجر متجهات — فهرس تشابه كوساين في الذاكرة مع حفظ JSON اختياري.

Designed to be a drop-in tier for RAG / recommender / clustering layers
without requiring Postgres+pgvector or external vector DBs. Persists to
disk only when ``persist_path`` is set so unit tests remain hermetic.
"""

from __future__ import annotations

import heapq
import json
import math
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Sequence

from dealix.intelligence.layers.embeddings import EmbeddingModel, cosine_similarity


@dataclass
class VectorRecord:
    id: str
    text: str
    vector: tuple[float, ...]
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "text": self.text,
            "vector": list(self.vector),
            "metadata": self.metadata,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "VectorRecord":
        return cls(
            id=str(payload["id"]),
            text=str(payload.get("text", "")),
            vector=tuple(float(x) for x in payload.get("vector", [])),
            metadata=dict(payload.get("metadata", {})),
            created_at=float(payload.get("created_at", time.time())),
        )


class VectorStore:
    """Thread-safe in-memory vector store with cosine ranking."""

    def __init__(
        self,
        *,
        embedder: EmbeddingModel | None = None,
        persist_path: str | Path | None = None,
    ) -> None:
        self._embedder = embedder or EmbeddingModel()
        self._records: dict[str, VectorRecord] = {}
        self._lock = threading.RLock()
        self._persist_path = Path(persist_path) if persist_path else None
        if self._persist_path and self._persist_path.exists():
            self._load_from_disk()

    # ── Properties ────────────────────────────────────────────────
    @property
    def size(self) -> int:
        return len(self._records)

    @property
    def dim(self) -> int:
        return self._embedder.dim

    @property
    def backend(self) -> str:
        return self._embedder.backend

    # ── CRUD ──────────────────────────────────────────────────────
    def upsert(
        self,
        record_id: str,
        text: str,
        metadata: dict[str, Any] | None = None,
        *,
        vector: Sequence[float] | None = None,
    ) -> VectorRecord:
        if not record_id:
            raise ValueError("record_id required")
        vec = tuple(vector) if vector is not None else self._embedder.embed(text).vector
        record = VectorRecord(
            id=record_id,
            text=text,
            vector=vec,
            metadata=metadata or {},
        )
        with self._lock:
            self._records[record_id] = record
            self._persist()
        return record

    def upsert_many(self, items: Iterable[tuple[str, str, dict[str, Any] | None]]) -> int:
        count = 0
        with self._lock:
            for rid, text, meta in items:
                vec = self._embedder.embed(text).vector
                self._records[rid] = VectorRecord(
                    id=rid, text=text, vector=vec, metadata=meta or {}
                )
                count += 1
            self._persist()
        return count

    def delete(self, record_id: str) -> bool:
        with self._lock:
            existed = record_id in self._records
            self._records.pop(record_id, None)
            if existed:
                self._persist()
        return existed

    def get(self, record_id: str) -> VectorRecord | None:
        return self._records.get(record_id)

    def clear(self) -> None:
        with self._lock:
            self._records.clear()
            self._persist()

    # ── Search ────────────────────────────────────────────────────
    def search(
        self,
        query: str,
        *,
        top_k: int = 5,
        min_score: float = 0.0,
        metadata_filter: dict[str, Any] | None = None,
    ) -> list[tuple[VectorRecord, float]]:
        qvec = self._embedder.embed(query).vector
        return self.search_by_vector(
            qvec, top_k=top_k, min_score=min_score, metadata_filter=metadata_filter
        )

    def search_by_vector(
        self,
        vector: Sequence[float],
        *,
        top_k: int = 5,
        min_score: float = 0.0,
        metadata_filter: dict[str, Any] | None = None,
    ) -> list[tuple[VectorRecord, float]]:
        with self._lock:
            candidates = list(self._records.values())
        if metadata_filter:
            candidates = [r for r in candidates if _match_metadata(r.metadata, metadata_filter)]
        if not candidates:
            return []
        scored: list[tuple[float, VectorRecord]] = []
        for rec in candidates:
            score = cosine_similarity(vector, rec.vector)
            if score >= min_score:
                scored.append((score, rec))
        if not scored:
            return []
        top = heapq.nlargest(max(1, top_k), scored, key=lambda x: x[0])
        return [(rec, score) for score, rec in top]

    # ── Stats ─────────────────────────────────────────────────────
    def stats(self) -> dict[str, Any]:
        with self._lock:
            sizes = [len(r.vector) for r in self._records.values()]
        return {
            "size": len(sizes),
            "dim": self._embedder.dim,
            "backend": self._embedder.backend,
            "avg_vector_dim": (sum(sizes) / len(sizes)) if sizes else 0,
            "persistent": self._persist_path is not None,
        }

    # ── Persistence ───────────────────────────────────────────────
    def _persist(self) -> None:
        if not self._persist_path:
            return
        try:
            self._persist_path.parent.mkdir(parents=True, exist_ok=True)
            payload = [rec.to_dict() for rec in self._records.values()]
            tmp = self._persist_path.with_suffix(self._persist_path.suffix + ".tmp")
            tmp.write_text(json.dumps(payload), encoding="utf-8")
            tmp.replace(self._persist_path)
        except Exception:  # pragma: no cover — best-effort durability
            pass

    def _load_from_disk(self) -> None:
        try:
            payload = json.loads(self._persist_path.read_text(encoding="utf-8"))  # type: ignore[union-attr]
            for item in payload:
                rec = VectorRecord.from_dict(item)
                self._records[rec.id] = rec
        except Exception:  # pragma: no cover
            pass


def _match_metadata(meta: dict[str, Any], flt: dict[str, Any]) -> bool:
    for k, v in flt.items():
        if meta.get(k) != v:
            return False
    return True


def cosine(a: Sequence[float], b: Sequence[float]) -> float:
    """Re-export for convenience."""
    return cosine_similarity(a, b)


def euclidean_distance(a: Sequence[float], b: Sequence[float]) -> float:
    if len(a) != len(b):
        return float("inf")
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))
