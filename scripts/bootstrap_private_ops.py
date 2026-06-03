#!/usr/bin/env python3
"""Bootstrap the dealix-ops-private/ working tree.

Creates the canonical folder + CSV layout described in
DEALIX_FINAL_REPO_TREE.md. Idempotent: existing files are NOT overwritten
unless --force is passed.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


CSV_HEADERS: dict[str, str] = {
    "pipeline/pipeline_tracker.csv": "company,sector,contact,stage,priority,next_action,last_touch,notes\n",
    "revenue/revenue_action_log.csv": "date,lead_or_client,action,type,status,next_action,evidence\n",
    "revenue/cash_collected.csv": "date,client,offer,amount_sar,payment_method,status,notes\n",
    "revenue/pipeline_value.csv": "company,offer,stage,deal_value_sar,probability,weighted_value,next_action\n",
    "revenue/mrr_tracker.csv": "client,plan,monthly_amount_sar,status,start_date,next_renewal,notes\n",
    "finance/expenses.csv": "date,category,description,amount_sar,recurring,notes\n",
    "finance/unit_economics.csv": "client,offer,revenue_sar,direct_cost_sar,gross_margin_sar,hours_invested,effective_hourly_sar,notes\n",
    "finance/discount_log.csv": "date,client,offer,list_price_sar,discounted_price_sar,reason,approved_by\n",
    "trust/approval_log.csv": "date,item,type,risk_level,decision,approved_by,evidence\n",
    "trust/claim_review_log.csv": "date,claim,channel,proof_level,decision,approved_by,notes\n",
    "trust/risk_register.csv": "date,risk,severity,likelihood,owner,mitigation,status\n",
    "trust/redaction_log.csv": "date,source,target,reason,approved_by\n",
    "icp/icp_scorecard.csv": "sector,lead_count,dms,replies,samples,proposals,paid,fit_score,decision,next_action\n",
    "acquisition/source_performance.csv": "source,leads_found,qualified,contacted,replies,samples,proposals,paid,notes\n",
    "acquisition/message_performance.csv": "message_name,sector,dms_sent,replies,positive_replies,samples,proposals,paid,notes\n",
    "sales/proposal_tracker.csv": "date,client,offer,amount_sar,status,follow_up_date,decision_maker,next_action,notes\n",
    "delivery/sample_quality_log.csv": "date,prospect,sector,sample_path,quality_score,status,next_action\n",
    "delivery/qa_score_log.csv": "date,client,deliverable,score,notes\n",
    "client_success/retention_tracker.csv": "client,start_date,status,renewals,churn_reason,notes\n",
    "productization/candidates.csv": "workflow,frequency,manual_time_hours,automation_value,priority,owner,notes\n",
    "people/delegation_log.csv": "date,task,from,to,scope,status,notes\n",
    "people/contractor_tracker.csv": "contractor,role,start_date,scope,access_level,status,notes\n",
    "people/access_log.csv": "date,actor,resource,access_change,approved_by\n",
    "partners/partner_pipeline.csv": "partner,type,stage,owner,referral_terms,next_action,notes\n",
    "partners/partner_tracker.csv": "partner,type,stage,owner,referral_terms,leads_referred,leads_won,notes\n",
    "evidence/execution_evidence_ledger.csv": "date,system,evidence_type,evidence_path,description,status,next_action\n",
    "business_audit/score_history.csv": "date,score,top_action,notes\n",
    "metrics_history/weekly_metrics.csv": "week_ending,leads,dms,replies,samples,proposals,cash_collected_sar,notes\n",
    "experiments/market_experiments.csv": "date,hypothesis,sector,offer,message_angle,metric,target,result,decision,next_action\n",
    "content/content_calendar.csv": "date,channel,title,status,proof_level,approval_required,notes\n",
    "content/published_log.csv": "date,channel,title,url_or_path,proof_level,result,notes\n",
    "content/content_pipeline_influence.csv": "date,asset,channel,leads_influenced,proposals_influenced,paid_influenced,notes\n",
}

MARKDOWN_TEMPLATES: dict[str, str] = {
    "OPERATING_INDEX.md": "# Dealix Ops Private Operating Index\n\nThis tree is private. Do not push to a public repo.\n",
    "content/proof_library.md": "# Proof Library (PRIVATE)\n\nApproved customer proofs and anonymized cases.\n",
    "content/content_ideas.md": "# Content Ideas (PRIVATE)\n\nRaw ideas before they enter the calendar.\n",
    "content/approved_claims.md": "# Approved Claims (PRIVATE)\n\nClaims approved by Trust workflow for external use.\n",
    "content/templates/founder_post.md": "# Founder Post Template (PRIVATE)\n\n- Hook:\n- Story:\n- Proof:\n- CTA:\n",
    "content/templates/case_study_outline.md": "# Case Study Outline (PRIVATE)\n\n- Client:\n- Problem:\n- Approach:\n- Outcome:\n- Proof level:\n",
    "founder/mission_control.md": "# Mission Control (PRIVATE)\n\nUpdated by `make mission-control`.\n",
    "founder/ceo_action_queue.md": "# CEO Action Queue (PRIVATE)\n\nUpdated by `make ceo-action-queue`.\n",
    "founder/control_tower_brief.md": "# Control Tower Brief (PRIVATE)\n\nUpdated by `make control-tower`.\n",
    "founder/founder_bottleneck_log.csv": "date,task,reason,delegation_target,status\n",
    "business_audit/ceo_business_score.md": "# CEO Business Score (PRIVATE)\n\nUpdated by `make business-score`.\n",
    "evidence/execution_assurance_report.md": "# Execution Assurance Report (PRIVATE)\n\nUpdated by `make assurance`.\n",
    "client_success/client_success_dashboard.md": "# Client Success Dashboard (PRIVATE)\n",
    "productization/repeated_workflows.md": "# Repeated Workflows (PRIVATE)\n",
    "productization/automation_backlog.md": "# Automation Backlog (PRIVATE)\n",
}

CLIENT_TEMPLATE_FILES: dict[str, str] = {
    "client_os.md": "# {client} - Client OS (PRIVATE)\n\n- Owner: Founder\n- Offer:\n- Start date:\n- Stage:\n",
    "intake.md": "# {client} - Intake (PRIVATE)\n\n- Goal:\n- Scope:\n- Constraints:\n- Success criteria:\n",
    "proposal.md": "# {client} - Proposal (PRIVATE)\n\n- Offer:\n- Price:\n- Terms:\n",
    "lead_table.csv": "lead_name,sector,contact,priority,notes\n",
    "delivery_report.md": "# {client} - Delivery Report (PRIVATE)\n\n- Highlights:\n- Caveats:\n- Next steps:\n",
    "qa_checklist.md": "# {client} - QA Checklist (PRIVATE)\n\n- Data accuracy:\n- Privacy:\n- Tone:\n- Clarity:\n- Score:\n",
    "handoff.md": "# {client} - Handoff (PRIVATE)\n\n- Recipients:\n- Channel:\n- Date:\n",
    "feedback.md": "# {client} - Feedback (PRIVATE)\n\n- Requested on:\n- Response:\n",
    "health_score.md": "# {client} - Health Score (PRIVATE)\n\n- Engagement:\n- Outcomes:\n- Risk:\n- Score:\n",
    "proof_approval.md": "# {client} - Proof Approval (PRIVATE)\n\n- What we want to share:\n- Approved by client:\n- Trust workflow approval:\n",
    "renewal.md": "# {client} - Renewal (PRIVATE)\n\n- Trigger date:\n- Offer:\n- Decision:\n",
}


def write_if_missing(path: Path, content: str, force: bool) -> str:
    if path.exists() and not force:
        return "skip"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return "write"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="../dealix-ops-private", help="Private ops root")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    root.mkdir(parents=True, exist_ok=True)

    actions = {"write": 0, "skip": 0}

    for rel, header in CSV_HEADERS.items():
        result = write_if_missing(root / rel, header, args.force)
        actions[result] += 1

    for rel, content in MARKDOWN_TEMPLATES.items():
        result = write_if_missing(root / rel, content, args.force)
        actions[result] += 1

    template_dir = root / "clients" / "_template"
    for rel, content in CLIENT_TEMPLATE_FILES.items():
        result = write_if_missing(template_dir / rel, content.replace("{client}", "_template"), args.force)
        actions[result] += 1

    # Top-level operating index + .gitignore for the private tree.
    gitignore = root / ".gitignore"
    if not gitignore.exists():
        gitignore.write_text("exports/\n*.log\n.DS_Store\n", encoding="utf-8")
        actions["write"] += 1

    print(f"Private ops bootstrap @ {root}")
    print(f"  written: {actions['write']}")
    print(f"  skipped: {actions['skip']}")
    print("PASS: private ops bootstrap complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
