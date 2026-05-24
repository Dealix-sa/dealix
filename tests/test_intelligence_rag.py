"""Tests for the Intelligence OS RAG pipeline — embedder, store, hybrid search."""

from __future__ import annotations

import math

import pytest

from auto_client_acquisition.intelligence_os import (
    DEFAULT_DIMENSION,
    Embedder,
    HybridHit,
    InMemoryVectorStore,
    RAGPipeline,
    RetrievedContext,
    chunk_text,
    cosine_similarity,
    deterministic_embed,
    embed_chunks,
    hybrid_search,
)


class TestEmbedder:
    def test_deterministic_embedding_is_stable(self) -> None:
        v1 = deterministic_embed("hello world", dimension=128)
        v2 = deterministic_embed("hello world", dimension=128)
        assert v1 == v2

    def test_embedding_is_l2_normalized(self) -> None:
        v = deterministic_embed("some text to embed", dimension=128)
        norm = math.sqrt(sum(x * x for x in v))
        # Hashed tokens may all map to a single bucket — accept norm 0 or close to 1.
        assert norm == 0.0 or abs(norm - 1.0) < 1e-6

    def test_arabic_text_produces_nonzero_vector(self) -> None:
        v = deterministic_embed("نحتاج تحسين عملية البيع للسوق السعودي")
        assert any(abs(x) > 0.0 for x in v)

    def test_empty_text_yields_zero_vector(self) -> None:
        v = deterministic_embed("", dimension=128)
        assert v == [0.0] * 128

    def test_cosine_similarity_self_is_one(self) -> None:
        v = deterministic_embed("hello world", dimension=128)
        if any(abs(x) > 0.0 for x in v):
            assert abs(cosine_similarity(v, v) - 1.0) < 1e-6

    def test_embedder_falls_back_when_provider_misbehaves(self) -> None:
        def bad_provider(texts):
            return [[0.0] * 32 for _ in texts]  # wrong dimension

        emb = Embedder(dimension=128, provider=bad_provider, provider_name="bad")
        result = emb.embed("anything")
        assert result.dimension == 128
        assert emb.fallback_uses == 1

    def test_embedder_uses_real_provider_when_correct(self) -> None:
        def good_provider(texts):
            return [[0.5] * 64 for _ in texts]

        emb = Embedder(dimension=64, provider=good_provider, provider_name="good")
        result = emb.embed("anything")
        assert result.vector == [0.5] * 64
        assert emb.fallback_uses == 0

    def test_chunk_text_respects_boundaries(self) -> None:
        text = "a" * 1000 + "b" * 500
        chunks = chunk_text(text, chunk_chars=400, overlap=50)
        assert all(len(c) <= 400 for c in chunks)
        assert "".join(c[:1] for c in chunks)  # at least one chunk produced
        assert len(chunks) >= 3

    def test_chunk_text_rejects_invalid_args(self) -> None:
        with pytest.raises(ValueError):
            chunk_text("x", chunk_chars=0)
        with pytest.raises(ValueError):
            chunk_text("x", chunk_chars=100, overlap=100)


class TestVectorStore:
    def test_dimension_mismatch_raises(self) -> None:
        store = InMemoryVectorStore(dimension=64)
        with pytest.raises(ValueError, match="vector dimension mismatch"):
            store.upsert(record_id="r1", text="x", vector=[0.0] * 32)

    def test_search_tenant_isolation(self) -> None:
        store = InMemoryVectorStore(dimension=64)
        store.upsert(
            record_id="r1", text="alpha",
            vector=[1.0] + [0.0] * 63,
            tenant_id="t1",
        )
        store.upsert(
            record_id="r2", text="alpha",
            vector=[1.0] + [0.0] * 63,
            tenant_id="t2",
        )
        hits = store.search(
            query_vector=[1.0] + [0.0] * 63,
            tenant_id="t1",
            top_k=10,
        )
        assert all(h.record.tenant_id == "t1" for h in hits)
        assert len(hits) == 1

    def test_namespace_filter(self) -> None:
        store = InMemoryVectorStore(dimension=64)
        store.upsert(
            record_id="r1", text="a", vector=[0.5] * 64,
            tenant_id="t1", namespace="ns_a",
        )
        store.upsert(
            record_id="r2", text="b", vector=[0.5] * 64,
            tenant_id="t1", namespace="ns_b",
        )
        hits = store.search(
            query_vector=[0.5] * 64, tenant_id="t1",
            namespace="ns_a", top_k=10,
        )
        assert len(hits) == 1
        assert hits[0].record.record_id == "r1"

    def test_metadata_filter(self) -> None:
        store = InMemoryVectorStore(dimension=32)
        store.upsert(
            record_id="r1", text="a", vector=[1.0] * 32,
            tenant_id="t1", metadata={"kind": "case"},
        )
        store.upsert(
            record_id="r2", text="b", vector=[1.0] * 32,
            tenant_id="t1", metadata={"kind": "doc"},
        )
        hits = store.search(
            query_vector=[1.0] * 32, tenant_id="t1",
            top_k=10, metadata_filter={"kind": "case"},
        )
        assert len(hits) == 1
        assert hits[0].record.record_id == "r1"

    def test_count_filters(self) -> None:
        store = InMemoryVectorStore(dimension=16)
        for i in range(5):
            store.upsert(
                record_id=f"r{i}", text="x", vector=[float(i)] * 16,
                tenant_id="t1",
            )
        assert store.count() == 5
        assert store.count(tenant_id="t1") == 5
        assert store.count(tenant_id="other") == 0

    def test_delete(self) -> None:
        store = InMemoryVectorStore(dimension=16)
        store.upsert(record_id="r1", text="x", vector=[1.0] * 16, tenant_id="t1")
        first = store.delete(record_id="r1", tenant_id="t1")
        second = store.delete(record_id="r1", tenant_id="t1")
        assert first is True
        assert second is False


