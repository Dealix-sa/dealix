#!/usr/bin/env python3
"""Seed the Saudi Opportunity Graph from the committed CSV.

Loads data/opportunity_graph/companies.seed.csv, scores + segments each row,
and persists them to the JSON store. Draft-only: no outreach is generated or
sent here. Safe to re-run — ids are stable and existing state is preserved.

Usage:
    python scripts/commercial/seed_saudi_opportunity_graph.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.opportunity_graph.collectors import load_seed_companies
from dealix.opportunity_graph.pipeline import score_and_segment
from dealix.opportunity_graph.store import get_store


def main() -> int:
    store = get_store()
    companies = load_seed_companies(store)
    scored = [score_and_segment(c) for c in companies]
    store.upsert_companies(scored)

    print(f"Seeded {len(scored)} companies into {store.data_dir}")
    by_class: dict[str, int] = {}
    for c in scored:
        by_class[c.score_class] = by_class.get(c.score_class, 0) + 1
    for cls in ("hot", "warm", "research", "not_fit"):
        print(f"  {cls:9s}: {by_class.get(cls, 0)}")
    print("Draft-only. No outreach generated or sent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
