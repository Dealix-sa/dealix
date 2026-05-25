#!/usr/bin/env python3
"""Verify the Dealix Product Distribution OS.

Checks:
- Required product docs exist.
- Product runtime CSVs exist with the canonical headers.
- offer_ladder.csv has the 7 rungs.
- product_distribution.csv references the same 7 offers.
- No banned phrases in product docs.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_PRODUCT_DOCS = [
    "docs/product/DEALIX_PRODUCT_LADDER.md",
    "docs/product/PRODUCT_DISTRIBUTION_OS.md",
    "docs/product/PRODUCT_POSITIONING.md",
    "docs/product/OFFER_PACKAGING.md",
    "docs/product/PRICING_GUARDRAILS.md",
]

REQUIRED_CSVS = {
    "data/product/offer_ladder.csv": [
        "offer_id",
        "name",
        "rung",
        "target_personas",
        "promise",
        "deliverables",
        "trust_note",
        "price_band_sar_low",
        "price_band_sar_high",
        "cycle",
        "upgrade_path",
        "channels",
        "proof_required",
        "owner",
        "status",
    ],
    "data/product/product_distribution.csv": [
        "offer_id",
        "offer_name",
        "primary_channel",
        "supporting_channel",
        "proof_required",
        "owner",
    ],
}

REQUIRED_OFFER_IDS = [f"OFF-{n:02d}" for n in range(1, 8)]

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

BANNED_ALLOWLIST = {
    "docs/product/DEALIX_PRODUCT_LADDER.md",
    "docs/product/PRODUCT_POSITIONING.md",
    "docs/product/OFFER_PACKAGING.md",
    "docs/product/PRICING_GUARDRAILS.md",
    "docs/product/PRODUCT_DISTRIBUTION_OS.md",
    # Pre-existing doctrine docs that legitimately list banned terms.
    "docs/product/GOVERNANCE_AS_CODE.md",
    "docs/product/agent_cards/outreach_agent.md",
}


def check_files(failures: list[str]) -> None:
    for rel in REQUIRED_PRODUCT_DOCS:
        if not (ROOT / rel).exists():
            failures.append(f"missing file: {rel}")
    for rel in REQUIRED_CSVS:
        if not (ROOT / rel).exists():
            failures.append(f"missing file: {rel}")


def check_csv_headers(failures: list[str]) -> None:
    for rel, required in REQUIRED_CSVS.items():
        p = ROOT / rel
        if not p.exists():
            continue
        with p.open(newline="", encoding="utf-8") as f:
            try:
                header = next(csv.reader(f))
            except StopIteration:
                failures.append(f"{rel}: empty CSV")
                continue
        for col in required:
            if col not in header:
                failures.append(f"{rel}: missing required column '{col}'")


def check_offers(failures: list[str]) -> None:
    rel = "data/product/offer_ladder.csv"
    p = ROOT / rel
    if not p.exists():
        return
    seen = []
    with p.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            oid = (row.get("offer_id") or "").strip()
            if oid:
                seen.append(oid)
    for oid in REQUIRED_OFFER_IDS:
        if oid not in seen:
            failures.append(
                f"{rel}: missing canonical offer_id {oid} "
                f"(expected OFF-01 through OFF-07)"
            )


def check_distribution_consistency(failures: list[str]) -> None:
    ladder = ROOT / "data/product/offer_ladder.csv"
    dist = ROOT / "data/product/product_distribution.csv"
    if not (ladder.exists() and dist.exists()):
        return
    ladder_ids = set()
    with ladder.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ladder_ids.add((row.get("offer_id") or "").strip())
    dist_ids = set()
    with dist.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            dist_ids.add((row.get("offer_id") or "").strip())
    missing_in_dist = (ladder_ids - dist_ids) - {""}
    extra_in_dist = (dist_ids - ladder_ids) - {""}
    for oid in sorted(missing_in_dist):
        failures.append(
            f"product_distribution.csv: missing offer_id {oid} "
            f"(present in offer_ladder.csv)"
        )
    for oid in sorted(extra_in_dist):
        failures.append(
            f"product_distribution.csv: unknown offer_id {oid} "
            f"(not in offer_ladder.csv)"
        )


def check_banned(failures: list[str]) -> None:
    product_dir = ROOT / "docs/product"
    if not product_dir.exists():
        return
    for path in product_dir.rglob("*.md"):
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
    check_offers(failures)
    check_distribution_consistency(failures)
    check_banned(failures)

    print("=" * 60)
    print("Dealix Product Distribution Verifier")
    print("=" * 60)
    if not failures:
        print("[PASS] product distribution verified")
        return 0
    print(f"[FAIL] {len(failures)} issue(s):")
    for f in failures:
        print(f"  - {f}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
