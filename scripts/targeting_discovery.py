#!/usr/bin/env python3
"""Discovery — assemble raw candidates from ALLOWED, manually-collected seeds.

This is the Market Discovery stage (Phase A). It does NOT browse the web, scrape,
or call any search API. It consolidates seed lists the founder/VA collected by
hand from allowed public sources, tags each with its source, and emits a single
raw candidate file for the normalizer.

The "400/day" target is a research volume goal for the human-driven collection;
this script just consolidates whatever seeds exist and reports the count so the
founder can see how close they are.

Usage:
    python scripts/targeting_discovery.py \\
        --seeds data/targeting/company_seed_template.csv \\
        --out data/targeting/out/raw_candidates.jsonl
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from scripts.targeting_common import OUT_DIR, load_companies, normalize_record

DAILY_TARGET = 400


def consolidate(seed_paths: list[Path]) -> list[dict[str, Any]]:
    """Read all seed files and return normalized raw candidates, source-tagged."""
    candidates: list[dict[str, Any]] = []
    for path in seed_paths:
        if not path.exists():
            continue
        for rec in load_companies(path):
            rec = normalize_record(rec)
            rec.setdefault("discovery_source", path.name)
            candidates.append(rec)
    return candidates


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Dealix market discovery (seed consolidation)")
    ap.add_argument("--seeds", nargs="+", required=True, help="seed CSV/JSONL paths")
    ap.add_argument("--out", dest="outfile", default=str(OUT_DIR / "raw_candidates.jsonl"))
    args = ap.parse_args(argv)

    candidates = consolidate([Path(p) for p in args.seeds])
    out_path = Path(args.outfile)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fh:
        for rec in candidates:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")

    pct = round(100 * len(candidates) / DAILY_TARGET) if DAILY_TARGET else 0
    print(f"raw_candidates={len(candidates)} ({pct}% of daily target {DAILY_TARGET}) → {out_path}")
    print(
        "Next: python scripts/targeting_normalizer.py --in",
        out_path,
        "--out data/targeting/company_master.jsonl",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
