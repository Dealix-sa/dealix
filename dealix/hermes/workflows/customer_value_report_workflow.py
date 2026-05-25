"""
Customer Value Report Workflow — تقرير قيمة العميل الشهري.

يحوّل سجل القيمة (Value Ledger) لكل عميل إلى تقرير شهري يربط
المخرجات المسلَّمة بالأثر التشغيلي، مع شواهد قابلة للتدقيق.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..execution.workflow_runtime import WorkflowSpec, WorkflowStep

if TYPE_CHECKING:
    from ..execution.workflow_runtime import WorkflowRuntime


SPEC: WorkflowSpec = WorkflowSpec(
    workflow_id="customer_value_report",
    name="Customer Value Report",
    purpose=(
        "إصدار تقرير شهري يوثّق قيمة العميل من Value Ledger مع شواهد "
        "قابلة للتدقيق."
    ),
    steps=(
        WorkflowStep(
            step_id="ledger_extract",
            description="استخراج أحداث القيمة للعميل خلال الشهر.",
            handler="fn:value_report_extract_ledger",
            inputs=(),
            outputs=("ledger_events",),
        ),
        WorkflowStep(
            step_id="tier_breakdown",
            description="تقسيم الأحداث حسب tier (estimated/observed/verified/client_confirmed).",
            handler="fn:value_report_tier_breakdown",
            inputs=("ledger_events",),
            outputs=("tier_summary",),
        ),
        WorkflowStep(
            step_id="impact_narrative",
            description="صياغة قصّة الأثر بصيغة العميل.",
            handler="agent:customer_value_report_agent",
            inputs=("tier_summary",),
            outputs=("impact_narrative",),
        ),
        WorkflowStep(
            step_id="evidence_attach",
            description="إرفاق شواهد ProofPack المرتبطة بكل بند.",
            handler="fn:value_report_attach_evidence",
            inputs=("ledger_events",),
            outputs=("evidence_attachments",),
        ),
        WorkflowStep(
            step_id="adoption_score",
            description="حساب درجة التبنّي من adoption_os.",
            handler="fn:value_report_adoption_score",
            inputs=("ledger_events",),
            outputs=("adoption_score",),
        ),
        WorkflowStep(
            step_id="next_value_plan",
            description="خطة القيمة المقترحة للشهر القادم.",
            handler="agent:customer_value_report_agent",
            inputs=("tier_summary", "adoption_score"),
            outputs=("next_value_plan",),
        ),
        WorkflowStep(
            step_id="report_render",
            description="تجميع التقرير النهائي ثنائي اللغة.",
            handler="fn:value_report_render",
            inputs=("impact_narrative", "evidence_attachments", "adoption_score", "next_value_plan"),
            outputs=("value_report_doc",),
        ),
        WorkflowStep(
            step_id="client_delivery",
            description="إرسال التقرير المعتمد للعميل.",
            handler="fn:value_report_deliver",
            inputs=("value_report_doc",),
            outputs=("delivery_receipt",),
        ),
    ),
    owner="founder",
)


def register(runtime: WorkflowRuntime) -> None:
    runtime.register_spec(SPEC)


__all__ = ["SPEC", "register"]
