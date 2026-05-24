#!/usr/bin/env python3
"""
verify_brand_system.py — minimal brand surface check.

Asserts:
  - apps/web/lib/brand-tokens.ts exists and exports a tokens object.
  - apps/web/components/founder-shell.tsx exists.

Brand assets (assets/brand/) are optional in this session; the verifier
emits a WARN if absent, not a FAIL.

Exit: 0 PASS / 1 FAIL.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    ROOT / "apps" / "web" / "lib" / "brand-tokens.ts",
    ROOT / "apps" / "web" / "components" / "founder-shell.tsx",
]
OPTIONAL = [
    ROOT / "assets" / "brand",
]


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []

    for p in REQUIRED:
        if not p.exists():
            failures.append(f"missing: {p.relative_to(ROOT)}")

    tokens = REQUIRED[0]
    if tokens.exists():
        text = tokens.read_text(encoding="utf-8")
        if "export const" not in text and "export default" not in text:
            failures.append(f"{tokens.relative_to(ROOT)}: no exported tokens")

    for p in OPTIONAL:
        if not p.exists():
            warnings.append(f"optional missing: {p.relative_to(ROOT)}")

    verdict = "PASS" if not failures else "FAIL"
    print(f"BRAND_SYSTEM={verdict.lower()}")
    print(f"BRAND_SYSTEM_FAILS={len(failures)}")
    print(f"BRAND_SYSTEM_WARNS={len(warnings)}")
    if failures:
        print("\n## Brand FAILURES")
        for f in failures:
            print(f"  - {f}")
    if warnings:
        print("\n## Brand WARNINGS")
        for w in warnings:
            print(f"  - {w}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
