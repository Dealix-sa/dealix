"""
Venture Test Workflow — اختبار فرضية مشروع جديد.

دورة قصيرة لاختبار فرضية تجارية: من تأطير الفرضية، تصميم التجربة،
جمع الإشارات، وقرار continue/pivot/kill.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..execution.workflow_runtime import WorkflowSpec, WorkflowStep

if TYPE_CHECKING:
    from ..execution.workflow_runtime import WorkflowRuntime


SPEC: WorkflowSpec = WorkflowSpec(
    workflow_id="venture_test",
    name="Venture Test",
    purpose=(
        "تشغيل دورة قصيرة لاختبار فرضية تجارية: تأطير، تصميم تجربة، "
        "جمع إشارات، قرار continue/pivot/kill."
    ),
    steps=(
        WorkflowStep(
            step_id="hypothesis_framing",
            description="تأطير الفرضية بصيغة قابلة للاختبار.",
            handler="agent:venture_test_agent",
            inputs=(),
            outputs=("hypothesis",),
        ),
        WorkflowStep(
            step_id="success_criteria",
            description="تعريف معايير النجاح/الفشل قبل التجربة.",
            handler="agent:venture_test_agent",
            inputs=("hypothesis",),
            outputs=("success_criteria",),
        ),
        WorkflowStep(
            step_id="experiment_design",
            description="تصميم تجربة محدودة الزمن والكلفة.",
            handler="agent:venture_test_agent",
            inputs=("hypothesis", "success_criteria"),
            outputs=("experiment_plan",),
        ),
        WorkflowStep(
            step_id="risk_assessment",
            description="تقييم مخاطر التجربة (PDPL، سمعة، كلفة).",
            handler="fn:venture_test_risk_assess",
            inputs=("experiment_plan",),
            outputs=("risk_report",),
        ),
        WorkflowStep(
            step_id="founder_greenlight",
            description="موافقة الـ founder قبل التشغيل (S2).",
            handler="fn:venture_test_greenlight",
            inputs=("experiment_plan", "risk_report"),
            outputs=("greenlight_record",),
        ),
        WorkflowStep(
            step_id="experiment_execution",
            description="تشغيل التجربة وجمع الإشارات.",
            handler="fn:venture_test_execute",
            inputs=("experiment_plan", "greenlight_record"),
            outputs=("signals",),
        ),
        WorkflowStep(
            step_id="signal_analysis",
            description="تحليل الإشارات مقابل معايير النجاح.",
            handler="agent:venture_test_agent",
            inputs=("signals", "success_criteria"),
            outputs=("analysis",),
        ),
        WorkflowStep(
            step_id="decision_log",
            description="قرار continue/pivot/kill مع تبرير وتوثيق.",
            handler="fn:venture_test_decide",
            inputs=("analysis",),
            outputs=("decision_record",),
        ),
    ),
    owner="founder",
)


def register(runtime: WorkflowRuntime) -> None:
    runtime.register_spec(SPEC)


__all__ = ["SPEC", "register"]
