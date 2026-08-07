"""Master verification for Dealix Ultimate Commercial OS.

Usage:
    python3 scripts/verify_dealix_ultimate_os.py
"""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    # Brand
    "business/brand/DEALIX_BRAND_SYSTEM.md",
    "business/brand/DEALIX_LOGO_AND_IDENTITY_SYSTEM.md",
    "business/brand/DEALIX_COPY_BANK_AR.md",
    "business/brand/DEALIX_COPY_BANK_EN.md",
    "apps/web/public/dealix-logo.svg",
    "apps/web/public/dealix-mark.svg",
    "apps/web/public/dealix-og.svg",
    # Website pages
    "apps/web/app/brand/page.tsx",
    "apps/web/app/offers/page.tsx",
    "apps/web/app/pricing/page.tsx",
    "apps/web/app/cases/page.tsx",
    "apps/web/app/revenue-machine/page.tsx",
    "apps/web/app/sales-assets/page.tsx",
    "apps/web/app/lead-engine/page.tsx",
    "apps/web/app/persuasion-room/page.tsx",
    "apps/web/app/command-center/page.tsx",
    "apps/web/app/war-room/page.tsx",
    "apps/web/app/pipeline/page.tsx",
    "apps/web/app/delivery-os/page.tsx",
    "apps/web/app/partner-room/page.tsx",
    "apps/web/app/daily-draft/page.tsx",
    "apps/web/app/kpi-finance/page.tsx",
    "apps/web/app/client-acquisition/page.tsx",
    "apps/web/app/automated-sales/page.tsx",
    # APIs
    "apps/web/app/api/company-os/ceo-brief/route.ts",
    "apps/web/app/api/company-os/founder-dashboard/route.ts",
    "apps/web/app/api/sales-machine/ultimate-pack/route.ts",
    "apps/web/app/api/sales-machine/daily-pack/route.ts",
    # Libraries
    "apps/web/lib/company-os/company-os.ts",
    "apps/web/lib/company-os/pipeline.ts",
    "apps/web/lib/sales-machine/ultimate-sales-os.ts",
    "apps/web/lib/sales-automation/lead-sources.ts",
    "apps/web/lib/generated/founder-dashboard.ts",
    # Sales machine docs
    "business/sales-machine/DEALIX_MASTER_SALES_FILE_AR.md",
    "business/sales-machine/DEALIX_MASTER_SALES_FILE_EN.md",
    "business/sales-machine/OBJECTION_HANDLING_LIBRARY.md",
    "business/sales-machine/PERSUASION_ANGLE_MATRIX.md",
    "business/sales-machine/LEAD_SOURCE_CONNECTORS_SPEC.md",
    "business/sales-machine/SALES_DAILY_OPERATING_SYSTEM.md",
    "business/sales-machine/INDUSTRY_WEAKNESS_TAXONOMY.md",
    "business/sales-machine/OFFER_MATCHING_RULES.md",
    "business/sales-machine/HUMAN_REVIEW_POLICY.md",
    # CRM
    "business/crm/schema.md",
    "business/crm/prospects.seed.json",
    "business/crm/README.md",
    # Proposals
    "business/proposals/PROPOSAL_TEMPLATE_AR.md",
    "business/proposals/PROPOSAL_TEMPLATE_EN.md",
    "business/proposals/PROPOSAL_SECTIONS_LIBRARY.md",
    # Delivery
    "business/delivery/CLIENT_DELIVERY_SOP.md",
    "business/delivery/CLIENT_ONBOARDING_CHECKLIST.md",
    "business/delivery/PROOF_REPORT_TEMPLATE.md",
    "business/delivery/WEEKLY_COMMAND_REPORT_TEMPLATE.md",
    "business/delivery/CHANGE_REQUEST_POLICY.md",
    "business/delivery/DELIVERY_AUTOMATION_BLUEPRINT.md",
    # Governance
    "business/governance/AI_HUMAN_REVIEW_POLICY.md",
    "business/governance/PDPL_AWARE_DATA_BOUNDARIES.md",
    "business/governance/OUTREACH_COMPLIANCE_POLICY.md",
    "business/governance/NO_SPAM_POLICY.md",
    "business/governance/SOURCE_AND_DATA_USAGE_REGISTER.md",
    "business/legal-lite/CLIENT_BOUNDARIES.md",
    # Pricing/Finance
    "business/pricing/OFFER_LADDER.md",
    "business/pricing/PRICING_STRATEGY_AR.md",
    "business/pricing/PRICING_STRATEGY_EN.md",
    "business/pricing/QUOTE_RULES.md",
    "business/finance/UNIT_ECONOMICS_MODEL.md",
    "business/finance/KPI_FINANCE_CONTROL.md",
    # CEO
    "business/ceo/FOUNDER_WAR_ROOM.md",
    "business/reports/DAILY_CEO_BRIEF_TEMPLATE.md",
    "business/reports/WEEKLY_OPERATING_REVIEW.md",
    # AI
    "business/ai/AI_TASK_ROUTING.md",
    "docs/ai/AI_MODEL_ROUTER_PLAN.md",
    "docs/integrations/INTEGRATION_ARCHITECTURE.md",
    "docs/integrations/GOOGLE_PLACES_CONNECTOR_PLAN.md",
    "docs/integrations/WHATSAPP_BUSINESS_CONNECTOR_PLAN.md",
    "docs/integrations/HUBSPOT_OR_CRM_CONNECTOR_PLAN.md",
    "docs/integrations/OPEN_DATA_CONNECTOR_PLAN.md",
    "docs/integrations/EMAIL_OUTREACH_CONNECTOR_PLAN.md",
    "docs/security/SALES_AUTOMATION_SECURITY_MODEL.md",
    "docs/security/DATA_MINIMIZATION.md",
    "docs/security/AUDIT_LOGGING_PLAN.md",
    # Scripts
    "scripts/import_leads_csv.py",
    "scripts/score_leads.py",
    "scripts/generate_outreach_drafts.py",
    "scripts/approve_outreach_draft.py",
    "scripts/reject_outreach_draft.py",
    "scripts/generate_prospect_pack.py",
    "scripts/generate_followup_queue.py",
    "scripts/generate_proposal.py",
    "scripts/generate_client_brief.py",
    "scripts/generate_workflow_review_agenda.py",
    "scripts/generate_delivery_plan.py",
    "scripts/generate_weekly_command_report.py",
    "scripts/generate_daily_ceo_brief.py",
    "scripts/generate_weekly_operating_review.py",
    "scripts/generate_ultimate_sales_os_pack.py",
    "scripts/generate_sales_machine_pack.py",
    "scripts/verify_dealix_ultimate_os.py",
    "scripts/verify_ultimate_sales_os.py",
    "scripts/verify_sales_machine.py",
    "scripts/verify_client_acquisition_delivery_os.py",
]

