#!/usr/bin/env python3
"""Render the founder daily review bundle from an existing draft queue, or
generate fresh and render in one shot.

Usage:
    python scripts/commercial_founder_review_report.py            # generate + render today
    python scripts/commercial_founder_review_report.py --date 2026-06-04 --from-queue
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
    GenerationResult,
    OUTPUTS_DIR,
    generate_drafts,
    iter_jsonl,
    write_outputs,
)
from dealix.commercial_launch.review import write_review_bundle  # noqa: E402


def _load_from_queue(run_date: str) -> GenerationResult:
    out = OUTPUTS_DIR / run_date
    accepted = list(iter_jsonl(out / "draft_queue.jsonl"))
    rejected = list(iter_jsonl(out / "rejected_drafts.jsonl"))
    res = GenerationResult(run_date=run_date, accepted=accepted, rejected=rejected)
    res.used_real_leads = any(d.get("source_lead_id") for d in accepted)
    return res


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Founder daily review report")
    ap.add_argument("--date", type=str, default=None)
    ap.add_argument("--target", type=int, default=400)
    ap.add_argument("--from-queue", action="store_true", help="Render from an existing queue instead of generating")
    args = ap.parse_args(argv)

    run_date = args.date or date.today().isoformat()
    if args.from_queue:
        result = _load_from_queue(run_date)
        if not result.accepted:
            print(f"[review][FAIL] no draft_queue.jsonl for {run_date}", file=sys.stderr)
            return 1
    else:
        result = generate_drafts(target=args.target, run_date=run_date)
        write_outputs(result)

    paths = write_review_bundle(result)
    print(f"[review] run_date={run_date} drafts={result.total_accepted}")
    for name, p in paths.items():
        print(f"[review] {name} -> {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
