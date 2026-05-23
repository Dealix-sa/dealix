#!/usr/bin/env python3
"""
verify_docs_complete.py — assert every required doc file exists and is non-empty.

Uses the manifest from scripts/generate_master_tree.py as source of truth.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from generate_master_tree import collect_public_manifest  # noqa: E402


MIN_DOC_BYTES = 30


def main() -> int:
    manifest = collect_public_manifest()
    missing: list[str] = []
    empty: list[str] = []

    for relative_dir, files in manifest.items():
        directory = REPO / relative_dir if relative_dir else REPO
        for filename in files:
            target = directory / filename
            if not target.exists():
                missing.append(str(target.relative_to(REPO)))
                continue
            if filename.endswith(".md") and target.stat().st_size < MIN_DOC_BYTES:
                empty.append(str(target.relative_to(REPO)))

    if missing:
        print(f"[FAIL] {len(missing)} files missing:")
        for m in missing[:20]:
            print(f"  - {m}")
        if len(missing) > 20:
            print(f"  ... {len(missing) - 20} more")
        return 1
    if empty:
        print(f"[FAIL] {len(empty)} docs are empty (< {MIN_DOC_BYTES} bytes):")
        for e in empty[:20]:
            print(f"  - {e}")
        return 1

    print(f"[OK] verify_docs_complete: {sum(len(v) for v in manifest.values())} files present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
