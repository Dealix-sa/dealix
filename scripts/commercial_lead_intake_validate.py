#!/usr/bin/env python3
"""Lead intake validation gate (delegates to seed-leads validator by default).

Validates an inbound lead file against the CRM schema before it enters the
pipeline. Read-only; sends nothing.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from startup_os_common import DATA_DIR

# Reuse the seed-leads validator's logic.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from commercial_seed_leads_validate import validate


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", default=str(DATA_DIR / "commercial_seed_leads.example.jsonl"))
    args = ap.parse_args()
    r = validate(Path(args.path))
    if r["passed"]:
        print(f"Lead intake valid: {r['count']} records.")
        return 0
    print("Lead intake validation FAILED:")
    for e in r["errors"]:
        print(f"  - {e}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
