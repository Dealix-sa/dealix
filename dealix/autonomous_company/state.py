"""Durable memory for the Autonomous Company OS.

State lives in data/autonomous_company/state.json (gitignored — it is the
company's private CRM memory). New leads are ingested from a founder-owned inbox
file. Nothing here is committed as real client data.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

from .schemas import Deal, DealStage

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "autonomous_company"
STATE_PATH = DATA_DIR / "state.json"
INBOX_PATH = DATA_DIR / "inbox.json"

STATE_SCHEMA = "dealix.autonomous_company.state.v1"


def load_state(path: Path | None = None) -> dict[str, Any]:
    p = path or STATE_PATH
    if not p.exists():
        return {"schema": STATE_SCHEMA, "deals": [], "history": []}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"schema": STATE_SCHEMA, "deals": [], "history": []}
    data.setdefault("deals", [])
    data.setdefault("history", [])
    return data


def load_deals(state: dict[str, Any]) -> list[Deal]:
    return [Deal.from_dict(d) for d in state.get("deals", [])]


def save_state(deals: list[Deal], history: list[dict[str, Any]], path: Path | None = None) -> Path:
    p = path or STATE_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": STATE_SCHEMA,
        "updated_at": date.today().isoformat(),
        "deals": [d.to_dict() for d in deals],
        "history": history[-365:],  # keep a year of cycle summaries
    }
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return p


def ingest_inbox(existing: list[Deal], today: date, path: Path | None = None) -> tuple[list[Deal], int]:
    """Merge new leads from the inbox file into the deal list.

    The inbox is a founder-owned JSON list. Only warm / opted-in leads should be
    placed there — the engine never scrapes or invents contacts. Returns
    (deals, added_count). Leads with an id that already exists are skipped.
    """

    p = path or INBOX_PATH
    if not p.exists():
        return existing, 0
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return existing, 0
    items = raw.get("leads", raw) if isinstance(raw, dict) else raw
    known_ids = {d.id for d in existing}
    known_names = {_norm(d.account_name) for d in existing}
    added = 0
    for item in items or []:
        if not isinstance(item, dict):
            continue
        deal = Deal.from_dict(item)
        if not deal.account_name:
            continue
        # Deterministic, name-based id so the same lead is never re-ingested.
        if not deal.id:
            deal.id = _slug(deal.account_name)
        if deal.id in known_ids or _norm(deal.account_name) in known_names:
            continue
        deal.created_at = deal.created_at or today.isoformat()
        deal.last_touch_at = deal.last_touch_at or deal.created_at
        deal.stage = deal.stage or DealStage.NEW
        if not deal.has_event("lead_identified"):
            from .schemas import DealEvent

            deal.events.append(DealEvent(event="lead_identified", at=today.isoformat()))
        existing.append(deal)
        known_ids.add(deal.id)
        known_names.add(_norm(deal.account_name))
        added += 1
    return existing, added


def _norm(name: str) -> str:
    return " ".join(name.lower().split())


def _slug(name: str) -> str:
    base = "-".join("".join(c if c.isalnum() else " " for c in name).lower().split())
    return (base or "lead")[:48]


def seed_example_inbox(path: Path | None = None) -> Path:
    """Write an EMPTY inbox template (no fake customers). Founder fills it in."""

    p = path or INBOX_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists():
        return p
    template = {
        "schema": "dealix.autonomous_company.inbox.v1",
        "note": (
            "Add ONLY warm / opted-in leads you can legitimately contact. "
            "The engine never scrapes or invents contacts. No fake customers."
        ),
        "leads": [],
        "example_shape": {
            "account_name": "<real account name>",
            "sector": "<sector>",
            "source": "<how you got this warm lead>",
            "offer": "Revenue Proof Sprint",
            "value_sar": 499,
            "contact_hint": "<founder-owned channel note>",
            "opted_in": True,
        },
    }
    p.write_text(json.dumps(template, ensure_ascii=False, indent=2), encoding="utf-8")
    return p
