#!/usr/bin/env python3
"""Read-only import auditor for the auto_client_acquisition package.

Counts how many *external* Python files reference each top-level submodule of
``auto_client_acquisition/`` (imports that originate outside that submodule's
own directory). Used to separate the canonical / imported-peripheral modules
from genuinely orphaned scaffolding before any archival — see
``docs/architecture/CANONICAL_MAP.md``.

Usage:
    python3 scripts/audit_module_imports.py            # full table
    python3 scripts/audit_module_imports.py --orphans  # only zero-ref modules
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PKG = "auto_client_acquisition"
PKG_DIR = REPO_ROOT / PKG


def submodules() -> list[str]:
    return sorted(
        p.name for p in PKG_DIR.iterdir()
        if p.is_dir() and not p.name.startswith(("_", "."))
    )


def _ref_pattern(mod: str) -> re.Pattern[str]:
    # Matches `from auto_client_acquisition.<mod>...`, `import a_c_a.<mod>`,
    # and the bare dotted string "auto_client_acquisition.<mod>" (dynamic).
    return re.compile(rf"{re.escape(PKG)}(?:\.|\s+import\s+){re.escape(mod)}\b")


def count_external_refs(mod: str) -> tuple[int, list[str]]:
    pat = _ref_pattern(mod)
    own_prefix = f"{PKG}/{mod}/"
    hits: list[str] = []
    for py in REPO_ROOT.rglob("*.py"):
        rel = py.relative_to(REPO_ROOT).as_posix()
        if rel.startswith(own_prefix) or "/.venv/" in f"/{rel}":
            continue
        try:
            if pat.search(py.read_text(encoding="utf-8")):
                hits.append(rel)
        except Exception:
            continue
    return len(hits), hits


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit auto_client_acquisition imports")
    ap.add_argument("--orphans", action="store_true", help="show only zero-reference modules")
    args = ap.parse_args()

    rows = [(mod, *count_external_refs(mod)) for mod in submodules()]
    rows.sort(key=lambda r: r[1])  # ascending by ref count

    orphans = [m for m, n, _ in rows if n == 0]
    if args.orphans:
        for m in orphans:
            print(m)
        return 0

    print(f"{'module':40} external_refs")
    print("-" * 56)
    for mod, n, _ in rows:
        print(f"{mod:40} {n}")
    print("-" * 56)
    print(f"total modules: {len(rows)} | orphans (0 refs): {len(orphans)}")
    if orphans:
        print("orphans:", ", ".join(orphans))
    return 0


if __name__ == "__main__":
    sys.exit(main())
