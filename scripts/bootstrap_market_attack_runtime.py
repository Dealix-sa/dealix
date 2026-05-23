#!/usr/bin/env python3
"""Seed the runtime PRIVATE_OPS tree with Market Attack bootstrap CSVs.

Idempotent: only copies a file if the runtime path does not exist yet.
Never overwrites live operator data.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from market_attack_common import (  # type: ignore[import-not-found]
    BOOTSTRAP_ROOT,
    private_ops_root,
)


def main() -> int:
    priv = private_ops_root()
    priv.mkdir(parents=True, exist_ok=True)
    copied = 0
    skipped = 0
    for src in BOOTSTRAP_ROOT.rglob("*.csv"):
        rel = src.relative_to(BOOTSTRAP_ROOT)
        dst = priv / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists():
            print(f"skip (exists): {dst}")
            skipped += 1
            continue
        shutil.copy2(src, dst)
        print(f"copied: {src} -> {dst}")
        copied += 1
    print()
    print(f"Done. copied={copied} skipped={skipped} root={priv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
