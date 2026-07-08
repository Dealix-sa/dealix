"""Markdown report rendering for Company OS outputs."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any


def render_daily_report(plan: dict[str, Any]) -> str:
    brain = plan["client"]
    lines = [
        f"# Dealix Company OS Daily Report — {datetime.now(UTC).date().isoformat()}",
        "",
        "## Mode",
        "- draft-only",
        "- external_action_enabled: false",
        "- live_outbound_enabled: false",
        "- payment_capture_enabled: false",
        "- production_mutation_enabled: false",
        "",
        "## Company Brain",
        f"- Client: {brain['name']}",
        f"- Positioning: {brain['positioning']}",
        f"- Primary offer: {brain['primary_offer']}",
        "",
        "## Top Opportunities",
    ]
    for opp in plan["top_opportunities"]:
        lines.extend(
            [
                f"### {opp['company_name']} — score {opp['score']}",
                f"- Vertical: {opp['vertical']}",
                f"- Offer: {opp['offer_match']}",
                f"- Reason: {opp['reason']}",
                f"- Next action: {opp['next_action']}",
                "",
            ]
        )
    lines.append("## Approval Queue")
    for approval in plan["approvals"]:
        lines.append(f"- {approval['approval_id']}: {approval['summary']} — {approval['status']}")
    lines.extend(["", "## Drafts"])
    for draft in plan["drafts"]:
        lines.extend(
            [
                f"### {draft['draft_id']} — {draft['company_name']}",
                f"- Channel: {draft['channel']}",
                f"- Status: {draft['status']}",
                f"- Subject: {draft['subject']}",
                "",
                draft["body"],
                "",
            ]
        )
    lines.extend(
        [
            "## Proof Log Summary",
            f"- Proof events: {len(plan['proof_log'])}",
            "- Every generated item is internal evidence only until founder approval.",
            "",
            "## Blocked Actions",
            "- send_email",
            "- send_whatsapp",
            "- send_sms",
            "- post_content",
            "- capture_payment",
            "- merge_pr",
            "- modify_production",
        ]
    )
    return "\n".join(lines) + "\n"
