"""
Proposal Workflow — مصنع المقترحات.

تحويل brief عميل إلى مقترح موثَّق، مع verification للمصادر والادعاءات،
وإصدار نسخة قابلة للتسليم بعد موافقة الـ founder.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..execution.workflow_runtime import WorkflowSpec, WorkflowStep

if TYPE_CHECKING:
    from ..execution.workflow_runtime import WorkflowRuntime


SPEC: WorkflowSpec = WorkflowSpec(
    workflow_id="proposal_factory",
    name="Proposal Factory",
    purpose=(
        "تحويل brief عميل إلى مقترح موثَّق مع تحقّق من المصادر والادعاءات "
        "قبل التسليم."
    ),
    steps=(
        WorkflowStep(
            step_id="intake_brief",
            description="استقبال brief العميل وتطبيعه إلى صيغة موحّدة.",
            handler="fn:proposal_intake",
            inputs=(),
            outputs=("normalized_brief",),
        ),
        WorkflowStep(
            step_id="scope_outline",
            description="مخطّط النطاق الأوّلي مع افتراضات واضحة.",
            handler="agent:proposal_factory_agent",
            inputs=("normalized_brief",),
            outputs=("scope_outline",),
        ),
        WorkflowStep(
            step_id="proof_assembly",
            description="تجميع الأدلة والمراجع من Proof OS.",
            handler="agent:proposal_factory_agent",
            inputs=("scope_outline",),
            outputs=("proof_pack",),
        ),
        WorkflowStep(
            step_id="claim_verification",
            description="مرور الادعاءات عبر claim_verifier.",
            handler="fn:proposal_verify_claims",
            inputs=("scope_outline", "proof_pack"),
            outputs=("verified_claims",),
        ),
        WorkflowStep(
            step_id="pricing_draft",
            description="مسوّدة التسعير حسب نطاق العمل.",
            handler="agent:proposal_factory_agent",
            inputs=("scope_outline",),
            outputs=("pricing_draft",),
        ),
        WorkflowStep(
            step_id="proposal_render",
            description="تجميع مستند المقترح النهائي.",
            handler="agent:proposal_factory_agent",
            inputs=("normalized_brief", "scope_outline", "verified_claims", "pricing_draft"),
            outputs=("proposal_doc",),
        ),
        WorkflowStep(
            step_id="founder_approval",
            description="عرض المقترح على الـ founder للموافقة (S2).",
            handler="fn:proposal_request_approval",
            inputs=("proposal_doc",),
            outputs=("approval_record",),
        ),
        WorkflowStep(
            step_id="proposal_delivery",
            description="تسليم النسخة المعتمدة للعميل.",
            handler="fn:proposal_deliver",
            inputs=("proposal_doc", "approval_record"),
            outputs=("delivery_receipt",),
        ),
    ),
    owner="founder",
)


def register(runtime: WorkflowRuntime) -> None:
    runtime.register_spec(SPEC)


__all__ = ["SPEC", "register"]
