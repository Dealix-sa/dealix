#!/usr/bin/env python3
"""Build the Founder Action Queue from the day's review-only draft queue.

Reads:
    outputs/commercial_launch/YYYY-MM-DD/draft_queue.jsonl
    outputs/commercial_launch/YYYY-MM-DD/top_50_priority.md  (presence only)

Writes (under outputs/founder_action_queue/YYYY-MM-DD/):
    founder_actions.csv
    founder_actions.md
    manual_send_queue.example.csv
    call_priority_list.md
    today_revenue_plan.md

Each action is a decision the FOUNDER makes by hand. This script never sends,
never calls an API, never touches SMTP/WhatsApp/LinkedIn. If today's draft
queue is missing it is generated first (review-only) so the queue is never empty.

    AI prepares. Founder approves. Manual action only. No external sending.
"""

from __future__ import annotations

import argparse

from _v7_revenue_common import (
    ACTION_STATES,
    OUTPUTS,
    SAFETY_BANNER,
    read_jsonl,
    today,
    write_csv,
    write_text,
)

ACTION_FIELDS = [
    "action_id",
    "source_draft_id",
    "company",
    "vertical",
    "channel",
    "language",
    "priority_score",
    "risk_level",
    "recommended_action",
    "manual_copy_text",
    "founder_decision",
    "status",
    "notes",
]


def _recommended_action(channel: str, risk: str) -> str:
    base = {
        "email": "Copy text → send from your own email manually",
        "whatsapp_manual": "Copy text → send manually from your WhatsApp",
        "linkedin_manual": "Copy text → send manually as a LinkedIn DM",
        "phone": "Add to call priority list and dial manually",
    }.get(channel, "Manual review")
    if risk == "high":
        return f"HOLD for extra research before any contact — {base}"
    return base


def _load_drafts(date: str) -> list[dict]:
    path = OUTPUTS / "commercial_launch" / date / "draft_queue.jsonl"
    drafts = read_jsonl(path)
    if drafts:
        return drafts
    # Generate review-only drafts on demand so the queue is never empty.
    from commercial_generate_400_drafts import generate as gen_drafts

    gen_drafts(target=400, date=date)
    return read_jsonl(path)


def generate(date: str | None = None, limit: int = 50) -> dict:
    date = today(date)
    drafts = _load_drafts(date)
    top = sorted(drafts, key=lambda d: d.get("priority_score", 0), reverse=True)[:limit]

    actions: list[dict] = []
    for i, d in enumerate(top, start=1):
        risk = d.get("risk_level", "medium")
        actions.append(
            {
                "action_id": f"ACT-{date}-{i:03d}",
                "source_draft_id": d.get("draft_id", ""),
                "company": d.get("company", ""),
                "vertical": d.get("vertical", ""),
                "channel": d.get("channel", ""),
                "language": d.get("language", ""),
                "priority_score": d.get("priority_score", 0),
                "risk_level": risk,
                "recommended_action": _recommended_action(d.get("channel", ""), risk),
                "manual_copy_text": d.get("manual_copy_text", ""),
                "founder_decision": "",
                "status": "needs_research" if risk == "high" else "review",
                "notes": "",
            }
        )

    out_dir = OUTPUTS / "founder_action_queue" / date

    write_csv(out_dir / "founder_actions.csv", ACTION_FIELDS, actions)

    md = [
        "# Founder Action Queue",
        "",
        f"> {SAFETY_BANNER}",
        "",
        f"Date: {date} · Actions: {len(actions)}",
        "",
        f"Allowed statuses: {', '.join(ACTION_STATES)}",
        "",
        "| action_id | company | vertical | channel | score | risk | status | recommended_action |",
        "| --------- | ------- | -------- | ------- | ----- | ---- | ------ | ------------------ |",
    ]
    for a in actions:
        md.append(
            f"| {a['action_id']} | {a['company']} | {a['vertical']} | {a['channel']} | "
            f"{a['priority_score']} | {a['risk_level']} | {a['status']} | {a['recommended_action']} |"
        )
    md += ["", "Edit the CSV to record your decisions. No message is sent by this tool.", ""]
    write_text(out_dir / "founder_actions.md", "\n".join(md))

    # Manual send queue is an EXAMPLE template the founder fills + executes by hand.
    send_fields = [
        "action_id", "company", "channel", "manual_copy_text",
        "sent_manually_yes_no", "sent_at", "founder_initials",
    ]
    send_rows = [
        {
            "action_id": a["action_id"],
            "company": a["company"],
            "channel": a["channel"],
            "manual_copy_text": a["manual_copy_text"],
            "sent_manually_yes_no": "",
            "sent_at": "",
            "founder_initials": "",
        }
        for a in actions
        if a["status"] != "needs_research"
    ]
    write_csv(out_dir / "manual_send_queue.example.csv", send_fields, send_rows)

    # Call priority list (phone channel + highest scores).
    calls = [a for a in actions if a["channel"] == "phone"]
    calls = sorted(calls, key=lambda a: a["priority_score"], reverse=True)
    call_md = [
        "# Call Priority List",
        "",
        f"> {SAFETY_BANNER}",
        "",
        f"Date: {date} · Calls to make manually: {len(calls)}",
        "",
    ]
    for i, a in enumerate(calls, start=1):
        call_md.append(f"{i}. {a['company']} ({a['vertical']}) — score {a['priority_score']} — dial manually")
    call_md += ["", "Dial each number yourself. This list does not place calls.", ""]
    write_text(out_dir / "call_priority_list.md", "\n".join(call_md))

    # Today revenue plan.
    plan = [
        "# Today Revenue Plan",
        "",
        f"> {SAFETY_BANNER}",
        "",
        f"Date: {date}",
        "",
        "## Top 5 manual actions",
        "",
    ]
    for a in actions[:5]:
        plan.append(f"- {a['company']} — {a['recommended_action']}")
    plan += [
        "",
        "## Rules",
        "",
        "- Approve drafts before any contact.",
        "- Send everything manually from your own accounts.",
        "- Record replies in data/revenue_manual_events.example.jsonl.",
        "- Stop chasing low-fit prospects (mark `suppressed`).",
        "",
    ]
    write_text(out_dir / "today_revenue_plan.md", "\n".join(plan))

    return {
        "date": date,
        "actions": len(actions),
        "needs_research": sum(1 for a in actions if a["status"] == "needs_research"),
        "out_dir": str(out_dir),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=None)
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()
    result = generate(args.date, args.limit)
    print(f"[founder_action_queue] {result['actions']} actions → {result['out_dir']}")
    print(f"[founder_action_queue] {SAFETY_BANNER}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
