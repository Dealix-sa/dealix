"""Thread-safe JSON store for the Saudi Opportunity Command Room.

Durable state lives under ``data/opportunity_graph/`` as three JSON files:

    opportunities.json   scored OpportunityCompany records
    outreach_drafts.json OutreachDraft records (draft-first)
    approvals.json       append-only approval/decision audit log

The store never sends anything; it only persists graph state. The location can
be overridden with ``DEALIX_OPPORTUNITY_GRAPH_DIR`` (used by tests).
"""

from __future__ import annotations

import json
import os
import threading
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import TypeAdapter

from dealix.opportunity_graph.schemas import OpportunityCompany, OutreachDraft

_DIR_ENV = "DEALIX_OPPORTUNITY_GRAPH_DIR"
_REPO_ROOT = Path(__file__).resolve().parents[2]

_COMPANIES_TA = TypeAdapter(list[OpportunityCompany])
_DRAFTS_TA = TypeAdapter(list[OutreachDraft])


def default_data_dir() -> Path:
    raw = os.environ.get(_DIR_ENV, "").strip()
    if raw:
        p = Path(raw)
        return p if p.is_absolute() else _REPO_ROOT / p
    return _REPO_ROOT / "data" / "opportunity_graph"


def uid(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def _utcnow_iso() -> str:
    return datetime.now(UTC).isoformat()


class OpportunityGraphStore:
    def __init__(self, data_dir: Path | None = None) -> None:
        self._dir = data_dir or default_data_dir()
        self._lock = threading.Lock()

    @property
    def data_dir(self) -> Path:
        return self._dir

    def _companies_path(self) -> Path:
        return self._dir / "opportunities.json"

    def _drafts_path(self) -> Path:
        return self._dir / "outreach_drafts.json"

    def _approvals_path(self) -> Path:
        return self._dir / "approvals.json"

    def _ensure_dir(self) -> None:
        self._dir.mkdir(parents=True, exist_ok=True)

    def _read_json(self, path: Path, default: Any) -> Any:
        if not path.exists():
            return default
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return default

    def _write_json(self, path: Path, payload: Any) -> None:
        self._ensure_dir()
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, default=str),
            encoding="utf-8",
        )
        tmp.replace(path)

    # ── Companies ──────────────────────────────────────────────────────
    def load_companies(self) -> list[OpportunityCompany]:
        raw = self._read_json(self._companies_path(), [])
        rows = raw.get("companies", raw) if isinstance(raw, dict) else raw
        try:
            return _COMPANIES_TA.validate_python(rows)
        except Exception:
            return []

    def save_companies(self, companies: list[OpportunityCompany]) -> None:
        with self._lock:
            self._write_json(
                self._companies_path(),
                {
                    "version": 1,
                    "generated_at": _utcnow_iso(),
                    "companies": [c.model_dump(mode="json") for c in companies],
                },
            )

    def upsert_companies(self, companies: list[OpportunityCompany]) -> list[OpportunityCompany]:
        with self._lock:
            existing = {c.id: c for c in self.load_companies()}
            for c in companies:
                existing[c.id] = c
            merged = list(existing.values())
        self.save_companies(merged)
        return merged

    # ── Drafts ─────────────────────────────────────────────────────────
    def load_drafts(self) -> list[OutreachDraft]:
        raw = self._read_json(self._drafts_path(), [])
        rows = raw.get("drafts", raw) if isinstance(raw, dict) else raw
        try:
            return _DRAFTS_TA.validate_python(rows)
        except Exception:
            return []

    def save_drafts(self, drafts: list[OutreachDraft]) -> None:
        with self._lock:
            self._write_json(
                self._drafts_path(),
                {
                    "version": 1,
                    "generated_at": _utcnow_iso(),
                    "drafts": [d.model_dump(mode="json") for d in drafts],
                },
            )

    def upsert_drafts(self, drafts: list[OutreachDraft]) -> list[OutreachDraft]:
        with self._lock:
            existing = {d.id: d for d in self.load_drafts()}
            for d in drafts:
                existing[d.id] = d
            merged = list(existing.values())
        self.save_drafts(merged)
        return merged

    def get_draft(self, draft_id: str) -> OutreachDraft | None:
        for d in self.load_drafts():
            if d.id == draft_id:
                return d
        return None

    # ── Approvals (append-only audit log) ──────────────────────────────
    def append_approval(self, entry: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            log = self._read_json(self._approvals_path(), [])
            if not isinstance(log, list):
                log = []
            record = {"id": uid("apr"), "at": _utcnow_iso(), **entry}
            log.append(record)
            self._write_json(self._approvals_path(), log)
        return record

    def load_approvals(self) -> list[dict[str, Any]]:
        log = self._read_json(self._approvals_path(), [])
        return log if isinstance(log, list) else []


_DEFAULT_STORE: OpportunityGraphStore | None = None


def get_store() -> OpportunityGraphStore:
    """Process-wide default store (honors the env override at first call)."""
    global _DEFAULT_STORE
    if _DEFAULT_STORE is None:
        _DEFAULT_STORE = OpportunityGraphStore()
    return _DEFAULT_STORE


def reset_default_store() -> None:
    """Test helper — drop the cached default store."""
    global _DEFAULT_STORE
    _DEFAULT_STORE = None
