"""Bootstrap the Dealix private ops directory.

Creates CSV ledgers, markdown operating files, and the client template
required by the Implementation Automation Pack. Lives outside the public
repo so customer data never leaks. Idempotent: never overwrites existing
files. Default target: ../dealix-ops-private (sibling of the public repo).
"""

from pathlib import Path
import argparse

CSV_FILES = {
    "pipeline/pipeline_tracker.csv": "company,sector,contact,stage,priority,next_action,last_touch,notes\n",
    "revenue/revenue_action_log.csv": "date,lead_or_client,action,type,status,next_action,evidence\n",
    "revenue/cash_collected.csv": "date,client,offer,amount_sar,payment_method,status,notes\n",
    "revenue/pipeline_value.csv": "company,offer,stage,deal_value_sar,probability,weighted_value,next_action\n",
    "revenue/mrr_tracker.csv": "client,plan,monthly_amount_sar,status,start_date,next_renewal,notes\n",
    "finance/expenses.csv": "date,category,description,amount_sar,recurring,notes\n",
    "finance/unit_economics.csv": "client,offer,price_sar,direct_cost_sar,founder_hours,delivery_hours,total_hours,gross_margin_estimate,effective_hourly_value,retainer_probability,decision\n",
    "finance/discount_log.csv": "date,client,offer,original_price_sar,discounted_price_sar,discount_percent,reason,scope_change,approved_by,result\n",
    "trust/approval_log.csv": "date,item,type,risk_level,decision,approved_by,evidence\n",
    "trust/claim_review_log.csv": "date,asset,claim,claim_type,evidence,decision,next_action\n",
    "trust/risk_register.csv": "date,risk,domain,likelihood,impact,severity,mitigation,status,owner\n",
    "trust/redaction_log.csv": "date,file,redacted_item,reason,reviewed_by,status\n",
    "evidence/execution_evidence_ledger.csv": "date,system,evidence_type,evidence_path,description,status,next_action\n",
    "business_audit/score_history.csv": "date,total_score,revenue_score,pipeline_score,finance_score,delivery_score,trust_score,learning_score,ceo_score,product_score,status,next_action\n",
    "icp/icp_scorecard.csv": "sector,lead_count,dms,replies,samples,proposals,paid,fit_score,decision,next_action\n",
    "acquisition/source_performance.csv": "source,leads_found,qualified,contacted,replies,samples,proposals,paid,notes\n",
    "acquisition/message_performance.csv": "message_name,sector,dms_sent,replies,positive_replies,samples,proposals,paid,notes\n",
    "sales/proposal_tracker.csv": "date,client,offer,amount_sar,status,follow_up_date,decision_maker,next_action,notes\n",
    "delivery/sample_quality_log.csv": "date,prospect,sector,sample_path,quality_score,status,next_action\n",
    "delivery/qa_score_log.csv": "date,client,icp_fit,evidence_quality,lead_relevance,outreach_usefulness,summary_clarity,trust_safety,next_action_clarity,total_score,status,notes\n",
    "client_success/retention_tracker.csv": "client,delivery_date,feedback_received,health_score,retainer_ask_sent,retainer_status,proof_status,next_action\n",
    "content/content_calendar.csv": "date,channel,pillar,title,status,evidence_path,approval_needed,next_action\n",
    "content/published_log.csv": "date,channel,title,url,pillar,evidence_path,result,notes\n",
    "content/content_pipeline_influence.csv": "date,content_title,channel,lead_or_client,influence_type,next_action,notes\n",
    "productization/candidates.csv": "date,workflow,pain,manual_frequency,evidence,client_demand,risk_level,decision,next_action\n",
    "people/delegation_log.csv": "date,task,from_owner,to_owner,delegation_level,qa_required,status,notes\n",
    "people/contractor_tracker.csv": "name,role,start_date,status,access_level,scorecard,weekly_output,quality_rating,next_action\n",
    "people/access_log.csv": "date,person,access_level,system_or_file,reason,approved_by,remove_date,status\n",
    "partners/partner_pipeline.csv": "date,partner,lead,sector,status,proposal_value,cash_collected,next_action\n",
    "partners/partner_tracker.csv": "partner,type,status,terms,leads,revenue,trust_rating,next_review\n",
    "experiments/market_experiments.csv": "date,hypothesis,sector,offer,message_angle,metric,target,result,decision,next_action\n",
}

MD_FILES = {
    "OPERATING_INDEX.md": "# Dealix Private Ops Operating Index\n\n",
    "founder/mission_control.md": "# Dealix Mission Control\n\n",
    "founder/ceo_action_queue.md": "# CEO Action Queue\n\n",
    "founder/weekly_war_room.md": "# Weekly CEO War Room\n\n",
    "founder/monthly_board_pack.md": "# Monthly Board Pack\n\n",
    "founder/personal_leverage_dashboard.md": "# Personal Leverage Dashboard\n\n",
    "learning/weekly_intelligence_review.md": "# Weekly Intelligence Review\n\n",
    "learning/company_memory.md": "# Company Memory\n\n",
    "pipeline/win_loss_log.md": "# Win/Loss Log\n\n",
    "trust/incident_log.md": "# Trust Incident Log\n\n",
    "trust/security_incident_log.md": "# Security Incident Log\n\n",
    "content/proof_library.md": "# Proof Library\n\n",
    "content/content_ideas.md": "# Content Ideas\n\n",
    "content/approved_claims.md": "# Approved Claims\n\n",
    "productization/repeated_workflows.md": "# Repeated Workflows\n\n",
    "productization/automation_backlog.md": "# Automation Backlog\n\n",
    "client_success/client_success_dashboard.md": "# Client Success Dashboard\n\n",
    "finance/capital_allocation_review.md": "# Capital Allocation Review\n\n",
}


def write_if_missing(root: Path, path: str, content: str) -> None:
    p = root / path
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        p.write_text(content, encoding="utf-8")
        print(f"created: {p}")
    else:
        print(f"exists:  {p}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-ops", default="../dealix-ops-private")
    args = parser.parse_args()
    root = Path(args.private_ops).resolve()
    root.mkdir(parents=True, exist_ok=True)
    for path, content in CSV_FILES.items():
        write_if_missing(root, path, content)
    for path, content in MD_FILES.items():
        write_if_missing(root, path, content)
    client_template = root / "clients/_template"
    client_template.mkdir(parents=True, exist_ok=True)
    template_files = {
        "client_os.md": "# Client Operating File\n\n",
        "intake.md": "# Client Intake\n\n",
        "proposal.md": "# Proposal\n\n",
        "kickoff.md": "# Kickoff\n\n",
        "research_notes.md": "# Research Notes\n\n",
        "lead_table.csv": "company,sector,website,buyer_title,why_relevant,priority,evidence,suggested_angle,source,notes\n",
        "outreach_pack.md": "# Outreach Pack\n\n",
        "delivery_report.md": "# Delivery Report\n\n",
        "qa_checklist.md": "# QA Checklist\n\n",
        "handoff.md": "# Handoff\n\n",
        "feedback.md": "# Feedback\n\n",
        "health_score.md": "# Health Score\n\n",
        "retainer_offer.md": "# Retainer Offer\n\n",
        "proof_approval.md": "# Proof Approval\n\n",
        "renewal.md": "# Renewal\n\n",
    }
    for path, content in template_files.items():
        write_if_missing(root, f"clients/_template/{path}", content)
    print(f"\nPASS: private ops bootstrapped at {root}")


if __name__ == "__main__":
    main()
