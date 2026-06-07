"""Founder Daily Brief renderer for the Dealix Now engine (os/02 #16).

Renders the assembled Now pack into Arabic markdown following the section
structure of ``os/10_FOUNDER_DAILY_BRIEF.md``: revenue pipeline (new leads),
drafts-ready, today's three priorities, cash / pipeline view, intelligence
alerts, and previous-day metric placeholders. Ends with the literal os/10
footer line.

Pure and deterministic: no network, no API keys, no LLM. Internal read-only
report — never sent.
"""

from __future__ import annotations

_FOOTER = (
    "*مُولَّد تلقائياً بواسطة Dealix Chief of Staff Agent — للقراءة اليومية فقط، "
    "لا يُرسل لأي طرف خارجي*"
)


def _fmt_int(value: object) -> str:
    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return str(value)


def render_daily_brief_markdown(pack: dict) -> str:
    """Render the Now ``pack`` dict to Arabic markdown."""
    metrics = pack.get("metrics", {})
    pipeline = pack.get("pipeline", {})
    leads = pack.get("leads", [])
    drafts = pack.get("drafts", [])
    priorities = pack.get("priorities", [])
    alerts = pack.get("intelligence_alerts", [])
    date = pack.get("date", "")
    generated_at = pack.get("generated_at", "")

    lines: list[str] = []
    lines.append("# البريف اليومي للمؤسس — Dealix Now")
    lines.append("")
    lines.append(f"**التاريخ:** {date}")
    lines.append(f"**الوقت:** {generated_at}")
    lines.append("**مُنشئ الـ Brief:** Chief of Staff Agent")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ── 1. Revenue Pipeline — new leads ──
    lines.append("## 1. Revenue Pipeline — خط الإيرادات")
    lines.append("")
    lines.append("### Leads جديدة (آخر 24 ساعة)")
    lines.append("")
    lines.append("| الشركة | القطاع | الـ Score | العرض المقترح | الإجراء المطلوب |")
    lines.append("|--------|--------|----------|--------------|----------------|")
    for lead in leads:
        offer = lead.get("recommended_offer", {})
        lines.append(
            f"| {lead.get('company_name','')} "
            f"| {lead.get('sector_ar', lead.get('sector',''))} "
            f"| {lead.get('fit_score','')}/100 "
            f"| {offer.get('id','')} — {offer.get('name_ar','')} "
            f"| {lead.get('next_action','')} |"
        )
    lines.append("")
    lines.append(f"**إجمالي leads جديدة اليوم:** {metrics.get('leads_total', 0)}")
    lines.append(f"**يحتاج موافقتك على drafts:** {metrics.get('drafts_ready', 0)}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ── Drafts ready ──
    lines.append("### Drafts جاهزة للمراجعة")
    lines.append("")
    lines.append("| الشركة | العرض | السطر الأول (Subject) | تقييم Safety Agent |")
    lines.append("|--------|------|----------------------|------------------|")
    for draft in drafts:
        safety = draft.get("safety", {})
        approved = "جاهز للمراجعة" if safety.get("approved_for_review") else "مراجعة مطلوبة"
        lines.append(
            f"| {draft.get('company_name','')} "
            f"| {draft.get('offer_id','')} "
            f"| {draft.get('subject','')} "
            f"| {safety.get('safety_score','')} / {approved} |"
        )
    lines.append("")
    lines.append(f"**إجمالي drafts بانتظارك:** {len(drafts)}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ── 2. أولويات اليوم الثلاث ──
    lines.append("## 2. أولويات اليوم الثلاث")
    lines.append("")
    lines.append(
        "> قانون: يوم بدون واحد من هذه ليس يوم إنتاجي: "
        "20 company brief | 20 draft | 5 follow-ups | 1 proposal"
    )
    lines.append("")
    if priorities:
        for prio in priorities:
            lines.append(f"### الأولوية {prio.get('rank','')}")
            lines.append(f"**ماذا:** {prio.get('what_ar','')}")
            lines.append(f"**لماذا الآن:** {prio.get('why_now_ar','')}")
            lines.append(f"**الوقت المقدر:** {prio.get('est_minutes','')} دقيقة")
            lines.append("")
    else:
        lines.append("لا توجد أولويات draftable اليوم — راجع nurture list.")
        lines.append("")
    lines.append("---")
    lines.append("")

    # ── 3. Cash / Pipeline View ──
    pv = metrics.get("pipeline_value_sar", {})
    lines.append("## 3. Cash / Pipeline View — الوضع المالي وخط الأنابيب")
    lines.append("")
    lines.append("| البند | القيمة |")
    lines.append("|------|--------|")
    lines.append(f"| leads جديدة | {pipeline.get('new_leads_24h', 0)} |")
    lines.append(f"| drafts بانتظار الموافقة | {pipeline.get('drafts_awaiting', 0)} |")
    lines.append(f"| ردود تحتاج إجراء | {pipeline.get('replies_to_handle', 0)} |")
    lines.append(f"| مكالمات اليوم | {pipeline.get('calls_today', 0)} |")
    lines.append(f"| proposals معلّقة | {pipeline.get('proposals_pending', 0)} |")
    lines.append(f"| صفقات في خطر | {pipeline.get('deals_at_risk', 0)} |")
    lines.append(f"| قيمة خط الأنابيب — typical (SAR) | {_fmt_int(pv.get('typical', 0))} |")
    lines.append(
        f"| نطاق خط الأنابيب (SAR) | {_fmt_int(pv.get('low', 0))} – {_fmt_int(pv.get('high', 0))} |"
    )
    lines.append("")
    lines.append("---")
    lines.append("")

    # ── 4. Intelligence Alerts ──
    lines.append("## 4. Intelligence Alerts — معلومات مهمة")
    lines.append("")
    if alerts:
        for alert in alerts:
            lines.append(f"- {alert}")
    else:
        lines.append("- لا توجد تنبيهات اليوم.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ── 5. مقياس اليوم السابق (placeholders) ──
    lines.append("## 5. مقياس اليوم السابق")
    lines.append("")
    lines.append("| المقياس | الهدف اليومي | الفعلي أمس | الفجوة |")
    lines.append("|---------|------------|-----------|-------|")
    lines.append("| Leads researched | 20 | — | — |")
    lines.append("| Drafts created | 20 | — | — |")
    lines.append("| Emails approved & sent | 5+ | — | — |")
    lines.append("| Follow-ups done | 5 | — | — |")
    lines.append("| Proposals drafted | 1 | — | — |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(_FOOTER)

    return "\n".join(lines)


__all__ = ["render_daily_brief_markdown"]
