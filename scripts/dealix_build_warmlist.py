#!/usr/bin/env python3
"""Dealix Warm-List Builder — PII-safe daily candidate seed.

Transforms the git-tracked Saudi lead graph (public business information only)
into the candidate CSV consumed by ``scripts/dealix_daily_lead_prep.py``.

Why this exists
---------------
The daily lead board should not be empty on a fresh server. The repo already
tracks ``docs/ops/lead_machine/SAUDI_LEAD_GRAPH_MASTER.csv`` — 150+ Saudi B2B
companies described with **public** fields (company, sector, website, country).
This script projects that file down to the minimal candidate shape and writes it
to a **gitignored** path so the daily engine can score it.

Constitution guarantees (Article 4 — IMMUTABLE)
-----------------------------------------------
- **No PII is ever written.** Contact name / title / email / phone columns are
  emitted **blank**, regardless of the source file. Pre-drafted outreach
  messages (``first_message_angle`` / ``recommended_message`` / ``notes``) are
  **never** copied.
- ``source`` is set to ``public_business_info_allowed`` — an honest Tier-1
  source (NOT ``warm_intro``). These are research targets from public info, not
  warm relationships; the founder upgrades them via real warm intros.
- Output path is gitignored (``data/*``) — nothing leaks into the repo.

Usage
-----
    python3 scripts/dealix_build_warmlist.py
    python3 scripts/dealix_build_warmlist.py --source path/to/graph.csv --out path/to/out.csv

Output (default): ``data/wave12/warmlist/candidates.csv`` (or ``$DEALIX_WARMLIST_PATH``)
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = REPO_ROOT / "docs" / "ops" / "lead_machine" / "SAUDI_LEAD_GRAPH_MASTER.csv"
DEFAULT_OUT = REPO_ROOT / "data" / "wave12" / "warmlist" / "candidates.csv"

# The exact header the daily engine's ``load_candidates_from_csv`` understands.
# Contact columns are intentionally present-but-blank so the shape is stable and
# the PII-safety guarantee is explicit.
OUT_HEADER = [
    "name", "sector", "city", "country", "domain",
    "contact_name", "contact_title", "source", "locale",
    "annual_turnover_sar", "notes",
]

# Honest Tier-1 source: public business info, NOT a warm route (Article 4).
WARMLIST_SOURCE = "public_business_info_allowed"


def _strip_domain(website: str) -> str:
    """Normalize a website URL down to a bare domain (no protocol/path)."""
    d = website.strip().lower()
    for prefix in ("https://", "http://", "www."):
        if d.startswith(prefix):
            d = d[len(prefix):]
    return d.split("/")[0].strip()


def build_rows(source: Path) -> list[dict[str, str]]:
    """Project the lead graph → minimal, PII-free candidate rows (deduped by name)."""
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    with source.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            company = (r.get("company") or r.get("name") or "").strip()
            if not company:
                continue
            key = company.lower()
            if key in seen:
                continue
            seen.add(key)
            rows.append({
                "name": company,
                "sector": (r.get("sector") or "").strip().lower(),
                "city": "",  # PII-safe: graph has no city; never derive personal data
                "country": (r.get("country") or "SA").strip() or "SA",
                "domain": _strip_domain(r.get("website") or r.get("domain") or ""),
                "contact_name": "",   # PII-safe — never written
                "contact_title": "",  # PII-safe — never written
                "source": WARMLIST_SOURCE,
                "locale": "ar",
                "annual_turnover_sar": "",
                "notes": "",  # never copy pre-drafted messages / private notes
            })
    return rows


def _assert_no_pii(rows: list[dict[str, str]]) -> None:
    """Defensive guard: fail loudly if any PII-bearing cell got populated."""
    for r in rows:
        if r["contact_name"] or r["contact_title"]:
            raise SystemExit("PII guard tripped: contact columns must be blank")
        for v in r.values():
            if "@" in v:  # no emails anywhere
                raise SystemExit(f"PII guard tripped: '@' found in cell {v!r}")


def write_warmlist(rows: list[dict[str, str]], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUT_HEADER)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build PII-safe daily warm-list candidates")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE,
                        help=f"Source lead graph CSV (default: {DEFAULT_SOURCE})")
    parser.add_argument("--out", type=Path,
                        default=Path(os.environ.get("DEALIX_WARMLIST_PATH", str(DEFAULT_OUT))),
                        help=f"Output candidates CSV (default: {DEFAULT_OUT})")
    args = parser.parse_args()

    if not args.source.exists():
        print(f"ERROR: source not found: {args.source}", file=sys.stderr)
        return 2

    rows = build_rows(args.source)
    _assert_no_pii(rows)
    write_warmlist(rows, args.out)

    print(f"Source: {args.source}")
    print(f"Wrote {len(rows)} PII-free candidates → {args.out}")
    print(f"Source field set to '{WARMLIST_SOURCE}' (Tier-1, not warm — honest).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
