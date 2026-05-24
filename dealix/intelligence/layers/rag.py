"""
RAG engine — chunk → embed → retrieve → pack with citations.
محرّك استرجاع وتوليد — تقطيع وتضمين واسترجاع مع استشهادات.

End-to-end pipeline that ties the embeddings, vector_store, chunker, and
optional LLM gateway layers together. Returns a citation-rich payload
that callers can hand to a generator (or just display as a search result).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Sequence

from dealix.intelligence.layers.chunker import SmartChunker
from dealix.intelligence.layers.embeddings import EmbeddingModel
from dealix.intelligence.layers.vector_store import VectorRecord, VectorStore


@dataclass(frozen=True)
class Citation:
    document_id: str
    chunk_id: str
    chunk_index: int
    score: float
    snippet: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RAGResult:
    query: str
    citations: tuple[Citation, ...]
    context: str
    prompt: str
    documents_searched: int
    backend: str


@dataclass(frozen=True)
class IngestReport:
    document_id: str
    chunks_indexed: int
    total_chars: int
    skipped: bool
    reason: str = ""


PROMPT_TEMPLATE = (
    "أجب باعتمادك حصراً على المقاطع المُرفقة. إن لم تجد إجابة قل: لا أعلم.\n"
    "Use only the provided context. If unanswered, reply: I don't know.\n\n"
    "السياق / Context:\n{context}\n\n"
    "السؤال / Question: {query}\n\nالإجابة / Answer:"
)


class RAGEngine:
    """End-to-end RAG over the in-memory VectorStore."""

    def __init__(
        self,
        *,
        store: VectorStore | None = None,
        chunker: SmartChunker | None = None,
        embedder: EmbeddingModel | None = None,
        snippet_chars: int = 320,
    ) -> None:
        self._embedder = embedder or EmbeddingModel()
        self._store = store or VectorStore(embedder=self._embedder)
        self._chunker = chunker or SmartChunker()
        self.snippet_chars = snippet_chars

    # ── Ingest ────────────────────────────────────────────────────
    def ingest(
        self,
        document_id: str,
        text: str,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> IngestReport:
        if not document_id:
            raise ValueError("document_id required")
        if not text or not text.strip():
            return IngestReport(document_id, 0, 0, True, "empty_text")
        chunks = self._chunker.chunk(text, metadata=metadata)
        if not chunks:
            return IngestReport(document_id, 0, 0, True, "no_chunks")
        items = []
        for c in chunks:
            chunk_id = f"{document_id}#{c.index}"
            meta = {
                "document_id": document_id,
                "chunk_index": c.index,
                "start_char": c.start_char,
                "end_char": c.end_char,
                **(metadata or {}),
            }
            items.append((chunk_id, c.text, meta))
        self._store.upsert_many(items)
        return IngestReport(
            document_id=document_id,
            chunks_indexed=len(items),
            total_chars=sum(len(c.text) for c in chunks),
            skipped=False,
        )

    def ingest_many(
        self,
        docs: Iterable[tuple[str, str, dict[str, Any] | None]],
    ) -> list[IngestReport]:
        return [self.ingest(did, text, metadata=meta) for did, text, meta in docs]

    def remove_document(self, document_id: str) -> int:
        ids = [
            rid for rid in list(self._store._records.keys())  # type: ignore[attr-defined]
            if rid.split("#", 1)[0] == document_id
        ]
        for rid in ids:
            self._store.delete(rid)
        return len(ids)

    # ── Retrieve ──────────────────────────────────────────────────
    def retrieve(
        self,
        query: str,
        *,
        top_k: int = 4,
        min_score: float = 0.05,
        metadata_filter: dict[str, Any] | None = None,
    ) -> list[Citation]:
        hits = self._store.search(
            query, top_k=top_k, min_score=min_score, metadata_filter=metadata_filter
        )
        return [self._to_citation(rec, score) for rec, score in hits]

    # ── Ask (build prompt) ────────────────────────────────────────
    def ask(
        self,
        query: str,
        *,
        top_k: int = 4,
        min_score: float = 0.05,
        metadata_filter: dict[str, Any] | None = None,
    ) -> RAGResult:
        citations = self.retrieve(
            query, top_k=top_k, min_score=min_score, metadata_filter=metadata_filter
        )
        context = self._format_context(citations)
        prompt = PROMPT_TEMPLATE.format(context=context, query=query)
        return RAGResult(
            query=query,
            citations=tuple(citations),
            context=context,
            prompt=prompt,
            documents_searched=self._store.size,
            backend=self._store.backend,
        )

    # ── Stats / store passthrough ─────────────────────────────────
    def stats(self) -> dict[str, Any]:
        return {
            "store": self._store.stats(),
            "chunker": {
                "max_chars": self._chunker.max_chars,
                "overlap": self._chunker.overlap_chars,
            },
        }

    # ── Internals ─────────────────────────────────────────────────
    def _to_citation(self, record: VectorRecord, score: float) -> Citation:
        meta = dict(record.metadata or {})
        document_id = meta.get("document_id", record.id.split("#", 1)[0])
        chunk_index = int(meta.get("chunk_index", 0))
        snippet = record.text
        if len(snippet) > self.snippet_chars:
            snippet = snippet[: self.snippet_chars].rstrip() + "…"
        return Citation(
            document_id=document_id,
            chunk_id=record.id,
            chunk_index=chunk_index,
            score=round(score, 4),
            snippet=snippet,
            metadata=meta,
        )

    def _format_context(self, citations: Sequence[Citation]) -> str:
        lines: list[str] = []
        for i, c in enumerate(citations, 1):
            lines.append(f"[{i}] (doc={c.document_id} chunk={c.chunk_index} score={c.score})")
            lines.append(c.snippet)
            lines.append("")
        return "\n".join(lines).strip()
