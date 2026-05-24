#!/usr/bin/env python3
"""verify_market_attack_system.py — verify market_attack templates index.

Per Article 13 and Doctrine Lock, the market_attack surface contains
TEMPLATES only — never claims. The verifier asserts presence of
template files and refuses any claim-shaped headers.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "market_attack" / "INDEX.md"
REQUIRED = [
    ROOT / "docs" / "market_attack" / "BEACHHEAD_TEMPLATE.md",
    ROOT / "docs" / "market_attack" / "STRATEGIC_ACCOUNTS_TEMPLATE.md",
    ROOT / "docs" / "market_attack" / "OFFER_MARKET_FIT_TEMPLATE.md",
]
BANNED_CLAIM = re.compile(r"\b(guaranteed|نضمن|مضمون|قطعي)\b", re.I)


def main() -> int:
    failures: list[str] = []
    if not INDEX.exists():
        failures.append(f"missing index: {INDEX.relative_to(ROOT)}")
    for p in REQUIRED:
        if not p.exists():
            failures.append(f"missing template: {p.relative_to(ROOT)}")
            continue
        text = p.read_text(encoding="utf-8")
        if BANNED_CLAIM.search(text):
            failures.append(f"{p.relative_to(ROOT)}: contains banned claim word")
    verdict = "PASS" if not failures else "FAIL"
    print(f"MARKET_ATTACK_SYSTEM={verdict.lower()}")
    print(f"MARKET_ATTACK_SYSTEM_FAILS={len(failures)}")
    if failures:
        print("\n## Market-Attack FAILURES")
        for f in failures:
            print(f"  - {f}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
