#!/usr/bin/env python3
"""Generate the daily founder-review-only draft queue (>= 400 drafts).

REVIEW-ONLY. This script NEVER sends anything. It produces drafts and the
full founder-review bundle under outputs/commercial_launch/<date>/.

Usage:
    python scripts/commercial_generate_400_drafts.py --target 400
    python scripts/commercial_generate_400_drafts.py --target 400 --leads data/commercial_seed_leads.jsonl
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_launch.engine import (  # noqa: E402
    generate_drafts,
    load_config,
    load_leads,
    write_outputs,
)
from dealix.commercial_launch.review import write_review_bundle  # noqa: E402
from dealix.commercial_launch.safety import (  # noqa: E402
    audit_outputs_dir,
    write_safety_audit,
)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Generate >=400 review-only drafts")
    ap.add_argument("--target", type=int, default=400)
    ap.add_argument("--leads", type=str, default=None, help="Path to a JSONL lead file (optional)")
    ap.add_argument("--date", type=str, default=None, help="Run date YYYY-MM-DD (default today)")
    ap.add_argument("--seed", type=int, default=None)
    args = ap.parse_args(argv)

    run_date = args.date or date.today().isoformat()
    cfg = load_config()
    leads = None
    if args.leads:
        lp = Path(args.leads)
        if not lp.is_absolute():
            lp = ROOT / lp
        leads = load_leads(lp)

    result = generate_drafts(target=args.target, config=cfg, leads=leads, seed=args.seed, run_date=run_date)

    write_outputs(result)
    write_review_bundle(result)

    # Safety audit over the freshly written queue.
    report = audit_outputs_dir(run_date)
    write_safety_audit(report, run_date)

    print(f"[commercial] run_date={run_date}")
    print(f"[commercial] accepted={result.total_accepted} rejected={len(result.rejected)} target={args.target}")
    print(f"[commercial] used_real_leads={result.used_real_leads}")
    for w in result.warnings:
        print(f"[commercial][warn] {w}")
    print(f"[commercial] safety_passed={report.passed} (findings={len(report.findings)}, "
          f"draft_violations={len(report.draft_violations)})")
    print(f"[commercial] outputs -> outputs/commercial_launch/{run_date}/")

    if result.total_accepted < args.target:
        print(f"[commercial][FAIL] target not met: {result.total_accepted} < {args.target}", file=sys.stderr)
        return 1
    if not report.passed:
        print("[commercial][FAIL] safety audit failed", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
