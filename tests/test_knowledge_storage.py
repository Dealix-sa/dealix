"""Knowledge and Research OS durable-storage regression tests."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from api.routers import ops_knowledge, ops_research
from intelligence.bilingual import BilingualRenderer
from intelligence.deep_research import DeepResearchEngine, ResearchSource
from intelligence.knowledge_accumulator import KnowledgeAccumulator, KnowledgeEntry
from intelligence.knowledge_storage import (
    FileKnowledgeStorage,
    KnowledgeStorageUnavailable,
    PostgresKnowledgeStorage,
    UnavailableKnowledgeStorage,
    get_knowledge_storage,
)


def _entry(
    entry_id: str,
    *,
    expires_at: str | None = None,
    source: str = "verified-test-source",
) -> KnowledgeEntry:
    return KnowledgeEntry(
        entry_id=entry_id,
        category="market_signal",
        title=BilingualRenderer.bt("Fintech signal", "إشارة التقنية المالية"),
        content=BilingualRenderer.bt("Verified market data", "بيانات سوق موثقة"),
        source=source,
        sector="fintech",
        company="Example Company",
        tags=["verified", "test"],
        confidence=0.91,
        created_at=datetime.now(UTC).isoformat(),
        expires_at=expires_at,
    )


def test_file_adapter_is_lazy_and_preserves_governance_fields(
    tmp_path: Path,
) -> None:
    store_path = tmp_path / "knowledge" / "entries.json"
    accumulator = KnowledgeAccumulator(
        storage=FileKnowledgeStorage(store_path),
    )

    assert not store_path.parent.exists()
    assert accumulator.storage_readiness()["status"] == "ready"
    assert not store_path.parent.exists()

    accumulator.ingest(_entry("knowledge-1"))

    stored = accumulator.get("knowledge-1")
    assert stored is not None
    assert store_path.exists()
    assert stored.source == "verified-test-source"
    assert stored.confidence == 0.91
    assert stored.title.ar == "إشارة التقنية المالية"
    assert stored.content.en == "Verified market data"
    assert stored.expires_at is None


def test_postgres_adapter_persists_batch_redaction_and_expiry() -> None:
    engine = create_engine("sqlite:///:memory:", future=True)
    first = KnowledgeAccumulator(
        storage=PostgresKnowledgeStorage(engine=engine, create_tables=True)
    )
    expired_at = (datetime.now(UTC) - timedelta(minutes=1)).isoformat()

    assert (
        first.ingest_batch(
            [
                _entry("active"),
                _entry("expired", expires_at=expired_at),
            ]
        )
        == 2
    )

    second = KnowledgeAccumulator(
        storage=PostgresKnowledgeStorage(engine=engine, create_tables=False)
    )
    assert second.redact("active", ["title", "source"]) is True
    redacted = second.get("active")
    assert redacted is not None
    assert redacted.title.en == "[redacted]"
    assert redacted.title.ar == "[محذوف]"
    assert redacted.source == "[redacted]"
    assert second.purge_expired() == 1
    assert second.get("expired") is None
    assert second.stats()["total_entries"] == 1


def test_production_rejects_file_and_ephemeral_storage() -> None:
    storage = get_knowledge_storage(
        environment="production",
        backend="file",
        file_store_path="/tmp/knowledge-os.json",
    )

    assert storage.readiness() == {
        "status": "degraded",
        "backend": "unavailable",
        "durable": False,
        "write_ready": False,
        "reason": "production_requires_postgres",
    }


def test_missing_migration_degrades_and_mutations_fail_closed() -> None:
    engine = create_engine("sqlite:///:memory:", future=True)
    storage = PostgresKnowledgeStorage(engine=engine, create_tables=False)

    assert storage.readiness()["status"] == "degraded"
    try:
        storage.mutate(lambda rows: rows.append({}))
    except KnowledgeStorageUnavailable:
        pass
    else:
        raise AssertionError("mutation must fail closed when the table is unavailable")


def test_router_readiness_survives_and_writes_return_sanitized_503(
    monkeypatch,
) -> None:
    unavailable = UnavailableKnowledgeStorage("test_database_unavailable")
    accumulator = KnowledgeAccumulator(storage=unavailable)
    monkeypatch.setattr(ops_knowledge, "_accumulator", accumulator)
    monkeypatch.setattr(
        ops_research,
        "_engine",
        DeepResearchEngine(knowledge=accumulator),
    )

    app = FastAPI()
    app.include_router(ops_knowledge.router)
    app.include_router(ops_research.router)
    client = TestClient(app, raise_server_exceptions=False)

    route_paths = {route.path for route in app.routes}
    assert "/api/v1/ops/knowledge/readiness" in route_paths
    assert "/api/v1/ops/research/readiness" in route_paths

    readiness = client.get("/api/v1/ops/knowledge/readiness")
    assert readiness.status_code == 200
    assert readiness.json()["reason"] == "test_database_unavailable"

    ingest = client.post(
        "/api/v1/ops/knowledge/ingest",
        json={
            "category": "market_signal",
            "title_en": "Signal",
            "title_ar": "إشارة",
            "content_en": "Verified data",
            "content_ar": "بيانات موثقة",
            "source": "test",
        },
    )
    assert ingest.status_code == 503
    assert ingest.json()["detail"]["code"] == "knowledge_storage_unavailable"

    research = client.post(
        "/api/v1/ops/research/query",
        json={
            "query": "Saudi fintech",
            "sources": ["market_signals"],
        },
    )
    assert research.status_code == 503
    assert research.json()["detail"]["code"] == "knowledge_storage_unavailable"


def test_research_uses_one_injected_accumulator_and_persists_atomically(
    tmp_path: Path,
) -> None:
    accumulator = KnowledgeAccumulator(store_path=tmp_path / "knowledge.json")
    engine = DeepResearchEngine(knowledge=accumulator)

    bundle = engine.research(
        "Saudi fintech",
        sources=[ResearchSource.MARKET_SIGNALS],
        sector="fintech",
    )

    assert bundle.findings
    stored = accumulator.search("fintech")
    assert len(stored) == len(bundle.findings)
    assert all(entry.category == "research_finding" for entry in stored)
    assert all(entry.source == "market_signals" for entry in stored)
