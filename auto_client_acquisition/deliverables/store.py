"""Deliverables in-memory + JSONL store.

Persistence: append-only JSONL at data/wave13/deliverables.jsonl.
Index: in-memory dict keyed by deliverable_id.

Article 11: minimum viable persistence — when first paid customer signs,
swap to Postgres ORM following proof_ledger/postgres_backend.py.
"""

from __future__ import annotations

import json
import os
import re
import uuid
from datetime import UTC, datetime, timezone

from auto_client_acquisition.deliverables.schemas import (
    Deliverable,
    DeliverableType,
)
from auto_client_acquisition.runtime_paths import resolve_deliverables_dir
from core.logging import get_logger

log = get_logger(__name__)

_JSONL_PATH = os.path.join("data", "wave13", "deliverables.jsonl")
_INDEX: dict[str, Deliverable] = {}


def _ensure_dir() -> None:
    os.makedirs(os.path.dirname(_JSONL_PATH), exist_ok=True)


def _persist(rec: Deliverable) -> None:
    _ensure_dir()
    _INDEX[rec.deliverable_id] = rec
    with open(_JSONL_PATH, "a", encoding="utf-8") as f:
        f.write(rec.model_dump_json() + "\n")


def create_deliverable(
    *,
    session_id: str,
    customer_handle: str,
    type: DeliverableType,
    title_ar: str,
    title_en: str,
    customer_visible: bool = True,
    approval_required: bool = True,
    proof_related: bool = False,
    proof_event_id: str | None = None,
    artifact_uri: str | None = None,
    persist: bool = True,
) -> Deliverable:
    """Create a Deliverable in 'draft' status and (optionally) persist."""
    rec = Deliverable(
        deliverable_id=f"deliv_{uuid.uuid4().hex[:10]}",
        session_id=session_id,
        customer_handle=customer_handle,
        type=type,
        title_ar=title_ar,
        title_en=title_en,
        status="draft",
        version=1,
        customer_visible=customer_visible,
        approval_required=approval_required,
        proof_related=proof_related,
        proof_event_id=proof_event_id,
        artifact_uri=artifact_uri,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    if persist:
        _persist(rec)
    else:
        _INDEX[rec.deliverable_id] = rec
    return rec


def get_deliverable(deliverable_id: str) -> Deliverable | None:
    return _INDEX.get(deliverable_id)


def list_by_session(session_id: str, *, customer_visible_only: bool = False) -> list[Deliverable]:
    """List all deliverables for a session.

    `customer_visible_only=True` filters to customer_visible=True (portal use).
    """
    items = [d for d in _INDEX.values() if d.session_id == session_id]
    if customer_visible_only:
        items = [d for d in items if d.customer_visible]
    items.sort(key=lambda d: d.created_at)
    return items


def save_rendered_artifact(rec: Deliverable, html: str) -> str | None:
    """Persist a rendered HTML artifact to disk and set ``artifact_uri``.

    Writes the self-contained HTML to the deliverables artifact directory,
    updates the record's ``artifact_uri`` + ``updated_at``, and re-persists
    so the ``delivered`` transition references a real file.

    Degrades gracefully: a write failure logs a warning and returns None
    — rendering still succeeds, the record simply keeps no ``artifact_uri``.
    """
    try:
        out_dir = resolve_deliverables_dir()
        out_dir.mkdir(parents=True, exist_ok=True)
        safe_id = re.sub(r"[^A-Za-z0-9_-]", "_", rec.deliverable_id)
        path = out_dir / f"{rec.type}_{safe_id}.html"
        path.write_text(html, encoding="utf-8")
        rec.artifact_uri = str(path)
        rec.updated_at = datetime.now(UTC)
        _persist(rec)
        return str(path)
    except Exception as exc:  # never fail rendering on artifact I/O
        log.warning("deliverable_artifact_write_failed", error=str(exc))
        return None


def reset_for_test() -> None:
    """Test-only helper to clear the in-memory index."""
    _INDEX.clear()
