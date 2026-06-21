"""Founder daily command generator for the Dealix launch OS.

Produces a structured daily brief that surfaces:
  - Priority accounts to contact today
  - Outreach drafts awaiting approval
  - Pipeline items needing action
  - One content task
  - A rendered bilingual (Arabic + English) brief

The output aligns with ``schemas/launch/founder_daily_command.schema.json``.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from dealix.launch_os.icp_scorer import score_account
from dealix.launch_os.pipeline_tracker import PipelineItem, PipelineStage, PipelineTracker


@dataclass
class DailyCommand:
    """Structured daily brief for the founder.

    Attributes:
        date:                   ISO date of the brief.
        priority_accounts:      Top accounts to contact today (list of dicts).
        outreach_queue:         Accounts with pending outreach drafts.
        approval_queue:         Drafts / proposals waiting founder approval.
        content_task:           One content action for today.
        pipeline_review_items:  Pipeline items needing a stage update.

    Examples:
        >>> cmd = DailyCommand(
        ...     date="2026-06-12",
        ...     priority_accounts=[],
        ...     outreach_queue=[],
        ...     approval_queue=[],
        ...     content_task="Publish one LinkedIn post about revenue leakage",
        ...     pipeline_review_items=[],
        ... )
        >>> cmd.date
        '2026-06-12'
    """

    date: str
    priority_accounts: list[dict[str, Any]]
    outreach_queue: list[dict[str, Any]]
    approval_queue: list[dict[str, Any]]
    content_task: str
    pipeline_review_items: list[dict[str, Any]]


_CONTENT_TASKS_EN = [
    "Post a LinkedIn snippet about the #1 cause of revenue leakage in the automotive sector",
    "Share an anonymised case outcome from a past engagement",
    "Record a 60-second voice note on the key lesson learned this week",
    "Write an Arabic LinkedIn post on 3 common sales-system mistakes",
    "Share a question your ideal clients are asking about operating systems",
]


def _today_str() -> str:
    return datetime.now(UTC).date().isoformat()


def generate_daily_command(
    pipeline: PipelineTracker,
    target_accounts: list[dict[str, Any]],
    *,
    approval_queue: list[dict[str, Any]] | None = None,
) -> DailyCommand:
    """Generate today's founder daily command.

    Args:
        pipeline:        Loaded :class:`~dealix.launch_os.pipeline_tracker.PipelineTracker`.
        target_accounts: List of account dicts to score and prioritise.
        approval_queue:  Optional list of pending approval items.

    Returns:
        Populated :class:`DailyCommand`.

    Examples:
        >>> import tempfile, os
        >>> with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
        ...     tmp = f.name
        >>> tracker = PipelineTracker(path=tmp)
        >>> _ = tracker.add("acme_001", "Acme", icp_score=80)
        >>> accounts = [{"account_id": "acme_001", "account_name": "Acme", "urgency": "high",
        ...              "revenue_leak_sar": 200000, "process_chaos_score": 12,
        ...              "decision_maker_access": "direct", "start_small_score": 8,
        ...              "proof_speed_score": 7, "budget_signal": "likely"}]
        >>> cmd = generate_daily_command(tracker, accounts)
        >>> isinstance(cmd.priority_accounts, list)
        True
        >>> os.unlink(tmp)
    """
    today = _today_str()

    # Score and rank target accounts.
    scored = []
    for acct in target_accounts:
        try:
            s = score_account(acct)
            scored.append({"account": acct, "icp_score": s})
        except Exception:
            pass

    scored.sort(key=lambda x: x["icp_score"].total, reverse=True)
    priority_accounts = []
    for entry in scored[:10]:
        acct = entry["account"]
        s = entry["icp_score"]
        priority_accounts.append({
            "account_id": acct.get("account_id", ""),
            "account_name": acct.get("account_name", acct.get("account_id", "")),
            "tier": s.tier,
            "total_score": s.total,
            "action": s.action,
        })

    # Outreach queue — accounts in RESEARCH that have a next_action.
    research_items = pipeline.list_by_stage(PipelineStage.RESEARCH)
    outreach_queue = [
        {
            "account_id": item.account_id,
            "account_name": item.company_name,
            "offer_id": item.offer_id,
            "next_action": item.next_action,
        }
        for item in research_items[:5]
    ]

    # Pipeline review — items in OUTREACH, DISCOVERY, PROPOSAL, NEGOTIATION.
    review_stages = [
        PipelineStage.OUTREACH,
        PipelineStage.DISCOVERY,
        PipelineStage.PROPOSAL,
        PipelineStage.NEGOTIATION,
    ]
    review_items: list[dict[str, Any]] = []
    for stage in review_stages:
        for item in pipeline.list_by_stage(stage):
            review_items.append({
                "account_id": item.account_id,
                "account_name": item.company_name,
                "stage": item.stage,
                "value_sar": item.value_sar,
                "next_action": item.next_action,
                "last_touch_date": item.last_touch_date,
            })
    review_items.sort(key=lambda x: x.get("value_sar", 0), reverse=True)

    day_of_week = datetime.now(UTC).weekday()
    content_task = _CONTENT_TASKS_EN[day_of_week % len(_CONTENT_TASKS_EN)]

    return DailyCommand(
        date=today,
        priority_accounts=priority_accounts,
        outreach_queue=outreach_queue,
        approval_queue=list(approval_queue) if approval_queue else [],
        content_task=content_task,
        pipeline_review_items=review_items,
    )


def render_brief(cmd: DailyCommand) -> str:
    """Render a :class:`DailyCommand` as a bilingual Arabic + English brief.

    Args:
        cmd: Populated daily command.

    Returns:
        Formatted string ready for terminal or messaging.

    Examples:
        >>> cmd = DailyCommand(
        ...     date="2026-06-12",
        ...     priority_accounts=[{"account_name": "Acme", "tier": "A",
        ...                          "total_score": 82, "action": "pursue_today"}],
        ...     outreach_queue=[],
        ...     approval_queue=[],
        ...     content_task="Post about revenue leakage",
        ...     pipeline_review_items=[],
        ... )
        >>> brief = render_brief(cmd)
        >>> "2026-06-12" in brief
        True
        >>> "Acme" in brief
        True
    """
    lines: list[str] = []

    lines.append("=" * 60)
    lines.append(f"DEALIX FOUNDER DAILY COMMAND — {cmd.date}")
    lines.append(f"اليومية التشغيلية — {cmd.date}")
    lines.append("=" * 60)

    lines.append("\n--- PRIORITY ACCOUNTS / الحسابات ذات الأولوية ---")
    if cmd.priority_accounts:
        for i, acct in enumerate(cmd.priority_accounts, 1):
            lines.append(
                f"  {i}. {acct.get('account_name', 'Unknown'):<30} "
                f"[{acct.get('tier', '?')}] score={acct.get('total_score', 0)} "
                f"-> {acct.get('action', '')}"
            )
    else:
        lines.append("  (no priority accounts scored today)")

    lines.append("\n--- OUTREACH QUEUE / قائمة الإرسال ---")
    if cmd.outreach_queue:
        for item in cmd.outreach_queue:
            lines.append(
                f"  - {item.get('account_name', '')}: {item.get('next_action', '')}"
            )
    else:
        lines.append("  (queue empty)")

    lines.append("\n--- APPROVAL QUEUE / قيد الموافقة ---")
    if cmd.approval_queue:
        for item in cmd.approval_queue:
            lines.append(f"  - {item}")
    else:
        lines.append("  (nothing awaiting approval)")

    lines.append("\n--- CONTENT TASK / مهمة المحتوى ---")
    lines.append(f"  {cmd.content_task}")

    lines.append("\n--- PIPELINE REVIEW / مراجعة خط الأنابيب ---")
    if cmd.pipeline_review_items:
        for item in cmd.pipeline_review_items:
            lines.append(
                f"  [{item.get('stage', '?')}] {item.get('account_name', ''):<28} "
                f"{item.get('value_sar', 0):>8,} SAR | {item.get('next_action', '')}"
            )
    else:
        lines.append("  (no active pipeline items)")

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)


if __name__ == "__main__":
    import doctest
    results = doctest.testmod(verbose=False)
    print(f"Founder daily command doctests: {results.attempted} run, {results.failed} failed")

    import os
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
        tmp = f.name

    tracker = PipelineTracker(path=tmp)
    tracker.add("acme_001", "Acme Motors", offer_id="REVENUE_LEAK_AUDIT",
                value_sar=15000, icp_score=82, next_action="Send intro email")
    tracker.add("realty_001", "Global Realty", offer_id="SALES_COMMAND_CENTER",
                value_sar=25000, icp_score=70, next_action="Book discovery call")
    t3 = tracker.add("clinic_001", "Clinic Pro", offer_id="WHATSAPP_FOLLOWUP_OS",
                     value_sar=10000, icp_score=60, next_action="Send proposal")
    tracker.advance(t3.account_id, to_stage=PipelineStage.PROPOSAL)

    accounts = [
        {"account_id": "acme_001", "account_name": "Acme Motors", "urgency": "high",
         "revenue_leak_sar": 300_000, "process_chaos_score": 12, "decision_maker_access": "direct",
         "start_small_score": 8, "proof_speed_score": 7, "budget_signal": "likely"},
    ]
    cmd = generate_daily_command(tracker, accounts)
    print(render_brief(cmd))
    os.unlink(tmp)
