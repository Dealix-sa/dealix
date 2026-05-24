"""Shared helpers for daily/weekly generator scripts.

Private-ops is intentionally OUTSIDE the repo — it holds CSV/markdown
that must never reach GitHub. These helpers read it safely and refuse
to silently invent rows if a ledger is missing.
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import os
from pathlib import Path
from typing import Iterable


def parse_args(prog: str) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog=prog, allow_abbrev=False)
    p.add_argument(
        "--private-ops",
        default=os.environ.get("DEALIX_PRIVATE_OPS", "/opt/dealix-ops-private"),
        help="Path to the private ops runtime (default: $DEALIX_PRIVATE_OPS or /opt/dealix-ops-private)",
    )
    p.add_argument("--output", default=None, help="Optional output path (defaults to stdout)")
    p.add_argument("--strict", action="store_true",
                   help="Exit non-zero if any required ledger is missing.")
    return p.parse_args()


def ledger_path(private_ops: str, *parts: str) -> Path:
    return Path(private_ops, *parts)


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        return [], []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        return list(reader.fieldnames or []), rows


def write_or_print(text: str, output: str | None) -> None:
    if not output:
        print(text)
        return
    p = Path(output)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    print(f"[written] {p}")


def today_iso() -> str:
    return _dt.date.today().isoformat()


def section(title: str, rows: Iterable[str]) -> str:
    body = "\n".join(f"- {r}" for r in rows) or "- (no entries)"
    return f"## {title}\n\n{body}\n"
