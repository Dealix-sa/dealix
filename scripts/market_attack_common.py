"""Shared helpers for the Dealix Market Attack & Scaling generators.

Doctrine:
- Read-only. Never mutate input CSVs.
- Never crash on missing inputs; emit a clearly-flagged fallback.
- Never include "guaranteed" language in generated reports.
"""

from __future__ import annotations

import csv
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent
BOOTSTRAP_ROOT = REPO_ROOT / "scripts" / "market_attack_bootstrap"

BANNED_PHRASES = (
    "guaranteed",
    "guaranteed leads",
    "guaranteed revenue",
    "100% success",
    "always wins",
    "risk-free",
    "we promise",
    "we will deliver",
)


def now_iso() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def private_ops_root() -> Path:
    raw = os.environ.get("PRIVATE_OPS", "").strip()
    if raw:
        return Path(raw)
    # Fallback: write under a local .private_ops sandbox so the script
    # still works in CI / dev without exposing real data.
    return REPO_ROOT / ".private_ops_sandbox"


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    """Return (headers, rows). Returns ([], []) if the file is missing."""
    if not path.exists():
        return [], []
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        try:
            headers = next(reader)
        except StopIteration:
            return [], []
        rows = [dict(zip(headers, row)) for row in reader if row]
    return headers, rows


def load_with_fallback(
    primary: Path, bootstrap: Path
) -> tuple[list[str], list[dict[str, str]], str]:
    """Try the runtime path first, then the bootstrap template.

    Returns (headers, rows, source) where source is 'runtime' or 'fallback'.
    """
    if primary.exists():
        headers, rows = read_csv(primary)
        return headers, rows, "runtime"
    headers, rows = read_csv(bootstrap)
    return headers, rows, "fallback"


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_markdown(path: Path, lines: Iterable[str]) -> None:
    ensure_parent(path)
    content = "\n".join(lines).rstrip() + "\n"
    path.write_text(content, encoding="utf-8")


def assert_proof_safe(text: str, label: str) -> list[str]:
    """Return a list of doctrine violations in text (case-insensitive)."""
    lower = text.lower()
    hits: list[str] = []
    for phrase in BANNED_PHRASES:
        if phrase in lower:
            hits.append(f"{label}: banned phrase '{phrase}'")
    return hits


@dataclass
class ReportContext:
    name: str
    runtime_paths_checked: list[Path]
    fallback_paths_used: list[Path]
    started_at: str

    def header(self) -> list[str]:
        lines = [
            f"# {self.name}",
            "",
            f"_Generated: {self.started_at}_",
            "",
        ]
        if self.fallback_paths_used:
            lines.extend(
                [
                    "> **Source: fallback.** One or more runtime CSVs were not "
                    "found; bootstrap templates were used instead. "
                    "Run `make bootstrap-runtime PRIVATE_OPS=...` to seed.",
                    "",
                ]
            )
        return lines


def safe_int(value: str | int | None, default: int = 0) -> int:
    if value is None:
        return default
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return default


def fail_with(message: str, code: int = 1) -> "Never":  # type: ignore[name-defined]
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)
