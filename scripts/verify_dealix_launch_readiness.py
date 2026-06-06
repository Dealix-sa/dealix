#!/usr/bin/env python3
"""Dealix Launch Readiness — aggregate gate + score.

Dependency-free (stdlib only). Composes the other three verifiers plus a
required-artifact checklist into a single readiness score and a
Private / Public launch verdict.

Scoring:
  - Each required artifact present = weight points.
  - Each sub-verifier PASS = weight points.
  - Score is reported 0-100.

Private Launch Ready when:
  - all P0 artifacts present AND positioning/module/growth verifiers PASS.
Public Launch Ready when:
  - Private Launch Ready AND score >= 85 AND npm build evidence present.

This script always exits 0 (it reports a score, never blocks), unless
invoked with --strict, in which case it exits non-zero if not Private-Launch
ready. The launch-gates workflow uses --strict.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# (label, path, weight)
REQUIRED_ARTIFACTS = [
    ("Platform Source of Truth", "docs/00_platform_truth/PLATFORM_SOURCE_OF_TRUTH.md", 6),
    ("Module Status Map", "docs/00_platform_truth/MODULE_STATUS_MAP.md", 6),
    ("Launch Control Tower", "docs/00_platform_truth/LAUNCH_CONTROL_TOWER.md", 4),
    ("Claims Register", "docs/03_governance/CLAIMS_REGISTER.md", 8),
    ("Human Approval Policy", "docs/03_governance/HUMAN_APPROVAL_POLICY.md", 8),
    ("Proof Pack Template", "docs/04_delivery/PROOF_PACK_TEMPLATE.md", 8),
    ("Customer Folder Template", "docs/04_delivery/CUSTOMER_FOLDER_TEMPLATE.md", 8),
    ("Self-Growth OS", "docs/06_growth/SELF_GROWTH_OS.md", 4),
    ("Command Sprint One-Pager", "sales/COMMAND_SPRINT_ONE_PAGER.md", 8),
    ("Diagnostic Script", "sales/DIAGNOSTIC_SCRIPT.md", 8),
    ("CLAUDE.md", "CLAUDE.md", 2),
]

# (label, script, weight)
SUB_VERIFIERS = [
    ("Positioning", "scripts/verify_dealix_positioning.py", 8),
    ("Module Status", "scripts/verify_dealix_module_status.py", 7),
    ("Growth Assets", "scripts/verify_dealix_growth_assets.py", 7),
]


def run_script(rel: str) -> bool:
    path = ROOT / rel
    if not path.is_file():
        return False
    res = subprocess.run(
        [sys.executable, str(path)],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    return res.returncode == 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help="exit non-zero if not Private-Launch ready")
    args = ap.parse_args()

    print("== Dealix Launch Readiness ==")
    total = 0
    earned = 0

    print("-- required artifacts --")
    all_p0 = True
    for label, rel, weight in REQUIRED_ARTIFACTS:
        total += weight
        present = (ROOT / rel).is_file()
        if present:
            earned += weight
            print(f"PASS: {label}")
        else:
            all_p0 = False
            print(f"FAIL: missing {label} ({rel})")

    print("-- sub-verifiers --")
    verifiers_ok = True
    for label, rel, weight in SUB_VERIFIERS:
        total += weight
        passed = run_script(rel)
        if passed:
            earned += weight
            print(f"PASS: {label} verifier")
        else:
            verifiers_ok = False
            print(f"FAIL: {label} verifier")

    score = round(earned / total * 100) if total else 0

    # Public-launch evidence:
    #  - build log present AND records a passing build, and
    #  - a business-proof marker that is created ONLY after 3 paid Command
    #    Sprints + 3 Proof Packs + 1 case-safe story (see LAUNCH_CONTROL_TOWER).
    build_log = ROOT / "reports/launch/npm_build.log"
    build_evidence = build_log.is_file()
    build_passed = False
    if build_evidence:
        log_text = build_log.read_text(encoding="utf-8", errors="ignore")
        build_passed = "npm run build exit=0" in log_text
    proof_marker = ROOT / "reports/launch/PUBLIC_LAUNCH_PROOF.md"
    revenue_proof = proof_marker.is_file()

    private_ready = all_p0 and verifiers_ok
    public_ready = private_ready and score >= 85 and build_passed and revenue_proof

    print()
    print(f"SCORE: {score}/100")
    print(f"BUILD EVIDENCE: {'PASS' if build_passed else ('present, not passing' if build_evidence else 'none')}")
    print(f"PRIVATE LAUNCH READY: {'YES' if private_ready else 'NO'}")
    pub_reason = []
    if not build_passed:
        pub_reason.append("no passing build log")
    if not revenue_proof:
        pub_reason.append("no reports/launch/PUBLIC_LAUNCH_PROOF.md (needs 3 paid Sprints + 3 Proof Packs + case story)")
    print(f"PUBLIC LAUNCH READY:  {'YES' if public_ready else 'NO'}"
          + (f"  ({'; '.join(pub_reason)})" if pub_reason else ""))

    if args.strict and not private_ready:
        print("\nRESULT: FAIL (strict: not Private-Launch ready)")
        return 1
    print("\nRESULT: PASS (score reported)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
