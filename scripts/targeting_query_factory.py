#!/usr/bin/env python3
"""Query factory — generates ALLOWED research queries (you run them manually).

Dealix does not auto-search or scrape. This factory produces a list of honest,
robots-respecting search queries the founder (or a VA) runs by hand against
public sources: official sites, services/clients/case-study pages, jobs pages,
news, and public directories. The output is a checklist, not an automation.

Queries are built by crossing sectors × cities × intent modifiers from the
targeting config.

Usage:
    python scripts/targeting_query_factory.py --per-sector 6 --out data/targeting/out
"""
from __future__ import annotations

import argparse
from pathlib import Path

from scripts.targeting_common import OUT_DIR, load_cities, load_sectors

# Intent modifiers — phrasing that surfaces companies with observable signals,
# all from public, non-login sources.
INTENT_MODIFIERS = [
    ("case studies", "دراسات حالة"),
    ("our clients", "عملاؤنا"),
    ("careers hiring", "وظائف توظيف"),
    ("services", "خدماتنا"),
    ("press news", "أخبار"),
    ("partners", "شركاء"),
]


def generate_queries(per_sector: int = 6) -> list[dict[str, str]]:
    """Cross sectors × cities × intent into a deduped query list."""
    sectors = load_sectors()
    cities = load_cities()
    queries: list[dict[str, str]] = []
    seen: set[str] = set()
    for skey, sval in sectors.items():
        # Skip sensitive sectors in the default factory run — they need review.
        if sval.get("sensitive"):
            continue
        sname = sval.get("name_en", skey)
        count = 0
        for ckey, cval in cities.items():
            if ckey == "other":
                continue
            for mod_en, mod_ar in INTENT_MODIFIERS:
                if count >= per_sector:
                    break
                q = f'"{sname}" {cval.get("name_en", ckey)} {mod_en} Saudi'
                if q in seen:
                    continue
                seen.add(q)
                queries.append({
                    "sector": skey,
                    "city": ckey,
                    "query_en": q,
                    "query_ar": f'{sval.get("name_ar", skey)} {cval.get("name_ar", ckey)} {mod_ar}',
                    "source_note": "public web only — respect robots.txt, no login, no scraping",
                })
                count += 1
            if count >= per_sector:
                break
    return queries


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Dealix research query factory (manual run)")
    ap.add_argument("--per-sector", type=int, default=6)
    ap.add_argument("--out", dest="outdir", default=str(OUT_DIR))
    args = ap.parse_args(argv)

    queries = generate_queries(args.per_sector)
    out_dir = Path(args.outdir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "research_queries.md"
    lines = [
        "# Research Queries — RUN MANUALLY (no automation, no scraping)\n",
        "> Respect robots.txt and source terms. Public pages only. "
        "Manual LinkedIn visits allowed; no LinkedIn automation.\n",
    ]
    for i, q in enumerate(queries, 1):
        lines.append(f"{i}. `{q['query_en']}`  \n   - AR: {q['query_ar']}  \n   - {q['source_note']}")
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"queries={len(queries)} → {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