# V10 enterprise release baseline
V10_REQUIRED = [
    "business/enterprise/ENTERPRISE_READINESS_PACK.md",
    "business/enterprise/SECURITY_QUESTIONNAIRE_TEMPLATE.md",
    "business/enterprise/DATA_BOUNDARY_STATEMENT.md",
    "business/enterprise/AI_GOVERNANCE_STATEMENT.md",
    "business/enterprise/HUMAN_REVIEW_STATEMENT.md",
    "business/enterprise/SERVICE_LEVEL_BOUNDARIES.md",
    "business/enterprise/IMPLEMENTATION_ASSURANCE_PLAN.md",
    "business/enterprise/ENTERPRISE_BUYER_FAQ_AR.md",
    "business/enterprise/ENTERPRISE_BUYER_FAQ_EN.md",
    "apps/web/app/enterprise-readiness/page.tsx",
    "business/demo/DEALIX_DEMO_SCRIPT_AR.md",
    "business/demo/DEALIX_DEMO_SCRIPT_EN.md",
    "business/demo/FOUNDER_DEMO_FLOW.md",
    "business/demo/LIVE_WORKFLOW_REVIEW_SCRIPT.md",
    "business/demo/DEMO_QA_OBJECTIONS.md",
    "business/demo/DEMO_CLOSE.md",
    "scripts/generate_demo_pack.py",
    "scripts/generate_release_notes.py",
    "scripts/generate_health_snapshot.py",
    "scripts/check_required_env.py",
    "scripts/generate_env_report.py",
    "scripts/dealix_v10_run_all.sh",
]

