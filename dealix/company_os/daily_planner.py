"""Daily planner for the founder-first Company OS run."""

from __future__ import annotations

from typing import Any

from dealix.execution.action_queue import build_action_queue
from dealix.execution.approval_center import build_approval_items
from dealix.opportunity_graph.graph_store import seed_dealix_opportunities
from dealix.proof.proof_ledger import build_proof_log

from .company_brain import CompanyBrain


def build_drafts(opportunities: list[dict[str, Any]], brain: CompanyBrain) -> list[dict[str, Any]]:
    drafts: list[dict[str, Any]] = []
    for index, opp in enumerate(opportunities, start=1):
        cta = "Would it be useful if I send a one-page snapshot?"
        if opp["vertical"] in {"clinics", "training_centers", "b2b_services"}:
            body = (
                f"السلام عليكم، لاحظت أن {opp['company_name']} قد تستفيد من ترتيب المتابعة والفرص اليومية. "
                f"Dealix يساعد الفريق يحدد من نتابع ولماذا، ويجهز رسائل وعروض وتقارير للموافقة قبل أي تواصل خارجي. "
                "هل يناسب أرسل نموذج صفحة واحدة؟"
            )
            channel = "linkedin_or_email_manual"
        else:
            body = (
                f"Hi, I am based in Riyadh and noticed a potential Saudi market access angle for {opp['company_name']}. "
                f"Dealix prepares qualified opportunities, partner mapping, outreach drafts, and proof reports while keeping external action approval-first. {cta}"
            )
            channel = "email_or_linkedin_manual"
        drafts.append(
            {
                "draft_id": f"draft-{index:03d}",
                "opportunity_id": opp["id"],
                "company_name": opp["company_name"],
                "channel": channel,
                "subject": f"{brain.name}: {opp['offer_match']} idea for {opp['company_name']}",
                "body": body,
                "status": "draft_pending_founder_approval",
                "external_action_enabled": False,
            }
        )
    return drafts


def build_daily_company_os_plan(*, brain: CompanyBrain, limit: int = 50) -> dict[str, Any]:
    graph = seed_dealix_opportunities(limit=limit)
    opportunities = sorted(graph["opportunities"], key=lambda item: item["score"], reverse=True)
    drafts = build_drafts(opportunities, brain)
    actions = build_action_queue(opportunities)
    approvals = build_approval_items(actions)
    proof = build_proof_log(opportunities=opportunities, drafts=drafts, approvals=approvals)
    return {
        "client": brain.to_dict(),
        "opportunity_graph": graph,
        "top_opportunities": opportunities,
        "drafts": drafts,
        "actions": actions,
        "approvals": approvals,
        "proof_log": proof,
        "safety": {
            "mode": "draft-only",
            "external_action_enabled": False,
            "live_outbound_enabled": False,
            "payment_capture_enabled": False,
            "production_mutation_enabled": False,
        },
    }
