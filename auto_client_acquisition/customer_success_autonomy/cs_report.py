"""Bilingual Markdown renderer for the Customer Success cycle report."""
from __future__ import annotations

from typing import Any


def render_cs_report_markdown(
    *,
    cycle_id: str,
    on_date: str,
    title_ar: str,
    title_en: str,
    summary: dict[str, Any],
    opportunities: list[dict[str, Any]],
    hard_gates: list[str],
    warnings: list[str],
) -> str:
    """Return a bilingual Markdown report. Arabic block first, then English."""
    ar_lines: list[str] = [
        f"# {title_ar}",
        "",
        f"- معرّف الدورة: `{cycle_id}`",
        f"- التاريخ: {on_date}",
        "",
        "## الملخّص",
        f"- العملاء النشطون: {summary.get('active_customers', 0)}",
        f"- إجمالي الفرص: {summary.get('opportunities_total', 0)}",
        f"- معرّضون لخطر: {summary.get('at_risk', 0)}",
        f"- جاهزون للترقية: {summary.get('expansion_ready', 0)}",
        f"- تجديدات مستحقّة: {summary.get('renewals_due', 0)}",
        f"- معترضو NPS: {summary.get('nps_detractors', 0)}",
        "",
        "## الفرص",
    ]
    if not opportunities:
        ar_lines.append("- لا فرص محتفظ بها هذا اليوم.")
    else:
        for opp in opportunities:
            ar_lines.append(
                f"- [{opp.get('urgency', 'normal')}] {opp.get('type', '')} — "
                f"{opp.get('customer_id', '')}: {opp.get('recommended_action_ar', '')}"
            )

    ar_lines.extend([
        "",
        "## البوابات الصلبة",
        *(f"- {g}" for g in hard_gates),
    ])

    if warnings:
        ar_lines.extend(["", "## تحذيرات", *(f"- {w}" for w in warnings)])

    en_lines: list[str] = [
        f"# {title_en}",
        "",
        f"- Cycle id: `{cycle_id}`",
        f"- Date: {on_date}",
        "",
        "## Summary",
        f"- Active customers: {summary.get('active_customers', 0)}",
        f"- Opportunities total: {summary.get('opportunities_total', 0)}",
        f"- At risk: {summary.get('at_risk', 0)}",
        f"- Expansion ready: {summary.get('expansion_ready', 0)}",
        f"- Renewals due: {summary.get('renewals_due', 0)}",
        f"- NPS detractors: {summary.get('nps_detractors', 0)}",
        "",
        "## Opportunities",
    ]
    if not opportunities:
        en_lines.append("- No retention opportunities today.")
    else:
        for opp in opportunities:
            en_lines.append(
                f"- [{opp.get('urgency', 'normal')}] {opp.get('type', '')} — "
                f"{opp.get('customer_id', '')}: {opp.get('recommended_action_en', '')}"
            )
    en_lines.extend([
        "",
        "## Hard gates",
        *(f"- {g}" for g in hard_gates),
    ])
    if warnings:
        en_lines.extend(["", "## Warnings", *(f"- {w}" for w in warnings)])

    return "\n".join(ar_lines) + "\n\n---\n\n" + "\n".join(en_lines) + "\n"


__all__ = ["render_cs_report_markdown"]
