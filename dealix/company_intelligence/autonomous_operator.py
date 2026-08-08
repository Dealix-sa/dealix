"""Autonomous Company Operator — the master brain that runs the company.

Orchestrates the full 12-stage autonomous operating cycle that replaces
the need for dedicated employees across research, qualification, outreach,
follow-up, negotiation, closing, delivery, and growth.

Every stage produces proposals that flow through the human approval chain.
The operator NEVER takes external action autonomously — it prepares
everything and presents a ready-to-execute plan to the founder.

The 12 stages:
1.  DISCOVER — find and profile prospects from data sources
2.  QUALIFY — score against ICP criteria
3.  PLAN — design outreach approach
4.  DRAFT — generate personalized communications
5.  APPROVE — queue for founder review
6.  EXECUTE — send approved messages (controlled-live)
7.  RESPOND — classify and handle responses
8.  NEGOTIATE — manage objections and deal terms
9.  CLOSE — drive deals to completion
10. DELIVER — manage post-sale fulfillment
11. GROW — identify expansion and renewal
12. LEARN — extract patterns and improve

No database, network, or LLM calls. All external effects require
human approval.

Design principles:
- Deterministic content-addressable IDs (SHA-256).
- Frozen Pydantic v2 models — no silent mutation.
- Safety: ``autonomous_execution=False`` always.
- Every cycle produces a FounderActionPack for human review.
- Arabic-first bilingual output.
"""
from __future__ import annotations

import json
from datetime import UTC, datetime
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

from dealix.company_intelligence.followup_engine import (
    ClosingSignal,
    DealProgression,
    DealStage,
    FollowUpAction,
    ObjectionCategory,
    assess_deal_progression,
    handle_response,
)
from dealix.company_intelligence.fulfillment_engine import (
    ClientEngagement,
    EngagementStatus,
    RenewalAssessment,
    assess_renewal,
)
from dealix.company_intelligence.outreach_engine import (
    CadenceSpeed,
    OutreachChannel,
    OutreachSequence,
    plan_sequence,
)
from dealix.company_intelligence.research_engine import (
    CompanyProfile,
    ICPScore,
    ProspectPriority,
    ResearchBrief,
    batch_research,
    rank_prospects,
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


class CycleStage(StrEnum):
    """The 12 stages of the autonomous operating cycle."""

    DISCOVER = "discover"
    QUALIFY = "qualify"
    PLAN = "plan"
    DRAFT = "draft"
    APPROVE = "approve"
    EXECUTE = "execute"
    RESPOND = "respond"
    NEGOTIATE = "negotiate"
    CLOSE = "close"
    DELIVER = "deliver"
    GROW = "grow"
    LEARN = "learn"


class ActionPriority(StrEnum):
    """Priority of a founder action."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ActionCategory(StrEnum):
    """Category of a founder action."""

    APPROVE_OUTREACH = "approve_outreach"
    RESPOND_TO_LEAD = "respond_to_lead"
    REVIEW_PROPOSAL = "review_proposal"
    HANDLE_OBJECTION = "handle_objection"
    CLOSE_DEAL = "close_deal"
    DELIVERY_DECISION = "delivery_decision"
    RENEWAL_DECISION = "renewal_decision"
    REVIEW_REPORT = "review_report"
    STRATEGY_DECISION = "strategy_decision"


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class FounderAction(BaseModel):
    """A single action requiring founder attention."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    action_id: str = ""
    priority: ActionPriority = ActionPriority.MEDIUM
    category: ActionCategory = ActionCategory.REVIEW_REPORT
    title: str = ""
    title_ar: str = ""
    description: str = ""
    description_ar: str = ""
    prospect_name: str = ""
    prospect_company: str = ""
    recommended_action: str = ""
    recommended_action_ar: str = ""
    estimated_minutes: int = 5
    stage: CycleStage = CycleStage.DISCOVER


class FounderActionPack(BaseModel):
    """Daily pack of actions for the founder — the operator's output."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    pack_id: str = ""
    cycle_date: str = ""
    actions: tuple[FounderAction, ...] = ()
    total_actions: int = 0
    critical_actions: int = 0
    estimated_total_minutes: int = 0
    summary_ar: str = ""
    summary_en: str = ""
    autonomous_execution: bool = False
    source_id: NonEmptyString = ""
    created_at: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat(),
    )

    @model_validator(mode="after")
    def _never_autonomous(self) -> FounderActionPack:
        if self.autonomous_execution:
            raise ValueError(
                "FounderActionPack.autonomous_execution must be False — "
                "the operator prepares, the founder decides"
            )
        return self

    def model_post_init(self, _context: Any) -> None:
        if not self.pack_id:
            object.__setattr__(
                self,
                "pack_id",
                _stable_id(
                    "actionpack",
                    {
                        "tenant": self.tenant_id,
                        "date": self.cycle_date,
                        "source": self.source_id,
                    },
                ),
            )
        if not self.total_actions:
            object.__setattr__(self, "total_actions", len(self.actions))
        if not self.critical_actions:
            c = sum(1 for a in self.actions if a.priority == ActionPriority.CRITICAL)
            object.__setattr__(self, "critical_actions", c)
        if not self.estimated_total_minutes:
            t = sum(a.estimated_minutes for a in self.actions)
            object.__setattr__(self, "estimated_total_minutes", t)


class OperatingCycle(BaseModel):
    """One complete cycle of the autonomous operator."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    cycle_id: str = ""
    cycle_date: str = ""

    # Stage outputs
    research_briefs: tuple[ResearchBrief, ...] = ()
    qualified_prospects: tuple[ICPScore, ...] = ()
    outreach_sequences: tuple[OutreachSequence, ...] = ()
    follow_up_actions: tuple[FollowUpAction, ...] = ()
    deal_progressions: tuple[DealProgression, ...] = ()
    active_engagements: tuple[ClientEngagement, ...] = ()
    renewal_assessments: tuple[RenewalAssessment, ...] = ()

    # Aggregate metrics
    new_prospects_found: int = 0
    qualified_count: int = 0
    sequences_planned: int = 0
    responses_handled: int = 0
    deals_in_pipeline: int = 0
    active_clients: int = 0

    # Output for founder
    action_pack: FounderActionPack | None = None

    autonomous_execution: bool = False
    source_id: NonEmptyString = ""
    created_at: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat(),
    )

    @model_validator(mode="after")
    def _never_autonomous(self) -> OperatingCycle:
        if self.autonomous_execution:
            raise ValueError(
                "OperatingCycle.autonomous_execution must be False — "
                "the operator proposes, the founder disposes"
            )
        return self

    def model_post_init(self, _context: Any) -> None:
        if not self.cycle_id:
            object.__setattr__(
                self,
                "cycle_id",
                _stable_id(
                    "cycle",
                    {
                        "tenant": self.tenant_id,
                        "date": self.cycle_date,
                        "source": self.source_id,
                    },
                ),
            )