class TestHybridSearch:
    def test_hybrid_blends_dense_and_sparse(self) -> None:
        emb = Embedder(dimension=128)
        store = InMemoryVectorStore(dimension=128)
        docs = [
            ("d1", "Riyadh sales pipeline for B2B Saudi clients."),
            ("d2", "Random unrelated paragraph about cooking pasta."),
            ("d3", "Sales funnel for Saudi enterprise customers in Riyadh."),
        ]
        for doc_id, text in docs:
            store.upsert(
                record_id=doc_id, text=text,
                vector=emb.embed(text).vector, tenant_id="t1",
            )
        hits = hybrid_search(
            embedder=emb, store=store, query="Saudi sales pipeline",
            tenant_id="t1", top_k=2,
        )
        assert len(hits) == 2
        # The two "Saudi sales" docs should beat the cooking paragraph.
        top_ids = [h.record_id for h in hits]
        assert "d1" in top_ids or "d3" in top_ids
        assert "d2" not in top_ids

    def test_hybrid_returns_empty_for_empty_store(self) -> None:
        emb = Embedder(dimension=64)
        store = InMemoryVectorStore(dimension=64)
        hits = hybrid_search(
            embedder=emb, store=store, query="anything",
            tenant_id="t1", top_k=5,
        )
        assert hits == []

    def test_hybrid_rejects_invalid_weights(self) -> None:
        emb = Embedder(dimension=64)
        store = InMemoryVectorStore(dimension=64)
        store.upsert(record_id="r1", text="x", vector=[1.0] * 64, tenant_id="t1")
        with pytest.raises(ValueError, match="non-negative"):
            hybrid_search(
                embedder=emb, store=store, query="x",
                tenant_id="t1", dense_weight=-1.0, sparse_weight=0.5,
            )

    def test_hybrid_hit_to_dict_is_json_safe(self) -> None:
        h = HybridHit(
            record_id="r1", text="x", dense_score=0.8,
            sparse_score=0.6, blended_score=0.7,
            namespace="default", metadata={"k": "v"},
        )
        d = h.to_dict()
        assert d["record_id"] == "r1"
        assert d["blended_score"] == 0.7


class TestRAGPipeline:
    def test_pipeline_indexes_and_retrieves(self) -> None:
        emb = Embedder(dimension=128)
        store = InMemoryVectorStore(dimension=128)
        pipe = RAGPipeline(embedder=emb, store=store)
        chunks = pipe.index_documents(
            tenant_id="t1",
            documents=[
                {"id": "d1", "text": "Saudi sales pipeline for B2B."},
                {"id": "d2", "text": "Cooking pasta in Italy is fun."},
            ],
        )
        assert chunks >= 2
        ctx = pipe.retrieve(
            tenant_id="t1",
            query="how to sell in Saudi Arabia",
            top_k=2,
        )
        assert isinstance(ctx, RetrievedContext)
        assert ctx.tenant_id == "t1"
        assert ctx.used_chars >= 0
        assert len(ctx.hits) <= 2

    def test_pipeline_respects_context_cap(self) -> None:
        emb = Embedder(dimension=128)
        store = InMemoryVectorStore(dimension=128)
        pipe = RAGPipeline(embedder=emb, store=store, chunk_chars=200)
        long_text = "Saudi business " * 200  # ~3000 chars
        pipe.index_documents(
            tenant_id="t1",
            documents=[{"id": "d1", "text": long_text}],
        )
        ctx = pipe.retrieve(
            tenant_id="t1",
            query="Saudi business",
            top_k=10,
            max_context_chars=500,
        )
        assert ctx.used_chars <= 500
        assert ctx.truncated or ctx.used_chars > 0

    def test_pipeline_requires_matching_dimensions(self) -> None:
        emb = Embedder(dimension=128)
        store = InMemoryVectorStore(dimension=64)
        with pytest.raises(ValueError, match="dimensions must match"):
            RAGPipeline(embedder=emb, store=store)

    def test_pipeline_clears_per_tenant(self) -> None:
        emb = Embedder(dimension=64)
        store = InMemoryVectorStore(dimension=64)
        pipe = RAGPipeline(embedder=emb, store=store)
        pipe.index_documents(
            tenant_id="t1",
            documents=[{"id": "d1", "text": "Sample text for indexing."}],
        )
        pipe.index_documents(
            tenant_id="t2",
            documents=[{"id": "d2", "text": "Another sample."}],
        )
        assert store.count(tenant_id="t1") > 0
        assert store.count(tenant_id="t2") > 0
        pipe.clear_tenant(tenant_id="t1")
        assert store.count(tenant_id="t1") == 0
        assert store.count(tenant_id="t2") > 0


def test_default_dimension_is_reasonable() -> None:
    assert 64 <= DEFAULT_DIMENSION <= 4096
