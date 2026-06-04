#!/usr/bin/env python3
"""
Final Launch Control verifier — runs the safety-critical V5 chain and confirms
GO/NO-GO. Orchestrates the sub-verifiers and asserts the review-only invariant.

Exit 0 only if all critical gates pass. Writes a console GO/NO-GO summary and
relies on outputs/startup_os + outputs/commercial_launch artifacts.
"""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable

# (label, argv, critical)
STEPS = [
    ("draft factory >=400", ["scripts/commercial_generate_400_drafts.py", "--target", "400"], True),
    ("score drafts", ["scripts/commercial_score_drafts.py"], True),
    ("safety audit", ["scripts/commercial_safety_audit.py"], True),
    ("compliance gate", ["scripts/commercial_compliance_gate.py"], True),
    ("crm schema verify", ["scripts/commercial_crm_schema_verify.py"], True),
    ("seed leads validate", ["scripts/commercial_seed_leads_validate.py"], True),
    ("media social calendar", ["scripts/media_social_calendar_generate.py"], True),
    ("media social verify", ["scripts/media_social_verify.py"], True),
    ("site static check", ["scripts/site_launch_static_check.py"], True),
    ("api no-send check", ["scripts/api_commercial_static_check.py"], True),
    ("secret & risk scan", ["scripts/final_secret_and_risk_scan.py"], True),
    ("ai eval sample", ["scripts/ai_eval_sample_drafts.py"], True),
    ("doc tree present", ["scripts/v5/scaffold_docs.py", "--check"], True),
    ("verticals present", ["scripts/v5/scaffold_verticals.py", "--check"], True),
    ("web pages present", ["scripts/v5/scaffold_web_pages.py", "--check"], True),
]


def main() -> int:
    results = []
    for label, argv, critical in STEPS:
        proc = subprocess.run([PY, *[str(ROOT / argv[0])], *argv[1:]],
                              cwd=ROOT, capture_output=True, text=True)
        ok = proc.returncode == 0
        results.append((label, ok, critical, proc.returncode))
        print(f"[{'PASS' if ok else 'FAIL'}] {label}")
        if not ok:
            sys.stdout.write(proc.stdout[-500:])
            sys.stderr.write(proc.stderr[-500:])

    crit_fail = [r for r in results if r[2] and not r[1]]
    status = "GO" if not crit_fail else "NO-GO"

    print("\n=== FINAL LAUNCH CONTROL ===")
    print(f"Decision: {status}")
    print("GO (ready): site, review-only drafts, founder review, manual posting, paid diagnostics, "
          "analytics schema, delivery/support prep, finance/legal templates, investor/partner/hiring readiness.")
    print("NO-GO (forbidden): automated email/WhatsApp/LinkedIn sending, auto-submit, bulk send, "
          "live paid ads without tracking/compliance, external sends from Actions, unbacked claims.")
    if crit_fail:
        print("Critical failures:", [r[0] for r in crit_fail])
    print("\nInvariant: the system never sends externally — all external actions remain founder-gated.")
    return 0 if status == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
