#!/usr/bin/env python3
"""
Dealix Ultimate OS Verification
Checks that core commercial files, scripts, and docs exist.
Exit 0 if verified, 1 if gaps found.
"""

import sys
from pathlib import Path

REQUIRED = [
    "scripts/check_no_secrets.py",
    "scripts/dealix_daily_operator.py",
    "scripts/generate_founder_dashboard_data.py",
    "scripts/score_leads.py",
    "scripts/generate_outreach_drafts.py",
    "scripts/generate_proposal.py",
    "scripts/review_proposal_quality.py",
    "scripts/production_readiness_check.py",
    "business/scoring/LEAD_SCORING_MODEL.md",
    "business/persuasion/OBJECTION_TO_RESPONSE_MAP.json",
    "business/persuasion/CTA_LIBRARY.json",
    "business/sales-machine/INDUSTRY_WEAKNESS_TAXONOMY.md",
    "business/sales-machine/OFFER_MATCHING_RULES.md",
    "business/governance/OUTREACH_REVIEW_GATE.md",
    "business/governance/CLIENT_DATA_RETENTION_POLICY.md",
    "business/governance/AI_OUTPUT_RISK_CLASSES.md",
    "business/governance/APPROVAL_MATRIX.md",
    "docs/ops/DAILY_OPERATOR_COMMANDS.md",
    "docs/deploy/VERCEL_FRONTEND_DEPLOYMENT.md",
    "docs/deploy/RAILWAY_BACKEND_DEPLOYMENT.md",
    "docs/deploy/ENVIRONMENT_VARIABLES.md",
    "docs/deploy/POST_DEPLOY_SMOKE_TEST.md",
    "docs/security/PRODUCTION_SECURITY_CHECKLIST.md",
    "tests/test_no_auto_send.py",
]

def main():
    root = Path(__file__).resolve().parent.parent
    missing = []
    for rel in REQUIRED:
        if not (root / rel).exists():
            missing.append(rel)
    if missing:
        print("[FAIL] Dealix Ultimate OS missing files:")
        for m in missing:
            print(f"  - {m}")
        sys.exit(1)
    print("[PASS] Dealix Ultimate OS core files present.")
    sys.exit(0)

if __name__ == "__main__":
    main()
