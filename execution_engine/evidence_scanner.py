from __future__ import annotations

"""Filesystem-level evidence helpers.

These helpers degrade gracefully when paths are missing — they never raise on
absent inputs, since the private ops directory is allowed to be empty.
"""

import csv
import subprocess
from pathlib import Path
from typing import Callable, Optional


def count_csv_rows(path: Path, filter_fn: Optional[Callable[[dict], bool]] = None) -> int:
    """Count non-header rows in a CSV.

    Returns 0 if the file does not exist or is unreadable.
    """
    path = Path(path)
    if not path.exists() or not path.is_file():
        return 0
    try:
        with path.open("r", encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            if filter_fn is None:
                return sum(1 for _ in reader)
            return sum(1 for row in reader if filter_fn(row))
    except (OSError, csv.Error):
        return 0


def count_files_in_dir(path: Path, pattern: str = "*") -> int:
    """Count files in `path` matching `pattern`; 0 if missing.

    Hidden files (dotfiles) are excluded.
    """
    path = Path(path)
    if not path.exists() or not path.is_dir():
        return 0
    return sum(
        1 for p in path.glob(pattern) if p.is_file() and not p.name.startswith(".")
    )


def latest_commit_in_path(path: Path) -> Optional[str]:
    """Return the latest git commit short-hash that touched `path`.

    Returns None if not a git repo, no commits, or git is unavailable.
    """
    path = Path(path)
    if not path.exists():
        return None
    try:
        # Use the repo root that owns `path`. We pass -C to git, which already
        # handles non-repo dirs by exiting non-zero.
        result = subprocess.run(
            ["git", "log", "-n", "1", "--format=%h", "--", str(path)],
            cwd=str(path.parent if path.is_file() else path),
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    sha = result.stdout.strip()
    return sha or None
