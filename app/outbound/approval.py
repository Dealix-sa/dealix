"""Approval queue — all outbound sends require human approval before sending.

Drafts may be generated freely, but a message must reach status="approved"
(via this queue) before the policy gate will allow any send. This module is the
in-memory approval store. Production deployments should persist approval
records with approver identity, timestamp, and audit trail in a database, but
the interface (``submit_for_approval`` / ``approve`` / ``reject`` /
``approval_status``) stays the same.
"""

from __future__ import annotations

import time
import uuid
from threading import Lock
from typing import Any, Mapping

_LOCK = Lock()
# _QUEUE[message_id] = {message_id, channel, contact, status, submitted_at,
#                       approved_by, approved_at, rejected_reason}
_QUEUE: "dict[str, dict[str, Any]]" = {}

STATUS_PENDING = "pending"
STATUS_APPROVED = "approved"
STATUS_REJECTED = "rejected"


def submit_for_approval(
    channel: str,
    message: Mapping[str, Any],
    contact: Mapping[str, Any],
    submitted_by: str = "system",
) -> str:
    """Submit a draft message to the approval queue. Returns the message id."""
    message_id = str(message.get("id") or uuid.uuid4().hex)
    now = time.time()
    with _LOCK:
        _QUEUE[message_id] = {
            "message_id": message_id,
            "channel": channel,
            "message": dict(message),
            "contact": dict(contact),
            "status": STATUS_PENDING,
            "submitted_by": submitted_by,
            "submitted_at": now,
            "approved_by": None,
            "approved_at": None,
            "rejected_reason": None,
        }
    return message_id


def approve(message_id: str, approved_by: str = "founder") -> bool:
    """Approve a pending message. Returns True on success."""
    with _LOCK:
        entry = _QUEUE.get(message_id)
        if entry is None or entry["status"] != STATUS_PENDING:
            return False
        entry["status"] = STATUS_APPROVED
        entry["approved_by"] = approved_by
        entry["approved_at"] = time.time()
        # Reflect approval status into the embedded message dict so the gate
        # sees status == "approved".
        entry["message"]["status"] = STATUS_APPROVED
        return True


def reject(message_id: str, reason: str = "", rejected_by: str = "founder") -> bool:
    """Reject a pending message. Returns True on success."""
    with _LOCK:
        entry = _QUEUE.get(message_id)
        if entry is None or entry["status"] != STATUS_PENDING:
            return False
        entry["status"] = STATUS_REJECTED
        entry["approved_by"] = rejected_by
        entry["rejected_reason"] = reason
        entry["message"]["status"] = STATUS_REJECTED
        return True


def approval_status(message_id: str) -> str | None:
    """Return the current approval status of a message (or None if unknown)."""
    with _LOCK:
        entry = _QUEUE.get(message_id)
        return entry["status"] if entry else None


def get_entry(message_id: str) -> dict[str, Any] | None:
    """Return a copy of the approval queue entry for a message."""
    with _LOCK:
        entry = _QUEUE.get(message_id)
        return dict(entry) if entry else None


def pending_messages() -> list[dict[str, Any]]:
    """Return all pending approval entries (copies)."""
    with _LOCK:
        return [dict(e) for e in _QUEUE.values() if e["status"] == STATUS_PENDING]


def clear_queue() -> None:
    """Clear all approval state (used by tests)."""
    with _LOCK:
        _QUEUE.clear()