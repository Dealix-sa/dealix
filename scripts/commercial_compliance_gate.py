#!/usr/bin/env python3
"""Commercial compliance gate.

Rejects drafts that break the Dealix outreach compliance rules:
no missing opt-out, no fake familiarity, no fake urgency, no guaranteed ROI,
no personal-data claims, no "from our database" / "as discussed", no
"replace your team" / "no human needed", privacy-first language for sensitive
sectors, and no channel that implies automated sending.

Usable as a library (compliance_gate / evaluate_compliance) and as a CLI that
re-checks an existing draft_queue.jsonl.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commercial_common import COMMERCIAL_OUTPUTS, load_config, read_jsonl, today_str


def _haystack(draft: dict[str, Any]) -> str:
    return f"{draft.get('subject', '')} {draft.get('body', '')} {draft.get('cta', '')}".lower()


def evaluate_compliance(draft: dict[str, Any], gates: dict[str, Any]) -> dict[str, Any]:
    """Return {score, passed, reasons[]} for a single draft."""
    reasons: list[str] = []
    score = 100
    text = _haystack(draft)

    for phrase in gates.get("forbidden_phrases", []):
        if phrase.lower() in text:
            reasons.append(f"forbidden_phrase:{phrase}")
            score -= 25
    for phrase in gates.get("fake_urgency_phrases", []):
        if phrase.lower() in text:
            reasons.append(f"fake_urgency:{phrase}")
            score -= 20
    for phrase in gates.get("fake_familiarity_phrases", []):
        if phrase.lower() in text:
            reasons.append(f"fake_familiarity:{phrase}")
            score -= 20

    required = gates.get("required_elements", {})
    opt_out_channels = required.get("opt_out_required_channels", [])
    if draft.get("channel") in opt_out_channels and not str(draft.get("opt_out", "")).strip():
        reasons.append("missing_opt_out")
        score -= 30

    privacy_verticals = required.get("privacy_first_required_verticals", [])
    if draft.get("vertical") in privacy_verticals:
        markers = [m.lower() for m in gates.get("privacy_first_markers_en", [])]
        markers += list(gates.get("privacy_first_markers_ar", []))
        raw = f"{draft.get('subject', '')} {draft.get('body', '')}".lower()
        if not any(m in raw for m in markers):
            reasons.append("missing_privacy_first_language")
            score -= 25

    # Safety flag integrity — a draft that claims it may be auto-sent is non-compliant.
    if draft.get("send_allowed") is True:
        reasons.append("send_allowed_true")
        score -= 100
    if draft.get("external_send_blocked") is False:
        reasons.append("external_send_blocked_false")
        score -= 100
    if draft.get("no_auto_send") is False:
        reasons.append("no_auto_send_false")
        score -= 100

    score = max(0, score)
    passed = score >= gates.get("min_compliance_score", 80) and not any(
        r.startswith(("forbidden_phrase", "send_allowed", "external_send", "no_auto_send"))
        for r in reasons
    )
    return {"score": score, "passed": passed, "reasons": reasons}


def compliance_gate(draft: dict[str, Any], gates: dict[str, Any]) -> tuple[int, bool, list[str]]:
    result = evaluate_compliance(draft, gates)
    return result["score"], result["passed"], result["reasons"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Re-run the compliance gate on a draft queue.")
    parser.add_argument("--date", default=today_str())
    parser.add_argument("--queue", default=None)
    args = parser.parse_args()

    gates = load_config("commercial_compliance_gates.json")
    queue = Path(args.queue) if args.queue else COMMERCIAL_OUTPUTS / args.date / "draft_queue.jsonl"
    drafts = read_jsonl(queue)
    if not drafts:
        print(f"No drafts found at {queue}")
        return 0

    failed = 0
    for draft in drafts:
        result = evaluate_compliance(draft, gates)
        if not result["passed"]:
            failed += 1
    print(f"Compliance gate: {len(drafts)} drafts, {failed} non-compliant.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
