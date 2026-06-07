#!/usr/bin/env python3
"""Dealix MRR forecast — توقّع الدخل الشهري المتكرر.

Reads ``finance/mrr_targets.yml`` and reports each milestone's package mix, the
implied MRR, ARR, and the funnel math to ~500k. Also validates that each
milestone's stated ``target_mrr`` matches the sum of its ``mix`` lines.

Usage:
  python scripts/generate_mrr_forecast.py
  python scripts/generate_mrr_forecast.py --json
  python scripts/generate_mrr_forecast.py --milestone mrr_100k

Terminal markers:
  MRR_FORECAST_OK
  MRR_FORECAST_MISMATCH   -> a milestone's target_mrr != sum(mix)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

_REPO = Path(__file__).resolve().parents[1]
_TARGETS = _REPO / "finance" / "mrr_targets.yml"


def _load(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"missing config: {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def summarize(targets: dict) -> dict:
    out = {"milestones": [], "all_consistent": True}
    for ms in targets.get("milestones", []):
        mix = ms.get("mix", [])
        computed = sum(int(line.get("mrr", 0)) for line in mix)
        stated = int(ms.get("target_mrr", 0))
        consistent = computed == stated
        if not consistent:
            out["all_consistent"] = False
        out["milestones"].append({
            "id": ms.get("id"),
            "name": ms.get("name"),
            "target_mrr": stated,
            "computed_mrr": computed,
            "arr": stated * 12,
            "consistent": consistent,
            "mix": [
                {
                    "package": line.get("package"),
                    "count": line.get("count"),
                    "mrr": line.get("mrr"),
                }
                for line in mix
            ],
        })
    return out


def _print_human(summary: dict, targets: dict, only: str | None) -> None:
    for ms in summary["milestones"]:
        if only and ms["id"] != only:
            continue
        flag = "OK" if ms["consistent"] else "MISMATCH"
        print(f"\n=== {ms['name']} ({ms['id']}) — {flag} ===")
        print(f"  Target MRR : {ms['target_mrr']:,} SAR")
        if not ms["consistent"]:
            print(f"  Computed   : {ms['computed_mrr']:,} SAR  <-- mix sum differs")
        print(f"  Implied ARR: {ms['arr']:,} SAR")
        print("  Mix:")
        for line in ms["mix"]:
            print(f"    - {line['count']:>2} x {line['package']:<22} = {int(line['mrr'] or 0):>9,} SAR")

    if not only:
        funnel = targets.get("monthly_funnel_to_500k")
        if funnel:
            print("\n=== Monthly funnel to ~500k (cash + MRR) ===")
            for k in ("companies_researched", "controlled_outreach", "replies",
                      "calls", "proposals", "audits", "pilots", "production",
                      "new_retainers"):
                if k in funnel:
                    print(f"  {k:<22}: {funnel[k]:,}")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Dealix MRR forecast")
    p.add_argument("--json", action="store_true", help="emit JSON")
    p.add_argument("--milestone", help="show a single milestone id (e.g. mrr_100k)")
    args = p.parse_args(argv)

    targets = _load(_TARGETS)
    summary = summarize(targets)

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        _print_human(summary, targets, args.milestone)

    if summary["all_consistent"]:
        print("\nMRR_FORECAST_OK")
        return 0
    print("\nMRR_FORECAST_MISMATCH", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
