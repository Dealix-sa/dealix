"""
Market Radar Workflow — رادار السوق.

يجمع إشارات السوق من مصادر معتمدة، يقيس أهميّتها، ويصدر تقريرًا
دوريًا بالاتجاهات والإشارات المؤثّرة على الفرص الحالية.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..execution.workflow_runtime import WorkflowSpec, WorkflowStep

if TYPE_CHECKING:
    from ..execution.workflow_runtime import WorkflowRuntime


SPEC: WorkflowSpec = WorkflowSpec(
    workflow_id="market_radar",
    name="Market Radar",
    purpose=(
        "رصد إشارات السوق من مصادر معتمدة وإصدار تقرير اتجاهات يدعم "
        "قرارات الإيرادات."
    ),
    steps=(
        WorkflowStep(
            step_id="signal_intake",
            description="جلب الإشارات من قنوات RSS، تقارير، صحف.",
            handler="fn:market_radar_signal_intake",
            inputs=(),
            outputs=("raw_signals",),
        ),
        WorkflowStep(
            step_id="source_verification",
            description="فحص URLs عبر source_verifier.",
            handler="fn:market_radar_verify_sources",
            inputs=("raw_signals",),
            outputs=("verified_signals",),
        ),
        WorkflowStep(
            step_id="signal_dedup",
            description="إزالة التكرار وتوحيد الإشارات المتقاربة.",
            handler="fn:market_radar_dedup",
            inputs=("verified_signals",),
            outputs=("dedup_signals",),
        ),
        WorkflowStep(
            step_id="relevance_scoring",
            description="تقييم أهميّة كل إشارة بناءً على القطاعات المستهدفة.",
            handler="agent:market_radar_agent",
            inputs=("dedup_signals",),
            outputs=("scored_signals",),
        ),
        WorkflowStep(
            step_id="trend_synthesis",
            description="استخراج اتجاهات مركّبة من الإشارات.",
            handler="agent:market_radar_agent",
            inputs=("scored_signals",),
            outputs=("trends",),
        ),
        WorkflowStep(
            step_id="opportunity_mapping",
            description="ربط الاتجاهات بالفرص الحالية في pipeline.",
            handler="agent:market_radar_agent",
            inputs=("trends",),
            outputs=("opportunity_map",),
        ),
        WorkflowStep(
            step_id="radar_report_render",
            description="تجميع تقرير الرادار النهائي.",
            handler="fn:market_radar_render",
            inputs=("trends", "opportunity_map"),
            outputs=("radar_report",),
        ),
        WorkflowStep(
            step_id="report_distribution",
            description="توزيع التقرير على المعنيّين بعد المراجعة.",
            handler="fn:market_radar_distribute",
            inputs=("radar_report",),
            outputs=("distribution_receipt",),
            optional=True,
        ),
    ),
    owner="founder",
)


def register(runtime: WorkflowRuntime) -> None:
    runtime.register_spec(SPEC)


__all__ = ["SPEC", "register"]
