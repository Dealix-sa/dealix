"""
Training Workshop Workflow — تصميم وإدارة ورش التدريب.

من تصميم منهج الورشة إلى التسليم وقياس الأثر بعد الجلسة.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..execution.workflow_runtime import WorkflowSpec, WorkflowStep

if TYPE_CHECKING:
    from ..execution.workflow_runtime import WorkflowRuntime


SPEC: WorkflowSpec = WorkflowSpec(
    workflow_id="training_workshop",
    name="Training Workshop",
    purpose=(
        "تصميم منهج ورشة عمل، إعداد المواد، التسليم، وقياس الأثر بعد الجلسة."
    ),
    steps=(
        WorkflowStep(
            step_id="learning_needs_intake",
            description="استقبال احتياجات التعلّم من العميل/الجمهور.",
            handler="fn:training_intake_needs",
            inputs=(),
            outputs=("learning_needs",),
        ),
        WorkflowStep(
            step_id="objectives_design",
            description="صياغة الأهداف التعلّمية القابلة للقياس.",
            handler="agent:training_workshop_agent",
            inputs=("learning_needs",),
            outputs=("learning_objectives",),
        ),
        WorkflowStep(
            step_id="curriculum_outline",
            description="هيكلة المنهج وزمن كل جلسة.",
            handler="agent:training_workshop_agent",
            inputs=("learning_objectives",),
            outputs=("curriculum_outline",),
        ),
        WorkflowStep(
            step_id="materials_drafting",
            description="إعداد المواد، التمارين، أوراق العمل.",
            handler="agent:training_workshop_agent",
            inputs=("curriculum_outline",),
            outputs=("materials_pack",),
        ),
        WorkflowStep(
            step_id="claim_verification",
            description="تحقّق من الادعاءات في المواد.",
            handler="fn:training_verify_claims",
            inputs=("materials_pack",),
            outputs=("verified_materials",),
        ),
        WorkflowStep(
            step_id="logistics_plan",
            description="خطة لوجستية (مكان، أدوات، تسجيل).",
            handler="fn:training_logistics",
            inputs=("curriculum_outline",),
            outputs=("logistics_plan",),
        ),
        WorkflowStep(
            step_id="delivery_session",
            description="تسليم الورشة (مسجَّل كحدث).",
            handler="fn:training_deliver",
            inputs=("verified_materials", "logistics_plan"),
            outputs=("delivery_record",),
        ),
        WorkflowStep(
            step_id="impact_survey",
            description="إصدار استبيان أثر بعد الجلسة وتوثيق النتائج.",
            handler="fn:training_impact_survey",
            inputs=("delivery_record",),
            outputs=("impact_results",),
        ),
    ),
    owner="founder",
)


def register(runtime: WorkflowRuntime) -> None:
    runtime.register_spec(SPEC)


__all__ = ["SPEC", "register"]
