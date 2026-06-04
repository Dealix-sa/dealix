#!/usr/bin/env python3
"""Validate the commercial seed-lead JSONL file.

Works even when no real lead file exists (placeholder mode is allowed). Only
fails on malformed rows that ARE present.

Usage:
    python scripts/commercial_seed_leads_validate.py
    python scripts/commercial_seed_leads_validate.py --leads data/commercial_seed_leads.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_launch.leads import (  # noqa: E402
    default_lead_path,
    validate_lead_file,
)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Validate commercial seed leads")
    ap.add_argument("--leads", type=str, default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    path = Path(args.leads) if args.leads else default_lead_path()
    if not path.is_absolute():
        path = ROOT / path

    result = validate_lead_file(path)
    if args.json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(f"[leads] path={result.path} exists={result.file_exists}")
        print(f"[leads] total={result.total} valid={result.valid} passed={result.passed}")
        for w in result.warnings:
            print(f"[leads][warn] {w}")
        for e in result.errors:
            print(f"[leads][error] {e}")

    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
