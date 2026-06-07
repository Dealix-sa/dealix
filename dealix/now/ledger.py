"""Append-only decision ledger for the Dealix Now engine.

Every founder decision on a draft (approve / reject / any note) is recorded as
one JSONL line. ``approve`` / ``reject`` ONLY log and return a result dict —
they never send anything. ``approve`` returns founder-operated ``mailto`` and
``whatsapp`` deep links (URL-encoded from the draft subject/body) so the
founder can send manually. Dealix never auto-sends (doctrine rule 5 + agent
interaction rule 1).

JSONL store with env override, mirroring ``value_os/value_ledger.py`` and
``payment_ops/renewal_scheduler.py``: path from ``DEALIX_NOW_LEDGER_PATH``,
default ``var/now_ledger.jsonl`` (``var/`` is gitignored).

Pure I/O + string building: no network, no API keys, no LLM.
"""

from __future__ import annotations

import json
import logging
import os
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import quote

log = logging.getLogger(__name__)

_DEFAULT_PATH = "var/now_ledger.jsonl"

APPROVED_STATUS = "approved — ready to send by founder (Dealix never auto-sends)"
REJECTED_STATUS = "rejected — archived, nothing sent"

VALID_DECISIONS = frozenset({"approved", "rejected", "noted"})


def _ledger_path() -> Path:
    raw = os.getenv("DEALIX_NOW_LEDGER_PATH", _DEFAULT_PATH)
    path = Path(raw)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _safe_log(value: object) -> str:
    """Strip CR/LF so a crafted draft_id/actor can't forge extra log lines."""
    return str(value).replace("\r", " ").replace("\n", " ")


def _find_latest(draft_id: str) -> dict | None:
    """Return the most recent ledger record for ``draft_id``, or ``None``."""
    latest: dict | None = None
    for rec in list_decisions():
        if rec.get("draft_id") == draft_id:
            latest = rec
    return latest


def record_decision(
    draft_id: str,
    decision: str,
    actor: str = "founder",
    note: str = "",
) -> dict:
    """Append one decision record and return it.

    ``decision`` is normalized; unknown values are stored as ``noted`` so the
    log never silently drops an action.
    """
    normalized = decision.strip().lower()
    if normalized not in VALID_DECISIONS:
        normalized = "noted"
    record = {
        "draft_id": str(draft_id),
        "decision": normalized,
        "actor": str(actor or "founder"),
        "note": str(note or ""),
        "logged_at": _now_iso(),
    }
    path = _ledger_path()
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False))
        handle.write("\n")
    log.info(
        "now_decision_recorded draft_id=%s decision=%s actor=%s",
        _safe_log(draft_id),
        normalized,
        _safe_log(actor),
    )
    return record


def list_decisions() -> list[dict]:
    """Return all decision records in append order (oldest first)."""
    path = _ledger_path()
    if not path.exists():
        return []
    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception:
                log.debug("skipping corrupt ledger line", exc_info=True)
                continue
    return rows


def _mailto_link(subject: str, body: str, to: str = "") -> str:
    return (
        f"mailto:{quote(to)}" f"?subject={quote(subject, safe='')}" f"&body={quote(body, safe='')}"
    )


def _whatsapp_link(text: str, phone: str = "") -> str:
    base = "https://wa.me/"
    digits = "".join(ch for ch in phone if ch.isdigit())
    return f"{base}{digits}?text={quote(text, safe='')}"


def approve(draft_id: str, draft: dict | None = None, actor: str = "founder") -> dict:
    """Log an approval and return founder-operated send links.

    This NEVER sends. It returns ``mailto`` / ``whatsapp`` deep links built from
    the draft's subject/body so the founder sends manually. If ``draft`` is not
    supplied, links are built from whatever subject/body are recoverable
    (empty otherwise) and the approval is still logged.
    """
    record_decision(draft_id, "approved", actor=actor)

    subject = ""
    body = ""
    to = ""
    if isinstance(draft, dict):
        subject = str(draft.get("subject") or "")
        body = str(draft.get("body") or "")
        to = str((draft.get("contact") or {}).get("to") or "")

    mailto = _mailto_link(subject, body, to)
    whatsapp = _whatsapp_link(f"{subject}\n\n{body}".strip())

    return {
        "ok": True,
        "draft_id": str(draft_id),
        "status": APPROVED_STATUS,
        "mailto": mailto,
        "whatsapp": whatsapp,
    }


def reject(draft_id: str, actor: str = "founder", note: str = "") -> dict:
    """Log a rejection and return a result dict. Sends nothing."""
    record_decision(draft_id, "rejected", actor=actor, note=note)
    return {
        "ok": True,
        "draft_id": str(draft_id),
        "status": REJECTED_STATUS,
    }


def clear_for_test() -> None:
    """Remove the ledger file (test helper only)."""
    path = _ledger_path()
    if path.exists():
        path.unlink()


__all__ = [
    "APPROVED_STATUS",
    "REJECTED_STATUS",
    "VALID_DECISIONS",
    "approve",
    "clear_for_test",
    "list_decisions",
    "record_decision",
    "reject",
]
