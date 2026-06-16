"""Daily / Weekly GTM report rendering (markdown).

Pure rendering from a metrics dict. Numbers are passed in by callers; this
module never invents metrics (doctrine: no un-sourced claims).
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

DAILY_METRIC_KEYS: tuple[str, ...] = (
    "drafts_generated",
    "drafts_quality_passed",
    "drafts_approved",
    "emails_sent",
    "bounces",
    "unsubscribes",
    "replies",
    "positive_replies",
    "meetings_booked",
    "proposals_requested",
    "job_signals_found",
    "content_posts_drafted",
    "partner_prospects_found",
)

WEEKLY_REVIEW_KEYS: tuple[str, ...] = (
    "best_sector",
    "best_offer",
    "best_subject_line",
    "best_cta",
    "best_signal_source",
    "worst_bounce_source",
    "pipeline_value",
    "lessons_learned",
    "next_week_experiments",
)


def _today() -> str:
    return datetime.now(UTC).date().isoformat()


def daily_gtm_report(metrics: dict[str, Any], *, date: str | None = None) -> str:
    date = date or _today()
    rows = "\n".join(
        f"| {key} | {metrics.get(key, 0)} |" for key in DAILY_METRIC_KEYS
    )
    auto_sent = int(metrics.get("auto_sent", 0))
    invariant = "PASS" if auto_sent == 0 else "FAIL"
    return (
        f"# Daily GTM Report — {date}\n\n"
        "> 250 drafts/day, 0 auto-sends. Sending is founder-approved + ramp-capped.\n\n"
        "| metric | value |\n|---|---:|\n"
        f"{rows}\n\n"
        f"**Auto-send invariant (auto_sent == 0):** {invariant} (auto_sent={auto_sent})\n\n"
        "> القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.\n"
    )


def weekly_gtm_review(metrics: dict[str, Any], *, week_of: str | None = None) -> str:
    week_of = week_of or _today()
    rows = "\n".join(
        f"| {key} | {metrics.get(key, '—')} |" for key in WEEKLY_REVIEW_KEYS
    )
    return (
        f"# Weekly GTM Review — week of {week_of}\n\n"
        "| dimension | finding |\n|---|---|\n"
        f"{rows}\n\n"
        "> القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.\n"
    )


__all__ = [
    "DAILY_METRIC_KEYS",
    "WEEKLY_REVIEW_KEYS",
    "daily_gtm_report",
    "weekly_gtm_review",
]
