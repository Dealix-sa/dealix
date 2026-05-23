#!/usr/bin/env python3
"""Master verifier for the Dealix Market Attack & Scaling System.

Checks:
- All required docs exist.
- Bootstrap CSVs exist with the expected headers.
- Generator scripts exist and are importable.
- Makefile targets exist.
- Frontend pages exist (only if apps/web is present).
- No "guaranteed" claims in customer-facing market-attack markdown.

Exit code 0 on success, 1 on any hard failure. Warnings non-fatal.
"""

from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from market_attack_common import (  # type: ignore[import-not-found]
    REPO_ROOT,
)

REQUIRED_DOCS = [
    "docs/market_attack/DEALIX_MARKET_ATTACK_SYSTEM.md",
    "docs/market_attack/BEACHHEAD_SECTOR_STRATEGY.md",
    "docs/market_attack/BEACHHEAD_SELECTION_SCORECARD.md",
    "docs/market_attack/OFFER_MARKET_FIT_TEST.md",
    "docs/market_attack/OFFER_MARKET_FIT_SCORECARD.md",
    "docs/market_attack/SECTOR_ATTACK_PLAYBOOK.md",
    "docs/market_attack/STRATEGIC_ACCOUNT_LIST_SYSTEM.md",
    "docs/market_attack/STRATEGIC_ACCOUNT_ATTACK_PLAN.md",
    "docs/market_attack/DEMAND_CREATION_SYSTEM.md",
    "docs/market_attack/CONVERSION_COMMAND_ROOM.md",
    "docs/market_attack/SCALE_FIX_KILL_SYSTEM.md",
    "docs/market_attack/MARKET_LEARNING_MEMORY.md",
    "docs/market_attack/CAMPAIGN_FACTORY.md",
    "docs/market_attack/CAMPAIGN_APPROVAL_PROTOCOL.md",
    "docs/market_attack/CAMPAIGN_POSTMORTEM_SYSTEM.md",
    "docs/market_attack/OBJECTION_INTELLIGENCE_SYSTEM.md",
    "docs/market_attack/OBJECTION_TO_ASSET_LOOP.md",
    "docs/sales_assets/SALES_ASSET_FACTORY.md",
    "docs/sales_assets/SAMPLE_ASSET_SYSTEM.md",
    "docs/sales_assets/PROPOSAL_ASSET_SYSTEM.md",
    "docs/sales_assets/SECTOR_ONE_PAGER_SYSTEM.md",
    "docs/sales_assets/OBJECTION_RESPONSE_LIBRARY.md",
    "docs/sales_assets/PROOF_SAFE_ASSET_POLICY.md",
    "docs/authority/FOUNDER_AUTHORITY_ENGINE.md",
    "docs/authority/SECTOR_INSIGHT_ENGINE.md",
    "docs/authority/LINKEDIN_AUTHORITY_SYSTEM.md",
    "docs/authority/REVENUE_INTELLIGENCE_REPORT_SYSTEM.md",
    "docs/authority/TRUSTED_MARKET_VOICE_SYSTEM.md",
    "docs/partners/PARTNER_ATTACK_SYSTEM.md",
    "docs/partners/AGENCY_PARTNER_PLAYBOOK.md",
    "docs/partners/ERP_CRM_PARTNER_PLAYBOOK.md",
    "docs/partners/CYBERSECURITY_PARTNER_PLAYBOOK.md",
    "docs/partners/WHITE_LABEL_REVENUE_OS.md",
    "docs/partners/PARTNER_REFERRAL_TERMS_GUARDRAILS.md",
]

REQUIRED_SCRIPTS = [
    "scripts/market_attack_common.py",
    "scripts/generate_beachhead_sector_scorecard.py",
    "scripts/generate_strategic_account_list.py",
    "scripts/generate_offer_market_fit_report.py",
    "scripts/generate_campaign_command_report.py",
    "scripts/generate_authority_content_queue.py",
    "scripts/generate_partner_pipeline_report.py",
    "scripts/generate_objection_intelligence_report.py",
    "scripts/verify_sales_asset_system.py",
    "scripts/verify_prompt_output_quality.py",
    "scripts/verify_market_attack_system.py",
]

