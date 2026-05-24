#!/usr/bin/env python3
"""
verify_non_empty_files.py — catches placeholder/empty files.

Walks every tracked .md/.py/.yaml/.yml under docs/, scripts/, evals/, policies/,
registries/ and reports anything below a meaningful size threshold. "Exists" is
not "done" — this verifier enforces that.

Excludes vendor/build dirs and the manifest itself.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MIN_DOC_BYTES = 200
MIN_SCRIPT_BYTES = 200
MIN_YAML_BYTES = 60

WATCHED_DIRS = ["docs", "scripts", "evals", "policies", "registries", "readiness"]

EXCLUDE_PARTS = {
    ".git", ".venv", "venv", "node_modules", "__pycache__", ".next", ".pytest_cache",
    "build", "dist", "htmlcov", ".mypy_cache", ".ruff_cache",
}

EXCLUDE_FILES = {
    "__init__.py",  # often legitimately empty
}


def is_excluded(p: Path) -> bool:
    parts = set(p.parts)
    if EXCLUDE_PARTS & parts:
        return True
    if p.name in EXCLUDE_FILES:
        return True
    return False


def min_for(p: Path) -> int:
    suf = p.suffix.lower()
    if suf == ".md":
        return MIN_DOC_BYTES
    if suf in {".yaml", ".yml"}:
        return MIN_YAML_BYTES
    if suf == ".py":
        return MIN_SCRIPT_BYTES
    return 1


def main() -> int:
    too_small: list[tuple[str, int, int]] = []
    scanned = 0

    for d in WATCHED_DIRS:
        base = ROOT / d
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if not p.is_file() or is_excluded(p):
                continue
            if p.suffix.lower() not in {".md", ".py", ".yaml", ".yml"}:
                continue
            scanned += 1
            min_size = min_for(p)
            try:
                size = len(p.read_text(encoding="utf-8", errors="ignore").strip())
            except Exception:
                continue
            if size < min_size:
                too_small.append((str(p.relative_to(ROOT)), size, min_size))

    if too_small:
        print(f"NON-EMPTY FILES: FAIL ({len(too_small)}/{scanned} below threshold)")
        for rel, size, min_size in too_small[:50]:
            print(f"  - {rel}: {size} bytes (need ≥ {min_size})")
        if len(too_small) > 50:
            print(f"  ... and {len(too_small) - 50} more")
        return 1
    print(f"NON-EMPTY FILES: PASS ({scanned} files scanned, all above threshold)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
