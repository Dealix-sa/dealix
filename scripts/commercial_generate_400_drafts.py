#!/usr/bin/env python3
"""Generate review-only commercial outreach drafts (default target 400).

Outputs (under ``outputs/commercial_launch/YYYY-MM-DD/``):
    - draft_queue.jsonl     one JSON object per draft
    - top_50_priority.md    the 50 highest-priority drafts as a review table
    - draft_summary.json    aggregate counts for dashboards/verifiers

SAFETY: every draft is REVIEW-ONLY. Nothing here sends email, WhatsApp,
LinkedIn, or submits a form. No scraping, no secrets. Companies/contacts are
synthetic placeholders unless a local seed file is provided by the founder.

    AI prepares. Founder approves. Manual action only. No external sending.
"""

from __future__ import annotations

import argparse
import hashlib

from _v7_revenue_common import (
    OUTPUTS,
    SAFETY_BANNER,
    SEED_CHANNELS,
    SEED_VERTICALS,
    today,
    write_json,
    write_jsonl,
    write_text,
)

LANGUAGES = ("ar", "en")
RISK_LEVELS = ("low", "medium", "high")


def _score(seed: str) -> int:
    """Deterministic 40-99 priority score from a stable hash (no randomness)."""
    h = int(hashlib.sha256(seed.encode("utf-8")).hexdigest(), 16)
    return 40 + (h % 60)


def _draft(idx: int) -> dict:
    vertical = SEED_VERTICALS[idx % len(SEED_VERTICALS)]
    channel = SEED_CHANNELS[idx % len(SEED_CHANNELS)]
    language = LANGUAGES[idx % len(LANGUAGES)]
    company = f"Prospect {idx:04d} ({vertical})"
    draft_id = f"DRAFT-{today()}-{idx:04d}"
    score = _score(draft_id)
    risk = RISK_LEVELS[score % len(RISK_LEVELS)]
    if language == "ar":
        copy = (
            f"مرحباً، لاحظنا أن شركات {vertical} تواجه احتكاكاً في عملياتها اليومية. "
            "أعددنا تشخيصاً مختصراً قد يكشف فرص توفير. هل تسمح بمكالمة 15 دقيقة؟ "
            "(مسودة للمراجعة فقط — لن تُرسل تلقائياً)"
        )
    else:
        copy = (
            f"Hi, we noticed {vertical} teams hit recurring operational friction. "
            "We prepared a short diagnostic that may surface savings. Open to a "
            "15-minute call? (Review-only draft — not auto-sent.)"
        )
    return {
        "draft_id": draft_id,
        "company": company,
        "vertical": vertical,
        "channel": channel,
        "language": language,
        "priority_score": score,
        "risk_level": risk,
        "stage": "draft_generated",
        "manual_copy_text": copy,
        "review_only": True,
        "send_blocked": True,
    }


def generate(target: int, date: str | None = None) -> dict:
    date = today(date)
    out_dir = OUTPUTS / "commercial_launch" / date
    drafts = [_draft(i) for i in range(1, target + 1)]

    write_jsonl(out_dir / "draft_queue.jsonl", drafts)

    top = sorted(drafts, key=lambda d: d["priority_score"], reverse=True)[:50]
    lines = [
        "# Top 50 Priority Drafts — Review Only",
        "",
        f"> {SAFETY_BANNER}",
        "",
        f"Generated: {date} · Total drafts: {len(drafts)}",
        "",
        "| # | draft_id | company | vertical | channel | lang | score | risk |",
        "| - | -------- | ------- | -------- | ------- | ---- | ----- | ---- |",
    ]
    for i, d in enumerate(top, start=1):
        lines.append(
            f"| {i} | {d['draft_id']} | {d['company']} | {d['vertical']} | "
            f"{d['channel']} | {d['language']} | {d['priority_score']} | {d['risk_level']} |"
        )
    lines += [
        "",
        "## Founder note",
        "",
        (
            "These are preparation drafts. Pick the strongest, copy the text "
            "**manually**, and send it yourself through your own account. "
            "Nothing here is auto-sent."
        ),
        "",
    ]
    write_text(out_dir / "top_50_priority.md", "\n".join(lines))

    summary = {
        "date": date,
        "target": target,
        "drafts_generated": len(drafts),
        "by_vertical": {v: sum(1 for d in drafts if d["vertical"] == v) for v in SEED_VERTICALS},
        "by_channel": {c: sum(1 for d in drafts if d["channel"] == c) for c in SEED_CHANNELS},
        "review_only": True,
        "send_blocked": True,
        "safety": SAFETY_BANNER,
    }
    write_json(out_dir / "draft_summary.json", summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=int, default=400, help="Number of drafts")
    parser.add_argument("--date", default=None, help="Override date (YYYY-MM-DD)")
    args = parser.parse_args()
    target = max(1, args.target)
    summary = generate(target, args.date)
    print(f"[commercial_generate] {summary['drafts_generated']} review-only drafts → "
          f"outputs/commercial_launch/{summary['date']}/")
    print(f"[commercial_generate] {SAFETY_BANNER}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
