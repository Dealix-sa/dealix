"""Evidence-sequence validation, stage derivation, and conservative forecasting."""

from __future__ import annotations

from datetime import date, datetime

from .models import DealRecord, DealSnapshot, DealStage, NextAction, PortfolioMetrics

_STAGE_RANK: dict[DealStage, int] = {
    DealStage.RESEARCH_HOLD: 0,
    DealStage.NEW: 1,
    DealStage.CONTACTED: 2,
    DealStage.ENGAGED: 3,
    DealStage.PROPOSED: 4,
    DealStage.PAID: 5,
    DealStage.PROOF_DELIVERED: 6,
    DealStage.REFERRAL: 7,
    DealStage.LOST: 8,
}
STAGE_PROBABILITY: dict[DealStage, float] = {
    DealStage.RESEARCH_HOLD: 0.0,
    DealStage.NEW: 0.05,
    DealStage.CONTACTED: 0.15,
    DealStage.ENGAGED: 0.35,
    DealStage.PROPOSED: 0.60,
    DealStage.PAID: 1.0,
    DealStage.PROOF_DELIVERED: 1.0,
    DealStage.REFERRAL: 1.0,
    DealStage.LOST: 0.0,
}
STAGE_STALE_DAYS: dict[DealStage, int] = {
    DealStage.RESEARCH_HOLD: 14,
    DealStage.NEW: 3,
    DealStage.CONTACTED: 4,
    DealStage.ENGAGED: 5,
    DealStage.PROPOSED: 5,
    DealStage.PAID: 7,
    DealStage.PROOF_DELIVERED: 21,
    DealStage.REFERRAL: 30,
}
_EXTERNAL_EVIDENCE = {
    "message_sent_manual",
    "message_sent",
    "reply_received",
    "call_booked",
    "demo_booked",
    "invoice_sent",
}


def _parse_date(value: str) -> date | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
    except ValueError:
        return None


def _advance(current: DealStage, candidate: DealStage) -> DealStage:
    return candidate if _STAGE_RANK[candidate] > _STAGE_RANK[current] else current


def _days_since_touch(deal: DealRecord, today: date) -> tuple[int, list[str]]:
    raw = deal.last_touch_at or deal.created_at
    parsed = _parse_date(raw)
    if not raw:
        return 0, ["missing_touch_date"]
    if parsed is None:
        return 0, ["invalid_touch_date"]
    if parsed > today:
        return 0, ["future_touch_date"]
    return (today - parsed).days, []


def analyze_deal(deal: DealRecord, today: date) -> DealSnapshot:
    """Derive a trustworthy stage without allowing evidence to skip prerequisites."""

    stage = DealStage.NEW if deal.contact_permission_confirmed else DealStage.RESEARCH_HOLD
    anomalies: list[str] = []
    chronological_events = []
    for index, event in enumerate(deal.events):
        parsed = _parse_date(event.occurred_at)
        if parsed is None:
            anomalies.append(f"invalid_event_date:{event.event_type}")
            continue
        if parsed > today:
            anomalies.append(f"future_event_date:{event.event_type}")
            continue
        chronological_events.append((parsed, index, event))
    chronological_events.sort(key=lambda item: (item[0], item[1]))

    seen_invoice = False
    valid_payment = False
    proof_delivered = False
    close_ready = False
    lost = False

    for _, _, event in chronological_events:
        event_type = event.event_type
        if event_type == "lost":
            lost = True
            continue
        if event_type in _EXTERNAL_EVIDENCE and not deal.contact_permission_confirmed:
            anomalies.append(f"commercial_event_without_permission:{event_type}")
        if event_type in {"message_sent_manual", "message_sent"}:
            if deal.contact_permission_confirmed:
                stage = _advance(stage, DealStage.CONTACTED)
        elif event_type in {"reply_received", "call_booked", "demo_booked"}:
            if deal.contact_permission_confirmed:
                stage = _advance(stage, DealStage.ENGAGED)
        elif event_type == "invoice_sent":
            seen_invoice = True
            if deal.contact_permission_confirmed:
                stage = _advance(stage, DealStage.PROPOSED)
        elif event_type == "payment_received":
            if not seen_invoice:
                anomalies.append("payment_before_invoice")
            else:
                valid_payment = True
                stage = _advance(stage, DealStage.PAID)
        elif event_type == "proof_pack_delivered":
            if not valid_payment:
                anomalies.append("proof_before_valid_payment")
            else:
                proof_delivered = True
                stage = _advance(stage, DealStage.PROOF_DELIVERED)
        elif event_type == "closed_won":
            if valid_payment and proof_delivered:
                close_ready = True
            else:
                anomalies.append("closed_won_before_payment_and_proof")
        elif event_type in {"referral_requested", "referral_received"}:
            if proof_delivered:
                stage = _advance(stage, DealStage.REFERRAL)
            else:
                anomalies.append("referral_before_proof")

    if valid_payment and proof_delivered:
        close_ready = True
    if not deal.contact_permission_confirmed and not valid_payment and not lost:
        stage = DealStage.RESEARCH_HOLD
    if lost:
        stage = DealStage.LOST
        close_ready = False

    days_since_touch, touch_anomalies = _days_since_touch(deal, today)
    anomalies.extend(touch_anomalies)
    threshold = STAGE_STALE_DAYS.get(stage, 7)
    stalled = stage not in {DealStage.LOST, DealStage.REFERRAL} and days_since_touch > threshold

    return DealSnapshot(
        deal_id=deal.deal_id,
        account_name=deal.account_name,
        stage=stage,
        value_sar=deal.value_sar,
        contact_permission_confirmed=deal.contact_permission_confirmed,
        valid_payment=valid_payment,
        proof_delivered=proof_delivered,
        close_ready=close_ready,
        stalled=stalled,
        days_since_touch=days_since_touch,
        forecast_probability=STAGE_PROBABILITY[stage],
        anomalies=tuple(dict.fromkeys(anomalies)),
    )


