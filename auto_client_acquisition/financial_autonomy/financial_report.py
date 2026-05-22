"""Bilingual report renderers for the financial autonomy cycle.

Pure-function helpers — every renderer takes a plain dict (the
``to_dict()`` projection of a report dataclass) and returns a single
Markdown string. The cycles call these from their persistence step.
"""
from __future__ import annotations

from typing import Any


def _fmt_number(value: Any) -> str:
    try:
        return f"{float(value):,.2f}"
    except Exception:  # noqa: BLE001
        return str(value)


def render_financial_report_markdown(report: dict[str, Any]) -> str:
    """Render a :class:`FinancialCycleReport` dict as bilingual Markdown."""
    metrics = report.get("metrics", {}) or {}
    anomalies = report.get("anomalies", []) or []
    violations = report.get("threshold_violations", []) or []
    approvals = report.get("approvals_pending", {}) or {}
    warnings = report.get("warnings", []) or []
    estimates = report.get("estimates_flagged", []) or metrics.get(
        "estimates_flagged", []
    ) or []

    lines: list[str] = [
        f"# {report.get('title_en', 'Financial cycle')}",
        "",
        f"- Cycle: `{report.get('cycle_id', '')}`",
        f"- Period end: {report.get('period_end', '')}",
        f"- Cadence: {report.get('cadence', 'weekly')}",
        f"- Generated: {report.get('generated_at', '')}",
        "",
        "## Metrics",
        f"- MRR: {_fmt_number(metrics.get('mrr_sar', 0))} SAR",
        f"- ARR: {_fmt_number(metrics.get('arr_sar', 0))} SAR",
        f"- NRR: {_fmt_number(metrics.get('nrr_pct', 0))}%",
        f"- Monthly churn: {_fmt_number(metrics.get('churn_pct_monthly', 0))}%",
        f"- ARPA: {_fmt_number(metrics.get('arpa_sar', 0))} SAR",
        f"- Active customers: {metrics.get('customers_active', 0)}",
        f"- Gross margin: {_fmt_number(metrics.get('gross_margin_pct', 0))}%",
        f"- LTV (est.): {_fmt_number(metrics.get('ltv_sar', 0))} SAR",
        f"- CAC payback (est.): {_fmt_number(metrics.get('cac_payback_months', 0))} months",
        f"- Runway (est.): {_fmt_number(metrics.get('runway_months', 0))} months",
        f"- Capital assets this period: {metrics.get('capital_assets_this_period', 0)}",
        "",
        f"## Anomalies: {len(anomalies)}",
    ]
    for a in anomalies:
        lines.append(
            f"- [{a.get('severity', '')}] {a.get('kind', '')}: {a.get('evidence_en', '')}"
        )
    lines += [
        "",
        f"## Threshold violations: {len(violations)}",
    ]
    for v in violations:
        rule = v.get("rule", {})
        lines.append(
            f"- [{rule.get('severity', '')}] {rule.get('rule_id', '')}: "
            f"observed={v.get('observed_value', '')} action={v.get('action_on_violation', '')}"
        )
    lines += [
        "",
        f"## Approvals pending: {approvals.get('count', 0)}",
        "",
        "## Estimates flagged",
    ]
    if estimates:
        lines += [f"- {name}" for name in estimates]
    else:
        lines.append("- none")
    lines += ["", "## Hard gates"]
    lines += [f"- {g}" for g in report.get("hard_gates", [])]
    if warnings:
        lines += ["", "## Warnings"]
        lines += [f"- {w}" for w in warnings]

    # Arabic mirror
    lines += [
        "",
        "---",
        "",
        f"# {report.get('title_ar', 'دورة مالية')}",
        "",
        "## المقاييس",
        f"- إيراد شهري: {_fmt_number(metrics.get('mrr_sar', 0))} ر.س",
        f"- إيراد سنوي: {_fmt_number(metrics.get('arr_sar', 0))} ر.س",
        f"- NRR: {_fmt_number(metrics.get('nrr_pct', 0))}%",
        f"- انسحاب شهري: {_fmt_number(metrics.get('churn_pct_monthly', 0))}%",
        f"- متوسط الإيراد لكل عميل: {_fmt_number(metrics.get('arpa_sar', 0))} ر.س",
        f"- عملاء نشطون: {metrics.get('customers_active', 0)}",
        f"- هامش إجمالي: {_fmt_number(metrics.get('gross_margin_pct', 0))}%",
        f"- LTV (تقدير): {_fmt_number(metrics.get('ltv_sar', 0))} ر.س",
        f"- استرداد CAC (تقدير): {_fmt_number(metrics.get('cac_payback_months', 0))} شهراً",
        f"- المدرّج الزمني (تقدير): {_fmt_number(metrics.get('runway_months', 0))} شهراً",
        f"- أصول رأس المال هذه الفترة: {metrics.get('capital_assets_this_period', 0)}",
        "",
        f"## شذوذ مالي: {len(anomalies)}",
    ]
    for a in anomalies:
        lines.append(
            f"- [{a.get('severity', '')}] {a.get('kind', '')}: {a.get('evidence_ar', '')}"
        )
    lines += [
        "",
        f"## مخالفات عتبات: {len(violations)}",
    ]
    for v in violations:
        rule = v.get("rule", {})
        lines.append(
            f"- [{rule.get('severity', '')}] {rule.get('rule_id', '')}: "
            f"مقياس={v.get('observed_value', '')} إجراء={v.get('action_on_violation', '')}"
        )
    lines += [
        "",
        f"## موافقات معلّقة: {approvals.get('count', 0)}",
        "",
    ]
    return "\n".join(lines)


def render_board_memo_markdown(report: dict[str, Any]) -> str:
    """Render a :class:`BoardMemoReport` dict as bilingual Markdown."""
    sections = report.get("sections", {}) or {}
    missing = report.get("missing_sections", []) or []

    lines: list[str] = [
        f"# Dealix Board Memo — {report.get('month', '')}",
        "",
        f"- Generated: {report.get('generated_at', '')}",
        f"- Approval: `{report.get('approval_id', '')}`",
        f"- Sections complete: {report.get('sections_complete', False)}",
        f"- Missing sections: {', '.join(missing) if missing else 'none'}",
        "",
    ]
    for idx, slug in enumerate(report.get("section_order", []), start=1):
        block = sections.get(slug, {}) or {}
        lines += [
            f"## {idx}. {block.get('title_en', slug)}",
            "",
            (block.get("body_en") or "—").strip(),
            "",
        ]
    lines += ["---", "", f"# مذكّرة مجلس Dealix — {report.get('month', '')}", ""]
    for idx, slug in enumerate(report.get("section_order", []), start=1):
        block = sections.get(slug, {}) or {}
        lines += [
            f"## {idx}. {block.get('title_ar', slug)}",
            "",
            (block.get("body_ar") or "—").strip(),
            "",
        ]
    return "\n".join(lines)


__all__ = [
    "render_board_memo_markdown",
    "render_financial_report_markdown",
]
