"""
Partner Pitch Workflow — مولّد العروض للشركاء.

يحوّل ملف الشريك المحتمل إلى pitch مخصّص مع وضوح في النموذج المالي وحدود
المسؤولية، مهيّأ للموافقة قبل الإرسال.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..execution.workflow_runtime import WorkflowSpec, WorkflowStep

if TYPE_CHECKING:
    from ..execution.workflow_runtime import WorkflowRuntime


SPEC: WorkflowSpec = WorkflowSpec(
    workflow_id="partner_pitch",
    name="Partner Pitch",
    purpose=(
        "إعداد عرض شراكة مخصّص مع نموذج مالي واضح وحدود مسؤولية موثَّقة "
        "قبل الإرسال."
    ),
    steps=(
        WorkflowStep(
            step_id="partner_profile_build",
            description="بناء ملف الشريك من المصادر المعتمدة.",
            handler="agent:partner_pitch_agent",
            inputs=(),
            outputs=("partner_profile",),
        ),
        WorkflowStep(
            step_id="value_fit_analysis",
            description="تحليل التوافق بين قدراتنا واحتياج الشريك.",
            handler="agent:partner_pitch_agent",
            inputs=("partner_profile",),
            outputs=("fit_analysis",),
        ),
        WorkflowStep(
            step_id="commercial_model_draft",
            description="مسوّدة النموذج المالي (revenue share، retainer، rev-cap).",
            handler="agent:partner_pitch_agent",
            inputs=("fit_analysis",),
            outputs=("commercial_model",),
        ),
        WorkflowStep(
            step_id="legal_boundaries",
            description="تحديد حدود المسؤولية والشروط القانونية الأساسية.",
            handler="agent:partner_pitch_agent",
            inputs=("commercial_model",),
            outputs=("legal_boundaries",),
        ),
        WorkflowStep(
            step_id="pitch_deck_render",
            description="تجميع العرض كملف قابل للمشاركة.",
            handler="agent:partner_pitch_agent",
            inputs=("partner_profile", "fit_analysis", "commercial_model", "legal_boundaries"),
            outputs=("pitch_deck",),
        ),
        WorkflowStep(
            step_id="claim_verification",
            description="تحقّق من الادعاءات قبل الإرسال.",
            handler="fn:partner_pitch_verify_claims",
            inputs=("pitch_deck",),
            outputs=("verified_claims",),
        ),
        WorkflowStep(
            step_id="founder_approval",
            description="عرض على الـ founder للموافقة (S2).",
            handler="fn:partner_pitch_request_approval",
            inputs=("pitch_deck", "verified_claims"),
            outputs=("approval_record",),
        ),
        WorkflowStep(
            step_id="pitch_dispatch",
            description="إرسال العرض المعتمد عبر قناة موثَّقة.",
            handler="fn:partner_pitch_dispatch",
            inputs=("pitch_deck", "approval_record"),
            outputs=("dispatch_receipt",),
        ),
    ),
    owner="founder",
)


def register(runtime: WorkflowRuntime) -> None:
    runtime.register_spec(SPEC)


__all__ = ["SPEC", "register"]
