"""Deterministic strategic planning for multi-department commercial relationships."""

from __future__ import annotations

from .contracts import (
    ActionEnvelope,
    ActionMode,
    Channel,
    Department,
    LifecycleStage,
    MeetingPlan,
    ObjectiveType,
    OfferType,
    PermissionStatus,
    RelationshipContext,
    RelationshipType,
    RiskLevel,
    StrategicOffer,
    StrategicRecommendation,
    ValueExchange,
)


_OFFER_TITLES = {
    OfferType.OPPORTUNITY_SNAPSHOT: "Saudi Opportunity Snapshot",
    OfferType.REVENUE_PROOF_SPRINT: "Revenue Proof Sprint",
    OfferType.REVENUE_COMMAND_PILOT: "Revenue Command Pilot",
    OfferType.SAUDI_MARKET_ACCESS_SPRINT: "Saudi Market Access Sprint",
    OfferType.B2G_READINESS_SPRINT: "B2G Readiness Sprint",
    OfferType.PARTNER_DISTRIBUTOR_DESK: "Partner / Distributor Desk",
    OfferType.CO_MARKETING_SPRINT: "Co-Marketing Evidence Sprint",
    OfferType.SERVICE_EXCHANGE_PILOT: "Service Exchange Pilot",
    OfferType.AI_COMPANY_OS_SETUP: "AI Company OS Setup",
    OfferType.CUSTOMER_SUCCESS_REVIEW: "Customer Success and Expansion Review",
}