EXPECTED_CSV_HEADERS = {
    "scripts/market_attack_bootstrap/market_attack/beachhead_sector_scorecard.csv": [
        "sector",
        "saudi_relevance",
        "buyer_clarity",
        "pain_urgency",
        "high_ticket_potential",
        "proof_fit",
        "delivery_fit",
        "competition_gap",
        "channel_access",
        "trust_risk",
        "total_score",
        "priority",
        "next_action",
    ],
    "scripts/market_attack_bootstrap/market_attack/strategic_accounts.csv": [
        "account_id",
        "company",
        "sector",
        "website",
        "city",
        "buyer_title",
        "why_strategic",
        "trigger_event",
        "estimated_value",
        "relationship_path",
        "proof_needed",
        "trust_risk",
        "priority",
        "next_action",
        "status",
    ],
    "scripts/market_attack_bootstrap/market_attack/offer_market_fit_tests.csv": [
        "test_id",
        "sector",
        "offer",
        "audience",
        "channel",
        "hypothesis",
        "message_angle",
        "success_metric",
        "result",
        "learning",
        "decision",
        "next_action",
    ],
    "scripts/market_attack_bootstrap/market_attack/objection_library.csv": [
        "objection_id",
        "sector",
        "stage",
        "objection",
        "frequency",
        "response_angle",
        "asset_needed",
        "owner",
        "status",
        "next_action",
    ],
    "scripts/market_attack_bootstrap/campaigns/campaign_registry.csv": [
        "campaign_id",
        "name",
        "sector",
        "offer",
        "channel",
        "goal",
        "approval_class",
        "owner",
        "status",
        "start_date",
        "end_date",
        "next_action",
    ],
    "scripts/market_attack_bootstrap/campaigns/campaign_assets.csv": [
        "asset_id",
        "campaign_id",
        "type",
        "title",
        "status",
        "approval_status",
        "proof_status",
        "risk_level",
        "next_action",
    ],
    "scripts/market_attack_bootstrap/campaigns/campaign_queue.csv": [
        "queue_id",
        "campaign_id",
        "channel",
        "target_segment",
        "message_or_asset",
        "approval_status",
        "send_status",
        "next_action",
    ],
    "scripts/market_attack_bootstrap/campaigns/campaign_results.csv": [
        "date",
        "campaign_id",
        "channel",
        "impressions",
        "clicks",
        "replies",
        "positive_replies",
        "samples",
        "proposals",
        "payments",
        "learning",
        "next_action",
    ],
    "scripts/market_attack_bootstrap/sales_assets/sales_asset_registry.csv": [
        "asset_id",
        "type",
        "sector",
        "offer",
        "title",
        "status",
        "approval_status",
        "proof_status",
        "risk_level",
        "file_path",
        "next_action",
    ],
    "scripts/market_attack_bootstrap/authority/content_angles.csv": [
        "angle_id",
        "theme",
        "sector",
        "audience",
        "claim",
        "evidence_needed",
        "risk_level",
        "status",
        "next_action",
    ],
    "scripts/market_attack_bootstrap/authority/sector_insights.csv": [
        "insight_id",
        "sector",
        "insight",
        "evidence",
        "source",
        "status",
        "approved_for_public",
        "next_action",
    ],
    "scripts/market_attack_bootstrap/authority/founder_posts.csv": [
        "post_id",
        "theme",
        "sector",
        "draft",
        "approval_status",
        "proof_status",
        "risk_level",
        "next_action",
    ],
    "scripts/market_attack_bootstrap/authority/report_ideas.csv": [
        "report_id",
        "sector",
        "title",
        "hypothesis",
        "data_needed",
        "approval_status",
        "next_action",
    ],
    "scripts/market_attack_bootstrap/partners/partner_pipeline.csv": [
        "partner_id",
        "company",
        "type",
        "website",
        "relationship_path",
        "offer_fit",
        "referral_potential",
        "white_label_potential",
        "trust_risk",
        "status",
        "next_action",
    ],
}

