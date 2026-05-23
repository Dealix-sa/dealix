#!/usr/bin/env python3
"""Verify Dealix product ladder and distribution mapping."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

PRODUCT_DOCS = [
    "docs/product/DEALIX_PRODUCT_LADDER.md",
    "docs/product/PRODUCT_DISTRIBUTION_OS.md",
    "docs/product/PRODUCT_POSITIONING.md",
    "docs/product/OFFER_PACKAGING.md",
    "docs/product/PRICING_GUARDRAILS.md",
]

LADDER_CSV = "data/private_ops_seed/product/offer_ladder.csv"
DIST_CSV = "data/private_ops_seed/product/product_distribution.csv"

REQUIRED_RUNGS = {
    1: "Free Sample / Diagnostic",
    2: "Revenue Sprint",
    3: "Managed Pilot",
    4: "Revenue Desk Retainer",
    5: "Founder Console",
    6: "Enterprise Revenue Intelligence OS",
    7: "Partner / White-label Revenue OS",
}

BANNED = [
    r"guarantee[d]?\s+(revenue|sales|leads|results|pipeline|roi)",
    r"\d+x\s+(your|in)\s+(sales|revenue|pipeline|leads|growth)",
    r"fully\s+autonomous\s+(outbound|sales|sending|posting)",
]


def main() -> int:
    failures: list[str] = []
    passes: list[str] = []
    for rel in PRODUCT_DOCS + [LADDER_CSV, DIST_CSV]:
        p = REPO_ROOT / rel
        if not p.exists() or p.stat().st_size == 0:
            failures.append(f"missing: {rel}")
        else:
            passes.append(rel)

    # Ladder CSV shape
    p = REPO_ROOT / LADDER_CSV
    if p.exists():
        with p.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            seen = set()
            for row in reader:
                rung = int(row["rung"])
                seen.add(rung)
                expected = REQUIRED_RUNGS.get(rung)
                if expected and expected.lower() not in row["name"].lower():
                    failures.append(
                        f"offer_ladder rung {rung} name '{row['name']}' does not match expected '{expected}'"
                    )
            for rung in REQUIRED_RUNGS:
                if rung not in seen:
                    failures.append(f"offer_ladder missing rung {rung}")

    # Banned voice
    for rel in PRODUCT_DOCS:
        p = REPO_ROOT / rel
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        for pattern in BANNED:
            for m in re.finditer(pattern, text, flags=re.IGNORECASE):
                snippet = text[max(0, m.start() - 60): m.end() + 60].replace("\n", " ")
                if "❌" in snippet or "Banned" in snippet or "banned" in snippet or "Forbidden" in snippet or "forbidden" in snippet.lower() or "```" in snippet or "regex" in snippet.lower():
                    continue
                failures.append(f"banned voice in {rel}: …{snippet}…")

    print("=== Dealix Product Distribution Verifier ===")
    print(f"checks passed: {len(passes)}")
    if failures:
        for f in failures:
            print(f"  - {f}")
        print("\nVERDICT: FAIL")
        return 1
    print("\nVERDICT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
