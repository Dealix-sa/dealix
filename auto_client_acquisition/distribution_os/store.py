"""Distribution OS persistence — JSONL stores with env-overridable paths.

Paths default under the repo's ``data/`` tree but can be redirected with env
vars (tests point them at ``tmp_path``). Runtime ``.jsonl`` files stay
git-ignored; only the synthetic ``prospects.example.json`` seed is tracked.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]


def _resolve(env_var: str, default_rel: str) -> Path:
    override = os.environ.get(env_var)
    return Path(override) if override else (REPO_ROOT / default_rel)


def prospects_path() -> Path:
    """Input prospects. Prefers a live ``prospects.json``; falls back to the seed."""
    override = os.environ.get("DEALIX_DISTRIBUTION_PROSPECTS_PATH")
    if override:
        return Path(override)
    live = REPO_ROOT / "data" / "distribution" / "prospects.json"
    if live.exists():
        return live
    return REPO_ROOT / "data" / "distribution" / "prospects.example.json"


def drafts_path() -> Path:
    return _resolve("DEALIX_DISTRIBUTION_DRAFTS_PATH", "data/drafts/drafts.jsonl")


def followups_path() -> Path:
    return _resolve("DEALIX_DISTRIBUTION_FOLLOWUPS_PATH", "data/followups/followups.jsonl")


def proposals_dir() -> Path:
    return _resolve("DEALIX_DISTRIBUTION_PROPOSALS_DIR", "data/proposals")


def reports_dir() -> Path:
    return _resolve("DEALIX_DISTRIBUTION_REPORTS_DIR", "reports/distribution")


def read_json(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = "\n".join(json.dumps(r, ensure_ascii=False, sort_keys=True) for r in rows)
    path.write_text(payload + ("\n" if rows else ""), encoding="utf-8")
    return path


def write_text(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
    return path


__all__ = [
    "REPO_ROOT",
    "drafts_path",
    "followups_path",
    "proposals_dir",
    "prospects_path",
    "read_json",
    "read_jsonl",
    "reports_dir",
    "write_jsonl",
    "write_text",
]
