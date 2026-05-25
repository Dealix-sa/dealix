"""
AI Trust Kit Workflow — حزمة الثقة في الذكاء الاصطناعي.

تُجمِّع موجز الحوكمة، لوحة المخاطر، شواهد التدقيق، وخطّة التحسين
كحزمة قابلة للتسليم للعميل أو الجهة التنظيمية.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..execution.workflow_runtime import WorkflowSpec, WorkflowStep

if TYPE_CHECKING:
    from ..execution.workflow_runtime import WorkflowRuntime


SPEC: WorkflowSpec = WorkflowSpec(
    workflow_id="ai_trust_kit",
    name="AI Trust Kit",
    purpose=(
        "إصدار حزمة موثَّقة تجمع حوكمة الذكاء الاصطناعي وضوابطه وشواهد "
        "التدقيق لتسليم العميل."
    ),
    steps=(
        WorkflowStep(
            step_id="discovery_questionnaire",
            description="استبيان اكتشاف لرسم خريطة استخدامات AI لدى العميل.",
            handler="agent:ai_trust_kit_agent",
            inputs=(),
            outputs=("discovery_responses",),
        ),
        WorkflowStep(
            step_id="risk_register_build",
            description="بناء سجل مخاطر AI من الاستبيان.",
            handler="agent:ai_trust_kit_agent",
            inputs=("discovery_responses",),
            outputs=("risk_register",),
        ),
        WorkflowStep(
            step_id="control_mapping",
            description="ربط المخاطر بالضوابط (PDPL، NCA، ISO).",
            handler="agent:ai_trust_kit_agent",
            inputs=("risk_register",),
            outputs=("control_map",),
        ),
        WorkflowStep(
            step_id="evidence_collection",
            description="تجميع الشواهد التشغيلية للضوابط المختارة.",
            handler="fn:trust_kit_collect_evidence",
            inputs=("control_map",),
            outputs=("evidence_bundle",),
        ),
        WorkflowStep(
            step_id="gap_analysis",
            description="تحليل الفجوات بين الضوابط المطلوبة والمنفّذة.",
            handler="agent:ai_trust_kit_agent",
            inputs=("control_map", "evidence_bundle"),
            outputs=("gap_report",),
        ),
        WorkflowStep(
            step_id="improvement_plan",
            description="خطة تحسين زمنيّة مع أولويات.",
            handler="agent:ai_trust_kit_agent",
            inputs=("gap_report",),
            outputs=("improvement_plan",),
        ),
        WorkflowStep(
            step_id="trust_kit_render",
            description="تجميع حزمة الثقة كملف قابل للتسليم.",
            handler="fn:trust_kit_render",
            inputs=("risk_register", "control_map", "evidence_bundle", "gap_report", "improvement_plan"),
            outputs=("trust_kit_doc",),
        ),
        WorkflowStep(
            step_id="founder_signoff",
            description="مراجعة وموافقة الـ founder قبل التسليم.",
            handler="fn:trust_kit_signoff",
            inputs=("trust_kit_doc",),
            outputs=("signoff_record",),
        ),
    ),
    owner="founder",
)


def register(runtime: WorkflowRuntime) -> None:
    runtime.register_spec(SPEC)


__all__ = ["SPEC", "register"]
