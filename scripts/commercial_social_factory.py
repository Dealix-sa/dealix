#!/usr/bin/env python3
"""Generate the daily Social & Media review-only queue.

REVIEW-ONLY. Never posts, schedules, or spends. Produces a founder-review
marketing bundle under outputs/commercial_launch/<date>/.

Usage:
    python scripts/commercial_social_factory.py
    python scripts/commercial_social_factory.py --target 120 --date 2026-06-04
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_launch.safety import (  # noqa: E402
    audit_outputs_dir,
    write_safety_audit,
)
from dealix.commercial_launch.social import (  # noqa: E402
    generate_social,
    load_social_config,
    write_social_outputs,
)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Generate the daily social/media review queue")
    ap.add_argument("--target", type=int, default=None, help="Optional higher total post target")
    ap.add_argument("--date", type=str, default=None)
    ap.add_argument("--seed", type=int, default=None)
    args = ap.parse_args(argv)

    run_date = args.date or date.today().isoformat()
    cfg = load_social_config()
    minimum = cfg["total_minimum"]

    result = generate_social(target=args.target, seed=args.seed, run_date=run_date)
    paths = write_social_outputs(result)

    report = audit_outputs_dir(run_date)
    write_safety_audit(report, run_date)

    print(f"[social] run_date={run_date} accepted={result.total_accepted} rejected={len(result.rejected)} min={minimum}")
    for name, p in paths.items():
        print(f"[social] {name} -> {p}")
    for w in result.warnings:
        print(f"[social][warn] {w}")
    print(f"[social] safety_passed={report.passed} (findings={len(report.findings)}, "
          f"violations={len(report.draft_violations)})")

    if result.total_accepted < minimum:
        print(f"[social][FAIL] target not met: {result.total_accepted} < {minimum}", file=sys.stderr)
        return 1
    if not report.passed:
        print("[social][FAIL] safety audit failed", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
