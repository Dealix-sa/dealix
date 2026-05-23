#!/usr/bin/env python3
"""
Verify the Dealix growth / market intelligence / distribution system.

Checks:
- Required intelligence + growth docs exist.
- Each distribution machine doc declares the mandatory contract sections.
- Distribution machine registry CSV references existing docs.
- AI agent registry references existing agent docs.
- No banned voice patterns in any growth/intelligence doc.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

INTELLIGENCE_DOCS = [
    "docs/intelligence_market/MARKET_DOMINATION_INTELLIGENCE.md",
    "docs/intelligence_market/SECTOR_RANKING_SYSTEM.md",
    "docs/intelligence_market/ICP_SEGMENTATION_SYSTEM.md",
    "docs/intelligence_market/BUYER_PERSONA_SYSTEM.md",
    "docs/intelligence_market/COMPETITIVE_INTELLIGENCE_SYSTEM.md",
    "docs/intelligence_market/TRIGGER_EVENT_SYSTEM.md",
    "docs/intelligence_market/ACCOUNT_SCORING_MODEL.md",
]

DISTRIBUTION_DOCS = [
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

MACHINE_CONTRACT_SECTIONS = [
    "## purpose",
    "## inputs",
    "## outputs",
    "## approval_class",
    "## trust_gate",
    "## owner",
    "## worker",
    "## KPI",
    "## failure_mode",
    "## recovery_path",
    "## kill_switch",
    "## audit",
]

POSITIONING_DOCS = [
    "docs/positioning/CATEGORY_CREATION_OS.md",
    "docs/positioning/DEALIX_POSITIONING.md",
    "docs/positioning/COMPETITIVE_NARRATIVE.md",
    "docs/positioning/WHY_DEALIX_NOW.md",
    "docs/positioning/MESSAGING_HIERARCHY.md",
]

REVENUE_DOCS = [
    "docs/revenue/REVENUE_FACTORY_OS.md",
    "docs/revenue/SAMPLE_FACTORY.md",
    "docs/revenue/PROPOSAL_FACTORY.md",
    "docs/finance/PAYMENT_CAPTURE_OS.md",
    "docs/delivery/DELIVERY_QA_OS.md",
    "docs/client_success/RETENTION_REFERRAL_OS.md",
    "docs/proof/PROOF_APPROVAL_OS.md",
]

AGENT_DOCS = [
    "docs/ai/AGENT_REGISTRY.md",
    "docs/ai/BRAND_GUARDIAN_AGENT.md",
    "docs/ai/GROWTH_STRATEGIST_AGENT.md",
    "docs/ai/DISTRIBUTION_OPERATOR_AGENT.md",
    "docs/ai/CONTENT_STRATEGIST_AGENT.md",
    "docs/ai/OFFER_ARCHITECT_AGENT.md",
    "docs/ai/PERFORMANCE_ANALYST_AGENT.md",
    "docs/ai/TRUST_GUARDIAN_AGENT.md",
    "docs/ai/EVAL_RED_TEAM_SYSTEM.md",
]

BANNED_VOICE = [
    r"guarantee[d]?\s+(revenue|sales|leads|results|pipeline|roi)",
    r"\d+x\s+(your|in)\s+(sales|revenue|pipeline|leads|growth)",
    r"fully\s+autonomous\s+(outbound|sales|sending|posting)",
    r"set\s+(it|and)\s+forget\s*(it)?",
]

MACHINE_REGISTRY_CSV = "data/private_ops_seed/growth/distribution_machines.csv"


def _check_file(rel: str) -> tuple[bool, str]:
    p = REPO_ROOT / rel
    if not p.exists() or p.stat().st_size == 0:
        return False, f"missing: {rel}"
    return True, rel


def main() -> int:
    failures: list[str] = []
    passes: list[str] = []

    for rel in INTELLIGENCE_DOCS + DISTRIBUTION_DOCS + POSITIONING_DOCS + REVENUE_DOCS + AGENT_DOCS:
        ok, msg = _check_file(rel)
        (passes if ok else failures).append(msg)

    # Each machine doc must include all contract sections
    for rel in DISTRIBUTION_DOCS:
        p = REPO_ROOT / rel
        if not p.exists():
            continue
        if not rel.endswith("MACHINE.md") or rel.endswith("WAR_MACHINE.md") or rel.endswith("AUTONOMOUS_DISTRIBUTION_MACHINES.md"):
            continue
        text = p.read_text(encoding="utf-8")
        for sec in MACHINE_CONTRACT_SECTIONS:
            if sec.lower() not in text.lower():
                failures.append(f"{rel}: missing section {sec}")

    # Registry CSV references each machine doc
    reg_path = REPO_ROOT / MACHINE_REGISTRY_CSV
    if reg_path.exists():
        with reg_path.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                doc_rel = row["doc_path"]
                if not (REPO_ROOT / doc_rel).exists():
                    failures.append(f"{MACHINE_REGISTRY_CSV} references missing {doc_rel}")
    else:
        failures.append(f"missing: {MACHINE_REGISTRY_CSV}")

    # Banned voice patterns in all of these docs (excluding banned-list documentation)
    DOC_GROUPS = INTELLIGENCE_DOCS + DISTRIBUTION_DOCS + POSITIONING_DOCS + REVENUE_DOCS + AGENT_DOCS
    for rel in DOC_GROUPS:
        p = REPO_ROOT / rel
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        for pattern in BANNED_VOICE:
            for m in re.finditer(pattern, text, flags=re.IGNORECASE):
                snippet = text[max(0, m.start() - 60): m.end() + 60].replace("\n", " ")
                if "❌" in snippet or "Banned" in snippet or "banned" in snippet or "forbidden" in snippet.lower() or "```" in snippet or "regex" in snippet.lower():
                    continue
                failures.append(f"banned voice in {rel}: …{snippet}…")

    print("=== Dealix Growth System Verifier ===")
    print(f"checks passed: {len(passes)}")
    if failures:
        print(f"failures: {len(failures)}")
        for f in failures:
            print(f"  - {f}")
        print("\nVERDICT: FAIL")
        return 1
    print("\nVERDICT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
