"""Daily Command Engine — the capstone executive brief generator.

Pure-logic engine that generates the daily operating brief by aggregating
company operator snapshots, pipeline intelligence, learning insights,
proof status, and pending approvals into a single actionable command.

This is the top of the product spine:
    Company Brain → … → Action → Draft → Approval → Outcome → Proof →
    Learning → **Daily Command**

No database, network, or LLM calls. The command is a read-only summary.
External actions still require approval. Revenue claims require payment
evidence.

Design principles:
- Deterministic content-addressable IDs (SHA-256).
- Frozen Pydantic v2 models — no silent mutation.
- Safety: ``execution_allowed=False`` always.
- Revenue and delivery states derived only from valid proof.
"""
from __future__ import annotations

import json
from datetime import UTC, date, datetime
from enum import StrEnum
from hashlib import sha256
from typing import Annotated, Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    model_validator,
)

from dealix.company_intelligence.company_operator import (
    CompanyOperatingSnapshot,
    OperatingHealth,
)
from dealix.company_intelligence.outcome_contracts import EvidenceState
from dealix.company_intelligence.pipeline_engine import (
    ForecastConfidence,
    PipelineAnalysis,
    PipelineHealth,
    RevenueForecast,
)

NonEmptyString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _stable_id(prefix: str, payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        default=str,
    )
    return f"{prefix}_{sha256(canonical.encode('utf-8')).hexdigest()[:16]}"


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class AttentionUrgency(StrEnum):
    """How urgently an item needs attention."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFORMATIONAL = "informational"


class CommandSection(StrEnum):
    """Sections of the daily command brief."""

    BLOCKERS = "blockers"
    APPROVALS = "approvals"
    PIPELINE = "pipeline"
    OPERATIONS = "operations"
    LEARNING = "learning"
    PROOF = "proof"
    NEXT_ACTIONS = "next_actions"


# ---------------------------------------------------------------------------
# Contracts
# ---------------------------------------------------------------------------


class AttentionItem(BaseModel):
    """Something that needs human attention today."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    section: CommandSection
    urgency: AttentionUrgency
    title: NonEmptyString
    description: str = ""
    action_required: bool = True
    entity_id: str = ""
    entity_type: str = ""


class DailyHealthAssessment(BaseModel):
    """Overall company health for the day."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    operating_health: OperatingHealth = OperatingHealth.GOOD
    pipeline_health: PipelineHealth = PipelineHealth.HEALTHY
    forecast_confidence: ForecastConfidence = ForecastConfidence.SPECULATIVE
    revenue_state: EvidenceState = EvidenceState.NOT_EVIDENCED
    delivery_state: EvidenceState = EvidenceState.NOT_EVIDENCED
    overall_score: float = Field(default=0.5, ge=0.0, le=1.0)
    summary: str = ""


class ApprovalQueueSummary(BaseModel):
    """Summary of pending approvals."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    total_pending: int = Field(default=0, ge=0)
    external_pending: int = Field(default=0, ge=0)
    high_risk_pending: int = Field(default=0, ge=0)
    oldest_pending_hours: float = Field(default=0.0, ge=0.0)
    items: tuple[str, ...] = ()


