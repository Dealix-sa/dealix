#!/usr/bin/env python3
"""Commercial quality gate.

Scores draft quality on completeness, length, personalization, CTA presence,
and opt-out presence. Usable as a library (evaluate_quality / quality_gate) and
as a CLI that re-checks an existing draft_queue.jsonl.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commercial_common import COMMERCIAL_OUTPUTS, load_config, read_jsonl, today_str


def evaluate_quality(draft: dict[str, Any], gates: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    score = 100

    subject = str(draft.get("subject", ""))
    body = str(draft.get("body", ""))

    if len(subject) < gates.get("min_subject_length", 8):
        reasons.append("subject_too_short")
        score -= 20
    if len(subject) > gates.get("max_subject_length", 90):
        reasons.append("subject_too_long")
        score -= 10
    if len(body) < gates.get("min_body_length", 120):
        reasons.append("body_too_short")
        score -= 40
    if len(body) > gates.get("max_body_length", 1400):
        reasons.append("body_too_long")
        score -= 10

    if gates.get("require_cta", True) and not str(draft.get("cta", "")).strip():
        reasons.append("missing_cta")
        score -= 20

    opt_out_channels = gates.get("require_opt_out_for_channels", [])
    if draft.get("channel") in opt_out_channels and not str(draft.get("opt_out", "")).strip():
        reasons.append("missing_opt_out")
        score -= 20

    # Personalization: at least one token's value should appear in the body.
    tokens = gates.get("personalization_tokens", [])
    personalized = any(
        str(draft.get(tok, "")).strip() and str(draft.get(tok, "")) in body for tok in tokens
    )
    if not personalized:
        reasons.append("not_personalized")
        score -= 15

    score = max(0, score)
    passed = score >= gates.get("min_quality_score", 60)
    return {"score": score, "passed": passed, "reasons": reasons}


def quality_gate(draft: dict[str, Any], gates: dict[str, Any]) -> tuple[int, bool, list[str]]:
    result = evaluate_quality(draft, gates)
    return result["score"], result["passed"], result["reasons"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Re-run the quality gate on a draft queue.")
    parser.add_argument("--date", default=today_str())
    parser.add_argument("--queue", default=None)
    args = parser.parse_args()

    gates = load_config("commercial_quality_gates.json")
    queue = Path(args.queue) if args.queue else COMMERCIAL_OUTPUTS / args.date / "draft_queue.jsonl"
    drafts = read_jsonl(queue)
    if not drafts:
        print(f"No drafts found at {queue}")
        return 0

    failed = sum(0 if evaluate_quality(d, gates)["passed"] else 1 for d in drafts)
    print(f"Quality gate: {len(drafts)} drafts, {failed} below threshold.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
