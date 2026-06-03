"""WhatsApp Client OS — JSONL stores.

Tenant-scoped, append-only JSONL persistence for sessions, message events,
action cards, assessments, and permissions. Mirrors the friction-log store
pattern: a ``DEALIX_WHATSAPP_*_PATH`` env override, default under
``data/whatsapp/``. Message text is redacted before persistence — no raw PII
or secret material is ever written.
"""

from __future__ import annotations

import json
import os
import threading
from pathlib import Path
from typing import Any

from auto_client_acquisition.friction_log.sanitizer import sanitize_notes
from auto_client_acquisition.whatsapp_client_os.permission_os import looks_like_secret
from auto_client_acquisition.whatsapp_client_os.schemas import (
    ActionCard,
    ClientAssessment,
    ClientPermission,
    ClientSession,
    MessageEvent,
)

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_lock = threading.Lock()

_STORES: dict[str, tuple[str, str]] = {
    "sessions": ("DEALIX_WHATSAPP_SESSIONS_PATH", "data/whatsapp/sessions.jsonl"),
    "messages": ("DEALIX_WHATSAPP_MESSAGES_PATH", "data/whatsapp/message_events.jsonl"),
    "cards": ("DEALIX_WHATSAPP_CARDS_PATH", "data/whatsapp/action_cards.jsonl"),
    "assessments": ("DEALIX_WHATSAPP_ASSESSMENTS_PATH", "data/whatsapp/client_assessments.jsonl"),
    "permissions": ("DEALIX_WHATSAPP_PERMISSIONS_PATH", "data/whatsapp/permissions.jsonl"),
}


def _path(store: str) -> Path:
    env_var, default = _STORES[store]
    p = Path(os.environ.get(env_var, default))
    if not p.is_absolute():
        p = _REPO_ROOT / p
    return p


def _append(store: str, record: dict[str, Any]) -> None:
    path = _path(store)
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock, path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def _read(store: str) -> list[dict[str, Any]]:
    path = _path(store)
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


# --- Sessions (append-on-update; latest wins) ------------------------------


def save_session(session: ClientSession) -> ClientSession:
    _append("sessions", session.to_dict())
    return session


def latest_session_for(wa_id_hash: str) -> ClientSession | None:
    latest: ClientSession | None = None
    for row in _read("sessions"):
        if row.get("wa_id_hash") == wa_id_hash:
            try:
                latest = ClientSession(**row)
            except TypeError:
                continue
    return latest


def get_session(session_id: str) -> ClientSession | None:
    latest: ClientSession | None = None
    for row in _read("sessions"):
        if row.get("session_id") == session_id:
            try:
                latest = ClientSession(**row)
            except TypeError:
                continue
    return latest


def list_sessions() -> list[ClientSession]:
    seen: dict[str, ClientSession] = {}
    for row in _read("sessions"):
        try:
            s = ClientSession(**row)
        except TypeError:
            continue
        seen[s.session_id] = s  # latest append wins
    return list(seen.values())


# --- Message events (redacted) ---------------------------------------------


def append_message(event: MessageEvent) -> MessageEvent:
    """Persist a message event with defensively-redacted text."""
    text = event.text_redacted
    if looks_like_secret(text):
        text = "[secret-redacted]"
    safe = MessageEvent(
        event_id=event.event_id,
        session_id=event.session_id,
        direction=event.direction,
        intent=event.intent,
        text_redacted=sanitize_notes(text),
        card_id=event.card_id,
        occurred_at=event.occurred_at,
    )
    _append("messages", safe.to_dict())
    return safe


def list_messages(session_id: str | None = None) -> list[MessageEvent]:
    out: list[MessageEvent] = []
    for row in _read("messages"):
        if session_id and row.get("session_id") != session_id:
            continue
        try:
            out.append(MessageEvent(**row))
        except TypeError:
            continue
    return out


# --- Cards / assessments / permissions -------------------------------------


def save_card(card: ActionCard) -> ActionCard:
    _append("cards", card.to_dict())
    return card


def list_cards(session_id: str | None = None) -> list[dict[str, Any]]:
    return [row for row in _read("cards") if not session_id or row.get("session_id") == session_id]


def save_assessment(assessment: ClientAssessment) -> ClientAssessment:
    _append("assessments", assessment.to_dict())
    return assessment


def list_assessments() -> list[dict[str, Any]]:
    return _read("assessments")


def save_permission(permission: ClientPermission) -> ClientPermission:
    _append("permissions", permission.to_dict())
    return permission


def list_permissions(session_id: str | None = None) -> list[dict[str, Any]]:
    return [
        row for row in _read("permissions") if not session_id or row.get("session_id") == session_id
    ]


def clear_for_test() -> None:
    for store in _STORES:
        path = _path(store)
        if path.exists():
            with _lock:
                path.write_text("", encoding="utf-8")


__all__ = [
    "append_message",
    "clear_for_test",
    "get_session",
    "latest_session_for",
    "list_assessments",
    "list_cards",
    "list_messages",
    "list_permissions",
    "list_sessions",
    "save_assessment",
    "save_card",
    "save_permission",
    "save_session",
]