# V11 CRM admin UI + API
V11_REQUIRED = [
    "apps/web/lib/crm/crm.ts",
    "apps/web/app/crm/page.tsx",
    "apps/web/app/crm/accounts/page.tsx",
    "apps/web/app/crm/accounts/[id]/page.tsx",
    "apps/web/app/crm/import/page.tsx",
    "apps/web/app/crm/review/page.tsx",
    "apps/web/app/crm/followups/page.tsx",
    "apps/web/app/crm/reports/page.tsx",
    "apps/web/app/operator/page.tsx",
    "apps/web/app/review-queue/page.tsx",
    "apps/web/app/outreach-lab/page.tsx",
    "apps/web/app/followups/page.tsx",
    "apps/web/components/crm/AccountTable.tsx",
    "apps/web/components/crm/PipelineSummary.tsx",
    "apps/web/components/crm/StageBadge.tsx",
    "apps/web/components/crm/ReviewStatusBadge.tsx",
    "apps/web/components/crm/DraftPreview.tsx",
    "apps/web/app/api/crm/accounts/route.ts",
    "apps/web/app/api/crm/accounts/[id]/route.ts",
    "apps/web/app/api/crm/accounts/[id]/stage/route.ts",
    "apps/web/app/api/crm/accounts/[id]/note/route.ts",
    "apps/web/app/api/crm/accounts/[id]/followup/route.ts",
    "apps/web/app/api/crm/drafts/route.ts",
    "apps/web/app/api/crm/drafts/[id]/approve/route.ts",
    "apps/web/app/api/crm/drafts/[id]/reject/route.ts",
    "apps/web/app/api/crm/reports/route.ts",
    "apps/web/app/api/crm/import/route.ts",
    "docs/auth/V11_ADMIN_ACCESS_BOUNDARY.md",
    "docs/auth/FOUNDER_ONLY_ROUTES.md",
    "docs/auth/PRODUCTION_AUTH_REQUIREMENTS.md",
]

# V12 quote-to-cash
V12_REQUIRED = [
    "business/_data/deals.ledger.json",
    "business/_data/quotes.index.json",
    "business/_data/invoices.index.json",
    "business/_schemas/deal.schema.json",
    "business/_schemas/quote.schema.json",
    "business/_schemas/invoice.schema.json",
    "scripts/lib/quote_engine.py",
    "scripts/generate_invoice_stub.py",
    "scripts/generate_revenue_report.py",
    "scripts/approve_quote.py",
    "scripts/review_quote.py",
    "scripts/mark_quote_sent.py",
    "business/deal-desk/DEAL_DESK_RULES.md",
    "business/contracts/MASTER_SERVICE_AGREEMENT_OUTLINE.md",
    "business/contracts/STATEMENT_OF_WORK_TEMPLATE_AR.md",
    "business/contracts/STATEMENT_OF_WORK_TEMPLATE_EN.md",
    "business/contracts/DATA_PROCESSING_ADDENDUM_OUTLINE.md",
    "business/contracts/ACCEPTANCE_CRITERIA_TEMPLATE.md",
    "business/contracts/CLIENT_RESPONSIBILITIES.md",
    "apps/web/lib/finance/deals.ts",
    "apps/web/app/deals/page.tsx",
    "apps/web/app/quotes/page.tsx",
    "apps/web/app/revenue/page.tsx",
    "docs/payments/PAYMENT_ARCHITECTURE.md",
    "docs/payments/MOYASAR_INTEGRATION_PLAN.md",
    "docs/payments/STRIPE_INTEGRATION_PLAN.md",
    "docs/payments/ZATCA_AWARE_INVOICING_NOTES.md",
    "docs/payments/PAYMENT_SECURITY_BOUNDARIES.md",
    "integrations/payments/base.py",
    "integrations/payments/moyasar_stub.py",
    "integrations/payments/stripe_stub.py",
]

