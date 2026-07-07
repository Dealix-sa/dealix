"""Weekly proof pack — evidence-based, no fabricated metrics.

All numbers come from the store's own counts (companies scored, drafts,
approvals). Nothing is invented; where a value is unknown it is omitted rather
than guessed.
"""

from __future__ import annotations

from collections import Counter
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

from dealix.opportunity_graph.schemas import ProofPack
from dealix.opportunity_graph.store import OpportunityGraphStore, get_store, uid


def _period_label(days: int) -> str:
    end = date.today()
    start = end - timedelta(days=days)
    return f"{start.isoformat()}..{end.isoformat()}"


def build_weekly_proof_pack(
    *,
    store: OpportunityGraphStore | None = None,
    client_id: str = "dealix_internal",
    days: int = 7,
) -> ProofPack:
    store = store or get_store()
    companies = store.load_companies()
    drafts = store.load_drafts()
    approvals = store.load_approvals()

    sectors = Counter(c.sector for c in companies if c.sector)
    top_sectors = [f"{name} ({count})" for name, count in sectors.most_common(5)]

    approved = sum(1 for d in drafts if d.approval_status == "approved")
    rejected = sum(1 for d in drafts if d.approval_status == "rejected")
    pending = sum(1 for d in drafts if d.approval_status == "pending")
    sent_manual = sum(1 for d in drafts if d.sent_at is not None)

    decisions = [
        f"{a.get('decision', a.get('kind'))} on {a.get('company_id','')}"
        for a in approvals[-10:]
    ]

    metrics = {
        "companies_scored": len(companies),
        "hot": sum(1 for c in companies if c.score_class == "hot"),
        "warm": sum(1 for c in companies if c.score_class == "warm"),
        "outreach_drafts_created": len(drafts),
        "drafts_approved": approved,
        "drafts_rejected": rejected,
        "drafts_pending": pending,
        "manual_sends_recorded": sent_manual,
    }

    return ProofPack(
        id=uid("proof"),
        client_id=client_id,
        period=_period_label(days),
        before_state="Scattered, un-scored target list with no approval trail.",
        actions_taken=[
            "Scored and segmented the seed company set deterministically.",
            "Generated approval-ready outreach drafts (no sends).",
            "Maintained an append-only approval/decision audit log.",
        ],
        evidence_links=[
            "data/opportunity_graph/opportunities.json",
            "data/opportunity_graph/outreach_drafts.json",
            "data/opportunity_graph/approvals.json",
            "reports/opportunity_command/daily/",
        ],
        metrics=metrics,
        decisions=decisions,
        next_steps=[
            "Clear the pending approval queue with the founder.",
            "Add fresh authorized seed rows and re-score.",
            f"Prioritize top sectors: {', '.join(top_sectors) or 'n/a'}.",
        ],
        acceptance_status="draft",
    )


def render_proof_pack_markdown(pack: ProofPack) -> str:
    lines = [
        f"# Dealix Weekly Proof Pack — {pack.period}",
        "",
        f"- Client: `{pack.client_id}`",
        f"- Acceptance status: **{pack.acceptance_status}**",
        "",
        "## Before state",
        "",
        pack.before_state,
        "",
        "## Actions taken",
        "",
        *[f"- {a}" for a in pack.actions_taken],
        "",
        "## Metrics (from store counts — no estimates)",
        "",
        "| Metric | Value |",
        "|---|---|",
        *[f"| {k} | {v} |" for k, v in pack.metrics.items()],
        "",
        "## Recent decisions (audit log)",
        "",
        *([f"- {d}" for d in pack.decisions] or ["_No decisions logged yet._"]),
        "",
        "## Evidence",
        "",
        *[f"- `{link}`" for link in pack.evidence_links],
        "",
        "## Next steps",
        "",
        *[f"- {s}" for s in pack.next_steps],
        "",
        "---",
        "",
        "_No fabricated metrics. Values are counts from the opportunity graph store. "
        "Outreach remains draft-only until explicit founder approval._",
        "",
    ]
    return "\n".join(lines)


def _weekly_dir() -> Path:
    root = Path(__file__).resolve().parents[3]
    return root / "reports" / "opportunity_command" / "weekly"


def write_weekly_proof_pack(
    *,
    store: OpportunityGraphStore | None = None,
    client_id: str = "dealix_internal",
    days: int = 7,
) -> Path:
    pack = build_weekly_proof_pack(store=store, client_id=client_id, days=days)
    out_dir = _weekly_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{date.today().isoformat()}_proof_pack.md"
    path.write_text(render_proof_pack_markdown(pack), encoding="utf-8")
    return path
