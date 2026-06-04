#!/usr/bin/env python3
"""Commercial draft scoring: fit, risk, and priority.

- fit_score: how well the lead/offer match the ICP signals we have.
- risk_level: low/medium/high based on risky language in the draft.
- priority_score: weighted blend used to rank the founder review queue.

Usable as a library and as a CLI that re-scores an existing draft_queue.jsonl.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commercial_common import (
    COMMERCIAL_OUTPUTS,
    load_config,
    read_jsonl,
    today_str,
    write_jsonl,
)


def compute_fit(draft: dict[str, Any]) -> int:
    score = 60
    if draft.get("vertical"):
        score += 10
    if draft.get("city"):
        score += 5
    if draft.get("buyer_title"):
        score += 5
    opt_in = str(draft.get("opt_in_status", "")).lower()
    if opt_in == "opted_in":
        score += 15
    elif opt_in == "not_opted_in":
        score -= 10
    return max(0, min(100, score))


def compute_risk(draft: dict[str, Any], risk_cfg: dict[str, Any]) -> str:
    text = f"{draft.get('subject', '')} {draft.get('body', '')} {draft.get('cta', '')}".lower()
    for term in risk_cfg.get("high_risk_terms", []):
        if term.lower() in text:
            return "high"
    for term in risk_cfg.get("sensitive_data_terms", []):
        if term.lower() in text:
            return "high"
    for term in risk_cfg.get("medium_risk_terms", []):
        if term.lower() in text:
            return "medium"
    return risk_cfg.get("default_risk_level", "low")


def compute_priority(draft: dict[str, Any], weights: dict[str, float]) -> float:
    value = (
        weights.get("fit_score", 0.45) * float(draft.get("fit_score", 0))
        + weights.get("quality_score", 0.35) * float(draft.get("quality_score", 0))
        + weights.get("compliance_score", 0.20) * float(draft.get("compliance_score", 0))
    )
    return round(value, 2)


def score_draft(
    draft: dict[str, Any], risk_cfg: dict[str, Any], weights: dict[str, float]
) -> dict[str, Any]:
    draft["fit_score"] = compute_fit(draft)
    draft["risk_level"] = compute_risk(draft, risk_cfg)
    draft["priority_score"] = compute_priority(draft, weights)
    return draft


def main() -> int:
    parser = argparse.ArgumentParser(description="Re-score a draft queue.")
    parser.add_argument("--date", default=today_str())
    parser.add_argument("--queue", default=None)
    args = parser.parse_args()

    risk_cfg = load_config("commercial_risk_terms.json")
    weights = load_config("commercial_founder_review_rules.json").get("priority_weights", {})
    queue = Path(args.queue) if args.queue else COMMERCIAL_OUTPUTS / args.date / "draft_queue.jsonl"
    drafts = read_jsonl(queue)
    if not drafts:
        print(f"No drafts found at {queue}")
        return 0
    for d in drafts:
        score_draft(d, risk_cfg, weights)
    write_jsonl(queue, drafts)
    print(f"Re-scored {len(drafts)} drafts in {queue}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
