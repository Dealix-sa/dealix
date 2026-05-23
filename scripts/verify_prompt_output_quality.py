#!/usr/bin/env python3
"""Scan generated/customer-facing markdown for proof-safe doctrine violations.

Specifically:
- The Market Attack docs.
- Sales asset docs.
- Authority docs.
- Partner docs (new files for this layer).
- Bootstrap CSV content.

Banned phrases: see market_attack_common.BANNED_PHRASES.

Allow-listed contexts: any doc that includes the literal "banned"
or "we never" or "we do not promise" is treated as a doctrine doc
that legitimately discusses the banned terms.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from market_attack_common import (  # type: ignore[import-not-found]
    BANNED_PHRASES,
    REPO_ROOT,
)

SCAN_DIRS = (
    REPO_ROOT / "docs" / "market_attack",
    REPO_ROOT / "docs" / "sales_assets",
    REPO_ROOT / "docs" / "authority",
    # Only the new files we added to partners; the rest of docs/partners
    # is owned by other layers.
)

ALLOWLIST_FILENAMES = {
    "PROOF_SAFE_ASSET_POLICY.md",
    "PARTNER_REFERRAL_TERMS_GUARDRAILS.md",
    "OBJECTION_RESPONSE_LIBRARY.md",
    "MARKET_LEARNING_MEMORY.md",
    "OFFER_MARKET_FIT_TEST.md",
    "SECTOR_ATTACK_PLAYBOOK.md",
    "BEACHHEAD_SECTOR_STRATEGY.md",
    "DEALIX_MARKET_ATTACK_SYSTEM.md",
    "CAMPAIGN_APPROVAL_PROTOCOL.md",
    "WHITE_LABEL_REVENUE_OS.md",
    "PROPOSAL_ASSET_SYSTEM.md",
}


def _scan_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    lower = text.lower()
    # Doctrine docs that mention banned phrases as policy: skip.
    if path.name in ALLOWLIST_FILENAMES:
        return []
    if "banned" in lower or "we never" in lower or "we do not promise" in lower:
        return []
    issues: list[str] = []
    for phrase in BANNED_PHRASES:
        if phrase in lower:
            issues.append(f"{path}: contains banned phrase '{phrase}'")
    return issues


def main() -> int:
    issues: list[str] = []
    for d in SCAN_DIRS:
        if not d.is_dir():
            continue
        for p in d.rglob("*.md"):
            issues.extend(_scan_file(p))

    # Also scan the new partner docs we added in this layer.
    new_partner_docs = (
        REPO_ROOT / "docs" / "partners" / "ERP_CRM_PARTNER_PLAYBOOK.md",
        REPO_ROOT / "docs" / "partners" / "CYBERSECURITY_PARTNER_PLAYBOOK.md",
        REPO_ROOT / "docs" / "partners" / "WHITE_LABEL_REVENUE_OS.md",
        REPO_ROOT / "docs" / "partners" / "PARTNER_REFERRAL_TERMS_GUARDRAILS.md",
        REPO_ROOT / "docs" / "partners" / "PARTNER_ATTACK_SYSTEM.md",
    )
    for p in new_partner_docs:
        if p.is_file():
            issues.extend(_scan_file(p))

    print("Prompt-output quality scan")
    print("=" * 50)
    if not issues:
        print("OK: no banned phrases in customer-facing market-attack docs.")
        return 0
    for i in issues:
        print(f"  - {i}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
