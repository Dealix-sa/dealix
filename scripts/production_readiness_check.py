#!/usr/bin/env python3
"""
Dealix Production Readiness Check
Runs a bundle of checks before launch.
"""

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

def run(cmd: list) -> int:
    print(f"\n>>> {' '.join(cmd)}")
    return subprocess.call(cmd)

def main():
    checks = [
        ([sys.executable, str(REPO / "scripts" / "check_no_secrets.py")], "No secrets"),
        ([sys.executable, str(REPO / "scripts" / "verify_dealix_ultimate_os.py")], "Ultimate OS verification"),
        ([sys.executable, str(REPO / "scripts" / "dealix_daily_operator.py"), "--mode", "demo"], "Daily operator demo"),
        ([sys.executable, str(REPO / "scripts" / "generate_outreach_drafts.py"), "--top", "5", "--mode", "demo"], "Outreach drafts"),
        ([sys.executable, str(REPO / "scripts" / "generate_proposal.py"), "--account-id", "demo-001", "--offer", "Revenue OS", "--lang", "en", "--mode", "demo"], "Proposal generation"),
    ]
    results = []
    for cmd, name in checks:
        rc = run(cmd)
        results.append((name, rc == 0))

    # Check deploy docs exist
    deploy_docs = [
        REPO / "docs" / "deploy" / "VERCEL_FRONTEND_DEPLOYMENT.md",
        REPO / "docs" / "deploy" / "RAILWAY_BACKEND_DEPLOYMENT.md",
        REPO / "docs" / "deploy" / "ENVIRONMENT_VARIABLES.md",
    ]
    for d in deploy_docs:
        results.append((str(d.relative_to(REPO)), d.exists()))

    # Check governance docs
    gov_docs = [
        REPO / "business" / "governance" / "OUTREACH_REVIEW_GATE.md",
        REPO / "business" / "governance" / "CLIENT_DATA_RETENTION_POLICY.md",
    ]
    for d in gov_docs:
        results.append((str(d.relative_to(REPO)), d.exists()))

    print("\n=== PRODUCTION READINESS RESULTS ===")
    all_pass = True
    for name, ok in results:
        status = "PASS" if ok else "FAIL"
        if not ok:
            all_pass = False
        print(f"  [{status}] {name}")

    if all_pass:
        print("\n[PASS] Production readiness check complete.")
        sys.exit(0)
    else:
        print("\n[FAIL] Some checks failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
