#!/usr/bin/env python3
"""Commercial Launch readiness gate — single Go/No-Go report.

Usage:
    python scripts/commercial_launch_readiness.py
    python scripts/commercial_launch_readiness.py --target 400
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_launch.readiness import (  # noqa: E402
    evaluate_readiness,
    write_readiness,
)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Commercial Launch readiness gate")
    ap.add_argument("--target", type=int, default=400)
    ap.add_argument("--no-generation", action="store_true", help="Skip the draft-factory check")
    ap.add_argument("--json", action="store_true", help="Print full JSON")
    args = ap.parse_args(argv)

    report = evaluate_readiness(target=args.target, run_generation=not args.no_generation)
    write_readiness(report)

    if args.json:
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    else:
        for c in report.checks:
            mark = "PASS" if c.passed else "FAIL"
            print(f"[readiness][{mark}] {c.name}: {c.detail}")
        print("[readiness] go_no_go:")
        for k, v in report.go_no_go.items():
            print(f"    - {k}: {v}")

    if not report.passed:
        print("[readiness][FAIL] launch readiness gate FAILED", file=sys.stderr)
        return 1
    print("[readiness][OK] launch readiness gate PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