# V13 client portal + delivery + proof
V13_REQUIRED = [
    "business/_data/client_portal.demo.json",
    "business/_data/client_workspaces.json",
    "business/_schemas/client_workspace.schema.json",
    "apps/web/lib/client/portal.ts",
    "apps/web/app/client-portal/page.tsx",
    "apps/web/app/client-portal/demo/page.tsx",
    "apps/web/app/client-portal/[clientId]/page.tsx",
    "apps/web/app/delivery-workspace/page.tsx",
    "apps/web/app/proof-vault/page.tsx",
    "apps/web/app/client-success/page.tsx",
    "apps/web/app/retention/page.tsx",
    "business/delivery-workspace/DELIVERY_WORKSPACE_SYSTEM.md",
    "business/proof/PROOF_ITEM_SCHEMA.md",
    "scripts/lib/workspace_store.py",
    "scripts/create_client_workspace.py",
    "scripts/add_deliverable.py",
    "scripts/mark_deliverable_done.py",
    "scripts/request_client_approval.py",
    "scripts/record_client_approval.py",
    "scripts/generate_client_status_report.py",
    "scripts/generate_retainer_expansion_plan.py",
    "scripts/generate_case_study_draft.py",
]

# V14 AI router + knowledge
V14_REQUIRED = [
    "scripts/lib/ai_router.py",
    "scripts/lib/ai_providers.py",
    "scripts/lib/prompt_registry.py",
    "scripts/lib/ai_safety.py",
    "scripts/lib/ai_memory.py",
    "scripts/lib/ai_eval.py",
    "scripts/run_ai_evals.py",
    "scripts/index_knowledge_sources.py",
    "scripts/search_knowledge_base.py",
    "scripts/generate_knowledge_pack.py",
    "docs/ai/V14_AGENT_OPERATIONS.md",
    "business/knowledge/KNOWLEDGE_BASE_SYSTEM.md",
    "business/_data/knowledge_sources.json",
    "business/ai/PROMPT_REGISTRY.md",
    "business/ai/BANNED_CLAIMS_POLICY.md",
    "business/ai/prompts/lead_scoring_explanation.md",
    "business/ai/prompts/outreach_draft_ar.md",
    "business/ai/prompts/outreach_draft_en.md",
    "business/ai/evals/outreach_eval_cases.json",
    "business/ai/evals/safety_eval_cases.json",
]

REQUIRED = REQUIRED + V10_REQUIRED + V11_REQUIRED + V12_REQUIRED + V13_REQUIRED + V14_REQUIRED


def _label_for(path: str) -> str:
    if path in V10_REQUIRED: return "V10"
    if path in V11_REQUIRED: return "V11"
    if path in V12_REQUIRED: return "V12"
    if path in V13_REQUIRED: return "V13"
    if path in V14_REQUIRED: return "V14"
    return "core"


def main() -> int:
    missing = [r for r in REQUIRED if not (REPO_ROOT / r).exists()]
    if missing:
        print("MISSING:")
        for m in missing:
            print(f"  - [{_label_for(m)}] {m}")
        return 1
    print("Dealix Ultimate Commercial OS V14 verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
