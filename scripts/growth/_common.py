#!/usr/bin/env python3
"""Shared helpers for the Dealix Self-Growth and Distribution OS generators."""

from __future__ import annotations

import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

_REPO = Path(__file__).resolve().parents[2]

DATA_DIR = _REPO / "data" / "growth"
REPORTS_DIR = _REPO / "reports" / "growth"

# The single allowed calls-to-action. Every growth asset must lead to exactly one.
ALLOWED_CTA: tuple[str, ...] = (
    "Business OS Score",
    "Free Diagnostic",
    "Command Sprint",
)

# The 12 repurpose assets a single source can be turned into.
REPURPOSE_ASSETS: tuple[str, ...] = (
    "linkedin_post",
    "x_thread",
    "newsletter_section",
    "short_video_script",
    "carousel",
    "blog_long_form",
    "sector_page_block",
    "nurture_email",
    "whatsapp_broadcast_optin",
    "founder_voice_note_script",
    "case_safe_insight",
    "free_tool_prompt",
)


def repo_root() -> Path:
    """Return the absolute repository root path."""
    return _REPO


def assert_single_cta(cta: str) -> str:
    """Validate that a CTA is exactly one of the allowed three. Returns it."""
    if cta not in ALLOWED_CTA:
        raise ValueError(
            f"CTA {cta!r} is not allowed. Use one of: {', '.join(ALLOWED_CTA)}",
        )
    return cta


def now_iso() -> str:
    """Return current UTC timestamp in ISO-8601 with trailing Z semantics."""
    return datetime.now(UTC).isoformat()


def ensure_dirs() -> None:
    """Create the data and reports growth directories if missing."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, payload: Any) -> int:
    """Write payload as deterministic, UTF-8, sorted-key JSON. Return byte size."""
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
    text += "\n"
    path.write_text(text, encoding="utf-8")
    return len(text.encode("utf-8"))


def read_json(path: Path) -> Any:
    """Read JSON from path, returning None if the file is absent."""
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, header: Sequence[str], rows: Iterable[Sequence[Any]]) -> int:
    """Write rows as CSV with a header. Return byte size."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)
    return path.stat().st_size


def append_jsonl_unique(
    path: Path,
    records: Sequence[Mapping[str, Any]],
    key: str,
) -> tuple[int, int]:
    """Append records to a JSONL file, skipping any whose key already exists.

    Returns a tuple of (added, skipped).
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: set[str] = set()
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if key in obj:
                existing.add(str(obj[key]))
    added = 0
    skipped = 0
    with path.open("a", encoding="utf-8") as handle:
        for record in records:
            if str(record.get(key)) in existing:
                skipped += 1
                continue
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True))
            handle.write("\n")
            existing.add(str(record.get(key)))
            added += 1
    return added, skipped


def append_jsonl(path: Path, record: Mapping[str, Any]) -> int:
    """Append a single record line to a JSONL file. Return byte size of the line."""
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line)
    return len(line.encode("utf-8"))
