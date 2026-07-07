"""Daily Saudi Opportunity Command Report — structured + markdown, draft-only."""

from __future__ import annotations

from datetime import UTC, date, datetime
from pathlib import Path

from dealix.opportunity_graph.schemas import DailyCommandReport, OpportunityCompany, OutreachDraft
from dealix.opportunity_graph.store import OpportunityGraphStore, get_store

_FOREIGN_SEGMENTS = {
    "foreign_saas_ai_entering_saudi",
    "foreign_supplier_needing_distributor",
}
_SAUDI_SEGMENTS = {
    "saudi_clinic_revenue_leak",
    "saudi_training_or_b2b_service_growth",
}
_PARTNER_SEGMENTS = {"rhq_vendor_or_partner_candidate", "foreign_supplier_needing_distributor"}


def _card(c: OpportunityCompany) -> dict:
    return {
        "id": c.id,
        "name": c.name,
        "sector": c.sector,
        "country": c.country,
        "segment": c.segment,
        "total_score": c.total_score,
        "score_class": c.score_class,
        "next_action": c.recommended_next_action,
    }


def build_daily_report(
    *,
    store: OpportunityGraphStore | None = None,
    report_date: str | None = None,
) -> DailyCommandReport:
    store = store or get_store()
    companies = sorted(store.load_companies(), key=lambda c: c.total_score, reverse=True)
    drafts = store.load_drafts()
    the_date = report_date or date.today().isoformat()

    ranked = [c for c in companies if c.score_class != "not_fit"]
    foreign = [c for c in ranked if c.segment in _FOREIGN_SEGMENTS]
    saudi = [c for c in ranked if c.segment in _SAUDI_SEGMENTS]
    partners = [c for c in ranked if c.segment in _PARTNER_SEGMENTS]
    b2g = [c for c in companies if c.segment == "b2g_readiness_candidate"]
    risky = [c for c in companies if c.trust_risk_score >= 6]

    pending = [d for d in drafts if d.approval_status == "pending"]
    approved = [d for d in drafts if d.approval_status == "approved"]

    decisions: list[str] = []
    if pending:
        decisions.append(f"Review {len(pending)} pending outreach draft(s) — approve, revise, or reject.")
    if b2g:
        decisions.append(f"Decide whether to pursue {len(b2g)} B2G readiness candidate(s).")
    if risky:
        decisions.append(f"Confirm trust/consent posture for {len(risky)} flagged company(ies) before any outreach.")

    tomorrow = [
        "Import new seed rows into data/opportunity_graph/companies.seed.csv (authorized sources only).",
        "Re-run run_daily_opportunity_targeting.py --mode draft-only.",
        "Clear the pending approval queue with the founder.",
    ]

    return DailyCommandReport(
        date=the_date,
        total_companies_scored=len(companies),
        top_opportunities=[_card(c) for c in ranked[:10]],
        top_foreign_entry=[_card(c) for c in foreign[:5]],
        top_saudi_recovery=[_card(c) for c in saudi[:5]],
        top_partner_candidates=[_card(c) for c in partners[:5]],
        b2g_watchlist=[_card(c) for c in b2g[:10]],
        top_followups=[_card(c) for c in ranked if c.status == "contacted_manual"][:5],
        risky_items=[_card(c) for c in risky[:10]],
        approved_drafts=len(approved),
        pending_approvals=len(pending),
        recommended_decisions=decisions,
        tomorrow_actions=tomorrow,
        proof_summary=(
            f"{len(companies)} scored · {len(ranked)} in play · "
            f"{len(pending)} drafts pending approval · draft-only (no sends)."
        ),
    )


def _section(title: str, cards: list[dict]) -> list[str]:
    lines = [f"## {title}", ""]
    if not cards:
        lines.append("_None this cycle._")
        lines.append("")
        return lines
    lines.append("| Company | Sector | Country | Segment | Score | Next action |")
    lines.append("|---|---|---|---|---|---|")
    for c in cards:
        lines.append(
            f"| {c['name']} | {c.get('sector','')} | {c.get('country','')} | "
            f"{c['segment']} | {c['total_score']} ({c['score_class']}) | {c.get('next_action','')} |"
        )
    lines.append("")
    return lines


def render_daily_markdown(report: DailyCommandReport) -> str:
    lines: list[str] = [
        f"# Dealix Daily Saudi Opportunity Command Report — {report.date}",
        "",
        "> Draft-only. No message is sent without explicit founder approval.",
        "",
        "## 1. Executive summary",
        "",
        f"- Companies scored: **{report.total_companies_scored}**",
        f"- Drafts pending approval: **{report.pending_approvals}**",
        f"- Approved drafts (awaiting manual send): **{report.approved_drafts}**",
        f"- {report.proof_summary}",
        "",
    ]
    lines += _section("2. Top 10 opportunities today", report.top_opportunities)
    lines += _section("3. Top 5 foreign market-entry targets", report.top_foreign_entry)
    lines += _section("4. Top 5 Saudi revenue-recovery targets", report.top_saudi_recovery)
    lines += _section("5. Top 5 partner/distributor candidates", report.top_partner_candidates)
    lines += _section("6. B2G readiness watchlist", report.b2g_watchlist)
    lines += _section("7. Follow-ups in flight", report.top_followups)
    lines += _section("8. Risk & trust warnings", report.risky_items)

    lines += ["## 9. Recommended founder decisions", ""]
    if report.recommended_decisions:
        lines += [f"- {d}" for d in report.recommended_decisions]
    else:
        lines.append("_No decisions required._")
    lines.append("")

    lines += ["## 10. Tomorrow's action queue", ""]
    lines += [f"- {a}" for a in report.tomorrow_actions]
    lines += [
        "",
        "---",
        "",
        "_Safety: outreach drafts are queued for human approval. Live WhatsApp/email/SMS "
        "sending remains disabled (OUTBOUND_MODE=draft_only)._",
        "",
    ]
    return "\n".join(lines)


def _daily_dir() -> Path:
    root = Path(__file__).resolve().parents[3]
    return root / "reports" / "opportunity_command" / "daily"


def write_daily_report(
    *,
    store: OpportunityGraphStore | None = None,
    report_date: str | None = None,
) -> Path:
    report = build_daily_report(store=store, report_date=report_date)
    out_dir = _daily_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{report.date}.md"
    path.write_text(render_daily_markdown(report), encoding="utf-8")
    return path
