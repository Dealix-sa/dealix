#!/usr/bin/env python3
"""
Launch conflict scanner — checks for file naming conflicts between the launch
bundle and existing repo content.

Run: python scripts/launch/launch_conflict_scan.py [--repo-root .]

Output: lists of conflicts, near-matches, and clean files.
No mutations. Safe any time.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

LAUNCH_BUNDLE_FILES = [
    "docs/strategy/BEST_FIRST_WEDGE_DECISION_AR.md",
    "docs/strategy/SAUDI_VERTICAL_SELECTION_MATRIX_AR.md",
    "docs/strategy/DEALIX_MARKET_ENTRY_STRATEGY_AR.md",
    "docs/strategy/DEALIX_POSITIONING_BIBLE_AR.md",
    "docs/strategy/COMPETITOR_POSITIONING_AR.md",
    "docs/offers/DEALIX_OFFER_LADDER_AR.md",
    "docs/offers/REVENUE_LEAK_AUDIT_OFFER_AR.md",
    "docs/offers/WHATSAPP_FOLLOWUP_OS_OFFER_AR.md",
    "docs/offers/SALES_COMMAND_CENTER_OFFER_AR.md",
    "docs/offers/PROPOSAL_PROOF_PACK_OS_OFFER_AR.md",
    "docs/offers/AI_OPERATING_SYSTEM_FOR_SMB_OFFER_AR.md",
    "docs/offers/CUSTOM_ENTERPRISE_OS_OFFER_AR.md",
    "docs/offers/PRICING_LOGIC_AND_APPROVAL_POLICY_AR.md",
    "docs/targeting/ICP_SCORING_SYSTEM_AR.md",
    "docs/targeting/TARGET_ACCOUNT_RESEARCH_PLAYBOOK_AR.md",
    "docs/targeting/DECISION_MAKER_PERSONAS_AR.md",
    "docs/targeting/BUYER_PAIN_MAP_AR.md",
    "docs/targeting/DISQUALIFICATION_RULES_AR.md",
    "docs/targeting/FIRST_100_TARGET_ACCOUNTS_TEMPLATE.md",
    "docs/sales/FOUNDER_LED_SALES_PLAYBOOK_AR.md",
    "docs/sales/OUTREACH_APPROVAL_PLAYBOOK_AR.md",
    "docs/trust/HUMAN_APPROVAL_MATRIX_AR.md",
    "docs/trust/NO_OVERCLAIM_POLICY_AR.md",
    "docs/trust/TRUST_PREFLIGHT_RULES_AR.md",
    "schemas/launch/icp_score.schema.json",
    "schemas/launch/outreach_draft.schema.json",
    "schemas/launch/proposal_pack.schema.json",
]

EXACT_CONFLICTS = [
    "docs/strategy/COMPETITIVE_POSITIONING_AR.md",  # near-match exists
]


def scan(repo_root: Path) -> None:
    print("=" * 60)
    print("DEALIX LAUNCH CONFLICT SCANNER")
    print(f"Repo root: {repo_root}")
    print("=" * 60)

    exact_hits = []
    near_hits = []
    clean = []

    for bundle_path in LAUNCH_BUNDLE_FILES:
        full = repo_root / bundle_path
        if full.exists():
            exact_hits.append(bundle_path)
        else:
            stem = full.stem.lower()
            parent = full.parent
            if parent.exists():
                for existing in parent.iterdir():
                    if existing.is_file() and (
                        stem[:12] in existing.stem.lower()
                        or existing.stem.lower()[:12] in stem
                    ):
                        near_hits.append((bundle_path, str(existing.relative_to(repo_root))))
                        break
                else:
                    clean.append(bundle_path)
            else:
                clean.append(bundle_path)

    print(f"\n✅ Clean (no conflict): {len(clean)} files")
    print(f"⚠️  Near-matches:       {len(near_hits)} files")
    print(f"🔴 Exact duplicates:    {len(exact_hits)} files\n")

    if near_hits:
        print("Near-matches (review manually):")
        for bundle_path, existing in near_hits:
            print(f"  BUNDLE: {bundle_path}")
            print(f"  REPO:   {existing}")
            print()

    if exact_hits:
        print("Exact duplicates (bundle adds new content to existing files):")
        for p in exact_hits:
            size = (repo_root / p).stat().st_size
            print(f"  {p} ({size:,} bytes)")

    print("=" * 60)
    print("✅ Conflict scan complete — no repo files modified")


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan launch bundle for file conflicts")
    parser.add_argument("--repo-root", default=".", help="Path to repo root")
    args = parser.parse_args()
    scan(Path(args.repo_root).resolve())


if __name__ == "__main__":
    main()
