#!/usr/bin/env python3
"""Validate a lead-intake JSONL file against the CRM schema.

Thin wrapper over the seed-leads validator so intake batches can be checked
with the same rules. Record-only: this never contacts a lead.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commercial_common import DATA_DIR
from commercial_seed_leads_validate import validate


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a lead-intake file.")
    parser.add_argument("--file", default=str(DATA_DIR / "commercial_seed_leads.example.jsonl"))
    args = parser.parse_args()

    errors = validate(Path(args.file))
    if errors:
        print("LEAD INTAKE VALIDATE: FAIL", file=sys.stderr)
        for e in errors[:25]:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print(f"LEAD INTAKE VALIDATE: PASS — {args.file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
