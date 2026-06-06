#!/usr/bin/env python3
"""Verify that core Dealix positioning documents exist.

Checks a small set of positioning and offer documents under ``docs/`` and
``sales/``. Prints a PASS/FAIL table and a verdict. The exit code reflects the
result: 0 when all required documents are present, 1 otherwise. Documents are
allowed to be created by a parallel content process; absence is reported, not
crashed on.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

# Each item: (label, list of acceptable relative paths). The check passes for an
# item if at least one of the candidate paths exists, so the verifier tolerates
# minor naming differences between parallel content streams.
POSITIONING_DOCS: list[tuple[str, list[str]]] = [
    ("positioning_and_icp", ["docs/POSITIONING_AND_ICP.md"]),
    ("offer_ladder", ["docs/OFFER_LADDER.md", "docs/OFFER_LADDER_AND_PRICING.md"]),
    ("business_model", ["docs/BUSINESS_MODEL.md"]),
    ("competitive_positioning", ["docs/COMPETITIVE_POSITIONING.md"]),
    (
        "operating_constitution",
        ["docs/DEALIX_OPERATING_CONSTITUTION.md"],
    ),
    ("discovery_script", ["docs/sales/DISCOVERY_SCRIPT.md"]),
]


def _first_existing(candidates: list[str]) -> str | None:
    for rel in candidates:
        if (ROOT / rel).is_file():
            return rel
    return None


def check_positioning() -> dict[str, Any]:
    """Check every positioning document. Returns a structured result."""
    items: list[dict[str, Any]] = []
    missing: list[str] = []
    for label, candidates in POSITIONING_DOCS:
        found = _first_existing(candidates)
        ok = found is not None
        if not ok:
            missing.append(label)
        items.append(
            {
                "label": label,
                "status": "PASS" if ok else "FAIL",
                "path": found or "",
                "candidates": candidates,
            }
        )
    verdict = "PASS" if not missing else "FAIL"
    return {"items": items, "missing": missing, "verdict": verdict}


def _print_table(result: dict[str, Any]) -> None:
    print("== Dealix Positioning Verification ==")
    for item in result["items"]:
        path = item["path"] or "(missing)"
        print(f"  [{item['status']}] {item['label']}: {path}")
    if result["missing"]:
        print(f"Missing: {', '.join(result['missing'])}")
    print(f"Verdict: {result['verdict']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args(argv)

    result = check_positioning()
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        _print_table(result)
    return 0 if result["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
