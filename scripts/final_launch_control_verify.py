#!/usr/bin/env python3
"""Final Launch Control verifier — runs the safety-critical spine and aggregates.

Runs (as subprocesses, file-only):
  - draft factory (target 400) + safety audit
  - commercial launch readiness
  - media-social verify
  - site launch static check
  - crm schema verify
  - api commercial static check
  - secret & risk scan
  - startup_os_verify

Aggregates pass/fail into outputs/startup_os/final_launch_control.{json,md}.
Exit 0 only if all critical checks pass. Read-only / file-only.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from startup_os_common import ROOT, now_iso, today_str, write_json

PY = sys.executable
S = str(ROOT / "scripts")

STEPS = [
    ("draft_factory", [PY, f"{S}/commercial_generate_400_drafts.py", "--target", "400"], True),
    ("score", [PY, f"{S}/commercial_score_drafts.py"], False),
    ("quality_gate", [PY, f"{S}/commercial_quality_gate.py"], False),
    ("compliance_gate", [PY, f"{S}/commercial_compliance_gate.py"], False),
    ("founder_review", [PY, f"{S}/commercial_founder_review_report.py"], False),
    ("metrics", [PY, f"{S}/commercial_metrics_summary.py"], False),
    ("safety_audit", [PY, f"{S}/commercial_safety_audit.py"], True),
    ("seed_leads", [PY, f"{S}/commercial_seed_leads_validate.py"], True),
    ("crm_schema", [PY, f"{S}/commercial_crm_schema_verify.py"], True),
    ("media_social", [PY, f"{S}/media_social_calendar_generate.py"], False),
    ("media_social_verify", [PY, f"{S}/media_social_verify.py"], True),
    ("site_static", [PY, f"{S}/site_launch_static_check.py"], True),
    ("api_static", [PY, f"{S}/api_commercial_static_check.py"], True),
    ("secret_scan", [PY, f"{S}/final_secret_and_risk_scan.py", "--strict"], True),
    ("startup_os_verify", [PY, f"{S}/startup_os_verify.py"], True),
]


def run() -> dict:
    results = []
    for name, cmd, critical in STEPS:
        proc = subprocess.run(cmd, capture_output=True, text=True)
        results.append(
            {
                "step": name,
                "rc": proc.returncode,
                "ok": proc.returncode == 0,
                "critical": critical,
                "tail": (proc.stdout.strip().splitlines()[-1:] or [""])[0],
            }
        )

    critical_fail = [r for r in results if r["critical"] and not r["ok"]]
    passed = not critical_fail
    report = {
        "generated_at": now_iso(),
        "day": today_str(),
        "passed": passed,
        "decision": "PASS" if passed else "FAIL",
        "results": results,
        "critical_failures": [r["step"] for r in critical_fail],
        "non_negotiable_rule": "System never sends externally. Founder reviews and acts manually.",
    }
    out_dir = ROOT / "outputs" / "startup_os"
    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "final_launch_control.json", report)

    md = [
        "# Final Launch Control",
        "",
        f"- Generated: {report['generated_at']}",
        f"- Decision: **{report['decision']}**",
        "",
        "| Step | Critical | OK | rc |",
        "|---|---|---|---|",
    ]
    for r in results:
        md.append(
            f"| {r['step']} | {'yes' if r['critical'] else 'no'} | {'✅' if r['ok'] else '❌'} | {r['rc']} |"
        )
    (out_dir / "final_launch_control.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return report


def main() -> int:
    r = run()
    print(f"Final Launch Control: {r['decision']}")
    for res in r["results"]:
        mark = "OK " if res["ok"] else "FAIL"
        print(f"  [{mark}] {res['step']} (rc={res['rc']})")
    return 0 if r["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
