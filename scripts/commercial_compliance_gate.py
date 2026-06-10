#!/usr/bin/env python3
"""Compliance gate over the daily draft queue -> compliance_report.json.

Checks each draft for: opt-out present, no guaranteed-ROI claims, no banned
phrases, compliance score threshold. Rejected drafts are written to
rejected_drafts.jsonl. Sends nothing.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from startup_os_common import (
    now_iso,
    output_day_dir,
    read_jsonl,
    today_str,
    write_json,
    write_jsonl,
)

MIN_COMPLIANCE = 70

# Phrases that would constitute unproven claims / guarantees.
BANNED_SUBSTRINGS = [
    "guaranteed roi",
    "guaranteed revenue",
    "guaranteed results",
    "ضمان عائد",
    "نضمن لك",
    "مضمون 100",
    "100% guaranteed",
    "double your revenue",
    "risk free",
]


def check(draft: dict) -> list[str]:
    reasons = []
    text = f"{draft.get('subject','')} {draft.get('body','')}".lower()
    for phrase in BANNED_SUBSTRINGS:
        if phrase in text:
            reasons.append(f"banned_phrase:{phrase}")
    if not draft.get("opt_out"):
        reasons.append("missing_opt_out")
    if draft.get("compliance_score", 0) < MIN_COMPLIANCE:
        reasons.append(f"compliance<{MIN_COMPLIANCE}")
    # Safety invariants must hold.
    if draft.get("send_allowed") is not False:
        reasons.append("send_allowed_must_be_false")
    if draft.get("external_send_blocked") is not True:
        reasons.append("external_send_must_be_blocked")
    if draft.get("requires_founder_approval") is not True:
        reasons.append("must_require_founder_approval")
    return reasons


def run(day: str) -> dict:
    d = output_day_dir(day)
    drafts = read_jsonl(d / "draft_queue.jsonl")
    rejected = []
    for dr in drafts:
        reasons = check(dr)
        if reasons:
            rec = dict(dr)
            rec["rejection_reason"] = ";".join(reasons)
            rec["status"] = "rejected_compliance"
            rejected.append(rec)
    write_jsonl(d / "rejected_drafts.jsonl", rejected)
    report = {
        "generated_at": now_iso(),
        "day": day,
        "total": len(drafts),
        "min_compliance": MIN_COMPLIANCE,
        "rejected": len(rejected),
        "approved_for_review": len(drafts) - len(rejected),
        "banned_phrase_checks": len(BANNED_SUBSTRINGS),
        "reasons_histogram": _histogram(rejected),
    }
    write_json(d / "compliance_report.json", report)
    return report


def _histogram(rejected: list[dict]) -> dict:
    hist: dict[str, int] = {}
    for r in rejected:
        for reason in r["rejection_reason"].split(";"):
            key = reason.split(":")[0]
            hist[key] = hist.get(key, 0) + 1
    return hist


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--day", default=today_str())
    args = ap.parse_args()
    r = run(args.day)
    print(
        f"Compliance gate: {r['approved_for_review']}/{r['total']} approved for review, {r['rejected']} rejected"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