def _offer_for(context: RelationshipContext) -> StrategicOffer:
    objective = context.objective.objective_type

    if objective is ObjectiveType.REVENUE:
        offer_type = OfferType.REVENUE_PROOF_SPRINT
        exchange = ValueExchange(
            tenant_gives=("bounded revenue-leak diagnosis", "prioritized action plan", "proof-pack format"),
            tenant_receives=("paid pilot", "measurable business evidence", "retainer decision signal"),
            counterparty_gives=("approved data access", "process owner time", "pilot payment"),
            counterparty_receives=("diagnosis", "next-best actions", "reviewable proof"),
            cash_component_sar=499,
            assumptions=("scope and price remain draft until approval",),
        )
        scope = ("diagnose one commercial bottleneck", "prepare a bounded action plan", "define proof criteria")
        proof = ("approved scope", "source-backed diagnosis", "payment evidence", "delivery evidence")
    elif objective in {ObjectiveType.STRATEGIC_PARTNERSHIP, ObjectiveType.CHANNEL_GROWTH}:
        offer_type = OfferType.PARTNER_DISTRIBUTOR_DESK
        exchange = ValueExchange(
            tenant_gives=("qualified opportunity intelligence", "joint offer design", "approval-first operating workflow"),
            tenant_receives=("distribution access", "warm introductions", "implementation or referral capacity"),
            counterparty_gives=("market reach", "domain credibility", "qualified introductions"),
            counterparty_receives=("commercial operating layer", "joint pipeline visibility", "proof-backed proposals"),
            assumptions=("no exclusivity or commission commitment without approval",),
        )
        scope = ("map mutual strengths", "design one joint offer", "define referral or channel workflow")
        proof = ("partner capability evidence", "joint ICP", "approved value exchange", "tracked introductions")
    elif objective is ObjectiveType.CO_MARKETING:
        offer_type = OfferType.CO_MARKETING_SPRINT
        exchange = ValueExchange(
            tenant_gives=("source-backed market insight", "campaign concept", "measurement plan"),
            tenant_receives=("audience access", "co-brand distribution", "qualified demand signals"),
            counterparty_gives=("channel reach", "content contribution", "campaign distribution"),
            counterparty_receives=("commercial intelligence", "co-branded asset", "measurable campaign learning"),
            assumptions=("public claims and publication require separate approval",),
        )
        scope = ("select one shared audience", "build one evidence-led campaign", "measure qualified engagement")
        proof = ("source citations", "approved co-brand copy", "distribution log", "campaign outcome metrics")
    elif objective is ObjectiveType.SERVICE_EXCHANGE:
        offer_type = OfferType.SERVICE_EXCHANGE_PILOT
        exchange = ValueExchange(
            tenant_gives=("commercial diagnosis", "opportunity prioritization", "approval workflow setup"),
            tenant_receives=("complementary specialist service", "implementation capacity", "joint case-study option"),
            counterparty_gives=("defined service capacity", "named owner", "delivery evidence"),
            counterparty_receives=("defined Dealix service package", "commercial operating support", "proof framework"),
            cash_component_sar=None,
            assumptions=("both sides must define equivalent scope and acceptance criteria",),
        )
        scope = ("define both service scopes", "agree acceptance criteria", "run a limited mutual-value pilot")
        proof = ("two-sided scope", "owner approvals", "delivery evidence from both parties", "no implied revenue claim")
    elif objective is ObjectiveType.MARKET_ENTRY:
        offer_type = OfferType.SAUDI_MARKET_ACCESS_SPRINT
        exchange = ValueExchange(
            tenant_gives=("Saudi opportunity map", "partner shortlist", "entry-risk analysis"),
            tenant_receives=("paid market-access engagement", "local proof", "follow-on operating mandate"),
            counterparty_gives=("product context", "target criteria", "decision-maker availability"),
            counterparty_receives=("source-backed market map", "partner paths", "next-entry actions"),
            assumptions=("no government access, tender win, or market outcome is promised",),
        )
        scope = ("define entry thesis", "rank companies and partner paths", "prepare first-meeting strategy")
        proof = ("source map", "assumption register", "ranked partner universe", "decision log")
    elif objective is ObjectiveType.B2G_READINESS:
        offer_type = OfferType.B2G_READINESS_SPRINT
        exchange = ValueExchange(
            tenant_gives=("readiness assessment", "evidence-gap map", "partner and procurement pathway"),
            tenant_receives=("paid readiness engagement", "proof asset", "implementation opportunity"),
            counterparty_gives=("capability files", "compliance evidence", "authorized stakeholder time"),
            counterparty_receives=("readiness score", "gap remediation plan", "reviewable procurement packet"),
            assumptions=("no government access, influence, or award is claimed",),
        )
        scope = ("assess readiness", "identify evidence gaps", "prepare a compliant pathway")
        proof = ("capability evidence", "gap register", "approved readiness packet", "source-backed pathway")
    elif objective in {ObjectiveType.RETENTION, ObjectiveType.EXPANSION}:
        offer_type = OfferType.CUSTOMER_SUCCESS_REVIEW
        exchange = ValueExchange(
            tenant_gives=("outcome review", "next-value roadmap", "operating improvement proposal"),
            tenant_receives=("renewal decision", "expansion signal", "new proof and referral options"),
            counterparty_gives=("usage and outcome feedback", "decision-maker review", "approved next priority"),
            counterparty_receives=("documented value", "risk remediation", "bounded next-phase options"),
            assumptions=("renewal and expansion terms remain uncommitted until approval",),
        )
        scope = ("review delivered outcomes", "identify risk and value gaps", "propose one next-value phase")
        proof = ("delivery evidence", "outcome metrics", "customer feedback", "approved next-phase scope")
    else:
        offer_type = OfferType.AI_COMPANY_OS_SETUP
        exchange = ValueExchange(
            tenant_gives=("commercial workflow design", "approval controls", "review command center blueprint"),
            tenant_receives=("implementation mandate", "operating data", "long-term platform relationship"),
            counterparty_gives=("process access", "owners", "approved integration scope"),
            counterparty_receives=("operating blueprint", "decision queues", "proof and review system"),
        )
        scope = ("map operating workflows", "define decision rights", "configure a controlled pilot")
        proof = ("approved process map", "decision matrix", "pilot acceptance criteria")

    return StrategicOffer(
        offer_type=offer_type,
        title=_OFFER_TITLES[offer_type],
        value_exchange=exchange,
        scope=scope,
        proof_requirements=proof,
        success_metric=context.objective.success_metric,
        term_notes=("all terms are draft-only until the authorized reviewer approves them",),
        assumptions=tuple(context.constraints),
    )


