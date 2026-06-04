"""Canonical output and config paths for the launch control tower."""

from __future__ import annotations

import os
from pathlib import Path

# Repo root = parent of this package directory.
REPO_ROOT = Path(__file__).resolve().parent.parent

# ── Config & data ────────────────────────────────────────────────────────────
CONFIG_DIR = REPO_ROOT / "config"
DATA_DIR = REPO_ROOT / "data"
CRM_SCHEMA = CONFIG_DIR / "crm_pipeline_schema.json"
MEDIA_CALENDAR_CONFIG = CONFIG_DIR / "media_social_calendar.json"
SEED_LEADS = DATA_DIR / "commercial_seed_leads.example.jsonl"

# ── Output roots ─────────────────────────────────────────────────────────────
OUTPUTS_DIR = REPO_ROOT / "outputs"
COMMERCIAL_OUT = OUTPUTS_DIR / "commercial_launch"
MEDIA_OUT = OUTPUTS_DIR / "media_social"
FINAL_CONTROL_OUT = OUTPUTS_DIR / "final_launch_control"

# Stable "latest" pointer (a real directory copy, not a symlink, so it is
# portable across CI runners and committable).
COMMERCIAL_LATEST = COMMERCIAL_OUT / "latest"


def ensure_dirs() -> None:
    """Create all output directories if they do not exist."""
    for d in (OUTPUTS_DIR, COMMERCIAL_OUT, MEDIA_OUT, FINAL_CONTROL_OUT, COMMERCIAL_LATEST):
        d.mkdir(parents=True, exist_ok=True)


def latest_dir() -> Path:
    """Return the directory holding the most recent commercial launch run.

    Prefers an explicit ``latest`` directory; falls back to the most recent
    timestamped run directory.
    """
    if COMMERCIAL_LATEST.exists() and any(COMMERCIAL_LATEST.iterdir()):
        return COMMERCIAL_LATEST
    if COMMERCIAL_OUT.exists():
        runs = sorted(
            (p for p in COMMERCIAL_OUT.iterdir() if p.is_dir() and p.name != "latest"),
            key=lambda p: p.name,
        )
        if runs:
            return runs[-1]
    return COMMERCIAL_LATEST


def rel(path: Path) -> str:
    """Return a repo-relative POSIX path string for stable reporting."""
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return os.fspath(path)
