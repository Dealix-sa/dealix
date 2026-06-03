"""Markdown renderers for distribution reports (kept out of the thin CLIs).

All renderers are PII-conscious: they emit company names + ids + counts only —
never contact fields (email/phone). Generated report files live under
``reports/distribution/`` and are gitignored (runtime, may reference real
prospects); only ``.gitkeep`` is tracked.
"""

from __future__ import annotations

from typing import Any

from dealix.distribution.ledger import now_iso


def render_queue(pending: list[dict[str, Any]]) -> str:
    lines = [
        "# Draft Queue Review — مراجعة قائمة المسودات",
        "",
        f"- Generated: {now_iso()}",
        f"- Pending (awaiting approval): **{len(pending)}**",
        "",
        "> راجع كل مسودة: اعتمد · عدّل · ارفض. الإرسال يدوي بعد الاعتماد.",
        "",
    ]
    if not pending:
        lines.append("_لا مسودات معلقة._")
        return "\n".join(lines) + "\n"
    for d in pending:
        lines.append(
            f"## `{d.get('id')}` — {d.get('company')} ({d.get('sector')} · {d.get('channel')})"
        )
        lines.append("")
        lines.append("```text")
        lines.append(str(d.get("body") or "").strip())
        lines.append("```")
        lines.append("")
    return "\n".join(lines) + "\n"


def render_metrics(snapshot: dict[str, Any]) -> str:
    k = snapshot["kpis"]
    f = snapshot["funnel"]
    lines = [
        "# Distribution Metrics — مؤشرات التصريف",
        "",
        f"- Generated: {now_iso()}",
        "",
        "## KPIs",
        "",
        f"- Pending drafts: {k['pending_drafts']}",
        f"- Approved drafts: {k['approved_drafts']}",
        f"- Due follow-ups: {k['due_followups']}",
        f"- Proposal drafts: {k['proposal_drafts']}",
        f"- Proof packs: {k['proof_packs']}",
        f"- Payment handoffs: {k['payment_handoffs']}",
        f"- Upcoming renewals: {k['upcoming_renewals']}",
        f"- Won / Lost: {k['won_deals']} / {k['lost_deals']}",
        "",
        "## Funnel conversion",
        "",
        f"- Draft approval rate: {f['draft_approval_rate_pct']}%",
        f"- Proposal accept rate: {f['proposal_accept_rate_pct']}%",
        f"- Payment close rate: {f['payment_close_rate_pct']}%",
        "",
        "## Sector performance (drafts)",
        "",
    ]
    for sector, n in sorted(snapshot["sector_performance"].items(), key=lambda x: -x[1]):
        lines.append(f"- {sector}: {n}")
    lines.append("")
    lines.append("## Channel performance (drafts)")
    lines.append("")
    for ch, n in sorted(snapshot["channel_performance"].items(), key=lambda x: -x[1]):
        lines.append(f"- {ch}: {n}")
    lines.append("")
    return "\n".join(lines) + "\n"


def render_win_loss(summary: dict[str, Any]) -> str:
    lines = [
        "# Win/Loss Learning — تعلّم الربح والخسارة",
        "",
        f"- Generated: {now_iso()}",
        f"- Total outcomes: {summary['total']}",
        f"- Win rate: {summary['win_rate_pct']}%",
        "",
        "## By outcome",
        "",
    ]
    for outcome, n in summary["by_outcome"].items():
        lines.append(f"- {outcome}: {n}")
    lines.extend(["", "## Top reasons", ""])
    for reason, n in summary["top_reasons"]:
        lines.append(f"- {reason}: {n}")
    lines.extend(["", "## Next changes", ""])
    for change in summary["next_changes"]:
        lines.append(f"- {change}")
    lines.append("")
    return "\n".join(lines) + "\n"


def render_weekly(snapshot: dict[str, Any]) -> str:
    k = snapshot["kpis"]
    f = snapshot["funnel"]
    wl = snapshot["win_loss"]
    lines = [
        "# Weekly Distribution Review — المراجعة الأسبوعية للتصريف",
        "",
        f"- Generated: {now_iso()}",
        "",
        "## This week's funnel",
        "",
        f"- Drafts: {f['drafts']} (approved {f['approved_drafts']}, {f['draft_approval_rate_pct']}%)",
        f"- Proposals: {f['proposals']} (accepted {f['accepted_proposals']}, "
        f"{f['proposal_accept_rate_pct']}%)",
        f"- Payments: {f['payments']} (paid {f['paid']}, {f['payment_close_rate_pct']}%)",
        f"- Due follow-ups: {k['due_followups']} · Upcoming renewals: {k['upcoming_renewals']}",
        "",
        "## Win/Loss",
        "",
        f"- Won / Lost: {k['won_deals']} / {k['lost_deals']} · Win rate: {wl['win_rate_pct']}%",
        "",
        "## Next changes (from win/loss)",
        "",
    ]
    for change in wl["next_changes"]:
        lines.append(f"- {change}")
    lines.extend(
        [
            "",
            "## Founder weekly decisions",
            "",
            "- [ ] أي قطاع نضاعف فيه؟ أي قطاع نوقفه؟",
            "- [ ] أي عرض/رسالة نحسّن؟",
            "- [ ] أي proof angle نضيف؟",
            "- [ ] أي حسابات أولوية الأسبوع القادم؟",
            "",
            "> مسودات وقرارات فقط — لا إرسال خارجي تلقائي.",
            "",
        ]
    )
    return "\n".join(lines)


__all__ = ["render_metrics", "render_queue", "render_weekly", "render_win_loss"]
