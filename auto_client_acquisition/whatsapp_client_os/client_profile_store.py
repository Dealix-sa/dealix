"""JSONL-backed store for the WhatsApp Client OS.

Mirrors the ``friction_log`` ledger pattern: env-overridable paths, a process
lock, append-on-write, and filtered reads. Five append-only ledgers live under
``data/whatsapp/`` by default:

- ``sessions.jsonl``            — WhatsAppSession snapshots (latest wins on read)
- ``client_assessments.jsonl``  — ClientAssessment rows
- ``action_cards.jsonl``        — ClientCard rows queued for review
- ``permissions.jsonl``         — PermissionGrant audit rows
- ``handoffs.jsonl``            — HandoffRequest rows

Pydantic ``datetime`` fields are serialized via ``model_dump(mode="json")`` so
rows round-trip cleanly. Handles are stored; raw PII is never written.
"""

from __future__ import annotations

import json
import os
import threading
from pathlib import Path
from typing import Any

from auto_client_acquisition.whatsapp_client_os.schemas import (
    ClientAssessment,
    ClientCard,
    HandoffRequest,
    PermissionGrant,
    WhatsAppSession,
)

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_DEFAULT_DIR = "data/whatsapp"
_lock = threading.Lock()

_FILES = {
    "sessions": "sessions.jsonl",
    "assessments": "client_assessments.jsonl",
    "action_cards": "action_cards.jsonl",
    "permissions": "permissions.jsonl",
    "handoffs": "handoffs.jsonl",
}


def _dir() -> Path:
    p = Path(os.environ.get("DEALIX_WHATSAPP_OS_DIR", _DEFAULT_DIR))
    if not p.is_absolute():
        p = _REPO_ROOT / p
    return p


def _path(ledger: str) -> Path:
    return _dir() / _FILES[ledger]


def _append(ledger: str, row: dict[str, Any]) -> None:
    path = _path(ledger)
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock, path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _read_all(ledger: str) -> list[dict[str, Any]]:
    path = _path(ledger)
    if not path.exists():
        return []
    out: list[dict[str, Any]] = []
    with _lock, path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


# ── Sessions (snapshot ledger — latest row per session_id wins) ──────────
def save_session(session: WhatsAppSession) -> WhatsAppSession:
    _append("sessions", session.model_dump(mode="json"))
    return session


def get_session(session_id: str) -> WhatsAppSession | None:
    latest: dict[str, Any] | None = None
    for row in _read_all("sessions"):
        if row.get("session_id") == session_id:
            latest = row
    if latest is None:
        return None
    try:
        return WhatsAppSession(**latest)
    except Exception:
        return None


def list_sessions(*, limit: int = 200) -> list[WhatsAppSession]:
    by_id: dict[str, dict[str, Any]] = {}
    for row in _read_all("sessions"):
        sid = row.get("session_id")
        if sid:
            by_id[sid] = row
    sessions: list[WhatsAppSession] = []
    for row in by_id.values():
        try:
            sessions.append(WhatsAppSession(**row))
        except Exception:
            pass
    sessions.sort(key=lambda s: s.updated_at, reverse=True)
    return sessions[:limit]


# ── Assessments ──────────────────────────────────────────────────────────
def save_assessment(assessment: ClientAssessment) -> ClientAssessment:
    _append("assessments", assessment.model_dump(mode="json"))
    return assessment


def get_assessment(assessment_id: str) -> ClientAssessment | None:
    latest: dict[str, Any] | None = None
    for row in _read_all("assessments"):
        if row.get("assessment_id") == assessment_id:
            latest = row
    if latest is None:
        return None
    try:
        return ClientAssessment(**latest)
    except Exception:
        return None


def list_assessments(*, limit: int = 200) -> list[ClientAssessment]:
    out: list[ClientAssessment] = []
    for row in _read_all("assessments"):
        try:
            out.append(ClientAssessment(**row))
        except Exception:
            pass
    return out[-limit:]


# ── Action cards / permissions / handoffs ────────────────────────────────
def queue_action_card(card: ClientCard) -> ClientCard:
    _append("action_cards", card.model_dump(mode="json"))
    return card


def list_action_cards(*, limit: int = 200) -> list[ClientCard]:
    out: list[ClientCard] = []
    for row in _read_all("action_cards"):
        try:
            out.append(ClientCard(**row))
        except Exception:
            pass
    return out[-limit:]


def record_permission(grant: PermissionGrant) -> PermissionGrant:
    _append("permissions", grant.model_dump(mode="json"))
    return grant


def list_permissions(*, limit: int = 200) -> list[PermissionGrant]:
    out: list[PermissionGrant] = []
    for row in _read_all("permissions"):
        try:
            out.append(PermissionGrant(**row))
        except Exception:
            pass
    return out[-limit:]


def record_handoff(handoff: HandoffRequest) -> HandoffRequest:
    _append("handoffs", handoff.model_dump(mode="json"))
    return handoff


def list_handoffs(*, limit: int = 200) -> list[HandoffRequest]:
    out: list[HandoffRequest] = []
    for row in _read_all("handoffs"):
        try:
            out.append(HandoffRequest(**row))
        except Exception:
            pass
    return out[-limit:]


def clear_for_test() -> None:
    for ledger in _FILES:
        path = _path(ledger)
        if path.exists():
            with _lock:
                path.write_text("", encoding="utf-8")


__all__ = [
    "clear_for_test",
    "get_assessment",
    "get_session",
    "list_action_cards",
    "list_assessments",
    "list_handoffs",
    "list_permissions",
    "list_sessions",
    "queue_action_card",
    "record_handoff",
    "record_permission",
    "save_assessment",
    "save_session",
]
