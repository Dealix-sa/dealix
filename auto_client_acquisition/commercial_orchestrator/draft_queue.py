"""Draft Queue — durable JSON-Lines store for outreach/proposal drafts
that are waiting for founder approval.

This is the **single founder approval queue** for the daily commercial loop.
The daily-draft loop (a separate process / GitHub Actions cron) writes here;
the founder API (`/api/v1/founder/approvals`) reads here. An in-memory store
(`approval_center`) cannot bridge those two processes — a file can.

Storage:
- File path: $DEALIX_DRAFT_QUEUE_PATH (default: var/draft-queue.jsonl)
- Format: JSON-Lines, append-only. Status changes are appended as new
  `{event:"status_change", ...}` lines so the audit trail is preserved
  (same pattern as `auto_client_acquisition/lead_inbox.py`).
- The `var/` directory is gitignored, so drafts never leak into the repo.

Hard rules (doctrine):
- NO external send from this module. It only persists drafts + approvals.
- Drafts are COMPANY-LEVEL. No personal PII is stored here.
- Every draft carries `approval_required=True` and `consent_status` until a
  founder explicitly approves.
"""
from __future__ import annotations

import json
import os
import threading
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

_DEFAULT_PATH = "var/draft-queue.jsonl"
_lock = threading.Lock()

VALID_STATUS = {"pending", "approved", "rejected", "sent", "expired"}


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_DRAFT_QUEUE_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        # repo root = parent of `auto_client_acquisition/`
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def enqueue(draft: dict[str, Any]) -> dict[str, Any]:
    """Persist a single draft awaiting approval. Returns the persisted record
    (with `id`, `created_at`, `status` added). Best-effort: a disk hiccup never
    raises — the record is returned with `persisted=False`.
    """
    now = datetime.now(UTC)
    rec: dict[str, Any] = {
        "id": draft.get("id") or f"draft_{int(now.timestamp() * 1000)}_{uuid.uuid4().hex[:8]}",
        "created_at": now.isoformat(),
        "status": "pending",
        "approval_required": True,
        "no_live_send": True,
        **{k: v for k, v in draft.items() if k not in {"created_at", "status"}},
    }
    try:
        path = _path()
        _ensure_dir(path)
        with _lock, path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        rec["persisted"] = True
    except Exception:
        rec["persisted"] = False
    return rec


def _read_all() -> list[dict[str, Any]]:
    path = _path()
    if not path.exists():
        return []
    out: list[dict[str, Any]] = []
    try:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except Exception:
                    continue
    except Exception:
        return []
    return out


def _materialize() -> dict[str, dict[str, Any]]:
    """Fold the append-only log into current draft state.

    Base records (no `event`) seed the map; `status_change` events update the
    status/approver of an existing draft. Returns {draft_id: current_record}.
    """
    drafts: dict[str, dict[str, Any]] = {}
    for rec in _read_all():
        if rec.get("event") == "status_change":
            did = rec.get("draft_id")
            if did and did in drafts:
                drafts[did]["status"] = rec.get("status", drafts[did].get("status"))
                drafts[did]["approver"] = rec.get("who")
                drafts[did]["decided_at"] = rec.get("ts")
                if rec.get("note"):
                    drafts[did]["decision_note"] = rec.get("note")
            continue
        did = rec.get("id")
        if did:
            drafts[did] = rec
    return drafts


def list_drafts(limit: int = 200, status: str | None = None) -> list[dict[str, Any]]:
    """Return current drafts (newest first). Optionally filter by status."""
    drafts = list(_materialize().values())
    if status:
        drafts = [d for d in drafts if d.get("status") == status]
    drafts.sort(key=lambda d: d.get("created_at", ""), reverse=True)
    return drafts[:limit]


def get(draft_id: str) -> dict[str, Any] | None:
    return _materialize().get(draft_id)


def set_status(
    draft_id: str, new_status: str, who: str = "founder", note: str = ""
) -> dict[str, Any] | None:
    """Append a status-change event. Returns the change record, or None if the
    draft does not exist. Raises ValueError on an invalid status.
    """
    if new_status not in VALID_STATUS:
        raise ValueError(f"invalid status: {new_status}")
    if draft_id not in _materialize():
        return None
    rec = {
        "event": "status_change",
        "draft_id": draft_id,
        "status": new_status,
        "who": who,
        "note": note,
        "ts": datetime.now(UTC).isoformat(),
    }
    try:
        path = _path()
        _ensure_dir(path)
        with _lock, path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        return rec
    except Exception:
        return None


def stats() -> dict[str, Any]:
    """Aggregate queue metrics. Safe on an empty store."""
    drafts = list(_materialize().values())
    by_status: dict[str, int] = {}
    by_sector: dict[str, int] = {}
    for d in drafts:
        st = d.get("status", "pending")
        by_status[st] = by_status.get(st, 0) + 1
        sec = d.get("sector") or "unknown"
        by_sector[sec] = by_sector.get(sec, 0) + 1
    return {
        "total_drafts": len(drafts),
        "pending": by_status.get("pending", 0),
        "by_status": by_status,
        "by_sector": by_sector,
        "store_path": str(_path()),
        "store_exists": _path().exists(),
    }


__all__ = ["enqueue", "list_drafts", "get", "set_status", "stats", "VALID_STATUS"]
