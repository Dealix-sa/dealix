#!/usr/bin/env python3
"""Shared helpers for the Dealix Revenue Execution & Scale Control OS (V7).

All V7 generators and verifiers import from here so that path handling, date
stamping, slugging, and safe JSON/CSV/JSONL IO behave identically everywhere.

Safety posture (enforced by tests + verifiers):
    AI prepares. Founder approves. Manual action only. No external sending.

Nothing in this module performs network IO, sends messages, or touches
secrets. It only reads/writes local artifact files inside the repo tree.
"""

from __future__ import annotations

import csv
import datetime as _dt
import json
import re
from collections.abc import Iterable
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
OUTPUTS = REPO / "outputs"
DOCS = REPO / "docs"
DATA = REPO / "data"
CONFIG = REPO / "config"

# Canonical revenue pipeline stages (single source of truth for V7).
PIPELINE_STAGES: tuple[str, ...] = (
    "raw_lead",
    "researched",
    "draft_generated",
    "founder_review",
    "manual_action_selected",
    "manually_contacted",
    "reply_positive",
    "reply_neutral",
    "reply_negative",
    "discovery_booked",
    "diagnostic_proposed",
    "diagnostic_sold",
    "diagnostic_delivered",
    "pilot_proposed",
    "pilot_sold",
    "pilot_delivered",
    "retainer_proposed",
    "retainer_started",
    "expansion_identified",
    "lost",
    "suppressed",
)

# Allowed manual event types for the manual events ledger.
MANUAL_EVENT_TYPES: tuple[str, ...] = (
    "manual_send_recorded",
    "reply_positive",
    "reply_negative",
    "discovery_booked",
    "diagnostic_sold",
    "diagnostic_delivered",
    "pilot_proposed",
    "pilot_sold",
    "retainer_started",
    "lost",
    "suppressed",
)

# Founder action queue states.
ACTION_STATES: tuple[str, ...] = (
    "review",
    "approved_for_manual_copy",
    "hold",
    "needs_research",
    "rejected",
    "done_manually",
    "reply_received",
    "suppressed",
)


def today(date: str | None = None) -> str:
    """Return an ISO date string (YYYY-MM-DD); ``date`` overrides for tests."""
    if date:
        return date
    return _dt.date.today().isoformat()


def iso_week(date: str | None = None) -> str:
    """Return ISO ``YYYY-WW`` for the given (or current) date."""
    d = _dt.date.fromisoformat(today(date))
    year, week, _ = d.isocalendar()
    return f"{year}-{week:02d}"


def slugify(value: str) -> str:
    """Lowercase ASCII slug; keeps Arabic out of paths by transliterating gaps."""
    value = (value or "").strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value or "company"


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_text(path: Path, content: str) -> Path:
    ensure_dir(path.parent)
    path.write_text(content, encoding="utf-8")
    return path


def write_json(path: Path, payload: Any) -> Path:
    ensure_dir(path.parent)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> Path:
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return path


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, Any]]) -> Path:
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})
    return path


def latest_dated_dir(base: Path) -> Path | None:
    """Return the most recent YYYY-MM-DD subdir under ``base`` if any."""
    if not base.exists():
        return None
    candidates = [
        p for p in base.iterdir()
        if p.is_dir() and re.fullmatch(r"\d{4}-\d{2}-\d{2}", p.name)
    ]
    if not candidates:
        return None
    return sorted(candidates, key=lambda p: p.name)[-1]


# Deterministic seed verticals/channels used when no upstream data exists.
SEED_VERTICALS: tuple[str, ...] = (
    "logistics",
    "retail",
    "healthcare",
    "real_estate",
    "professional_services",
    "manufacturing",
    "education",
    "hospitality",
)

SEED_CHANNELS: tuple[str, ...] = ("email", "whatsapp_manual", "linkedin_manual", "phone")

SAFETY_BANNER = (
    "AI prepares. Founder approves. Manual action only. No external sending."
)
