"""JSONL persistence for the Market Production OS.

Runtime stores default under ``data/<area>/<name>.jsonl`` (gitignored — runtime
data is not committed) and are overridable per-store with a ``DEALIX_*_PATH``
env var. Committed synthetic seeds live in ``seeds/<name>.seed.jsonl`` next to
this package and are loaded as a fallback when the runtime store is empty.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Iterable

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SEEDS_DIR = Path(__file__).resolve().parent / "seeds"

# store name -> (default relative path, env override var)
_STORES: dict[str, tuple[str, str]] = {
    "prospects": ("data/prospects/prospects.jsonl", "DEALIX_PROSPECTS_PATH"),
    "drafts": ("data/outreach/drafts.jsonl", "DEALIX_OUTREACH_DRAFTS_PATH"),
    "sending_batches": ("data/outreach/sending_batches.jsonl", "DEALIX_SENDING_BATCHES_PATH"),
    "suppression": ("data/outreach/suppression_list.jsonl", "DEALIX_SUPPRESSION_PATH"),
    "replies": ("data/outreach/replies.jsonl", "DEALIX_REPLIES_PATH"),
    "email_accounts": ("data/outreach/email_accounts.jsonl", "DEALIX_EMAIL_ACCOUNTS_PATH"),
    "job_signals": ("data/signals/job_signals.jsonl", "DEALIX_JOB_SIGNALS_PATH"),
    "post_ideas": ("data/content/post_ideas.jsonl", "DEALIX_POST_IDEAS_PATH"),
    "partners": ("data/partners/partners.jsonl", "DEALIX_PARTNERS_PATH"),
}


def store_path(name: str) -> Path:
    if name not in _STORES:
        raise KeyError(f"unknown store: {name}")
    default_rel, env_var = _STORES[name]
    raw = os.environ.get(env_var, "").strip()
    path = Path(raw) if raw else _REPO_ROOT / default_rel
    if not path.is_absolute():
        path = _REPO_ROOT / path
    return path


def seed_path(name: str) -> Path:
    return _SEEDS_DIR / f"{name}.seed.jsonl"


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    out: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def read_seed(name: str) -> list[dict[str, Any]]:
    return _read_jsonl(seed_path(name))


def read_all(name: str) -> list[dict[str, Any]]:
    """Runtime store contents (empty list if the store does not exist yet)."""
    return _read_jsonl(store_path(name))


def load(name: str) -> list[dict[str, Any]]:
    """Runtime store if it has records, else the committed seed fallback."""
    records = read_all(name)
    return records if records else read_seed(name)


def append(name: str, record: dict[str, Any]) -> Path:
    path = store_path(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    return path


def write_all(name: str, records: Iterable[dict[str, Any]]) -> Path:
    path = store_path(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for record in records:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    return path
