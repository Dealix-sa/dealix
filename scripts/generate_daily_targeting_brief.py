#!/usr/bin/env python3
"""Generate the Daily Targeting Brief (governed, draft-only) from declared inputs.

Loads operator-declared companies from a YAML file (filled from your own CRM /
network — never scraped), builds deterministic dossiers, ranks by priority, and
writes a bilingual markdown + JSON brief. All outreach is draft-only.

Usage:
    python3 scripts/generate_daily_targeting_brief.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from auto_client_acquisition.revenue_os.daily_targeting_brief import (
    build_daily_targeting_brief,
    load_target_companies,
    render_brief_markdown,
)

_DEFAULT_INPUT = "docs/commercial/operations/targeting/target_companies_seed.yaml"
_DEFAULT_OUT_DIR = "data/founder_briefs/targeting"


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate the Daily Targeting Brief.")
    parser.add_argument("--input", default=_DEFAULT_INPUT, help="Path to companies YAML.")
    parser.add_argument("--top-n", type=int, default=10, help="Number of targets to show.")
    parser.add_argument("--date", default=None, help="ISO date for the brief (YYYY-MM-DD).")
    parser.add_argument(
        "--dry-run", action="store_true", help="Print summary only; do not write files."
    )
    parser.add_argument("--out-dir", default=_DEFAULT_OUT_DIR, help="Output directory.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    input_path = (REPO_ROOT / args.input) if not Path(args.input).is_absolute() else Path(args.input)

    companies = load_target_companies(str(input_path))
    brief_date = args.date or date.today().isoformat()
    brief = build_daily_targeting_brief(
        companies, top_n=args.top_n, date_iso=brief_date
    )

    if args.dry_run:
        print(f"Input: {input_path}")
        print(f"Date: {brief['date']}")
        print(f"Total targets: {brief['total_targets']} · Shown: {brief['shown']}")
        print(f"Summary: {json.dumps(brief['summary'], ensure_ascii=False)}")
        print(f"Governance: {brief['governance_footer_en']}")
        print("DEALIX_TARGETING_BRIEF=OK")
        return 0

    out_dir = (REPO_ROOT / args.out_dir) if not Path(args.out_dir).is_absolute() else Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / f"{brief['date']}_targeting_brief.md"
    json_path = out_dir / f"{brief['date']}_targeting_brief.json"

    md_path.write_text(render_brief_markdown(brief), encoding="utf-8")
    json_path.write_text(
        json.dumps(brief, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"Wrote: {md_path}")
    print(f"Wrote: {json_path}")
    print("DEALIX_TARGETING_BRIEF=OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
