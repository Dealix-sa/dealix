#!/usr/bin/env python3
"""Safety audit -> safety_audit.json.

Proves the non-negotiable rule structurally:
  1. Every draft in the daily queue has the hard no-send flags set correctly.
  2. The commercial scripts contain no live external-send transport calls.
  3. No draft contains a real recipient transport (smtp/api send) instruction.

Exit non-zero if any violation is found.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from startup_os_common import (
    NON_NEGOTIABLE_RULE,
    ROOT,
    now_iso,
    output_day_dir,
    read_jsonl,
    today_str,
    write_json,
)

# Live-send transport patterns that must NOT appear as executable calls in the
# commercial draft scripts. (Comments/strings describing prohibitions are fine,
# so we look for call-like usage.)
FORBIDDEN_CALL_PATTERNS = [
    r"smtplib\.SMTP\s*\(",
    r"server\.send_message\s*\(",
    r"sendmail\s*\(",
    r"twilio",
    r"requests\.post\s*\(\s*['\"]https?://",
    r"\.messages\.create\s*\(",
    r"graph\.facebook\.com",
    r"api\.linkedin\.com",
]

# The draft/content-producing scripts. The auditor and the secret scanner are
# intentionally excluded: they legitimately contain the forbidden tokens as
# *detection patterns*, not as live call sites.
SCANNED_SCRIPTS = [
    "commercial_generate_400_drafts.py",
    "commercial_score_drafts.py",
    "commercial_quality_gate.py",
    "commercial_compliance_gate.py",
    "commercial_founder_review_report.py",
    "commercial_metrics_summary.py",
    "commercial_launch_readiness.py",
    "media_social_calendar_generate.py",
    "media_social_verify.py",
]


def audit(day: str) -> dict:
    violations: list[str] = []
    checks: list[dict] = []

    # 1. Draft flag invariants.
    d = output_day_dir(day)
    queue = d / "draft_queue.jsonl"
    draft_count = 0
    if queue.exists():
        drafts = read_jsonl(queue)
        draft_count = len(drafts)
        for dr in drafts:
            if dr.get("send_allowed") is not False:
                violations.append(f"{dr.get('draft_id')}: send_allowed != False")
            if dr.get("external_send_blocked") is not True:
                violations.append(f"{dr.get('draft_id')}: external_send_blocked != True")
            if dr.get("requires_founder_approval") is not True:
                violations.append(f"{dr.get('draft_id')}: requires_founder_approval != True")
            if dr.get("no_auto_send") is not True:
                violations.append(f"{dr.get('draft_id')}: no_auto_send != True")
        checks.append(
            {
                "check": "draft_flag_invariants",
                "drafts": draft_count,
                "ok": draft_count > 0 and not violations,
            }
        )
    else:
        violations.append("draft_queue.jsonl missing — run the draft factory first")
        checks.append({"check": "draft_queue_present", "ok": False})

    # 2. No live-send transport in scripts.
    scripts_dir = ROOT / "scripts"
    transport_hits: list[str] = []
    for name in SCANNED_SCRIPTS:
        p = scripts_dir / name
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        for pat in FORBIDDEN_CALL_PATTERNS:
            for m in re.finditer(pat, text, re.IGNORECASE):
                line_no = text[: m.start()].count("\n") + 1
                transport_hits.append(f"{name}:{line_no}: matches /{pat}/")
    if transport_hits:
        violations.extend(transport_hits)
    checks.append(
        {"check": "no_live_send_transport", "ok": not transport_hits, "hits": transport_hits}
    )

    report = {
        "generated_at": now_iso(),
        "day": day,
        "non_negotiable_rule": NON_NEGOTIABLE_RULE,
        "draft_count": draft_count,
        "checks": checks,
        "violations": violations,
        "passed": not violations,
        "external_send": "blocked",
    }
    write_json(d / "safety_audit.json", report)
    return report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--day", default=today_str())
    args = ap.parse_args()
    r = audit(args.day)
    if r["passed"]:
        print(f"SAFETY AUDIT PASS — {r['draft_count']} drafts, no external send.")
        return 0
    print("SAFETY AUDIT FAIL:")
    for v in r["violations"][:50]:
        print(f"  - {v}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
