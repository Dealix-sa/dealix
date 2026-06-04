#!/usr/bin/env python3
"""Shared helpers for the Dealix Commercial / Launch OS scripts.

Dependency-free (stdlib only) so the launch tooling runs in any environment,
including minimal GitHub Actions runners. The governing rule for every helper
here is the same one the whole OS enforces:

    AI drafts, ranks, and recommends.
    Founder reviews, approves, and sends manually.
    The system never sends externally.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config"
DATA_DIR = ROOT / "data"
OUTPUTS_DIR = ROOT / "outputs"
COMMERCIAL_OUTPUTS = OUTPUTS_DIR / "commercial_launch"
MEDIA_OUTPUTS = OUTPUTS_DIR / "media_social"
CONTROL_OUTPUTS = OUTPUTS_DIR / "final_launch_control"

GOVERNING_RULE = (
    "AI drafts, ranks, and recommends. "
    "Founder reviews, approves, and sends manually. "
    "The system never sends externally."
)

MANDATORY_SAFETY_FLAGS = {
    "send_allowed": False,
    "external_send_blocked": True,
    "requires_founder_approval": True,
    "no_auto_send": True,
}


def load_config(name: str) -> dict[str, Any]:
    """Load a JSON config from the repo config/ directory."""
    path = CONFIG_DIR / name
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def today_str(value: str | None = None) -> str:
    return value or date.today().isoformat()


def day_dir(base: Path, day: str | None = None) -> Path:
    d = base / today_str(day)
    d.mkdir(parents=True, exist_ok=True)
    return d


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False))
            fh.write("\n")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def csv_escape(value: Any) -> str:
    s = "" if value is None else str(value)
    if any(c in s for c in [",", '"', "\n", "\r"]):
        s = '"' + s.replace('"', '""') + '"'
    return s


def write_csv(path: Path, header: list[str], rows: list[list[Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [",".join(csv_escape(c) for c in header)]
    for row in rows:
        lines.append(",".join(csv_escape(c) for c in row))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
