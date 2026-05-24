"""RAG pipeline — embed → retrieve → re-rank → assemble context window.

The pipeline is the L3 (Intelligence) glue layer for the AI Stack. It takes
a customer query plus optional source documents, indexes them in the
vector store, retrieves the top-k relevant passages for the query, and
assembles a bounded context window that downstream agents (L5) can feed to
the model router (L4).

The pipeline is intentionally provider-agnostic and never calls an LLM
itself — that is the job of the agents. Everything here is pure
deterministic glue: embedding, retrieval, re-ranking, and concatenation.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from auto_client_acquisition.intelligence_os.embedder import (
    Embedder,
    chunk_text,
    embed_chunks,
)
from auto_client_acquisition.intelligence_os.semantic_search import (
    HybridHit,
    hybrid_search,
)
from auto_client_acquisition.intelligence_os.vector_store import InMemoryVectorStore


@dataclass(slots=True)
class RetrievedContext:
    """Final assembled context window for a single RAG query."""

    query: str
    tenant_id: str
    namespace: str
    hits: list[HybridHit] = field(default_factory=list)
    context_text: str = ""
    used_chars: int = 0
    truncated: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "tenant_id": self.tenant_id,
            "namespace": self.namespace,
            "hits": [h.to_dict() for h in self.hits],
            "context_text": self.context_text,
            "used_chars": self.used_chars,
            "truncated": self.truncated,
            "metadata": dict(self.metadata),
        }


def _assemble_context(
    hits: Sequence[HybridHit],
    *,
    max_chars: int,
    separator: str,
) -> tuple[str, int, bool]:
    """Pack hits into a bounded context window, preserving order by relevance.

    Strict cap: the returned ``used_chars`` is always ``<= max_chars`` even
    when the last hit must be truncated mid-sentence.
    """
    if max_chars <= 0:
        return "", 0, False
    parts: list[str] = []
    used = 0
    truncated = False
    sep_len = len(separator)
    for h in hits:
        fragment = h.text.strip()
        if not fragment:
            continue
        cost = len(fragment) + (sep_len if parts else 0)
        if used + cost > max_chars:
            # Tail-fit budget: account for the separator and a trailing ellipsis.
            ellipsis = "…"
            sep_cost = sep_len if parts else 0
            remaining = max_chars - used - sep_cost - len(ellipsis)
            if remaining > 50:
                fragment = fragment[:remaining].rstrip() + ellipsis
                parts.append(fragment)
                used += len(fragment) + sep_cost
            truncated = True
            break
        parts.append(fragment)
        used += cost
    return separator.join(parts), used, truncated


class RAGPipeline:
    """Embed → retrieve → re-rank → context window assembler.

    Usage:

        pipe = RAGPipeline(embedder=Embedder(dimension=256), store=...)
        pipe.index_documents(
            tenant_id="acme",
            documents=[{"id": "d1", "text": "..."}, ...],
        )
        ctx = pipe.retrieve(
            tenant_id="acme",
            query="how does Dealix score leads?",
            top_k=4,
        )
    """

    __slots__ = ("chunk_chars", "default_namespace", "embedder", "overlap", "store")

    def __init__(
        self,
        *,
        embedder: Embedder,
        store: InMemoryVectorStore,
        default_namespace: str = "default",
        chunk_chars: int = 800,
        overlap: int = 100,
    ) -> None:
        if embedder.dimension != store.dimension:
            raise ValueError(
                "embedder and store dimensions must match "
                f"(embedder={embedder.dimension}, store={store.dimension})"
            )
        self.embedder = embedder
        self.store = store
        self.default_namespace = default_namespace
        self.chunk_chars = chunk_chars
        self.overlap = overlap

    def index_documents(
        self,
        *,
        tenant_id: str,
        documents: Sequence[Mapping[str, Any]],
        namespace: str | None = None,
    ) -> int:
        """Chunk + embed + upsert documents into the vector store.

        Each document must have ``id`` and ``text``. Optional ``metadata``
        is propagated to every chunk. Returns the number of chunks indexed.
        """
        ns = namespace or self.default_namespace
        total_chunks = 0
        for doc in documents:
            doc_id = str(doc["id"])
            text = str(doc.get("text") or "")
            metadata = dict(doc.get("metadata") or {})
            chunks = chunk_text(text, chunk_chars=self.chunk_chars, overlap=self.overlap)
            if not chunks:
                continue
            embeddings = embed_chunks(self.embedder, chunks)
            for idx, emb in enumerate(embeddings):
                record_id = f"{doc_id}#chunk-{idx}"
                self.store.upsert(
                    record_id=record_id,
                    text=emb.text,
                    vector=emb.vector,
                    tenant_id=tenant_id,
                    namespace=ns,
                    metadata={**metadata, "doc_id": doc_id, "chunk_idx": idx},
                )
                total_chunks += 1
        return total_chunks

    def retrieve(
        self,
        *,
        tenant_id: str,
        query: str,
        namespace: str | None = None,
        top_k: int = 4,
        max_context_chars: int = 2500,
        dense_weight: float = 0.7,
        sparse_weight: float = 0.3,
        metadata_filter: Mapping[str, Any] | None = None,
        separator: str = "\n\n---\n\n",
    ) -> RetrievedContext:
        """Run hybrid retrieval and assemble a bounded context window."""
        if not query or not query.strip():
            return RetrievedContext(
                query=query,
                tenant_id=tenant_id,
                namespace=namespace or self.default_namespace,
            )
        ns = namespace or self.default_namespace
        hits = hybrid_search(
            embedder=self.embedder,
            store=self.store,
            query=query,
            tenant_id=tenant_id,
            namespace=ns,
            top_k=top_k,
            dense_weight=dense_weight,
            sparse_weight=sparse_weight,
            metadata_filter=metadata_filter,
        )
        context, used, truncated = _assemble_context(
            hits,
            max_chars=max_context_chars,
            separator=separator,
        )
        return RetrievedContext(
            query=query,
            tenant_id=tenant_id,
            namespace=ns,
            hits=list(hits),
            context_text=context,
            used_chars=used,
            truncated=truncated,
            metadata={
                "top_k": top_k,
                "max_context_chars": max_context_chars,
                "dense_weight": dense_weight,
                "sparse_weight": sparse_weight,
                "embedder_provider": self.embedder.provider_name,
                "embedder_model": self.embedder.model,
            },
        )

    def clear_tenant(self, *, tenant_id: str) -> int:
        return self.store.clear(tenant_id=tenant_id)


__all__ = [
    "RAGPipeline",
    "RetrievedContext",
]
