"""
Revenue Hunter Workflow — قنّاص الإيرادات.

سلسلة خطوات deterministic لاكتشاف الفرص، تأهيلها، صياغة الرسائل والمقترحات،
متابعتها، وتسجيل النتائج كأصول قابلة لإعادة الاستخدام.

كل خطوة موصوفة كـ `WorkflowStep` مع handler reference (لا يوجد agent فعلي
مطلوب في هذه المرحلة — التسجيل في الـ runtime يأتي لاحقًا).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..execution.workflow_runtime import WorkflowSpec, WorkflowStep

if TYPE_CHECKING:
    from ..execution.workflow_runtime import WorkflowRuntime


SPEC: WorkflowSpec = WorkflowSpec(
    workflow_id="revenue_hunter",
    name="Revenue Hunter",
    purpose=(
        "اكتشاف الفرص المؤهَّلة، صياغة الرسائل والمقترحات، تسجيل النتائج "
        "كأصول قابلة لإعادة الاستخدام."
    ),
    steps=(
        WorkflowStep(
            step_id="lead_discovery_draft",
            description="مسوّدة قائمة فرص أوّلية من مصادر معتمدة.",
            handler="agent:revenue_hunter_agent",
            inputs=(),
            outputs=("lead_draft",),
        ),
        WorkflowStep(
            step_id="lead_scoring",
            description="حساب درجة جاهزية الفرصة قبل التواصل.",
            handler="agent:revenue_hunter_agent",
            inputs=("lead_draft",),
            outputs=("scored_leads",),
        ),
        WorkflowStep(
            step_id="pain_hypothesis",
            description="صياغة فرضية الألم لكل فرصة مؤهَّلة.",
            handler="agent:revenue_hunter_agent",
            inputs=("scored_leads",),
            outputs=("pain_hypotheses",),
        ),
        WorkflowStep(
            step_id="message_drafts",
            description="إنشاء مسودات رسائل أولى تخضع لـ Trust Gate.",
            handler="agent:revenue_hunter_agent",
            inputs=("pain_hypotheses",),
            outputs=("message_drafts",),
        ),
        WorkflowStep(
            step_id="proposal_candidates",
            description="اقتراحات أوّلية تربط الألم بالحلّ.",
            handler="agent:proposal_factory_agent",
            inputs=("message_drafts", "pain_hypotheses"),
            outputs=("proposal_candidates",),
        ),
        WorkflowStep(
            step_id="follow_up_plan",
            description="خطة متابعة منضبطة مع كل فرصة.",
            handler="agent:revenue_hunter_agent",
            inputs=("proposal_candidates",),
            outputs=("follow_up_plan",),
        ),
        WorkflowStep(
            step_id="outcome_logging",
            description="تسجيل النتائج في Value Ledger.",
            handler="fn:revenue_hunter_log_outcome",
            inputs=("follow_up_plan",),
            outputs=("outcome_record",),
        ),
        WorkflowStep(
            step_id="asset_creation",
            description="تحويل الفائز إلى أصل (Asset) قابل لإعادة الاستخدام.",
            handler="fn:revenue_hunter_create_asset",
            inputs=("outcome_record",),
            outputs=("asset_id",),
        ),
    ),
    owner="founder",
)


def register(runtime: WorkflowRuntime) -> None:
    """تسجيل الـ workflow في runtime معيّن."""
    runtime.register_spec(SPEC)


__all__ = ["SPEC", "register"]
