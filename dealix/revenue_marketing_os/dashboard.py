"""
Growth Dashboard aggregator + Scale/Kill engine.

Reads the Revenue Marketing OS store, computes the dashboard sections
defined in the spec (Revenue by Offer / Channel / Campaign, pipeline
by ICP, reply rate by message, call rate by segment, proposal-to-win,
cost per qualified lead, revenue quality, partner-influenced revenue,
asset-influenced revenue), and produces a list of suggested scale,
pause, or kill decisions per campaign.

Decisions are always *suggested* — the Approval Center must clear
them before any external action takes place.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from dealix.revenue_marketing_os.attribution import summarize_attribution
from dealix.revenue_marketing_os.schemas import CampaignRecord, ScaleKillDecision
from dealix.revenue_marketing_os.scoring import (
    compute_revenue_quality_score,
    revenue_is_real,
)
from dealix.revenue_marketing_os.store import RevenueMarketingStore


def build_dashboard(store: RevenueMarketingStore) -> dict[str, Any]:
    """One-call dashboard snapshot."""
    revenue_rows = store.list_revenue()
    attribution_rows = store.list_attribution()
    leads = store.list_leads()
    touches = store.list_touches()
    campaigns = store.list_campaigns()
    offers = {o.id: o for o in store.list_offers()}

    # ── Verified revenue only ──────────────────────────────────────
    verified = [r for r in revenue_rows if revenue_is_real(r.model_dump())]
    verified_total = round(sum(r.amount_sar for r in verified), 2)
    pipeline_total = round(
        sum(r.amount_sar for r in revenue_rows if r.status in ("pipeline", "proposal_sent")),
        2,
    )

    by_offer: dict[str, float] = defaultdict(float)
    by_channel: dict[str, float] = defaultdict(float)
    by_campaign: dict[str, float] = defaultdict(float)
    for r in verified:
        if r.source_offer_id:
            by_offer[r.source_offer_id] += r.amount_sar
        by_channel[r.channel] += r.amount_sar
        if r.campaign_id:
            by_campaign[r.campaign_id] += r.amount_sar

    # ── Pipeline by ICP (via lead.icp_id) ──────────────────────────
    pipeline_by_icp: dict[str, int] = defaultdict(int)
    for lead in leads:
        if lead.status in ("mql", "sql", "discovery_booked", "discovery_done", "proposal_sent"):
            key = lead.icp_id or "unknown"
            pipeline_by_icp[key] += 1

    # ── Funnel ratios ──────────────────────────────────────────────
    status_counts: dict[str, int] = defaultdict(int)
    for lead in leads:
        status_counts[lead.status] += 1

    def safe_div(a: int, b: int) -> float:
        return round(a / b, 4) if b else 0.0

    funnel = {
        "lead_to_mql": safe_div(
            status_counts.get("mql", 0)
            + status_counts.get("sql", 0)
            + status_counts.get("discovery_booked", 0)
            + status_counts.get("discovery_done", 0)
            + status_counts.get("proposal_sent", 0)
            + status_counts.get("closed_won", 0),
            max(1, sum(status_counts.values())),
        ),
        "sql_to_call": safe_div(
            status_counts.get("discovery_booked", 0)
            + status_counts.get("discovery_done", 0)
            + status_counts.get("proposal_sent", 0)
            + status_counts.get("closed_won", 0),
            max(1, status_counts.get("sql", 0)
                + status_counts.get("discovery_booked", 0)
                + status_counts.get("discovery_done", 0)
                + status_counts.get("proposal_sent", 0)
                + status_counts.get("closed_won", 0)),
        ),
        "call_to_proposal": safe_div(
            status_counts.get("proposal_sent", 0)
            + status_counts.get("closed_won", 0),
            max(
                1,
                status_counts.get("discovery_done", 0)
                + status_counts.get("proposal_sent", 0)
                + status_counts.get("closed_won", 0),
            ),
        ),
        "proposal_to_win": safe_div(
            status_counts.get("closed_won", 0),
            max(1, status_counts.get("proposal_sent", 0) + status_counts.get("closed_won", 0)),
        ),
    }

    # ── Reply rate by message (touch outcome = "inbound_reply") ────
    outbound_by_msg: dict[str, int] = defaultdict(int)
    replies_by_msg: dict[str, int] = defaultdict(int)
    for t in touches:
        if t.touch_type == "outbound_sent_manual":
            outbound_by_msg[t.message_variant or "default"] += 1
        if t.touch_type == "inbound_reply":
            replies_by_msg[t.message_variant or "default"] += 1
    reply_rate_by_message = {
        msg: round(replies_by_msg.get(msg, 0) / sent, 4)
        for msg, sent in outbound_by_msg.items()
        if sent > 0
    }

    # ── Revenue quality ────────────────────────────────────────────
    qualities: list[int] = []
    for r in verified:
        score, _ = compute_revenue_quality_score(r.model_dump())
        qualities.append(score)
    avg_quality = round(sum(qualities) / len(qualities), 2) if qualities else 0.0

    # ── Asset / Partner influenced revenue ─────────────────────────
    asset_influenced = 0.0
    partner_influenced = 0.0
    agent_influenced = 0.0
    for a in attribution_rows:
        if a.asset_ids:
            asset_influenced += a.amount_sar
        if a.partner_ids:
            partner_influenced += a.amount_sar
        if a.agent_ids:
            agent_influenced += a.amount_sar

    # ── Red flags ──────────────────────────────────────────────────
    red_flags: list[str] = []
    if sum(status_counts.values()) > 0 and status_counts.get("closed_won", 0) == 0:
        red_flags.append("leads_without_wins")
    if (
        sum(t.touch_type == "outbound_sent_manual" for t in touches) > 0
        and sum(t.touch_type == "inbound_reply" for t in touches) == 0
    ):
        red_flags.append("outbound_without_replies")
    if revenue_rows and not verified:
        red_flags.append("revenue_without_verification")

    return {
        "schema_version": 1,
        "totals": {
            "verified_revenue_sar": verified_total,
            "pipeline_sar": pipeline_total,
            "leads": len(leads),
            "campaigns": len(campaigns),
            "verified_revenue_records": len(verified),
            "avg_revenue_quality_score": avg_quality,
        },
        "revenue_by_offer": {k: round(v, 2) for k, v in by_offer.items()},
        "revenue_by_channel": {k: round(v, 2) for k, v in by_channel.items()},
        "revenue_by_campaign": {k: round(v, 2) for k, v in by_campaign.items()},
        "pipeline_by_icp": dict(pipeline_by_icp),
        "reply_rate_by_message": reply_rate_by_message,
        "funnel": funnel,
        "asset_influenced_revenue_sar": round(asset_influenced, 2),
        "partner_influenced_revenue_sar": round(partner_influenced, 2),
        "agent_influenced_revenue_sar": round(agent_influenced, 2),
        "attribution_summary": summarize_attribution(attribution_rows),
        "red_flags": red_flags,
        "offers_registered": len(offers),
    }


# ── Scale / Kill engine ───────────────────────────────────────────


def evaluate_campaign(
    campaign: CampaignRecord, *, store: RevenueMarketingStore
) -> ScaleKillDecision:
    """
    Apply the campaign's own ``scale_rule`` / ``kill_rule`` against
    real funnel metrics. Returns a suggested ``ScaleKillDecision``;
    the founder approves it before any external action.
    """
    leads = store.list_leads(campaign_id=campaign.id, limit=10_000)
    revenue = [r for r in store.list_revenue() if r.campaign_id == campaign.id]
    verified_revenue = [r for r in revenue if revenue_is_real(r.model_dump())]
    targeted = len(leads)
    paid_diagnostics = sum(1 for r in verified_revenue if r.amount_sar > 0)
    qualified_replies = sum(
        1 for lead in leads if lead.status in ("mql", "sql", "discovery_booked", "discovery_done")
    )

    metrics = {
        "targeted_accounts": float(targeted),
        "qualified_replies": float(qualified_replies),
        "paid_diagnostics": float(paid_diagnostics),
        "verified_revenue_sar": round(sum(r.amount_sar for r in verified_revenue), 2),
    }

    # Defaults from the spec: scale ≥3 paid from 100 targeted; kill 0 replies from 100.
    if (
        targeted >= campaign.target_accounts
        and paid_diagnostics >= 3
    ):
        return ScaleKillDecision(
            campaign_id=campaign.id,
            decision="scale",
            reason_ar="بلغت الحملة العتبة: 3 صفقات مدفوعة على الأقل من العملاء المستهدفين.",
            reason_en="Campaign hit scale threshold: ≥3 paid conversions from targeted accounts.",
            metrics_snapshot=metrics,
            next_action="Increase budget/sequence reach and replicate winning message variant.",
        )

    if targeted >= campaign.target_accounts and qualified_replies == 0:
        return ScaleKillDecision(
            campaign_id=campaign.id,
            decision="kill",
            reason_ar="لا يوجد ردود مؤهلة بعد استهداف العدد المخطط.",
            reason_en="Zero qualified replies after the planned account target was reached.",
            metrics_snapshot=metrics,
            next_action="Pause sends, reposition the offer, and re-test message angle.",
        )

    if targeted >= campaign.target_accounts // 2 and paid_diagnostics == 0:
        return ScaleKillDecision(
            campaign_id=campaign.id,
            decision="pause",
            reason_ar="نصف الاستهداف بدون تحويلات مدفوعة — توقف لإعادة التقييم.",
            reason_en="Halfway to target without paid conversions — pause and reassess.",
            metrics_snapshot=metrics,
            next_action="Run a 5-account test with a new message angle before resuming.",
        )

    return ScaleKillDecision(
        campaign_id=campaign.id,
        decision="hold",
        reason_ar="الحملة لم تبلغ بعد عتبة القرار.",
        reason_en="Campaign has not yet reached the decision threshold.",
        metrics_snapshot=metrics,
        next_action="Continue current cadence and re-evaluate at the next checkpoint.",
    )
