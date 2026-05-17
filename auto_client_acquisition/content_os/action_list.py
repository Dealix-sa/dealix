"""Founder daily action list — one bilingual markdown block.

Aggregates the four things the founder must act on each morning:
approvals waiting, social posts to review, today's outreach state, and
"the single number" from ``docs/V14_FOUNDER_DAILY_OPS.md``.
"""
from __future__ import annotations

import datetime as _dt

from auto_client_acquisition.approval_center.approval_store import (
    get_default_approval_store,
)


def _today_outreach_count(day: _dt.date) -> tuple[int, float, list[str]]:
    """Return (messages_sent, hours_coding, warnings) from the pipeline tracker.

    Reuses ``scripts/founder_daily_scorecard.py``; degrades gracefully if
    the tracker CSV is absent.
    """
    try:
        from scripts.founder_daily_scorecard import (
            _aggregate_from_tracker,
            _load_tracker_rows,
        )

        rows, warnings = _load_tracker_rows()
        sc = _aggregate_from_tracker(rows, day)
        return sc.messages_sent, sc.hours_coding, warnings
    except Exception:
        return 0, 0.0, ["pipeline tracker unavailable"]


def build_action_list(date: _dt.date | None = None) -> str:
    """Build the bilingual founder action list for ``date``."""
    day = date or _dt.datetime.now(_dt.UTC).date()
    label = day.isoformat()

    pending = get_default_approval_store().list_pending()
    approvals_waiting = len(pending)
    social_to_review = sum(
        1 for r in pending if r.action_type == "draft_social_post"
    )
    messages_sent, hours, warnings = _today_outreach_count(day)

    single_number = "yes" if messages_sent >= 1 else "no"
    warn_line_ar = (
        f"\n- ⚠ ملاحظات البيانات: {', '.join(warnings)}" if warnings else ""
    )
    warn_line_en = (
        f"\n- ⚠ Data notes: {', '.join(warnings)}" if warnings else ""
    )

    return (
        f"# قائمة مهام المؤسس اليومية / Founder Daily Action List — {label}\n\n"
        "## العربية\n\n"
        f"- موافقات بانتظارك في الطابور: **{approvals_waiting}**\n"
        f"- بوستات سوشل جاهزة للمراجعة: **{social_to_review}**\n"
        f"- رسائل تواصل أُرسلت اليوم: **{messages_sent}**\n"
        "- الرقم الوحيد المهم: هل أرسلت رسالة واتساب دافئة واحدة لمالك "
        f"شركة باسمه اليوم؟ → **{'نعم' if single_number == 'yes' else 'لا'}**\n"
        f"- ساعات المؤسس اليوم: **{hours}** (الخط الأحمر ~120 ساعة/شهر)\n"
        "- افتح الطابور، راجع المسوّدات، ثم اضغط موافقة/تعديل — لا يُرسَل "
        f"شيء بدون موافقتك.{warn_line_ar}\n\n"
        "## English\n\n"
        f"- Approvals waiting in the queue: **{approvals_waiting}**\n"
        f"- Social posts ready to review: **{social_to_review}**\n"
        f"- Outreach messages sent today: **{messages_sent}**\n"
        "- The single number that matters: did you send one warm, named "
        f"WhatsApp to a real owner today? → **{single_number}**\n"
        f"- Founder hours today: **{hours}** (redline ~120 h/month)\n"
        "- Open the queue, review the drafts, then click approve/edit — "
        f"nothing is sent without your approval.{warn_line_en}\n"
    )


__all__ = ["build_action_list"]