# ---------------------------------------------------------------------------
# Public API — the autonomous operating cycle
# ---------------------------------------------------------------------------


def run_operating_cycle(
    *,
    tenant_id: str,
    cycle_date: str = "",
    # Stage 1: New prospects to research
    new_prospects: list[CompanyProfile] | None = None,
    # Stage 7: Responses received
    responses: list[dict[str, str]] | None = None,
    # Stage 10: Active engagements
    engagements: list[ClientEngagement] | None = None,
    # Stage 8-9: Active deals
    active_deals: list[dict[str, Any]] | None = None,
    source_id: str = "",
) -> OperatingCycle:
    """Run one complete autonomous operating cycle.

    This is the master function that orchestrates all 12 stages.
    It returns an OperatingCycle containing everything the founder
    needs to review and approve.
    """
    if not cycle_date:
        cycle_date = datetime.now(UTC).strftime("%Y-%m-%d")

    founder_actions: list[FounderAction] = []

    # ── Stage 1-2: DISCOVER & QUALIFY ──────────────────────────────────────
    research_briefs: list[ResearchBrief] = []
    qualified: list[ICPScore] = []

    if new_prospects:
        research_briefs = batch_research(
            tenant_id=tenant_id,
            profiles=new_prospects,
            source_id=source_id,
        )
        scores = [b.icp_score for b in research_briefs]
        ranked = rank_prospects(scores)
        qualified = [s for s in ranked if s.qualified]

        for brief in research_briefs:
            if brief.icp_score.qualified:
                founder_actions.append(FounderAction(
                    action_id=_stable_id("action", {"type": "review_prospect", "prospect": brief.profile.company_name}),
                    priority=ActionPriority.HIGH if brief.icp_score.priority == ProspectPriority.HOT else ActionPriority.MEDIUM,
                    category=ActionCategory.APPROVE_OUTREACH,
                    title=f"Review prospect: {brief.profile.company_name}",
                    title_ar=f"راجع العميل المحتمل: {brief.profile.company_name_ar or brief.profile.company_name}",
                    description=brief.summary_en,
                    description_ar=brief.summary_ar,
                    prospect_name=brief.profile.company_name,
                    prospect_company=brief.profile.company_name,
                    recommended_action=brief.recommended_approach,
                    recommended_action_ar=brief.recommended_approach,
                    estimated_minutes=3,
                    stage=CycleStage.QUALIFY,
                ))

    # ── Stage 3-4: PLAN & DRAFT ────────────────────────────────────────────
    sequences: list[OutreachSequence] = []

    for brief in research_briefs:
        if not brief.icp_score.qualified:
            continue
        profile = brief.profile
        dm_name = ""
        dm_email = ""
        dm_whatsapp = ""
        for dm in profile.decision_makers:
            if dm.is_primary or not dm_name:
                dm_name = dm.name
                dm_email = dm.email
                dm_whatsapp = dm.whatsapp

        seq = plan_sequence(
            tenant_id=tenant_id,
            prospect_name=dm_name or profile.company_name,
            prospect_company=profile.company_name,
            prospect_email=dm_email,
            prospect_whatsapp=dm_whatsapp,
            sector=profile.sector,
            pain_points=tuple(
                sig.value for sig in profile.pain_signals
            ),
            cadence=CadenceSpeed.STANDARD,
            channel=OutreachChannel(brief.recommended_channel) if brief.recommended_channel in ("email", "whatsapp", "sms") else OutreachChannel.EMAIL,
            source_id=source_id,
        )
        sequences.append(seq)

        founder_actions.append(FounderAction(
            action_id=_stable_id("action", {"type": "approve_sequence", "company": profile.company_name}),
            priority=ActionPriority.HIGH,
            category=ActionCategory.APPROVE_OUTREACH,
            title=f"Approve outreach sequence: {profile.company_name}",
            title_ar=f"اعتمد تسلسل التواصل: {profile.company_name_ar or profile.company_name}",
            description=f"{len(seq.touches)} touches planned via {seq.primary_channel.value}",
            description_ar=f"{len(seq.touches)} رسائل مخططة عبر {seq.primary_channel.value}",
            prospect_name=dm_name or profile.company_name,
            prospect_company=profile.company_name,
            recommended_action="Review and approve first message",
            recommended_action_ar="راجع واعتمد الرسالة الأولى",
            estimated_minutes=5,
            stage=CycleStage.DRAFT,
        ))

    # ── Stage 7: RESPOND ───────────────────────────────────────────────────
    follow_ups: list[FollowUpAction] = []

    if responses:
        for resp in responses:
            action = handle_response(
                tenant_id=tenant_id,
                prospect_name=resp.get("prospect_name", ""),
                prospect_company=resp.get("prospect_company", ""),
                response_text=resp.get("text", ""),
                source_id=source_id,
            )
            follow_ups.append(action)

            if action.action_type == "opt_out" or action.action_type in ("schedule_discovery", "provide_info"):
                priority = ActionPriority.CRITICAL
            elif action.action_type == "handle_objection":
                priority = ActionPriority.HIGH
            else:
                priority = ActionPriority.MEDIUM

            founder_actions.append(FounderAction(
                action_id=_stable_id("action", {"type": "respond", "prospect": resp.get("prospect_name", "")}),
                priority=priority,
                category=ActionCategory.RESPOND_TO_LEAD,
                title=f"Respond to {resp.get('prospect_name', 'prospect')}",
                title_ar=f"رد على {resp.get('prospect_name', 'العميل المحتمل')}",
                description=f"Action: {action.action_type} — {action.reason}",
                description_ar=action.reason,
                prospect_name=resp.get("prospect_name", ""),
                prospect_company=resp.get("prospect_company", ""),
                recommended_action=action.action_type,
                recommended_action_ar=action.reason,
                estimated_minutes=3 if action.action_type == "opt_out" else 5,
                stage=CycleStage.RESPOND,
            ))

    # ── Stage 8-9: NEGOTIATE & CLOSE ───────────────────────────────────────
    deal_progressions: list[DealProgression] = []

    if active_deals:
        for deal_data in active_deals:
            progression = assess_deal_progression(
                tenant_id=tenant_id,
                prospect_name=deal_data.get("prospect_name", ""),
                prospect_company=deal_data.get("prospect_company", ""),
                current_stage=DealStage(deal_data.get("stage", "prospect")),
                closing_signals=tuple(
                    ClosingSignal(s) for s in deal_data.get("closing_signals", [])
                ),
                objections_raised=tuple(
                    ObjectionCategory(o) for o in deal_data.get("objections_raised", [])
                ),
                objections_resolved=tuple(
                    ObjectionCategory(o) for o in deal_data.get("objections_resolved", [])
                ),
                days_in_stage=deal_data.get("days_in_stage", 0),
                total_touches=deal_data.get("total_touches", 0),
                total_replies=deal_data.get("total_replies", 0),
                estimated_value=deal_data.get("estimated_value", 0.0),
                source_id=source_id,
            )
            deal_progressions.append(progression)

            if progression.closing_probability >= 70:
                priority = ActionPriority.CRITICAL
                category = ActionCategory.CLOSE_DEAL
            elif progression.closing_probability >= 40:
                priority = ActionPriority.HIGH
                category = ActionCategory.REVIEW_PROPOSAL
            else:
                priority = ActionPriority.MEDIUM
                category = ActionCategory.STRATEGY_DECISION

            founder_actions.append(FounderAction(
                action_id=_stable_id("action", {"type": "deal", "company": deal_data.get("prospect_company", "")}),
                priority=priority,
                category=category,
                title=f"Deal: {deal_data.get('prospect_company', '')} ({progression.current_stage.value})",
                title_ar=f"صفقة: {deal_data.get('prospect_company', '')} ({progression.current_stage.value})",
                description=f"Closing probability: {progression.closing_probability:.0f}% — Next: {progression.next_action}",
                description_ar=f"احتمال الإغلاق: {progression.closing_probability:.0f}% — التالي: {progression.next_action_ar}",
                prospect_name=deal_data.get("prospect_name", ""),
                prospect_company=deal_data.get("prospect_company", ""),
                recommended_action=progression.next_action,
                recommended_action_ar=progression.next_action_ar,
                estimated_minutes=10,
                stage=CycleStage.NEGOTIATE if progression.current_stage == DealStage.NEGOTIATION else CycleStage.CLOSE,
            ))

    # ── Stage 10-11: DELIVER & GROW ────────────────────────────────────────
    renewal_list: list[RenewalAssessment] = []

    if engagements:
        for eng in engagements:
            if eng.status in (EngagementStatus.ACTIVE, EngagementStatus.AT_RISK):
                renewal = assess_renewal(
                    tenant_id=tenant_id,
                    engagement=eng,
                    source_id=source_id,
                )
                renewal_list.append(renewal)

                if eng.status == EngagementStatus.AT_RISK:
                    priority = ActionPriority.CRITICAL
                elif renewal.renewal_probability < 50:
                    priority = ActionPriority.HIGH
                else:
                    priority = ActionPriority.LOW

                founder_actions.append(FounderAction(
                    action_id=_stable_id("action", {"type": "renewal", "company": eng.client_company}),
                    priority=priority,
                    category=ActionCategory.RENEWAL_DECISION,
                    title=f"Client: {eng.client_company} — {eng.status.value}",
                    title_ar=f"عميل: {eng.client_company} — {eng.status.value}",
                    description=f"Renewal probability: {renewal.renewal_probability:.0f}% — {renewal.recommended_action}",
                    description_ar=f"احتمال التجديد: {renewal.renewal_probability:.0f}% — {renewal.recommended_action_ar}",
                    prospect_name=eng.client_name,
                    prospect_company=eng.client_company,
                    recommended_action=renewal.recommended_action,
                    recommended_action_ar=renewal.recommended_action_ar,
                    estimated_minutes=10,
                    stage=CycleStage.GROW,
                ))

    # ── Build Founder Action Pack ──────────────────────────────────────────
    # Sort actions by priority
    priority_order = {
        ActionPriority.CRITICAL: 0,
        ActionPriority.HIGH: 1,
        ActionPriority.MEDIUM: 2,
        ActionPriority.LOW: 3,
        ActionPriority.INFO: 4,
    }
    founder_actions.sort(key=lambda a: priority_order.get(a.priority, 5))

    action_pack = _build_action_pack(
        tenant_id=tenant_id,
        cycle_date=cycle_date,
        actions=founder_actions,
        source_id=source_id,
    )

    return OperatingCycle(
        tenant_id=tenant_id,
        cycle_date=cycle_date,
        research_briefs=tuple(research_briefs),
        qualified_prospects=tuple(qualified),
        outreach_sequences=tuple(sequences),
        follow_up_actions=tuple(follow_ups),
        deal_progressions=tuple(deal_progressions),
        active_engagements=tuple(engagements or []),
        renewal_assessments=tuple(renewal_list),
        new_prospects_found=len(new_prospects or []),
        qualified_count=len(qualified),
        sequences_planned=len(sequences),
        responses_handled=len(follow_ups),
        deals_in_pipeline=len(deal_progressions),
        active_clients=len(engagements or []),
        action_pack=action_pack,
        autonomous_execution=False,
        source_id=source_id,
    )


