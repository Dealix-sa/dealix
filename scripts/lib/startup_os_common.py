"""Shared helpers for the Dealix Startup Operating System scripts.

Dependency-free (stdlib only). The non-negotiable safety rule is enforced
structurally here: every generated draft carries hard "no external send"
flags and no module in this package opens a network socket or transport.
"""

from __future__ import annotations

import json
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = ROOT / "config"
DATA_DIR = ROOT / "data"
OUTPUTS_DIR = ROOT / "outputs"

NON_NEGOTIABLE_RULE = (
    "AI drafts, scores, ranks, analyzes, and recommends. "
    "Founder reviews, approves, and acts manually. System never sends externally."
)

# Hard safety flags stamped onto every draft. These are invariants, not options.
SAFETY_FLAGS = {
    "send_allowed": False,
    "external_send_blocked": True,
    "requires_founder_approval": True,
    "no_auto_send": True,
}

FORBIDDEN_TOKENS = (
    "smtp",
    "sendmail",
    "twilio",
    "whatsapp_send",
    "auto_submit",
    "scrape",
)


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def load_offers() -> dict[str, Any]:
    return load_json(CONFIG_DIR / "startup_os_offers.json")


def load_seed_leads(path: Path | None = None) -> list[dict[str, Any]]:
    p = path or (DATA_DIR / "commercial_seed_leads.example.jsonl")
    leads: list[dict[str, Any]] = []
    with p.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                leads.append(json.loads(line))
    return leads


def today_str() -> str:
    return date.today().isoformat()


def now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def output_day_dir(day: str | None = None) -> Path:
    d = OUTPUTS_DIR / "commercial_launch" / (day or today_str())
    d.mkdir(parents=True, exist_ok=True)
    return d


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False))
            fh.write("\n")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows
