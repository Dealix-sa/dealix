"""Shared helpers for Dealix scripts.

Conventions used by every generator / verifier:
  - private ops root from DEALIX_PRIVATE_OPS env (default /opt/dealix-ops-private)
  - all output docs are written under repo_root/docs/<section>/<NAME>.md
  - every report ends with the audit footer (source · freshness · actor)
"""
from __future__ import annotations

import argparse
import csv
import datetime
import os
from pathlib import Path
from typing import Iterable


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def workspace_root() -> Path:
    return Path(os.environ.get("DEALIX_PRIVATE_OPS", "/opt/dealix-ops-private"))


def cli(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--private-ops", default=os.environ.get("DEALIX_PRIVATE_OPS"))
    return parser


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def audit_footer(source_paths: Iterable[Path]) -> str:
    now = datetime.datetime.utcnow().isoformat(timespec="seconds")
    sources = " · ".join(str(p) for p in source_paths) or "no_workspace_files"
    return (
        "\n---\n"
        f"source: {sources}\n\n"
        f"freshness: {now}\n\n"
        "actor: dealix scripts\n\n"
        "policy: AI prepares · founder approves · no guaranteed claims · no auto external send\n"
    )


def write_doc(rel_path: str, body: str, sources: Iterable[Path]) -> Path:
    out = repo_root() / rel_path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body.rstrip() + "\n" + audit_footer(sources), encoding="utf-8")
    return out


def md_table(headers: list[str], rows: list[list[str]]) -> str:
    if not rows:
        return "_(no data yet)_\n"
    head = "| " + " | ".join(headers) + " |"
    sep = "| " + " | ".join("---" for _ in headers) + " |"
    body = "\n".join("| " + " | ".join(str(cell) for cell in row) + " |" for row in rows)
    return f"{head}\n{sep}\n{body}\n"