def summarize_cycle_for_founder(cycle: OperatingCycle) -> str:
    """Generate a bilingual founder summary of the operating cycle."""
    lines: list[str] = []
    lines.append("═══ Daily Operating Cycle — دورة التشغيل اليومية ═══")
    lines.append(f"التاريخ / Date: {cycle.cycle_date}")
    lines.append("")

    # Metrics
    lines.append("── المقاييس / Metrics ──")
    lines.append(f"  عملاء محتملون جدد / New prospects: {cycle.new_prospects_found}")
    lines.append(f"  مؤهلون / Qualified: {cycle.qualified_count}")
    lines.append(f"  تسلسلات مخططة / Sequences planned: {cycle.sequences_planned}")
    lines.append(f"  ردود معالجة / Responses handled: {cycle.responses_handled}")
    lines.append(f"  صفقات نشطة / Active deals: {cycle.deals_in_pipeline}")
    lines.append(f"  عملاء نشطون / Active clients: {cycle.active_clients}")
    lines.append("")

    # Action pack summary
    if cycle.action_pack:
        pack = cycle.action_pack
        lines.append("── إجراءات المؤسس / Founder Actions ──")
        lines.append(f"  إجمالي / Total: {pack.total_actions}")
        lines.append(f"  حرجة / Critical: {pack.critical_actions}")
        lines.append(f"  الوقت المقدر / Est. time: {pack.estimated_total_minutes} دقيقة/min")
        lines.append("")

        for i, action in enumerate(pack.actions[:10], 1):
            emoji = {"critical": "🔴", "high": "🟡", "medium": "🔵", "low": "⚪", "info": "ℹ️"}.get(action.priority.value, "•")
            lines.append(f"  {emoji} {i}. {action.title_ar}")
            lines.append(f"     → {action.recommended_action_ar}")
            lines.append(f"     ⏱️ {action.estimated_minutes} دقيقة/min")
            lines.append("")

    lines.append("═══════════════════════════════════════════════════")
    lines.append("المشغل يحضّر — المؤسس يقرر")
    lines.append("The operator prepares — the founder decides")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _build_action_pack(
    *,
    tenant_id: str,
    cycle_date: str,
    actions: list[FounderAction],
    source_id: str,
) -> FounderActionPack:
    """Build the founder action pack from collected actions."""
    critical = sum(1 for a in actions if a.priority == ActionPriority.CRITICAL)
    total_minutes = sum(a.estimated_minutes for a in actions)

    summary_ar = (
        f"حزمة إجراءات {cycle_date}: "
        f"{len(actions)} إجراء ({critical} حرج) — "
        f"الوقت المقدر: {total_minutes} دقيقة"
    )
    summary_en = (
        f"Action pack {cycle_date}: "
        f"{len(actions)} actions ({critical} critical) — "
        f"estimated time: {total_minutes} minutes"
    )

    return FounderActionPack(
        tenant_id=tenant_id,
        cycle_date=cycle_date,
        actions=tuple(actions),
        total_actions=len(actions),
        critical_actions=critical,
        estimated_total_minutes=total_minutes,
        summary_ar=summary_ar,
        summary_en=summary_en,
        autonomous_execution=False,
        source_id=source_id,
    )