def _channel_for(context: RelationshipContext) -> Channel:
    objective = context.objective.objective_type
    if objective in {
        ObjectiveType.STRATEGIC_PARTNERSHIP,
        ObjectiveType.SERVICE_EXCHANGE,
        ObjectiveType.CO_MARKETING,
        ObjectiveType.CHANNEL_GROWTH,
    }:
        return Channel.MEETING
    if objective in {ObjectiveType.RETENTION, ObjectiveType.EXPANSION}:
        return Channel.MEETING
    return Channel.EMAIL


def _posture_for(context: RelationshipContext) -> str:
    if context.objective.objective_type is ObjectiveType.SERVICE_EXCHANGE:
        return "Balance both scopes, owners, timelines, and acceptance criteria before discussing equivalence."
    if context.objective.objective_type in {
        ObjectiveType.STRATEGIC_PARTNERSHIP,
        ObjectiveType.CHANNEL_GROWTH,
        ObjectiveType.CO_MARKETING,
    }:
        return "Lead with mutual value and a reversible pilot; do not grant exclusivity, discounts, or public claims first."
    if context.objective.objective_type in {ObjectiveType.RETENTION, ObjectiveType.EXPANSION}:
        return "Start from evidenced outcomes and unresolved risk before proposing expansion."
    return "Lead with a bounded diagnosis and proof path; protect scope, price, and unsupported claims."


def recommend_strategy(context: RelationshipContext) -> StrategicRecommendation:
    """Produce an evidence-first strategy without authorizing external execution."""

    offer = _offer_for(context)
    if context.permission_status is PermissionStatus.OPTED_OUT:
        channel = Channel.INTERNAL
        requires_approval = False
        next_move = "Record suppression and stop external action."
    elif not context.contact_permission_confirmed:
        channel = Channel.INTERNAL
        requires_approval = False
        next_move = "Verify permission, an existing relationship, or a warm introduction before drafting outreach."
    else:
        channel = _channel_for(context)
        requires_approval = True
        next_move = "Prepare a bounded outreach or meeting proposal for authorized review."

    objections = ["priority and timing", "proof quality", "scope and ownership"]
    if context.objective.objective_type is ObjectiveType.SERVICE_EXCHANGE:
        objections.extend(["unequal value exchange", "unclear acceptance criteria"])
    elif context.objective.objective_type in {
        ObjectiveType.STRATEGIC_PARTNERSHIP,
        ObjectiveType.CHANNEL_GROWTH,
    }:
        objections.extend(["channel conflict", "commercial terms", "exclusivity"])
    elif context.objective.objective_type is ObjectiveType.CO_MARKETING:
        objections.extend(["brand approval", "audience quality", "claim substantiation"])

    return StrategicRecommendation(
        tenant_id=context.tenant_id,
        relationship_id=context.relationship_id,
        department=context.objective.department,
        objective_type=context.objective.objective_type,
        relationship_type=context.relationship_type,
        recommended_offer=offer,
        rationale=(
            f"priority_score={context.priority_score}",
            f"relationship_type={context.relationship_type.value}",
            f"objective={context.objective.objective_type.value}",
            f"permission={context.permission_status.value}",
        ),
        negotiation_posture=_posture_for(context),
        objections_to_expect=tuple(objections),
        red_lines=(
            "no guaranteed results",
            "no unsupported proof or access claim",
            "no live send, booking, price, contract, or payment without approval",
            "no exclusivity or public use of names without explicit approval",
        ),
        next_move=next_move,
        recommended_channel=channel,
        requires_approval=requires_approval,
    )


