#!/usr/bin/env python3
"""Measure the source payload that remains after Dealix Vercel exclusions.

This is a source-input budget, not a claim about Vercel's final dependency
bundle.  The final uncompressed function size must be read from Preview logs.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {
    ".agents",
    ".git",
    ".github",
    "apps/web",
    "frontend",
    "presentations",
    "reports",
    "tests",
}
EXCLUDED_SUFFIXES = {".pyc", ".tar.xz", ".zip"}
SOURCE_BUDGET_BYTES = 60 * 1024 * 1024


def _relative_directory_is_excluded(path: Path) -> bool:
    relative = path.relative_to(ROOT).as_posix()
    return any(relative == item or relative.startswith(f"{item}/") for item in EXCLUDED_DIRS)


def _suffix_is_excluded(path: Path) -> bool:
    name = path.name.lower()
    return any(name.endswith(suffix) for suffix in EXCLUDED_SUFFIXES)


def measure() -> dict[str, int | bool]:
    repository_bytes = 0
    excluded_bytes = 0
    included_bytes = 0
    included_files = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.is_symlink():
            continue
        size = path.stat().st_size
        repository_bytes += size
        if _relative_directory_is_excluded(path) or _suffix_is_excluded(path):
            excluded_bytes += size
            continue
        included_bytes += size
        included_files += 1
    return {
        "repository_bytes": repository_bytes,
        "excluded_bytes": excluded_bytes,
        "included_source_bytes": included_bytes,
        "included_files": included_files,
        "source_budget_bytes": SOURCE_BUDGET_BYTES,
        "within_source_budget": included_bytes <= SOURCE_BUDGET_BYTES,
    }


def main() -> int:
    result = measure()
    print(json.dumps(result, indent=2, sort_keys=True))
    print(
        "VERCEL_SOURCE_PAYLOAD_BUDGET="
        + ("PASS" if result["within_source_budget"] else "FAIL")
    )
    print("FINAL_FUNCTION_SIZE_REQUIRES_PREVIEW_LOG=1")
    return 0 if result["within_source_budget"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
