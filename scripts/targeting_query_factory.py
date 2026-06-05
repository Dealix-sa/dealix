#!/usr/bin/env python3
"""
targeting_query_factory.py — builds research queries for the Discovery Engine.

Combines sectors.yml × cities.yml (filtered by rollout phase) with hand-curated
queries from queries.txt to produce a deduplicated query list. These are
*research* queries against allowed public sources only — they never trigger
outreach. The actual fetching layer must respect robots.txt and site terms.

Usage:
    python scripts/targeting_query_factory.py --phase 1 --limit 80
    python scripts/targeting_query_factory.py --phase 1 --out data/targeting/out/queries.generated.txt
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import yaml  # noqa: E402

DATA = _ROOT / "data" / "targeting"


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def load_sectors(phase: int | None = None, path: Path | None = None) -> list[dict[str, Any]]:
    data = _load_yaml(path or DATA / "sectors.yml")
    rows = data.get("sectors", []) or []
    if phase is not None:
        rows = [r for r in rows if int(r.get("phase", 1)) <= phase]
    return sorted(rows, key=lambda r: int(r.get("priority", 5)))


def load_cities(phase: int | None = None, path: Path | None = None) -> list[dict[str, Any]]:
    data = _load_yaml(path or DATA / "cities.yml")
    rows = data.get("cities", []) or []
    if phase is not None:
        rows = [r for r in rows if int(r.get("phase", 1)) <= phase]
    return sorted(rows, key=lambda r: int(r.get("priority", 5)))


def load_seed_queries(path: Path | None = None) -> list[str]:
    path = path or DATA / "queries.txt"
    if not path.exists():
        return []
    out: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            out.append(line)
    return out


def build_queries(
    *,
    phase: int | None = 1,
    sectors: list[dict[str, Any]] | None = None,
    cities: list[dict[str, Any]] | None = None,
    seed_queries: list[str] | None = None,
    limit: int | None = None,
) -> list[str]:
    """Build a deduplicated, ordered query list.

    Order: curated seed queries first (highest intent), then generated
    sector×city queries by sector priority then city priority.
    """
    sectors = sectors if sectors is not None else load_sectors(phase)
    cities = cities if cities is not None else load_cities(phase)
    seed = seed_queries if seed_queries is not None else load_seed_queries()

    seen: set[str] = set()
    out: list[str] = []

    def _add(q: str) -> None:
        q = q.strip()
        key = q.lower()
        if q and key not in seen:
            seen.add(key)
            out.append(q)

    for q in seed:
        _add(q)

    for sec in sectors:
        kws = sec.get("keywords_ar") or [sec.get("name_ar", "")]
        for city in cities:
            city_ar = city.get("name_ar", "")
            for kw in kws:
                _add(f'"{kw} {city_ar}"')
            # one site-scoped proof-gap probe per sector/city
            _add(f'site:.sa "{sec.get("name_ar","")}" "{city_ar}" "تواصل معنا"')

    if limit is not None:
        out = out[:limit]
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Dealix Targeting OS query factory")
    ap.add_argument("--phase", type=int, default=1)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--out", default=None, help="write queries to this file")
    args = ap.parse_args(argv)

    queries = build_queries(phase=args.phase, limit=args.limit)
    text = "\n".join(queries)
    if args.out:
        outp = Path(args.out)
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text(text + "\n", encoding="utf-8")
        print(f"wrote {len(queries)} queries -> {outp}", file=sys.stderr)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