def build_action_envelope(
    context: RelationshipContext,
    recommendation: StrategicRecommendation,
) -> ActionEnvelope:
    """Turn a recommendation into an internal or approval-gated action card."""

    if context.tenant_id != recommendation.tenant_id:
        raise ValueError("context and recommendation must belong to the same tenant")

    if context.permission_status is PermissionStatus.OPTED_OUT:
        return ActionEnvelope(
            tenant_id=context.tenant_id,
            department=context.objective.department,
            relationship_id=context.relationship_id,
            account_id=context.account_id,
            contact_id=context.contact_id,
            action_type="suppression_review",
            action_mode=ActionMode.BLOCKED,
            channel=Channel.INTERNAL,
            summary_ar=f"إيقاف أي تواصل خارجي مع {context.account_name} وتأكيد suppression.",
            rationale="The relationship is opted out.",
            risk_level=RiskLevel.BLOCKED,
            proof_target="suppression_record_verified",
            evidence_refs=context.evidence_refs,
        )

    if not context.contact_permission_confirmed:
        return ActionEnvelope(
            tenant_id=context.tenant_id,
            department=context.objective.department,
            relationship_id=context.relationship_id,
            account_id=context.account_id,
            contact_id=context.contact_id,
            action_type="permission_research",
            action_mode=ActionMode.INTERNAL,
            channel=Channel.INTERNAL,
            summary_ar=f"تحقق من إذن التواصل أو اطلب warm introduction إلى {context.account_name}.",
            rationale="Research value cannot override missing permission.",
            risk_level=RiskLevel.LOW,
            proof_target="permission_or_warm_intro_recorded",
            evidence_refs=context.evidence_refs,
        )

    action_type = "partner_intro" if context.objective.objective_type in {
        ObjectiveType.STRATEGIC_PARTNERSHIP,
        ObjectiveType.CHANNEL_GROWTH,
        ObjectiveType.SERVICE_EXCHANGE,
        ObjectiveType.CO_MARKETING,
    } else "draft_email"
    summary = (
        f"مراجعة مقترح {recommendation.recommended_offer.title} لـ {context.account_name} "
        f"ضمن هدف {context.objective.title}."
    )
    draft_payload = {
        "purpose": context.objective.title,
        "relationship_type": context.relationship_type.value,
        "offer": recommendation.recommended_offer.to_dict(),
        "negotiation_posture": recommendation.negotiation_posture,
        "next_move": recommendation.next_move,
        "cta": "propose a short review meeting or ask permission to share the one-page proposal",
        "claims_status": "draft_only_evidence_required",
    }
    return ActionEnvelope(
        tenant_id=context.tenant_id,
        department=context.objective.department,
        relationship_id=context.relationship_id,
        account_id=context.account_id,
        contact_id=context.contact_id,
        action_type=action_type,
        action_mode=ActionMode.APPROVAL_REQUIRED,
        channel=recommendation.recommended_channel,
        summary_ar=summary,
        rationale="; ".join(recommendation.rationale),
        risk_level=RiskLevel.MEDIUM,
        proof_target="approved_external_action_and_outcome_recorded",
        draft_payload=draft_payload,
        evidence_refs=context.evidence_refs,
    )


def build_meeting_plan(
    context: RelationshipContext,
    recommendation: StrategicRecommendation,
) -> MeetingPlan:
    """Prepare meeting intelligence; it never books or invites participants."""

    exchange = recommendation.recommended_offer.value_exchange
    return MeetingPlan(
        tenant_id=context.tenant_id,
        relationship_id=context.relationship_id,
        account_id=context.account_id,
        department=context.objective.department,
        objective=f"Validate {context.objective.title} and agree a reversible next step.",
        agenda=(
            "Confirm both parties' current priorities and constraints.",
            "Validate the value-exchange hypothesis.",
            "Review the bounded offer, evidence, owners, and acceptance criteria.",
            "Choose the next action, owner, and approval path.",
        ),
        discovery_questions=(
            "What outcome is most valuable in the next 30-90 days?",
            "What evidence would make this worth approving?",
            "Who owns delivery, commercial approval, data, and follow-up?",
            "Which risks, policies, or conflicts could block the relationship?",
            f"Which of these values matter most: {', '.join(exchange.tenant_receives)}?",
        ),
        negotiation_plan=(
            recommendation.negotiation_posture,
            "Concede scope or sequence before price or strategic rights.",
            "Use a small pilot with explicit evidence and stop conditions.",
            *recommendation.red_lines,
        ),
        required_evidence=recommendation.recommended_offer.proof_requirements,
        participants=("authorized department owner", "counterparty decision owner"),
        proposed_slots=(),
    )
