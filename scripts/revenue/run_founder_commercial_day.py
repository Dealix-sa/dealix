#!/usr/bin/env python3
"""Founder commercial day planner for Dealix.

Draft-only and manual-review only.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "reports" / "go_live" / "FOUNDER_COMMERCIAL_DAY.md"

ACTIONS = [
    "Research 20 Saudi B2B companies.",
    "Verify 10 targets with website/source_url.",
    "Create 5 respectful Arabic drafts.",
    "Founder reviews every draft.",
    "Send manually only after review.",
    "Book diagnostic calls.",
]


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("# Founder Commercial Day\n\n" + "\n".join(f"- {a}" for a in ACTIONS) + "\n", encoding="utf-8")
    print("FOUNDER_COMMERCIAL_DAY_READY")
    print(OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
