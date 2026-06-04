#!/usr/bin/env python3
"""Build the founder review queue artifacts: CSV, markdown, top-50, next actions, metrics."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from v5.lib import out_dir  # noqa: E402


def main() -> int:
    d = out_dir()
    queue = d / "draft_queue.jsonl"
    if not queue.exists():
        print("run commercial_generate_400_drafts.py first", file=sys.stderr)
        return 1
    drafts = [json.loads(l) for l in queue.read_text(encoding="utf-8").splitlines() if l.strip()]
    drafts.sort(key=lambda x: x.get("priority_score", 0), reverse=True)

    # CSV
    cols = ["draft_id", "company_name", "vertical", "channel", "language", "offer_name",
            "priority_score", "quality_score", "compliance_score", "requires_founder_approval",
            "send_allowed", "external_send_blocked", "status"]
    with (d / "founder_review.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for x in drafts:
            w.writerow({c: x.get(c, "") for c in cols})

    # Markdown summary
    md = ["# Founder Review Queue", "",
          "> AI prepared these. **You review, approve, and send manually. Nothing is sent by the system.**", "",
          f"- Total drafts: **{len(drafts)}**",
          f"- Date: {d.name}", ""]
    md.append("## Top 10 by priority\n")
    md.append("| # | Draft | Vertical | Channel | Lang | Offer | Priority |")
    md.append("|---|-------|----------|---------|------|-------|----------|")
    for i, x in enumerate(drafts[:10], 1):
        md.append(f"| {i} | {x['draft_id']} | {x['vertical']} | {x['channel']} | {x['language']} | {x['offer_name']} | {x['priority_score']} |")
    (d / "founder_review.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # Top 50
    top = ["# Top 50 Priority Drafts (review-only)\n"]
    for i, x in enumerate(drafts[:50], 1):
        top.append(f"### {i}. {x['draft_id']} — {x['vertical']} ({x['channel']}, {x['language']})")
        top.append(f"- **Offer:** {x['offer_name']} ({x['offer_price_sar']})")
        top.append(f"- **Subject:** {x['subject']}")
        top.append(f"- **Body:** {x['body']}")
        top.append(f"- **CTA:** {x['cta']} · **Opt-out:** {x['opt_out']}")
        top.append(f"- _send_allowed={x['send_allowed']}, external_send_blocked={x['external_send_blocked']}_\n")
    (d / "top_50_priority.md").write_text("\n".join(top) + "\n", encoding="utf-8")

    # Next actions
    (d / "next_actions.md").write_text(
        "# Next Actions (Founder)\n\n"
        "1. Open `founder_review.csv` and sort by priority.\n"
        "2. Approve/reject each draft (edit `status`, add `founder_notes`).\n"
        "3. For approved drafts, copy into `approved_manual_sends.example.csv` and send **manually**.\n"
        "4. Log replies in the CRM (see `config/crm_pipeline_schema.json`).\n\n"
        "> The system never sends. Manual founder action only.\n", encoding="utf-8")

    # Daily metrics
    by_channel: dict[str, int] = {}
    for x in drafts:
        by_channel[x["channel"]] = by_channel.get(x["channel"], 0) + 1
    metrics = {
        "date": d.name,
        "drafts_generated": len(drafts),
        "by_channel": by_channel,
        "manual_sends": 0,
        "founder_reviewed": 0,
        "note": "manual_sends/founder_reviewed are filled by the founder; no fabricated numbers",
    }
    (d / "daily_metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Founder review artifacts written to {d}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
