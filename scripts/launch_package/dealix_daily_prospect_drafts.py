#!/usr/bin/env python3
"""Generate an approval-first outreach queue from a seed prospect CSV.

This script NEVER sends messages. It produces a review queue (CSV) that the
founder reads and approves manually before any external contact. This honors
the Dealix doctrine ("Govern before automating" / no external auto-send) and
the outbound policy in docs/compliance/OUTBOUND_AND_DATA_POLICY_AR.md.

Defaults read the tracked sample seed shipped beside this script. Point
``--input`` at your real prospect file (keep it under the gitignored
``data/prospects/`` so customer data is never committed).

Usage:
    python3 scripts/launch_package/dealix_daily_prospect_drafts.py
    python3 scripts/launch_package/dealix_daily_prospect_drafts.py \
        --input data/prospects/my_accounts.csv
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass, fields
from datetime import datetime
from pathlib import Path

PKG_DIR = Path(__file__).resolve().parent
REPO_ROOT = PKG_DIR.parents[1]
DEFAULT_INPUT = PKG_DIR / "sample_data" / "icp_seed_accounts_saudi.csv"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "reports" / "launch_package"


@dataclass
class Prospect:
    company: str = ""
    sector: str = ""
    city: str = ""
    website: str = ""
    public_contact: str = ""
    likely_pain: str = ""
    best_offer: str = ""
    priority: str = ""
    notes: str = ""


def load_prospects(input_path: Path) -> list[Prospect]:
    if not input_path.exists():
        raise SystemExit(f"Missing input file: {input_path}")
    known = {f.name for f in fields(Prospect)}
    with input_path.open("r", encoding="utf-8-sig", newline="") as f:
        return [Prospect(**{k: (row.get(k) or "") for k in known}) for row in csv.DictReader(f)]


def draft_message(p: Prospect) -> str:
    return (
        f"السلام عليكم، لاحظنا أن {p.company} تعمل في مجال {p.sector} في {p.city}. "
        f"غالبًا أحد أكبر فرص النمو عندكم هو: {p.likely_pain}. "
        f"في Dealix نقدر نبدأ معكم بـ {p.best_offer}: تشخيص/تنظيم فرص ومتابعة "
        "ورسائل قابلة للمراجعة بدون إرسال آلي أو وعود غير واقعية. "
        "هل يناسبكم نرسل لكم ملخص تشخيص بسيط يوضح أين ممكن تتحسن المتابعة والمبيعات؟"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--limit", type=int, default=25)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / f"outreach_queue_{datetime.now():%Y-%m-%d}.csv"

    prospects = sorted(
        load_prospects(args.input),
        key=lambda p: (p.priority != "High", p.company.lower()),
    )
    field_names = [
        "date",
        "company",
        "sector",
        "city",
        "website",
        "public_contact",
        "likely_pain",
        "best_offer",
        "priority",
        "draft_message",
        "approval_status",
        "outcome",
        "follow_up_due",
        "notes",
    ]
    with output.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        for p in prospects[: args.limit]:
            writer.writerow(
                {
                    "date": datetime.now().date().isoformat(),
                    "company": p.company,
                    "sector": p.sector,
                    "city": p.city,
                    "website": p.website,
                    "public_contact": p.public_contact,
                    "likely_pain": p.likely_pain,
                    "best_offer": p.best_offer,
                    "priority": p.priority,
                    "draft_message": draft_message(p),
                    "approval_status": "needs_founder_review",
                    "outcome": "pending",
                    "follow_up_due": "",
                    "notes": p.notes,
                }
            )
    print(f"Created approval queue: {output}")
    print("Rule: review manually before any external outreach. This script never sends messages.")


if __name__ == "__main__":
    main()
