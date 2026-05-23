#!/usr/bin/env python3
"""
Verify the Dealix Growth Operating Layer.

Checks:
- Required intelligence + growth docs exist.
- Distribution machine docs exist for every machine listed.
- Required CSV seeds exist with required columns.
- No CSV row carries a banned guarantee claim.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DOCS = [
    "docs/intelligence/MARKET_DOMINATION_INTELLIGENCE.md",
    "docs/intelligence/SECTOR_RANKING_SYSTEM.md",
    "docs/intelligence/ICP_SEGMENTATION_SYSTEM.md",
    "docs/intelligence/BUYER_PERSONA_SYSTEM.md",
    "docs/intelligence/COMPETITIVE_INTELLIGENCE_SYSTEM.md",
    "docs/intelligence/TRIGGER_EVENT_SYSTEM.md",
    "docs/intelligence/ACCOUNT_SCORING_MODEL.md",
    "docs/growth/DISTRIBUTION_WAR_MACHINE.md",
    "docs/growth/AUTONOMOUS_DISTRIBUTION_MACHINES.md",
    "docs/growth/OUTBOUND_DRAFT_MACHINE.md",
    "docs/growth/LINKEDIN_QUEUE_MACHINE.md",
    "docs/growth/EMAIL_DRAFT_MACHINE.md",
    "docs/growth/CONTACT_FORM_QUEUE_MACHINE.md",
    "docs/growth/FOLLOW_UP_MACHINE.md",
    "docs/growth/REPLY_ROUTER_MACHINE.md",
    "docs/growth/NURTURE_MACHINE.md",
    "docs/growth/PARTNER_REFERRAL_MACHINE.md",
    "docs/growth/ABM_STRATEGIC_ACCOUNT_MACHINE.md",
    "docs/growth/PROOF_TO_DEMAND_MACHINE.md",
]

REQUIRED_CSVS = {
    "data/seeds/growth/sector_targets.csv": [
        "sector_id", "name_en", "name_ar", "composite",
        "fit", "velocity", "arr", "proof_ready", "capacity",
        "strategic", "recommendation", "source",
    ],
    "data/seeds/growth/target_segments.csv": [
        "segment_id", "name_en", "name_ar", "tier", "lead_offer",
        "ideal_size", "ideal_arr_sar", "motion", "status", "source",
    ],
    "data/seeds/growth/account_scores.csv": [
        "account_id", "name", "sector_id", "segment_id",
        "fit", "intent", "capacity", "strategic", "score",
        "recommendation", "last_updated", "source",
    ],
    "data/seeds/growth/distribution_machines.csv": [
        "machine_id", "name", "queue_file", "owner",
        "approval_class", "kill_switch", "kpi", "status", "source",
    ],
}

BANNED = [
    "guaranteed revenue",
    "guaranteed sales",
    "guaranteed leads",
    "guaranteed results",
]


def main() -> int:
    failures: list[str] = []
    passes: list[str] = []

    for doc in REQUIRED_DOCS:
        if (ROOT / doc).exists():
            passes.append(f"doc exists: {doc}")
        else:
            failures.append(f"MISSING doc: {doc}")

    for csv_path, required_cols in REQUIRED_CSVS.items():
        path = ROOT / csv_path
        if not path.exists():
            failures.append(f"MISSING CSV: {csv_path}")
            continue
        with path.open("r", encoding="utf-8") as fh:
            reader = csv.reader(fh)
            try:
                header = next(reader)
            except StopIteration:
                failures.append(f"empty CSV: {csv_path}")
                continue
            missing_cols = [c for c in required_cols if c not in header]
            if missing_cols:
                failures.append(f"CSV {csv_path} missing columns: {missing_cols}")
            else:
                passes.append(f"CSV columns OK: {csv_path}")

            for row in reader:
                joined = " ".join(row).lower()
                for banned in BANNED:
                    if re.search(rf"\b{re.escape(banned.lower())}\b", joined):
                        failures.append(f"banned claim '{banned}' in row of {csv_path}")

    # Score sanity: ensure all account scores are in 0-100.
    accounts_csv = ROOT / "data/seeds/growth/account_scores.csv"
    if accounts_csv.exists():
        with accounts_csv.open("r", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                try:
                    score = float(row.get("score", "0"))
                except ValueError:
                    failures.append(f"non-numeric score in account_scores.csv: {row.get('account_id')}")
                    continue
                if not 0 <= score <= 100:
                    failures.append(
                        f"out-of-range score for {row.get('account_id')}: {score}"
                    )

    print(f"PASSED: {len(passes)}")
    for p in passes:
        print(f"  - {p}")
    print()
    print(f"FAILED: {len(failures)}")
    for f in failures:
        print(f"  - {f}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
