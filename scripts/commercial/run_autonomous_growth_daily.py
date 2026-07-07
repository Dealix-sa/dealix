#!/usr/bin/env python3
"""Dealix Autonomous Growth daily runner.

This runner is deliberately draft-only and safe-by-default. It creates local
reports and queues for founder review, but it never sends, publishes, merges,
charges, or changes production.
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
REPORT_ROOT = ROOT / "reports" / "autonomous_growth"

BLOCKED_EXTERNAL_ACTIONS = {
    "send_email",
    "send_whatsapp",
    "post_linkedin",
    "post_x",
    "merge_pr",
    "charge_payment",
    "change_production",
    "scrape_contacts",
    "cold_whatsapp",
}

STRATEGIES: list[dict[str, Any]] = [
    {
        "name": "technical_trust",
        "goal": "Protect launch credibility by surfacing CI, Railway, smoke, and PR blockers first.",
        "kpis": ["critical_blockers_count", "ready_pr_count", "production_health_status"],
        "safe_actions": ["summarize_repo_state", "draft_fix_plan", "write_founder_decision"],
        "approval_required_for": ["merge_pr", "change_production"],
    },
    {
        "name": "saudi_market_access",
        "goal": "Prioritize Saudi-entry opportunities and create proof-backed opportunity snapshots.",
        "kpis": ["companies_scored", "hot_targets", "approved_targets"],
        "safe_actions": ["score_companies", "draft_snapshot", "write_approval_queue"],
        "approval_required_for": ["external_outreach", "publish_snapshot"],
    },
    {
        "name": "revenue_sprint",
        "goal": "Create daily draft-only revenue actions for Snapshot, Sprint, and Retainer offers.",
        "kpis": ["drafts_created", "followups_ready", "proof_items"],
        "safe_actions": ["draft_outreach", "draft_followup", "draft_one_page_offer"],
        "approval_required_for": ["send_email", "send_whatsapp", "quote_final_price"],
    },
    {
        "name": "content_factory",
        "goal": "Turn proof and market signals into founder-approved content drafts.",
        "kpis": ["content_drafts", "proof_backed_posts"],
        "safe_actions": ["draft_linkedin_post", "draft_x_thread", "draft_newsletter"],
        "approval_required_for": ["post_linkedin", "post_x", "send_newsletter"],
    },
    {
        "name": "proof_pack",
        "goal": "Record evidence, decisions, and next steps so Dealix sells with proof instead of claims.",
        "kpis": ["proof_log_entries", "weekly_pack_ready"],
        "safe_actions": ["write_proof_log", "draft_weekly_pack"],
        "approval_required_for": ["share_client_pack"],
    },
]


@dataclass(frozen=True)
class QueuedAction:
    strategy: str
    action: str
    autonomy_level: int
    status: str
    reason: str


@dataclass(frozen=True)
class ApprovalItem:
    strategy: str
    requested_action: str
    risk: str
    reason: str
    default_decision: str = "needs_founder_approval"


def ensure_dirs() -> None:
    for child in ["daily", "actions", "approvals", "proof", "content"]:
        (REPORT_ROOT / child).mkdir(parents=True, exist_ok=True)


def select_strategies(limit: int) -> list[dict[str, Any]]:
    # Deterministic ordering: trust first, then revenue, market access, proof, content.
    ordered = ["technical_trust", "revenue_sprint", "saudi_market_access", "proof_pack", "content_factory"]
    by_name = {item["name"]: item for item in STRATEGIES}
    selected = [by_name[name] for name in ordered if name in by_name]
    return selected[: max(1, min(len(selected), limit))]


def build_queues(strategies: list[dict[str, Any]], autonomy_level: int) -> tuple[list[QueuedAction], list[ApprovalItem]]:
    actions: list[QueuedAction] = []
    approvals: list[ApprovalItem] = []
    for strategy in strategies:
        for action in strategy["safe_actions"]:
            actions.append(
                QueuedAction(
                    strategy=strategy["name"],
                    action=action,
                    autonomy_level=min(autonomy_level, 3),
                    status="queued_internal" if autonomy_level >= 3 else "recommended",
                    reason="Safe internal artifact only; no external side effects.",
                )
            )
        for requested in strategy["approval_required_for"]:
            approvals.append(
                ApprovalItem(
                    strategy=strategy["name"],
                    requested_action=requested,
                    risk="external_or_high_impact",
                    reason="Blocked until explicit founder approval is recorded.",
                )
            )
    return actions, approvals


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_daily_report(path: Path, *, date_key: str, strategies: list[dict[str, Any]], actions: list[QueuedAction], approvals: list[ApprovalItem]) -> None:
    lines: list[str] = []
    lines.append(f"# Dealix Autonomous Growth Daily Report — {date_key}")
    lines.append("")
    lines.append("## Executive summary")
    lines.append("Dealix ran in draft-only mode. It prepared internal actions, approval queues, proof logs, and content drafts. No external sends, publishing, merges, payments, or production changes were performed.")
    lines.append("")
    lines.append("## Strategies selected")
    for item in strategies:
        lines.append(f"- **{item['name']}** — {item['goal']}")
    lines.append("")
    lines.append("## Internal action queue")
    for item in actions:
        lines.append(f"- [{item.status}] `{item.strategy}` → `{item.action}` — {item.reason}")
    lines.append("")
    lines.append("## Approval queue")
    for item in approvals:
        lines.append(f"- `{item.strategy}` requests `{item.requested_action}` — {item.default_decision}: {item.reason}")
    lines.append("")
    lines.append("## Founder decisions")
    lines.append("1. Review any Railway/CI blocker before merging commercial PRs.")
    lines.append("2. Approve or revise the top outreach/content drafts before any manual send or post.")
    lines.append("3. Keep live outbound disabled until proof pack and suppression rules are reviewed.")
    lines.append("")
    lines.append("## Safety posture")
    lines.append("- OUTBOUND_MODE: draft_only")
    lines.append("- live_send_enabled: false")
    lines.append("- auto_publish_enabled: false")
    lines.append("- auto_merge_enabled: false")
    lines.append("- production_change_enabled: false")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Dealix autonomous growth in draft-only mode.")
    parser.add_argument("--autonomy-level", type=int, default=3, choices=[0, 1, 2, 3, 4])
    parser.add_argument("--mode", default="draft-only", choices=["draft-only"])
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()

    ensure_dirs()
    now = datetime.now(UTC)
    date_key = now.date().isoformat()

    strategies = select_strategies(args.limit)
    actions, approvals = build_queues(strategies, args.autonomy_level)

    base_payload = {
        "generated_at": now.isoformat(),
        "mode": args.mode,
        "autonomy_level": args.autonomy_level,
        "blocked_external_actions": sorted(BLOCKED_EXTERNAL_ACTIONS),
    }

    write_json(REPORT_ROOT / "actions" / f"{date_key}_actions.json", {**base_payload, "actions": [asdict(a) for a in actions]})
    write_json(REPORT_ROOT / "approvals" / f"{date_key}_approvals.json", {**base_payload, "approvals": [asdict(a) for a in approvals]})
    write_json(
        REPORT_ROOT / "proof" / f"{date_key}_proof_log.json",
        {
            **base_payload,
            "proof": [
                {"type": "safety", "status": "draft_only", "detail": "No external action executed."},
                {"type": "strategy", "status": "selected", "count": len(strategies)},
                {"type": "approval", "status": "queued", "count": len(approvals)},
            ],
        },
    )
    content_path = REPORT_ROOT / "content" / f"{date_key}_content_queue.md"
    content_path.write_text(
        "# Dealix Content Draft Queue\n\n"
        "- LinkedIn draft: What Saudi companies lose when follow-up is scattered across WhatsApp and email.\n"
        "- X thread draft: Saudi Market Access is not a report; it is a daily operating loop.\n"
        "- Newsletter draft: This week's proof-backed growth signals and founder decisions.\n",
        encoding="utf-8",
    )
    write_daily_report(
        REPORT_ROOT / "daily" / f"{date_key}.md",
        date_key=date_key,
        strategies=strategies,
        actions=actions,
        approvals=approvals,
    )

    print(f"DEALIX_AUTONOMOUS_GROWTH_READY=1 date={date_key} actions={len(actions)} approvals={len(approvals)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
