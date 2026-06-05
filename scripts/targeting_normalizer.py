#!/usr/bin/env python3
"""Normalizer — clean + dedupe raw candidates into the company master.

Takes a raw seed CSV/JSONL of candidates (manually collected), normalizes field
types, drops duplicates (by website host, else by lowercased name), and writes a
clean JSONL ready for the compliance gate + scorecard.

Usage:
    python scripts/targeting_normalizer.py \\
        --in data/targeting/company_seed_template.csv \\
        --out data/targeting/company_master.jsonl
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from scripts.targeting_common import COMPANY_MASTER, load_companies, normalize_record


def _dedupe_key(rec: dict[str, Any]) -> str:
    website = (rec.get("website") or "").strip().lower()
    if website:
        host = urlparse(website if "//" in website else f"//{website}").netloc or website
        return f"host:{host}"
    return f"name:{(rec.get('company_name') or '').strip().lower()}"


def normalize(records: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], int]:
    """Return (clean_records, duplicates_removed)."""
    seen: set[str] = set()
    clean: list[dict[str, Any]] = []
    dupes = 0
    for raw in records:
        rec = normalize_record(raw)
        if not (rec.get("company_name") or "").strip():
            continue
        key = _dedupe_key(rec)
        if key in seen:
            dupes += 1
            continue
        seen.add(key)
        clean.append(rec)
    return clean, dupes


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Dealix targeting normalizer (clean + dedupe)")
    ap.add_argument("--in", dest="infile", required=True)
    ap.add_argument("--out", dest="outfile", default=str(COMPANY_MASTER))
    args = ap.parse_args(argv)

    records = load_companies(Path(args.infile))
    clean, dupes = normalize(records)
    out_path = Path(args.outfile)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fh:
        for rec in clean:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"clean={len(clean)} dupes_removed={dupes} → {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
