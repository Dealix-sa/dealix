"""Outreach queue — drafts only; never sends; never crosses the network."""

from __future__ import annotations

import json
import os
import time
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path

_LEDGER_PATH_ENV = "DEALIX_HERMES_OUTREACH_PATH"
_DEFAULT_PATH = Path("data/hermes/outreach_queue.jsonl")


@dataclass(frozen=True)
class OutreachDraft:
    draft_id: str
    campaign_id: str
    account_id: str
    channel: str
    subject: str
    body: str
    status: str
    requires_approval: bool
    created_at: float


def _path() -> Path:
    raw = os.environ.get(_LEDGER_PATH_ENV)
    p = Path(raw) if raw else _DEFAULT_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def queue_draft(campaign_id: str, account_id: str, channel: str, subject: str, body: str) -> OutreachDraft:
    """Append a DRAFT outreach record to the queue; no network calls are made."""
    draft = OutreachDraft(
        draft_id=f"out_{uuid.uuid4().hex[:10]}",
        campaign_id=campaign_id,
        account_id=account_id,
        channel=channel,
        subject=subject,
        body=body,
        status="draft",
        requires_approval=True,
        created_at=time.time(),
    )
    with _path().open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(asdict(draft), sort_keys=True) + "\n")
    return draft


def list_drafts(campaign_id: str | None = None) -> list[OutreachDraft]:
    """Return drafts in the queue, optionally filtered by campaign_id."""
    p = _path()
    if not p.exists():
        return []
    out: list[OutreachDraft] = []
    with p.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            d = OutreachDraft(**json.loads(line))
            if campaign_id is None or d.campaign_id == campaign_id:
                out.append(d)
    return out
