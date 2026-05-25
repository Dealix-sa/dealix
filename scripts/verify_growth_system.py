#!/usr/bin/env python3
"""Verify the Strategic Targeting OS and Autonomous Distribution Machines.

Checks:
- Required growth docs exist.
- Growth runtime CSVs exist with the canonical headers.
- distribution_machines.csv has the 15 canonical machines.
- account_scores.csv carries the 10 scoring fields.
- sector_targets.csv covers the 8 canonical sectors.
- No banned phrases in growth docs.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_GROWTH_DOCS = [
    "docs/growth/STRATEGIC_TARGETING_OS.md",
    "docs/growth/ICP_SEGMENTATION_SYSTEM.md",
    "docs/growth/SECTOR_DOMINATION_ENGINE.md",
    "docs/growth/ACCOUNT_SCORING_MODEL.md",
    "docs/growth/BUYER_PERSONA_SYSTEM.md",
    "docs/growth/OFFER_CHANNEL_FIT_MATRIX.md",
    "docs/growth/AUTONOMOUS_DISTRIBUTION_MACHINES.md",
    "docs/growth/OUTBOUND_DRAFT_MACHINE.md",
    "docs/growth/INBOUND_CONTENT_MACHINE.md",
    "docs/growth/PARTNER_REFERRAL_MACHINE.md",
    "docs/growth/ABM_STRATEGIC_ACCOUNT_MACHINE.md",
    "docs/growth/PRODUCT_MARKETING_MACHINE.md",
    "docs/growth/NURTURE_MACHINE.md",
    "docs/growth/PROOF_TO_DEMAND_MACHINE.md",
]

REQUIRED_GROWTH_CSVS = {
    "data/growth/target_segments.csv": [
        "segment_id",
        "name",
        "layer",
        "description",
    ],
    "data/growth/sector_targets.csv": [
        "sector_id",
        "sector_name",
        "status",
        "sector_lead",
        "quarter",
    ],
    "data/growth/account_scores.csv": [
        "account_id",
        "name",
        "sector",
        "country",
        "saudi_relevance",
        "b2b_fit",
        "high_ticket_potential",
        "buyer_clarity",
        "pain_urgency",
        "outreach_fit",
        "proof_fit",
        "partner_potential",
        "delivery_complexity",
        "trust_risk",
        "final_priority",
        "next_action",
        "proof_needed",
        "recommended_offer",
        "recommended_channel",
        "owner",
    ],
    "data/growth/distribution_machines.csv": [
        "machine_id",
        "name",
        "purpose",
        "input",
        "output",
        "data_source",
        "approval_class",
        "trust_gate",
        "owner",
        "worker_name",
        "kpi",
        "failure_mode",
        "recovery_path",
    ],
    "data/growth/partners.csv": [
        "partner_id",
        "name",
        "sector",
        "status",
    ],
    "data/growth/warm_list.csv": [
        "candidate_id",
        "account_id",
        "source_proof_artefact",
    ],
}

REQUIRED_15_MACHINE_IDS = [f"M-{n:02d}" for n in range(1, 16)]

REQUIRED_8_SECTORS = [f"SEC-{n:03d}" for n in range(1, 9)]

BANNED_PHRASES = [
    "guaranteed revenue",
    "guaranteed sales",
    "guaranteed results",
    "guaranteed outcome",
    "fully autonomous",
    "ai that sells for you",
    "10x revenue",
    "100x",
]

# Files that legitimately list banned phrases (because they list what we
# refuse to do, e.g. trust pages).
BANNED_ALLOWLIST = {
    "docs/growth/STRATEGIC_TARGETING_OS.md",
    "docs/growth/AUTONOMOUS_DISTRIBUTION_MACHINES.md",
    "docs/growth/OUTBOUND_DRAFT_MACHINE.md",
    "docs/growth/INBOUND_CONTENT_MACHINE.md",
    "docs/growth/trust_page/what_we_do_not_do.md",
    "docs/growth/TRUST_MARKETING_CORE.md",
}


def _exists(rel: str, failures: list[str]) -> None:
    if not (ROOT / rel).exists():
        failures.append(f"missing file: {rel}")


def check_files(failures: list[str]) -> None:
    for rel in REQUIRED_GROWTH_DOCS:
        _exists(rel, failures)
    for rel in REQUIRED_GROWTH_CSVS:
        _exists(rel, failures)


def check_csv_headers(failures: list[str]) -> None:
    for rel, required_cols in REQUIRED_GROWTH_CSVS.items():
        path = ROOT / rel
        if not path.exists():
            continue
        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            try:
                header = next(reader)
            except StopIteration:
                failures.append(f"{rel}: empty CSV")
                continue
        for col in required_cols:
            if col not in header:
                failures.append(f"{rel}: missing required column '{col}'")


def check_machines(failures: list[str]) -> None:
    rel = "data/growth/distribution_machines.csv"
    path = ROOT / rel
    if not path.exists():
        return
    seen_ids: list[str] = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mid = (row.get("machine_id") or "").strip()
            if mid:
                seen_ids.append(mid)
    for mid in REQUIRED_15_MACHINE_IDS:
        if mid not in seen_ids:
            failures.append(
                f"{rel}: missing canonical machine_id {mid} "
                f"(expected M-01 through M-15)"
            )


def check_sectors(failures: list[str]) -> None:
    rel = "data/growth/sector_targets.csv"
    path = ROOT / rel
    if not path.exists():
        return
    seen_ids: list[str] = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sid = (row.get("sector_id") or "").strip()
            if sid:
                seen_ids.append(sid)
    for sid in REQUIRED_8_SECTORS:
        if sid not in seen_ids:
            failures.append(
                f"{rel}: missing canonical sector_id {sid} "
                f"(expected SEC-001 through SEC-008)"
            )


def check_banned(failures: list[str]) -> None:
    growth_dir = ROOT / "docs/growth"
    if not growth_dir.exists():
        return
    for path in growth_dir.rglob("*.md"):
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        if rel in BANNED_ALLOWLIST:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        for phrase in BANNED_PHRASES:
            if phrase in text:
                failures.append(f"banned phrase '{phrase}' found in {rel}")


def main() -> int:
    failures: list[str] = []

    check_files(failures)
    check_csv_headers(failures)
    check_machines(failures)
    check_sectors(failures)
    check_banned(failures)

    print("=" * 60)
    print("Dealix Growth System Verifier")
    print("=" * 60)
    if not failures:
        print("[PASS] growth system verified")
        return 0

    print(f"[FAIL] {len(failures)} issue(s):")
    for f in failures:
        print(f"  - {f}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