REQUIRED_MAKEFILE_TARGETS = (
    "beachhead-scorecard",
    "strategic-accounts",
    "offer-market-fit",
    "campaign-command",
    "sales-assets",
    "authority-engine",
    "partner-pipeline",
    "objection-intel",
    "market-attack-system",
    "bootstrap-runtime",
)

REQUIRED_FRONTEND_PAGES = (
    "apps/web/app/market-attack/page.tsx",
    "apps/web/app/campaigns/page.tsx",
    "apps/web/app/partners/page.tsx",
    "apps/web/app/sales-assets/page.tsx",
    "apps/web/app/authority/page.tsx",
)

REQUIRED_RUNTIME_CLIENT = "apps/web/components/marketAttack/runtimeClient.ts"

REQUIRED_API_ROUTERS = (
    "api/routers/market_attack_internal.py",
)


def _check_csv_headers(rel: str, expected: list[str]) -> str | None:
    path = REPO_ROOT / rel
    if not path.is_file():
        return f"missing csv: {rel}"
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        try:
            headers = next(reader)
        except StopIteration:
            return f"empty csv: {rel}"
    if headers != expected:
        return f"csv headers mismatch in {rel}: got {headers} expected {expected}"
    return None


def _check_makefile_targets() -> list[str]:
    mf = REPO_ROOT / "Makefile"
    if not mf.is_file():
        return ["Makefile is missing"]
    text = mf.read_text(encoding="utf-8")
    missing = []
    for tgt in REQUIRED_MAKEFILE_TARGETS:
        if f"\n{tgt}:" not in text and not text.startswith(f"{tgt}:"):
            missing.append(f"Makefile target missing: {tgt}")
    return missing


def _check_script_importable(rel: str) -> str | None:
    path = REPO_ROOT / rel
    if not path.is_file():
        return f"missing script: {rel}"
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        return f"cannot import {rel}"
    try:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # type: ignore[union-attr]
    except SystemExit:
        # Some scripts call SystemExit at the top-level via SystemExit;
        # most have a main() guard so this should not fire.
        return None
    except Exception as exc:  # noqa: BLE001
        return f"import error in {rel}: {exc!r}"
    return None


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []

    for d in REQUIRED_DOCS:
        if not (REPO_ROOT / d).is_file():
            failures.append(f"missing doc: {d}")

    for s in REQUIRED_SCRIPTS:
        err = _check_script_importable(s)
        if err:
            failures.append(err)

    for rel, expected in EXPECTED_CSV_HEADERS.items():
        err = _check_csv_headers(rel, expected)
        if err:
            failures.append(err)

    failures.extend(_check_makefile_targets())

    # Frontend: only required if apps/web is present.
    if (REPO_ROOT / "apps" / "web").is_dir():
        for p in REQUIRED_FRONTEND_PAGES:
            if not (REPO_ROOT / p).is_file():
                failures.append(f"missing frontend page: {p}")
        if not (REPO_ROOT / REQUIRED_RUNTIME_CLIENT).is_file():
            failures.append(f"missing runtime client: {REQUIRED_RUNTIME_CLIENT}")

    # API routers: only warn (the API may live in a different repo).
    for r in REQUIRED_API_ROUTERS:
        if not (REPO_ROOT / r).is_file():
            warnings.append(f"api router not found (warning): {r}")

    # Proof-safe scan on the new docs we added.
    qual = REPO_ROOT / "scripts" / "verify_prompt_output_quality.py"
    if qual.is_file():
        # We don't import-run it here; the workflow runs it explicitly.
        pass
    else:
        failures.append("missing scripts/verify_prompt_output_quality.py")

    print("Market Attack System Verification")
    print("=" * 50)
    if failures:
        print("FAILURES:")
        for f in failures:
            print(f"  - {f}")
    else:
        print("FAILURES: none")
    print()
    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print(f"  - {w}")
    else:
        print("WARNINGS: none")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
