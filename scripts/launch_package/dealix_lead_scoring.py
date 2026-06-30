#!/usr/bin/env python3
"""Score a founder-supplied prospect CSV (no scraping, no external calls).

Reads a CSV the founder already owns (public or consented context only),
assigns a 0-100 fit score, recommends a manual next action, and writes a
sorted CSV. This is a lightweight, dependency-free helper for the launch
package; the governed pipeline (POST /api/v1/leads) remains the canonical
scoring path inside the app.

Usage:
    python3 scripts/launch_package/dealix_lead_scoring.py
    python3 scripts/launch_package/dealix_lead_scoring.py \
        --input data/prospects/my_accounts.csv --output reports/launch_package/scored.csv
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

PKG_DIR = Path(__file__).resolve().parent
REPO_ROOT = PKG_DIR.parents[1]
DEFAULT_INPUT = PKG_DIR / "sample_data" / "icp_seed_accounts_saudi.csv"
DEFAULT_OUTPUT = REPO_ROOT / "reports" / "launch_package" / "scored_prospects.csv"

SECTOR_SCORE = {
    "real estate": 15,
    "training": 15,
    "training & consulting": 15,
    "marketing agency": 15,
    "clinic": 12,
    "ecommerce": 12,
    "b2b services": 14,
    "b2b saas": 14,
}

PAIN_KEYWORDS = [
    "whatsapp",
    "واتساب",
    "leads",
    "استفسارات",
    "sales",
    "مبيعات",
    "follow",
    "pipeline",
]
FIT_KEYWORDS = ["b2b", "عقار", "real estate", "training", "تدريب", "agency", "وكالة", "saas"]
URGENCY_KEYWORDS = ["hiring", "new branch", "campaign", "growth", "expansion", "توسع", "حملة"]
CONTACT_FIELDS = ["public_contact", "public_contact_source", "phone", "email"]


def score(row: dict) -> int:
    text = " ".join(str(v).lower() for v in row.values())
    s = 0
    if any(k in text for k in PAIN_KEYWORDS):
        s += 25
    if any(k in text for k in FIT_KEYWORDS):
        s += 25
    if (row.get("website") or "").strip():
        s += 10
    if any((row.get(f) or "").strip() for f in CONTACT_FIELDS):
        s += 10
    s += SECTOR_SCORE.get((row.get("sector") or "").lower().strip(), 8)
    if any(k in text for k in URGENCY_KEYWORDS):
        s += 15
    return min(s, 100)


def next_action(s: int) -> str:
    if s >= 90:
        return "Call today"
    if s >= 70:
        return "Personalized outreach"
    if s >= 50:
        return "Nurture"
    return "Ignore"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    if not args.input.exists():
        raise SystemExit(f"Missing input file: {args.input}")
    args.output.parent.mkdir(parents=True, exist_ok=True)

    with args.input.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise SystemExit("No prospects found")

    field_names = list(rows[0].keys())
    for extra in ("lead_score", "next_action"):
        if extra not in field_names:
            field_names.append(extra)

    for r in rows:
        sc = score(r)
        r["lead_score"] = sc
        r["next_action"] = next_action(sc)
    rows.sort(key=lambda r: int(r["lead_score"]), reverse=True)

    with args.output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} scored prospects to {args.output}")


if __name__ == "__main__":
    main()
