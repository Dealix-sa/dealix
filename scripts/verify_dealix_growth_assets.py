#!/usr/bin/env python3
"""Verify Dealix growth assets exist (P2 launch-readiness inputs).

Checks for the presence of the growth/distribution assets that back the P2
band of launch readiness: partner/referral program, growth scorecard,
sector/answer-library plans, and the warm-target seed lists.

Terminal markers:
    GROWTH_ASSETS_PRESENT=<n>/<total>
    DEALIX_GROWTH_ASSETS_OK=true|false
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# (label, candidate paths — present if ANY candidate exists)
GROWTH_ASSETS = (
    ("partner_referral_plan", ("docs/growth/PARTNER_STRATEGY.md", "docs/AGENCY_PARTNER_PROGRAM.md", "docs/growth/AGENCY_RESELLER_PLAYBOOK.md")),
    ("growth_metrics_report", ("reports/company_os/weekly/GROWTH_SCORECARD.md",)),
    ("case_study_factory", ("docs/growth/CASE_STUDY_FACTORY.md",)),
    ("warm_target_seed", ("data/outreach/first_30_targets.csv", "docs/ops/lead_machine/TODAY_15_TARGETS.csv")),
    ("outreach_approval_queue", ("data/outreach/approval_queue.csv",)),
)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass

    present = 0
    for label, candidates in GROWTH_ASSETS:
        found = next((c for c in candidates if (REPO / c).is_file()), None)
        if found:
            present += 1
            print(f"OK   {label}: {found}")
        else:
            print(f"MISS {label}: none of {candidates}")

    total = len(GROWTH_ASSETS)
    print(f"GROWTH_ASSETS_PRESENT={present}/{total}")
    # Growth assets are P2 — require a majority present, not all.
    ok = present >= (total - 1)
    print(f"DEALIX_GROWTH_ASSETS_OK={'true' if ok else 'false'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