class DailyCommandBrief(BaseModel):
    """The complete daily operating brief — capstone of the product spine."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    brief_id: NonEmptyString
    brief_date: date
    health: DailyHealthAssessment
    attention_items: tuple[AttentionItem, ...] = ()
    approval_queue: ApprovalQueueSummary = Field(
        default_factory=ApprovalQueueSummary,
    )
    blocker_count: int = Field(default=0, ge=0)
    active_opportunities: int = Field(default=0, ge=0)
    pipeline_value_weighted: float = Field(default=0.0, ge=0.0)
    completed_today: int = Field(default=0, ge=0)
    failed_today: int = Field(default=0, ge=0)
    learning_events_count: int = Field(default=0, ge=0)
    proof_events_count: int = Field(default=0, ge=0)
    top_priorities: tuple[str, ...] = ()
    next_actions: tuple[str, ...] = ()
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    execution_allowed: bool = False
    source_id: NonEmptyString = ""

    @model_validator(mode="after")
    def _enforce_safety(self) -> DailyCommandBrief:
        if self.execution_allowed:
            raise ValueError(
                "daily command brief must never authorize execution"
            )
        return self


# ---------------------------------------------------------------------------
# Engine functions
# ---------------------------------------------------------------------------


def generate_daily_command(
    *,
    tenant_id: str,
    brief_date: date | None = None,
    operating_snapshot: CompanyOperatingSnapshot | None = None,
    pipeline_analysis: PipelineAnalysis | None = None,
    revenue_forecast: RevenueForecast | None = None,
    pending_approvals: tuple[str, ...] | list[str] = (),
    external_approvals: tuple[str, ...] | list[str] = (),
    high_risk_approvals: tuple[str, ...] | list[str] = (),
    learning_events_count: int = 0,
    proof_events_count: int = 0,
    revenue_state: EvidenceState = EvidenceState.NOT_EVIDENCED,
    delivery_state: EvidenceState = EvidenceState.NOT_EVIDENCED,
    blockers: tuple[str, ...] | list[str] = (),
    source_id: str = "daily_command_engine",
) -> DailyCommandBrief:
    """Generate the daily operating brief from all engine outputs."""

    command_date = brief_date or date.today()
    attention_items: list[AttentionItem] = []
    priorities: list[str] = []
    next_actions: list[str] = []

    # --- Blockers ---
    blocker_list = list(blockers)
    for blocker in blocker_list:
        attention_items.append(
            AttentionItem(
                section=CommandSection.BLOCKERS,
                urgency=AttentionUrgency.CRITICAL,
                title=blocker,
                action_required=True,
            )
        )
    if blocker_list:
        priorities.append(f"resolve {len(blocker_list)} blocker(s)")

    # --- Approvals ---
    all_approvals = list(pending_approvals)
    ext_approvals = list(external_approvals)
    risk_approvals = list(high_risk_approvals)

    for approval in ext_approvals:
        attention_items.append(
            AttentionItem(
                section=CommandSection.APPROVALS,
                urgency=AttentionUrgency.HIGH,
                title=f"external approval: {approval}",
                action_required=True,
            )
        )

    for approval in risk_approvals:
        if approval not in ext_approvals:
            attention_items.append(
                AttentionItem(
                    section=CommandSection.APPROVALS,
                    urgency=AttentionUrgency.HIGH,
                    title=f"high-risk approval: {approval}",
                    action_required=True,
                )
            )

    if all_approvals:
        priorities.append(f"review {len(all_approvals)} pending approval(s)")
        next_actions.append("review and decide on pending approvals")

    approval_queue = ApprovalQueueSummary(
        total_pending=len(all_approvals),
        external_pending=len(ext_approvals),
        high_risk_pending=len(risk_approvals),
        items=tuple(all_approvals),
    )

    # --- Operating health ---
    op_health = OperatingHealth.GOOD
    completed_today = 0
    failed_today = 0

    if operating_snapshot is not None:
        op_health = operating_snapshot.overall_health
        completed_today = operating_snapshot.total_completed_today
        failed_today = operating_snapshot.total_failed_today

        if op_health == OperatingHealth.CRITICAL:
            attention_items.append(
                AttentionItem(
                    section=CommandSection.OPERATIONS,
                    urgency=AttentionUrgency.CRITICAL,
                    title="operations health is CRITICAL",
                    description=f"{failed_today} failed actions today",
                    action_required=True,
                )
            )
            priorities.append("address critical operations health")

        if failed_today > 0:
            next_actions.append(f"investigate {failed_today} failed action(s)")

    # --- Pipeline ---
    pipe_health = PipelineHealth.HEALTHY
    active_opps = 0
    pipeline_value = 0.0
    forecast_conf = ForecastConfidence.SPECULATIVE

    if pipeline_analysis is not None:
        pipe_health = pipeline_analysis.pipeline_health
        active_opps = pipeline_analysis.active_opportunities

        if pipe_health in (PipelineHealth.AT_RISK, PipelineHealth.CRITICAL):
            attention_items.append(
                AttentionItem(
                    section=CommandSection.PIPELINE,
                    urgency=AttentionUrgency.HIGH,
                    title=f"pipeline health is {pipe_health.value}",
                    description=f"{active_opps} active opportunities",
                    action_required=True,
                )
            )
            priorities.append("strengthen pipeline with new opportunities")

        for risk in pipeline_analysis.top_risks:
            attention_items.append(
                AttentionItem(
                    section=CommandSection.PIPELINE,
                    urgency=AttentionUrgency.MEDIUM,
                    title=f"pipeline risk: {risk}",
                    action_required=False,
                )
            )

    if revenue_forecast is not None:
        pipeline_value = revenue_forecast.weighted_pipeline_value
        forecast_conf = revenue_forecast.confidence

        if pipeline_value > 0:
            next_actions.append(
                f"pipeline weighted value: {pipeline_value:,.0f} SAR "
                f"({forecast_conf.value} confidence)"
            )

    # --- Learning ---
    if learning_events_count > 0:
        attention_items.append(
            AttentionItem(
                section=CommandSection.LEARNING,
                urgency=AttentionUrgency.LOW,
                title=f"{learning_events_count} learning event(s) to review",
                action_required=False,
            )
        )
        next_actions.append(f"review {learning_events_count} learning insight(s)")

    # --- Proof ---
    if proof_events_count > 0:
        attention_items.append(
            AttentionItem(
                section=CommandSection.PROOF,
                urgency=AttentionUrgency.INFORMATIONAL,
                title=f"{proof_events_count} proof event(s) recorded",
                action_required=False,
            )
        )

    # --- Health assessment ---
    overall_score = _compute_overall_score(
        op_health=op_health,
        pipe_health=pipe_health,
        blocker_count=len(blocker_list),
        approval_count=len(all_approvals),
        failed_count=failed_today,
    )

    summary_parts: list[str] = []
    if blocker_list:
        summary_parts.append(f"{len(blocker_list)} blocker(s)")
    if all_approvals:
        summary_parts.append(f"{len(all_approvals)} pending approval(s)")
    if active_opps:
        summary_parts.append(f"{active_opps} active opportunity(ies)")
    if completed_today:
        summary_parts.append(f"{completed_today} completed today")

    summary = "; ".join(summary_parts) if summary_parts else "no notable activity"

    health = DailyHealthAssessment(
        operating_health=op_health,
        pipeline_health=pipe_health,
        forecast_confidence=forecast_conf,
        revenue_state=revenue_state,
        delivery_state=delivery_state,
        overall_score=overall_score,
        summary=summary,
    )

    # Sort attention items by urgency
    urgency_order = {
        AttentionUrgency.CRITICAL: 0,
        AttentionUrgency.HIGH: 1,
        AttentionUrgency.MEDIUM: 2,
        AttentionUrgency.LOW: 3,
        AttentionUrgency.INFORMATIONAL: 4,
    }
    attention_items.sort(key=lambda x: urgency_order.get(x.urgency, 5))

    # Default next action
    if not next_actions:
        next_actions.append("continue normal operations")

    brief_id = _stable_id(
        "dailybrief",
        {
            "tenant_id": tenant_id.strip(),
            "brief_date": command_date.isoformat(),
            "blocker_count": len(blocker_list),
            "approval_count": len(all_approvals),
            "active_opps": active_opps,
            "overall_score": overall_score,
        },
    )

    return DailyCommandBrief(
        tenant_id=tenant_id,
        brief_id=brief_id,
        brief_date=command_date,
        health=health,
        attention_items=tuple(attention_items),
        approval_queue=approval_queue,
        blocker_count=len(blocker_list),
        active_opportunities=active_opps,
        pipeline_value_weighted=pipeline_value,
        completed_today=completed_today,
        failed_today=failed_today,
        learning_events_count=learning_events_count,
        proof_events_count=proof_events_count,
        top_priorities=tuple(priorities),
        next_actions=tuple(next_actions),
        execution_allowed=False,
        source_id=source_id,
    )


def prioritize_attention_items(
    items: tuple[AttentionItem, ...] | list[AttentionItem],
) -> list[AttentionItem]:
    """Prioritize attention items by urgency and action requirement."""

    urgency_order = {
        AttentionUrgency.CRITICAL: 0,
        AttentionUrgency.HIGH: 1,
        AttentionUrgency.MEDIUM: 2,
        AttentionUrgency.LOW: 3,
        AttentionUrgency.INFORMATIONAL: 4,
    }
    return sorted(
        items,
        key=lambda x: (
            urgency_order.get(x.urgency, 5),
            0 if x.action_required else 1,
        ),
    )


def summarize_for_founder(
    brief: DailyCommandBrief,
) -> str:
    """Generate a concise founder-friendly summary in bilingual format."""

    lines: list[str] = []
    lines.append(f"📋 Daily Command — {brief.brief_date.isoformat()}")
    lines.append(f"الصحة العامة / Overall Health: {brief.health.overall_score:.0%}")
    lines.append("")

    # Blockers
    if brief.blocker_count > 0:
        lines.append(f"🚨 عوائق / Blockers: {brief.blocker_count}")
        for item in brief.attention_items:
            if item.section == CommandSection.BLOCKERS:
                lines.append(f"  - {item.title}")
        lines.append("")

    # Approvals
    if brief.approval_queue.total_pending > 0:
        lines.append(
            f"✅ موافقات معلقة / Pending Approvals: "
            f"{brief.approval_queue.total_pending}"
        )
        if brief.approval_queue.external_pending > 0:
            lines.append(
                f"  ⚠️ خارجية / External: {brief.approval_queue.external_pending}"
            )
        lines.append("")

    # Pipeline
    if brief.active_opportunities > 0:
        lines.append(f"📊 فرص نشطة / Active Opportunities: {brief.active_opportunities}")
        if brief.pipeline_value_weighted > 0:
            lines.append(
                f"  💰 قيمة مرجحة / Weighted Value: "
                f"{brief.pipeline_value_weighted:,.0f} SAR"
            )
        lines.append("")

    # Operations
    if brief.completed_today > 0 or brief.failed_today > 0:
        lines.append(
            f"⚙️ عمليات / Operations: "
            f"{brief.completed_today} completed, {brief.failed_today} failed"
        )
        lines.append("")

    # Next actions
    if brief.next_actions:
        lines.append("🎯 الخطوات القادمة / Next Actions:")
        for action in brief.next_actions:
            lines.append(f"  → {action}")

    return "\n".join(lines)


def _compute_overall_score(
    *,
    op_health: OperatingHealth,
    pipe_health: PipelineHealth,
    blocker_count: int,
    approval_count: int,
    failed_count: int,
) -> float:
    """Compute overall health score (0.0 - 1.0)."""

    op_scores = {
        OperatingHealth.EXCELLENT: 1.0,
        OperatingHealth.GOOD: 0.8,
        OperatingHealth.NEEDS_ATTENTION: 0.6,
        OperatingHealth.AT_RISK: 0.4,
        OperatingHealth.CRITICAL: 0.2,
    }
    pipe_scores = {
        PipelineHealth.EXCELLENT: 1.0,
        PipelineHealth.HEALTHY: 0.8,
        PipelineHealth.NEEDS_ATTENTION: 0.6,
        PipelineHealth.AT_RISK: 0.4,
        PipelineHealth.CRITICAL: 0.2,
    }

    base = (
        op_scores.get(op_health, 0.5) * 0.4
        + pipe_scores.get(pipe_health, 0.5) * 0.3
        + 0.3  # baseline
    )

    # Penalties
    if blocker_count > 0:
        base -= min(0.2, blocker_count * 0.05)
    if failed_count > 0:
        base -= min(0.15, failed_count * 0.03)
    if approval_count > 10:
        base -= 0.05  # too many pending approvals

    return round(max(0.0, min(1.0, base)), 4)
