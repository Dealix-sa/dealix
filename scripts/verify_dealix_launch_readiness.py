#!/usr/bin/env python3
"""Dealix launch-readiness scorer (Wave 7) — the canonical private-launch gate.

Scores the presence + integrity of the assets needed to manually sell and
deliver the first Command Sprint. Each check is weighted; the total is a
0-100 readiness score with a verdict band:

  0-49   = No-Go
  50-69  = Internal Only
  70-84  = Private Launch Ready
  85-100 = Public Limited Ready

This does NOT run the build or external integrations — those are graded by
the master runner. This grades the *assets*. Exit code is 0 when the score
clears the private-launch threshold (>=70), else 1. Pure stdlib.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PRIVATE_LAUNCH_THRESHOLD = 70

# (weight, label, path-exists-check, optional substring that must be present)
CHECKS = [
    (15, "Command Sprint page", "landing/command-sprint.html", "Command Sprint"),
    (10, "Start path", "landing/start.html", None),
    (10, "Diagnostic path", "landing/diagnostic.html", None),
    (10, "Pricing page", "landing/pricing.html", None),
    (8, "Security/Trust page", "landing/security.html", None),
    (10, "Proof Pack template", "data/templates/proof_pack_ar.md", None),
    (12, "Customer Folder template", "customers/_template/00_intake.md", None),
    (10, "Claims Register", "docs/governance/CLAIMS_REGISTER.md", None),
    (10, "Human Approval Policy", "docs/governance/HUMAN_APPROVAL_POLICY.md", None),
    (5, "Sales one-pager", "sales/COMMAND_SPRINT_ONE_PAGER.md", None),
    (5, "Diagnostic script", "sales/COMMAND_SPRINT_DIAGNOSTIC_SCRIPT.md", None),
    (5, "Module status registry", "data/launch/module_status.json", None),
    (5, "First-30 targets file", "data/growth/first_30_targets.csv", None),
    (5, "Outreach approval queue", "reports/revenue/outreach_approval_queue.md", None),
]

# Some sales-kit assets may live under sales/ with alternate names; accept
# either canonical or any file matching a glob, to avoid brittle naming.
ALT_GLOBS = {
    "sales/COMMAND_SPRINT_ONE_PAGER.md": "sales/*ONE_PAGER*.md",
    "sales/COMMAND_SPRINT_DIAGNOSTIC_SCRIPT.md": "sales/*DIAGNOSTIC*SCRIPT*.md",
}


def _exists(rel: str) -> bool:
    p = ROOT / rel
    if p.is_file():
        return True
    glob = ALT_GLOBS.get(rel)
    if glob and list(ROOT.glob(glob)):
        return True
    return False


def main() -> int:
    print("== Dealix launch-readiness scorer ==")
    earned = 0
    total = 0
    missing: list[str] = []
    for weight, label, rel, needle in CHECKS:
        total += weight
        ok = _exists(rel)
        if ok and needle is not None:
            # confirm the substring is present for content-bearing assets
            content = (ROOT / rel).read_text(encoding="utf-8", errors="replace") if (ROOT / rel).is_file() else ""
            ok = needle.lower() in content.lower()
        if ok:
            earned += weight
            print(f"  [+{weight:>2}] OK   {label}")
        else:
            missing.append(f"{label} ({rel})")
            print(f"  [ +0] MISS {label} -> {rel}")

    score = round(100 * earned / total) if total else 0
    if score >= 85:
        verdict = "Public Limited Ready"
    elif score >= 70:
        verdict = "Private Launch Ready"
    elif score >= 50:
        verdict = "Internal Only"
    else:
        verdict = "No-Go"

    print(f"\nSCORE: {score}/100  ->  {verdict}")
    if missing:
        print("MISSING:")
        for m in missing:
            print(f"  - {m}")

    # Machine-readable line for the master runner to grep.
    print(f"READINESS_SCORE={score}")
    print(f"READINESS_VERDICT={verdict}")

    return 0 if score >= PRIVATE_LAUNCH_THRESHOLD else 1


if __name__ == "__main__":
    sys.exit(main())
