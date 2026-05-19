"""Board report — bilingual Markdown for a strategic cycle.

Renders a CEO/board-tier Markdown report from a strategic cycle's
signal snapshot, gate evaluations and decisions. The monthly cadence
additionally pulls the board memo section taxonomy from
``board_decision_os.board_memo_generator``.
"""

from __future__ import annotations

from typing import Any


def _decision_line(decision: dict[str, Any], lang: str) -> str:
    rationale = decision.get(f"rationale_{lang}", "")
    status = decision.get("status", "")
    flag = "[approval-gated]" if decision.get("irreversible") else ""
    if lang == "ar":
        flag = "[خلف موافقة]" if decision.get("irreversible") else ""
    return (
        f"- **{decision.get('decision_type', '')}** -> "
        f"{decision.get('target', '')} "
        f"(score={decision.get('score', 0)}, status={status}) {flag}\n"
        f"  {rationale}"
    )


def render_board_report_markdown(
    *,
    cycle_id: str,
    on_date: str,
    cadence: str,
    title_ar: str,
    title_en: str,
    signal_snapshot: dict[str, Any],
    gate_evaluations: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    approvals_pending: dict[str, Any],
    next_actions: list[dict[str, str]],
    hard_gates: list[str],
    warnings: list[str],
) -> str:
    """Render the bilingual board report Markdown for a strategic cycle."""
    s = signal_snapshot
    due_gates = [g for g in gate_evaluations if g.get("due")]
    pending_count = int(approvals_pending.get("count", 0))

    lines: list[str] = [
        f"# {title_en}",
        "",
        f"- Cycle: `{cycle_id}`",
        f"- Date: {on_date}",
        f"- Cadence: {cadence}",
        f"- Days since launch: {s.get('days_since_launch', 0)}",
        "",
        "## Strategic signals",
        f"- Cumulative revenue: {s.get('total_revenue_sar', 0)} SAR",
        f"- MRR: {s.get('mrr_sar', 0)} SAR",
        f"- Paid customers: {s.get('paid_customers', 0)}",
        f"- Active retainers: {s.get('retainer_count', 0)}",
        f"- Proof score: {s.get('proof_score', 0)}",
        f"- Adoption score: {s.get('adoption_score', 0)}",
        f"- Governance risk index: {s.get('governance_risk_index', 0)}",
        f"- Capital assets: {s.get('capital_asset_count', 0)}",
        f"- Founder hours / sprint: {s.get('founder_hours_per_sprint', 0)}",
        "",
        f"## Gate evaluations ({len(due_gates)} due / {len(gate_evaluations)} total)",
    ]
    for g in gate_evaluations:
        state = "due" if g.get("due") else "not-due"
        verdict = "pass" if g.get("passed") else "fail"
        conflict = " [conflict->hold]" if g.get("conflict") else ""
        lines.append(
            f"- `{g.get('gate_id')}` ({state}): {g.get('title_en')} "
            f"-> {g.get('decision_type')} ({verdict}){conflict}"
        )

    lines += ["", f"## Strategic decisions ({len(decisions)})"]
    if decisions:
        lines += [_decision_line(d, "en") for d in decisions]
    else:
        lines.append("- No strategic decisions this cycle.")

    lines += [
        "",
        f"## Approvals pending: {pending_count}",
    ]
    for item in approvals_pending.get("items", []):
        lines.append(
            f"- `{item.get('approval_id', '')}` {item.get('summary_en', '')}"
        )

    if cadence == "monthly":
        from auto_client_acquisition.board_decision_os.board_memo_generator import (
            BOARD_MEMO_SECTIONS,
        )

        lines += ["", "## Board memo sections (monthly)"]
        lines += [f"- {section}" for section in BOARD_MEMO_SECTIONS]

    lines += ["", "## Next actions"]
    lines += [f"- {a['en']}" for a in next_actions]
    lines += ["", "## Hard gates"]
    lines += [f"- {g}" for g in hard_gates]
    if warnings:
        lines += ["", f"## Warnings ({len(warnings)})"]
        lines += [f"- {w}" for w in warnings]

    # ── Arabic mirror ───────────────────────────────────────────────
    lines += [
        "",
        "---",
        "",
        f"# {title_ar}",
        "",
        f"- الدورة: `{cycle_id}`",
        f"- التاريخ: {on_date}",
        f"- الإيقاع: {cadence}",
        f"- أيام منذ الإطلاق: {s.get('days_since_launch', 0)}",
        "",
        "## الإشارات الاستراتيجية",
        f"- الإيراد التراكمي: {s.get('total_revenue_sar', 0)} ريال",
        f"- الإيراد الشهري المتكرر: {s.get('mrr_sar', 0)} ريال",
        f"- العملاء الدافعون: {s.get('paid_customers', 0)}",
        f"- الاشتراكات الفعّالة: {s.get('retainer_count', 0)}",
        f"- درجة الإثبات: {s.get('proof_score', 0)}",
        f"- درجة التبنّي: {s.get('adoption_score', 0)}",
        f"- مؤشر مخاطر الحوكمة: {s.get('governance_risk_index', 0)}",
        f"- الأصول الرأسمالية: {s.get('capital_asset_count', 0)}",
        f"- ساعات المؤسس لكل سبرنت: {s.get('founder_hours_per_sprint', 0)}",
        "",
        f"## تقييم البوابات ({len(due_gates)} مستحقّة / {len(gate_evaluations)} إجمالاً)",
    ]
    for g in gate_evaluations:
        state = "مستحقّة" if g.get("due") else "غير مستحقّة"
        verdict = "نجاح" if g.get("passed") else "إخفاق"
        conflict = " [تعارض->تعليق]" if g.get("conflict") else ""
        lines.append(
            f"- `{g.get('gate_id')}` ({state}): {g.get('title_ar')} "
            f"-> {g.get('decision_type')} ({verdict}){conflict}"
        )

    lines += ["", f"## القرارات الاستراتيجية ({len(decisions)})"]
    if decisions:
        lines += [_decision_line(d, "ar") for d in decisions]
    else:
        lines.append("- لا قرارات استراتيجية في هذه الدورة.")

    lines += ["", f"## موافقات معلّقة: {pending_count}"]
    for item in approvals_pending.get("items", []):
        lines.append(
            f"- `{item.get('approval_id', '')}` {item.get('summary_ar', '')}"
        )

    lines += ["", "## الإجراءات التالية"]
    lines += [f"- {a['ar']}" for a in next_actions]
    lines += ["", "## الخطوط الحمراء"]
    lines += [f"- {g}" for g in hard_gates]
    if warnings:
        lines += ["", f"## التحذيرات ({len(warnings)})"]
        lines += [f"- {w}" for w in warnings]
    lines.append("")
    return "\n".join(lines)


__all__ = ["render_board_report_markdown"]
