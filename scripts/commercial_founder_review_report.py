#!/usr/bin/env python3
"""Build the Founder Review Queue artifacts from the daily draft queue.

Outputs (all review-only, nothing is sent):
  - founder_review.csv          full queue for manual triage
  - founder_review.md           human-readable review pack
  - top_50_priority.md          top 50 by priority for the founder to action first
  - approved_manual_sends.example.csv   template the founder fills AFTER manual approval
  - next_actions.md             the founder's manual next-step checklist
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from startup_os_common import (
    NON_NEGOTIABLE_RULE,
    output_day_dir,
    read_jsonl,
    today_str,
)

CSV_FIELDS = [
    "draft_id",
    "channel",
    "language",
    "vertical",
    "company_name",
    "buyer_title",
    "offer_stage",
    "offer_name",
    "pain_angle",
    "priority_score",
    "quality_score",
    "compliance_score",
    "fit_score",
    "risk_level",
    "research_required",
    "requires_founder_approval",
    "send_allowed",
    "status",
    "subject",
]


def run(day: str) -> dict:
    d = output_day_dir(day)
    drafts = read_jsonl(d / "draft_queue.jsonl")
    drafts.sort(key=lambda x: x.get("priority_score", 0), reverse=True)

    # founder_review.csv
    with (d / "founder_review.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=CSV_FIELDS, extrasaction="ignore")
        w.writeheader()
        for dr in drafts:
            w.writerow(dr)

    # founder_review.md
    lines = [
        f"# Founder Review Queue — {day}",
        "",
        f"> {NON_NEGOTIABLE_RULE}",
        "",
        f"- Total drafts: **{len(drafts)}**",
        "- Channels: "
        + ", ".join(
            f"{c}={sum(1 for x in drafts if x['channel']==c)}"
            for c in ("cold_email", "follow_up", "linkedin_manual", "website_form")
        ),
        "",
        "**No draft has been sent. Every row requires your manual approval and manual send.**",
        "",
        "| # | draft_id | channel | vertical | company | offer | priority | risk |",
        "|---|----------|---------|----------|---------|-------|----------|------|",
    ]
    for i, dr in enumerate(drafts[:100], 1):
        lines.append(
            f"| {i} | {dr['draft_id']} | {dr['channel']} | {dr['vertical']} | "
            f"{dr['company_name']} | {dr['offer_stage']} | {dr['priority_score']} | {dr['risk_level']} |"
        )
    (d / "founder_review.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # top_50_priority.md
    top = drafts[:50]
    tlines = [f"# Top 50 Priority Drafts — {day}", "", f"> {NON_NEGOTIABLE_RULE}", ""]
    for i, dr in enumerate(top, 1):
        tlines += [
            f"## {i}. {dr['draft_id']} — {dr['company_name']} ({dr['vertical']})",
            f"- Channel: {dr['channel']} | Language: {dr['language']} | Offer: {dr['offer_name']}",
            f"- Priority: {dr['priority_score']} | Risk: {dr['risk_level']}",
            f"- Subject: {dr['subject']}",
            "",
            "```",
            dr["body"],
            "```",
            f"_CTA:_ {dr['cta']}  |  _Opt-out:_ {dr['opt_out']}",
            "",
            "**Action required: founder must review, edit, approve, and send manually.**",
            "",
        ]
    (d / "top_50_priority.md").write_text("\n".join(tlines) + "\n", encoding="utf-8")

    # approved_manual_sends.example.csv (template only)
    with (d / "approved_manual_sends.example.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(
            [
                "draft_id",
                "approved_by_founder",
                "edited",
                "sent_manually",
                "sent_channel",
                "sent_at",
                "notes",
            ]
        )
        for dr in top[:5]:
            w.writerow(
                [
                    dr["draft_id"],
                    "NO",
                    "NO",
                    "NO",
                    "",
                    "",
                    "example row — founder fills after manual approval",
                ]
            )

    # next_actions.md
    nlines = [
        f"# Founder Next Actions — {day}",
        "",
        f"> {NON_NEGOTIABLE_RULE}",
        "",
        "1. Open `top_50_priority.md` and review the highest-priority drafts.",
        "2. Edit any draft as needed. Verify the company, person, and offer fit.",
        "3. For approved drafts, send them MANUALLY from your own account/channel.",
        "4. Record approvals in `approved_manual_sends.example.csv`.",
        "5. Log replies into the CRM and update lead stages.",
        "6. Anything in `needs_research.jsonl` requires research before any outreach.",
        "",
        "The system has sent nothing. It only drafts, scores, ranks, and recommends.",
    ]
    (d / "next_actions.md").write_text("\n".join(nlines) + "\n", encoding="utf-8")

    return {"total": len(drafts), "top": len(top)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--day", default=today_str())
    args = ap.parse_args()
    r = run(args.day)
    print(f"Founder review report built for {r['total']} drafts (top {r['top']}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
