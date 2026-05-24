"""Vector store — in-memory by default, pgvector-ready by interface.

The store keeps a single collection of (id, vector, text, metadata) rows
indexed in memory. It is intentionally small — the production deployment
swaps the implementation for a pgvector-backed adapter that mirrors the
exact same surface (``upsert`` / ``search`` / ``delete`` / ``count``).

Search uses pure-Python cosine similarity over the registered vectors. For
modest corpora (< 50k rows, dimension <= 1536) this runs comfortably in
sub-50ms and is good enough for the AI Stack's free-tier demo.
"""

from __future__ import annotations

import threading
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from typing import Any

from auto_client_acquisition.intelligence_os.embedder import cosine_similarity


@dataclass(frozen=True, slots=True)
class VectorRecord:
    """A single row in the vector store."""

    record_id: str
    text: str
    vector: tuple[float, ...]
    metadata: Mapping[str, Any] = field(default_factory=dict)
    tenant_id: str = ""
    namespace: str = "default"


@dataclass(frozen=True, slots=True)
class SearchHit:
    """One scored search result."""

    record: VectorRecord
    score: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_id": self.record.record_id,
            "text": self.record.text,
            "score": self.score,
            "metadata": dict(self.record.metadata),
            "namespace": self.record.namespace,
        }


class InMemoryVectorStore:
    """Thread-safe in-memory vector store with cosine similarity search.

    Identity is keyed by ``(tenant_id, namespace, record_id)`` so two
    tenants can use the same record_id without collision.
    """

    __slots__ = ("_dimension", "_lock", "_rows")

    def __init__(self, *, dimension: int) -> None:
        if dimension <= 0:
            raise ValueError("dimension must be positive")
        self._dimension = dimension
        self._rows: dict[tuple[str, str, str], VectorRecord] = {}
        self._lock = threading.RLock()

    @property
    def dimension(self) -> int:
        return self._dimension

    def count(self, *, tenant_id: str | None = None, namespace: str | None = None) -> int:
        with self._lock:
            rows = self._rows.values()
            if tenant_id is not None:
                rows = [r for r in rows if r.tenant_id == tenant_id]
            if namespace is not None:
                rows = [r for r in rows if r.namespace == namespace]
            return sum(1 for _ in rows)

    def upsert(
        self,
        *,
        record_id: str,
        text: str,
        vector: Iterable[float],
        tenant_id: str = "",
        namespace: str = "default",
        metadata: Mapping[str, Any] | None = None,
    ) -> VectorRecord:
        if not record_id or not record_id.strip():
            raise ValueError("record_id is required")
        vec = tuple(float(v) for v in vector)
        if len(vec) != self._dimension:
            raise ValueError(
                f"vector dimension mismatch: got {len(vec)}, expected {self._dimension}"
            )
        record = VectorRecord(
            record_id=record_id.strip(),
            text=text,
            vector=vec,
            metadata=dict(metadata or {}),
            tenant_id=(tenant_id or "").strip(),
            namespace=namespace or "default",
        )
        with self._lock:
            self._rows[(record.tenant_id, record.namespace, record.record_id)] = record
        return record

    def upsert_many(self, records: Iterable[Mapping[str, Any]]) -> int:
        count = 0
        for r in records:
            self.upsert(
                record_id=str(r["record_id"]),
                text=str(r.get("text", "")),
                vector=r["vector"],
                tenant_id=str(r.get("tenant_id", "")),
                namespace=str(r.get("namespace", "default")),
                metadata=r.get("metadata") or {},
            )
            count += 1
        return count

    def delete(
        self,
        *,
        record_id: str,
        tenant_id: str = "",
        namespace: str = "default",
    ) -> bool:
        key = (tenant_id, namespace, record_id)
        with self._lock:
            return self._rows.pop(key, None) is not None

    def get(
        self,
        *,
        record_id: str,
        tenant_id: str = "",
        namespace: str = "default",
    ) -> VectorRecord | None:
        with self._lock:
            return self._rows.get((tenant_id, namespace, record_id))

    def search(
        self,
        *,
        query_vector: Iterable[float],
        tenant_id: str = "",
        namespace: str | None = None,
        top_k: int = 5,
        min_score: float = 0.0,
        metadata_filter: Mapping[str, Any] | None = None,
    ) -> list[SearchHit]:
        if top_k <= 0:
            return []
        qvec = tuple(float(v) for v in query_vector)
        if len(qvec) != self._dimension:
            raise ValueError(
                f"query dimension mismatch: got {len(qvec)}, expected {self._dimension}"
            )
        with self._lock:
            candidates = [
                r
                for r in self._rows.values()
                if r.tenant_id == tenant_id
                and (namespace is None or r.namespace == namespace)
            ]
        if metadata_filter:
            candidates = [
                r
                for r in candidates
                if all(r.metadata.get(k) == v for k, v in metadata_filter.items())
            ]
        scored = [
            SearchHit(record=r, score=cosine_similarity(qvec, r.vector))
            for r in candidates
        ]
        scored = [h for h in scored if h.score >= min_score]
        scored.sort(key=lambda h: h.score, reverse=True)
        return scored[:top_k]

    def clear(self, *, tenant_id: str | None = None) -> int:
        with self._lock:
            if tenant_id is None:
                count = len(self._rows)
                self._rows.clear()
                return count
            keys = [k for k in self._rows if k[0] == tenant_id]
            for k in keys:
                self._rows.pop(k, None)
            return len(keys)


# Module-level singleton for convenience — production wires its own.
_DEFAULT_STORE: InMemoryVectorStore | None = None
_default_lock = threading.Lock()


def get_default_store(*, dimension: int = 256) -> InMemoryVectorStore:
    """Lazy module-level vector store. Tests can call :func:`reset_default_store`."""
    global _DEFAULT_STORE
    with _default_lock:
        if _DEFAULT_STORE is None or _DEFAULT_STORE.dimension != dimension:
            _DEFAULT_STORE = InMemoryVectorStore(dimension=dimension)
        return _DEFAULT_STORE


def reset_default_store() -> None:
    global _DEFAULT_STORE
    with _default_lock:
        _DEFAULT_STORE = None


__all__ = [
    "InMemoryVectorStore",
    "SearchHit",
    "VectorRecord",
    "get_default_store",
    "reset_default_store",
]