def next_action(snapshot: DealSnapshot) -> NextAction:
    """Return the next internal/approval step without generating or sending copy."""

    if snapshot.stage == DealStage.LOST:
        key, rationale, approval = "archive_lost", "Deal is terminally lost.", False
    elif snapshot.anomalies:
        key, rationale, approval = "repair_evidence_chain", "; ".join(snapshot.anomalies), False
    elif not snapshot.contact_permission_confirmed:
        key, rationale, approval = (
            "obtain_permission_or_warm_intro",
            "Contact permission is not confirmed; scoring cannot override consent.",
            False,
        )
    elif snapshot.stage == DealStage.NEW:
        key, rationale, approval = "prepare_first_touch_draft", "Permitted lead has no recorded contact.", True
    elif snapshot.stage == DealStage.CONTACTED:
        key, rationale, approval = "prepare_follow_up_draft", "Contact exists; seek a qualified reply or meeting.", True
    elif snapshot.stage == DealStage.ENGAGED:
        key, rationale, approval = "prepare_scope_and_proposal", "Engagement exists; define a bounded offer.", True
    elif snapshot.stage == DealStage.PROPOSED:
        key, rationale, approval = "follow_up_payment_evidence", "Invoice is recorded; payment is not yet proven.", True
    elif snapshot.stage == DealStage.PAID:
        key, rationale, approval = "deliver_and_prepare_proof", "Valid payment exists; deliver the approved scope.", False
    elif snapshot.stage == DealStage.PROOF_DELIVERED:
        key, rationale, approval = "prepare_referral_or_retainer_review", "Proof is delivered; review expansion.", True
    else:
        key, rationale, approval = "review_relationship", "Referral/expansion relationship requires review.", False

    if snapshot.stalled:
        rationale = f"STALLED {snapshot.days_since_touch}d — {rationale}"
    return NextAction(
        deal_id=snapshot.deal_id,
        action_key=key,
        rationale=rationale,
        requires_approval=approval,
    )


def compute_portfolio(deals: list[DealRecord], today: date) -> tuple[list[DealSnapshot], PortfolioMetrics]:
    snapshots = [analyze_deal(deal, today) for deal in deals]
    recognized = sum(snapshot.value_sar for snapshot in snapshots if snapshot.valid_payment)
    open_pipeline = sum(
        snapshot.value_sar
        for snapshot in snapshots
        if not snapshot.valid_payment and snapshot.stage != DealStage.LOST
    )
    weighted = sum(
        snapshot.value_sar * snapshot.forecast_probability
        for snapshot in snapshots
        if not snapshot.valid_payment and snapshot.stage != DealStage.LOST
    )
    metrics = PortfolioMetrics(
        total_deals=len(snapshots),
        active_deals=sum(1 for item in snapshots if item.stage not in {DealStage.LOST, DealStage.REFERRAL}),
        lost_deals=sum(1 for item in snapshots if item.stage == DealStage.LOST),
        stalled_deals=sum(1 for item in snapshots if item.stalled),
        recognized_revenue_sar=recognized,
        open_pipeline_sar=open_pipeline,
        weighted_pipeline_sar=weighted,
        anomaly_count=sum(len(item.anomalies) for item in snapshots),
    )
    return snapshots, metrics
