"""Markdown report renderers for the daily distribution review surface.

These render to ``reports/distribution/*.md`` — the human review surface. They
are intentionally terse, table-first, and bilingual-friendly.
"""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.distribution_os.models import Draft, DraftStatus, Followup
from auto_client_acquisition.distribution_os.proposal_factory import ProposalDraft
from auto_client_acquisition.distribution_os.quality_gate import GateResult


def _truncate(text: str, n: int = 60) -> str:
    one_line = " ".join(text.split())
    return one_line if len(one_line) <= n else one_line[: n - 1] + "…"


def render_draft_queue_review(drafts: list[Draft]) -> str:
    pending = [
        d
        for d in drafts
        if d.status in {DraftStatus.PENDING_APPROVAL.value, DraftStatus.GENERATED.value}
    ]
    needs_edit = [d for d in drafts if d.status == DraftStatus.NEEDS_EDIT.value]
    lines = [
        "# Draft Queue Review — مراجعة طابور المسودات",
        "",
        "> كل المسودات تتطلب موافقة. لا إرسال خارجي من النظام — النسخ والإرسال يدوي بعد الموافقة.",
        "",
        f"- إجمالي المسودات: **{len(drafts)}**",
        f"- بانتظار الموافقة: **{len(pending)}**",
        f"- تحتاج تعديلاً: **{len(needs_edit)}**",
        "",
        "| Company | Sector | Channel | Type | Evidence | Risk | Status | Action |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for d in drafts:
        lines.append(
            f"| {d.company} | {d.sector} | {d.channel} | {d.draft_type} | "
            f"{d.evidence_level} | {d.risk_level} | {d.status} | approve/edit/reject/copy |"
        )
    lines.append("")
    if needs_edit:
        lines.append("## مسودات تحتاج تعديلاً (حُجبت من البوابة)")
        for d in needs_edit:
            lines.append(f"- `{d.id}` — {d.next_action}")
        lines.append("")
    return "\n".join(lines)


def render_followup_queue(followups: list[Followup]) -> str:
    due = [f for f in followups if f.status == "due"]
    lines = [
        "# Follow-up Queue — طابور المتابعات المستحقة",
        "",
        "> متابعات محكومة كمسودات فقط. القنوات يدوية بالكامل.",
        "",
        f"- إجمالي المتابعات: **{len(followups)}**",
        f"- المستحقة الآن: **{len(due)}**",
        "",
        "| Company | Type | Due date | Channel | Status | Notes |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for f in followups:
        lines.append(
            f"| {f.company} | {f.followup_type} | {f.due_date} | {f.channel} | {f.status} | {f.notes} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_proposal_report(proposals: list[ProposalDraft]) -> str:
    lines = [
        "# Proposal Draft Report — تقرير مسودات العروض",
        "",
        "> كل عرض مسودة تتطلب موافقة. لا التزام قانوني ولا أرقام نتائج بدون دليل.",
        "",
        f"- عروض جاهزة كمسودة: **{len(proposals)}**",
        "",
        "| Company | Sector | Evidence | Price range |",
        "| --- | --- | --- | --- |",
    ]
    for p in proposals:
        lines.append(
            f"| {p.company} | {p.sector} | {p.evidence_level} | {_truncate(p.sections.get('price', ''), 40)} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_metrics(metrics: dict[str, Any]) -> str:
    def _kv(d: dict[str, Any]) -> list[str]:
        return [f"- {k}: {v}" for k, v in sorted(d.items())]

    lines = [
        "# Distribution Metrics — مؤشرات التصريف",
        "",
        f"- إجمالي المسودات: **{metrics.get('drafts_total', 0)}**",
        f"- إجمالي المتابعات: **{metrics.get('followups_total', 0)}**",
        f"- المتابعات المستحقة: **{metrics.get('followups_due', 0)}**",
        "",
        "## المسودات حسب الحالة",
        *_kv(metrics.get("drafts_by_status", {})),
        "",
        "## المسودات حسب النوع",
        *_kv(metrics.get("drafts_by_type", {})),
        "",
        "## المسودات حسب القناة",
        *_kv(metrics.get("drafts_by_channel", {})),
        "",
        "## قمع العملاء (من حالة الـ prospect)",
        *_kv(metrics.get("prospect_funnel", {})),
        "",
        "## قرار المؤسس",
        "- اعتمد المسودات الأعلى ملاءمة أولاً.",
        "- أعطِ الأولوية للقطاعات التي فيها ردود أو مكالمات تشخيص محجوزة.",
        "- لا أرقام إيراد بدون دفع مثبت.",
        "",
    ]
    return "\n".join(lines)


def render_quality_gate(result: GateResult) -> str:
    lines = [
        "# Draft Quality Gate — بوابة جودة المسودات",
        "",
        f"- مسودات فُحصت: **{result.checked}**",
        f"- مخالفات: **{len(result.violations)}**",
        f"- النتيجة: **{'PASS' if result.ok else 'FAIL'}**",
        "",
    ]
    if result.violations:
        lines.append("| Draft | Code | Detail |")
        lines.append("| --- | --- | --- |")
        for v in result.violations:
            lines.append(f"| `{v.draft_id}` | {v.code} | {v.detail} |")
    else:
        lines.append("- لا مخالفات. ✅")
    lines.append("")
    return "\n".join(lines)


__all__ = [
    "render_draft_queue_review",
    "render_followup_queue",
    "render_metrics",
    "render_proposal_report",
    "render_quality_gate",
]
