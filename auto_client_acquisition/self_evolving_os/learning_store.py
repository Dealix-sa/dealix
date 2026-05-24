"""Learning store — append-only ledger of FeedbackEvents per tenant.

The store keeps every feedback event so the decision improver can compute
per-layer / per-agent / per-model statistics over a configurable window. It
is **strictly append-only**: events are inserted but never updated or
deleted (except in tests via :func:`clear_for_test`).

In production the backend is the Postgres ``ai_learning_events`` table
created in migration ``014``. In tests and development the in-memory backend
is used; both adapters share the same surface so callers can swap without
code changes.
"""

from __future__ import annotations

import json
import os
import threading
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from auto_client_acquisition.self_evolving_os.feedback_ingestion import (
    FeedbackEvent,
    OutcomeKind,
)


@dataclass(slots=True)
class LayerOutcomeSummary:
    """Aggregate outcomes for a single layer over a window."""

    layer: str
    total: int = 0
    by_kind: dict[str, int] = field(default_factory=dict)
    doctrine_violations: int = 0
    sum_outcome_value: float = 0.0

    def success_rate(self) -> float:
        if self.total == 0:
            return 0.0
        success = (
            self.by_kind.get(OutcomeKind.SUCCESS.value, 0)
            + self.by_kind.get(OutcomeKind.CUSTOMER_CONFIRMED.value, 0)
        )
        return success / self.total

    def to_dict(self) -> dict[str, Any]:
        return {
            "layer": self.layer,
            "total": self.total,
            "by_kind": dict(self.by_kind),
            "doctrine_violations": self.doctrine_violations,
            "sum_outcome_value": self.sum_outcome_value,
            "success_rate": self.success_rate(),
        }


class InMemoryLearningStore:
    """Thread-safe in-memory append-only learning ledger.

    The store keeps events keyed by tenant_id; each tenant's events are
    stored in insertion order. Per-window queries are computed at read time.
    """

    __slots__ = ("_events", "_lock")

    def __init__(self) -> None:
        self._events: dict[str, list[FeedbackEvent]] = {}
        self._lock = threading.RLock()

    def append(self, event: FeedbackEvent) -> FeedbackEvent:
        with self._lock:
            self._events.setdefault(event.tenant_id, []).append(event)
        return event

    def append_many(self, events: Iterable[FeedbackEvent]) -> int:
        count = 0
        with self._lock:
            for ev in events:
                self._events.setdefault(ev.tenant_id, []).append(ev)
                count += 1
        return count

    def list_events(
        self,
        *,
        tenant_id: str,
        layer: str | None = None,
        agent_name: str | None = None,
        since_days: int | None = None,
        limit: int = 1000,
    ) -> list[FeedbackEvent]:
        with self._lock:
            events = list(self._events.get(tenant_id, []))
        if layer is not None:
            events = [e for e in events if e.layer == layer]
        if agent_name is not None:
            events = [e for e in events if e.agent_name == agent_name]
        if since_days is not None and since_days >= 0:
            cutoff = datetime.now(UTC) - timedelta(days=since_days)
            kept: list[FeedbackEvent] = []
            for e in events:
                try:
                    ts = datetime.fromisoformat(e.created_at)
                except (ValueError, TypeError):
                    continue
                if ts.tzinfo is None:
                    ts = ts.replace(tzinfo=UTC)
                if ts >= cutoff:
                    kept.append(e)
            events = kept
        events.sort(key=lambda e: e.created_at, reverse=True)
        return events[:limit] if limit else events

    def summarize_layer(
        self,
        *,
        tenant_id: str,
        layer: str,
        since_days: int | None = None,
    ) -> LayerOutcomeSummary:
        events = self.list_events(
            tenant_id=tenant_id,
            layer=layer,
            since_days=since_days,
            limit=10_000,
        )
        summary = LayerOutcomeSummary(layer=layer)
        for e in events:
            summary.total += 1
            summary.by_kind[e.outcome_kind] = summary.by_kind.get(e.outcome_kind, 0) + 1
            if not e.doctrine_clean:
                summary.doctrine_violations += 1
            if e.outcome_value is not None:
                summary.sum_outcome_value += float(e.outcome_value)
        return summary

    def summarize_all_layers(
        self,
        *,
        tenant_id: str,
        since_days: int | None = None,
    ) -> dict[str, LayerOutcomeSummary]:
        events = self.list_events(
            tenant_id=tenant_id,
            since_days=since_days,
            limit=100_000,
        )
        summaries: dict[str, LayerOutcomeSummary] = {}
        for e in events:
            s = summaries.setdefault(e.layer, LayerOutcomeSummary(layer=e.layer))
            s.total += 1
            s.by_kind[e.outcome_kind] = s.by_kind.get(e.outcome_kind, 0) + 1
            if not e.doctrine_clean:
                s.doctrine_violations += 1
            if e.outcome_value is not None:
                s.sum_outcome_value += float(e.outcome_value)
        return summaries

    def clear_for_test(self, *, tenant_id: str | None = None) -> None:
        with self._lock:
            if tenant_id is None:
                self._events.clear()
            else:
                self._events.pop(tenant_id, None)


# Module-level singleton with optional JSONL persistence (dev-mode).
_DEFAULT_STORE: InMemoryLearningStore | None = None
_lock = threading.Lock()


def _persistence_path() -> Path | None:
    raw = os.environ.get("DEALIX_AI_LEARNING_LEDGER_PATH")
    if not raw:
        return None
    p = Path(raw)
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _maybe_persist(event: FeedbackEvent) -> None:
    path = _persistence_path()
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")


def get_default_store() -> InMemoryLearningStore:
    global _DEFAULT_STORE
    with _lock:
        if _DEFAULT_STORE is None:
            _DEFAULT_STORE = InMemoryLearningStore()
            _hydrate_from_jsonl(_DEFAULT_STORE)
        return _DEFAULT_STORE


def reset_default_store() -> None:
    global _DEFAULT_STORE
    with _lock:
        _DEFAULT_STORE = None


def _hydrate_from_jsonl(store: InMemoryLearningStore) -> None:
    path = _persistence_path()
    if path is None or not path.exists():
        return
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                event = FeedbackEvent(
                    event_id=str(data.get("event_id", "")),
                    tenant_id=str(data.get("tenant_id", "")),
                    run_id=str(data.get("run_id", "")),
                    layer=str(data.get("layer", "")),
                    outcome_kind=str(data.get("outcome_kind", "")),
                    outcome_value=(
                        float(data["outcome_value"])
                        if data.get("outcome_value") is not None
                        else None
                    ),
                    doctrine_clean=bool(data.get("doctrine_clean", True)),
                    decision_id=data.get("decision_id"),
                    agent_name=data.get("agent_name"),
                    model_task=data.get("model_task"),
                    learnings=dict(data.get("learnings") or {}),
                    created_at=str(data.get("created_at", "")),
                )
                if event.event_id and event.tenant_id and event.layer:
                    store.append(event)
            except (ValueError, KeyError, TypeError):
                continue


def record_feedback(event: FeedbackEvent) -> FeedbackEvent:
    """Append an event to the default store and optionally persist it."""
    store = get_default_store()
    store.append(event)
    _maybe_persist(event)
    return event


__all__ = [
    "InMemoryLearningStore",
    "LayerOutcomeSummary",
    "get_default_store",
    "record_feedback",
    "reset_default_store",
]
