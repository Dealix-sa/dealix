#!/usr/bin/env python3
"""
Dealix Master Tree Generator
============================

Builds the canonical Master File Tree for the public repo (and emits an
optional plan for the private ops repo). Idempotent: never overwrites an
existing file. Creates every directory and writes a sensible starter
template for every file in the tree.

Usage:
    python scripts/generate_master_tree.py            # build public tree in CWD
    python scripts/generate_master_tree.py --check    # report missing only
    python scripts/generate_master_tree.py --private /path/to/private/repo

This script is the source-of-truth for what the Master Tree should look
like. The verify scripts under scripts/verify_*.py use the same manifest
to assert the tree is intact.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Public repo manifest
# ---------------------------------------------------------------------------

PUBLIC_TOP_LEVEL_FILES = [
    "README.md",
    "README.ar.md",
    "QUICK_START.md",
    "DEPLOYMENT.md",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "LICENSE",
    "CHANGELOG.md",
    "AGENTS.md",
    "DASHBOARD.md",
    "DEALIX_OPERATING_DOCTRINE.md",
    "DEALIX_STAGE_STATUS.md",
    "DEALIX_COMPANY_OS_SCORECARD.md",
    "DEALIX_ARCHITECTURE_MAP.md",
    "DEALIX_EXECUTION_LEDGER.md",
    "DEALIX_DECISION_RULES.md",
    "DEALIX_READINESS.md",
    "DEALIX_COMPANY_OPERATIONAL_STATE.md",
    ".env.example",
    ".env.staging.example",
    ".gitignore",
    ".dockerignore",
    ".editorconfig",
    ".gitleaks.toml",
    ".pre-commit-config.yaml",
    ".secrets.baseline",
    "pyproject.toml",
    "requirements.txt",
    "requirements-dev.txt",
    "Dockerfile",
    "docker-compose.yml",
    "Makefile",
    "Procfile",
    "railway.json",
    "railway.toml",
    "alembic.ini",
]

GITHUB_WORKFLOWS = [
    "ci.yml",
    "dealix-control.yml",
    "dealix-full-ops.yml",
    "dealix-company-os.yml",
    "security.yml",
    "scorecard.yml",
    "release.yml",
]

GITHUB_ISSUE_TEMPLATES = [
    "bug_report.yml",
    "feature_request.yml",
    "readiness_gap.yml",
    "trust_risk.yml",
    "documentation_gap.yml",
]

API_PACKAGE = {
    "api": ["__init__.py", "main.py", "app_factory.py"],
    "api/dependencies": [
        "__init__.py", "auth.py", "db.py", "rate_limit.py", "request_context.py",
    ],
    "api/middleware": [
        "__init__.py", "request_id.py", "error_handler.py", "cors.py", "audit_context.py",
    ],
    "api/routers": [
        "__init__.py", "health.py", "readiness.py", "pricing.py", "demo_request.py",
        "partner_application.py", "leads.py", "opportunities.py", "reports.py",
        "approvals.py", "claims.py", "billing.py", "webhooks.py", "public.py",
    ],
    "api/schemas": [
        "__init__.py", "lead.py", "opportunity.py", "report.py", "approval.py",
        "pricing.py", "payment.py", "trust.py", "common.py",
    ],
    "api/services": [
        "__init__.py", "lead_service.py", "scoring_service.py", "report_service.py",
        "approval_service.py", "pricing_service.py", "billing_service.py",
        "public_form_service.py",
    ],
}

DB_PACKAGE = {
    "db": ["__init__.py", "session.py", "base.py"],
    "db/models": [
        "__init__.py", "account.py", "contact.py", "lead.py", "opportunity.py",
        "proposal.py", "payment.py", "report.py", "approval.py", "audit_log.py",
        "claim.py", "suppression.py", "incident.py",
    ],
    "db/repositories": [
        "__init__.py", "account_repo.py", "lead_repo.py", "opportunity_repo.py",
        "report_repo.py", "approval_repo.py", "audit_repo.py", "payment_repo.py",
    ],
}

MIGRATIONS = {
    "migrations/versions": [".gitkeep"],
}

CONTROL_PLANE = {
    "control_plane": [
        "__init__.py", "company_state.py", "ceo_brief.py", "decision_engine.py",
        "action_router.py", "approval_router.py", "risk_engine.py",
        "metrics_collector.py", "system_scorecard.py", "learning_router.py",
    ],
}

OPERATING_INTELLIGENCE = {
    "operating_intelligence": [
        "__init__.py", "operating_signals.py", "priority_engine.py",
        "bottleneck_detector.py", "opportunity_detector.py", "risk_prioritizer.py",
        "learning_synthesizer.py", "weekly_review_generator.py",
        "monthly_strategy_generator.py", "system_improvement_planner.py",
    ],
}

DEALIX_PACKAGE = {
    "dealix": ["__init__.py"],
    "dealix/agents": [
        "__init__.py", "founder_brief_agent.py", "strategy_review_agent.py",
        "lead_finder_agent.py", "enrichment_agent.py", "scoring_agent.py",
        "pain_hypothesis_agent.py", "message_agent.py", "followup_agent.py",
        "proposal_agent.py", "delivery_report_agent.py", "qa_agent.py",
        "trust_guard_agent.py", "content_agent.py", "finance_watch_agent.py",
        "client_success_agent.py", "learning_agent.py",
    ],
    "dealix/workflows": [
        "__init__.py", "daily_ceo_brief.py", "daily_lead_discovery.py",
        "lead_scoring_batch.py", "founder_outreach_queue.py",
        "sample_pack_generation.py", "proposal_generation.py",
        "payment_verification.py", "delivery_report_generation.py",
        "case_study_generation.py", "weekly_ceo_review.py",
        "monthly_strategy_review.py",
    ],
    "dealix/trust": [
        "__init__.py", "approval_matrix.py", "autonomy_policy.py", "claim_guard.py",
        "data_retention.py", "suppression.py", "evidence_pack.py",
        "public_safety.py", "audit.py", "incident_response.py", "policy_engine.py",
    ],
    "dealix/registers": [
        "no_overclaim.yaml", "compliance_saudi.yaml", "approval_classes.yaml",
        "public_claims.yaml", "agent_permissions.yaml", "workflow_risk_classes.yaml",
        "safe_language.yaml",
    ],
    "dealix/scoring": [
        "__init__.py", "lead_score.py", "client_health_score.py",
        "company_health_score.py", "system_score.py",
    ],
    "dealix/execution": [
        "__init__.py", "task_runner.py", "workflow_runner.py", "approval_gate.py",
        "audit_writer.py",
    ],
    "dealix/utils": [
        "__init__.py", "dates.py", "ids.py", "markdown.py", "csv_io.py",
    ],
}

INTEGRATIONS = {
    "integrations/moyasar": ["__init__.py", "client.py", "webhook.py", "schemas.py"],
    "integrations/calendly": ["__init__.py", "client.py", "webhook.py"],
    "integrations/sentry": ["__init__.py", "setup.py"],
    "integrations/posthog": ["__init__.py", "client.py"],
    "integrations/email": ["__init__.py", "sender.py", "templates.py"],
}

LANDING = {
    "landing": [
        "index.html", "revenue-sprint.html", "managed-pilot.html",
        "revenue-desk.html", "pricing.html", "partners.html", "trust.html",
        "demo.html", "thank-you.html",
    ],
    "landing/assets/logo": [
        "dealix-primary.svg", "dealix-icon.svg", "dealix-monochrome.svg",
        "favicon.svg",
    ],
    "landing/assets/brand": [".gitkeep"],
    "landing/assets/screenshots": [".gitkeep"],
    "landing/assets/icons": [".gitkeep"],
}

APPS_WEB = {
    "apps/web": ["README.md"],
    "apps/web/app": [".gitkeep"],
    "apps/web/components": [".gitkeep"],
    "apps/web/lib": [".gitkeep"],
    "apps/web/public": [".gitkeep"],
}

# ---- docs/ ----
DOCS = {
    "docs/founder": [
        "CEO_OPERATING_SYSTEM.md", "DAILY_COMMAND_BRIEF.md", "WEEKLY_CEO_REVIEW.md",
        "MONTHLY_STRATEGY_REVIEW.md", "DECISION_LOG.md", "CEO_DECISION_QUEUE.md",
        "RISK_REGISTER.md", "FOCUS_POLICY.md", "COMPANY_HEALTH_SCORE.md",
        "FOUNDER_LEVERAGE_INDEX.md", "FOUNDER_TIME_ACCOUNTING.md", "CEO_ALERTS.md",
        "CEO_RED_TEAM.md", "CEO_DASHBOARD_SPEC.md", "BOARD_PACK_TEMPLATE.md",
        "KILL_LIST.md",
    ],
    "docs/strategy": [
        "NORTH_STAR.md", "STRATEGIC_THESIS.md", "ICP_STRATEGY.md",
        "MARKET_MAP_SAUDI.md", "COMPETITIVE_STRATEGY.md", "MOAT_STRATEGY.md",
        "MOAT_SYSTEM.md", "MONTHLY_MOAT_REVIEW.md", "GTM_STRATEGY.md",
        "PRICING_STRATEGY.md", "GROWTH_MODEL.md", "90_DAY_PLAN.md",
    ],
    "docs/revenue": [
        "REVENUE_MODEL.md", "OFFER_LADDER.md", "PIPELINE_STAGES.md",
        "REVENUE_METRICS.md", "CASH_RULES.md", "PROPOSAL_RULES.md",
        "PRICING_EXPERIMENTS.md", "REVENUE_QUALITY.md", "BAD_REVENUE_FILTER.md",
        "OFFER_EVOLUTION_SYSTEM.md", "WIN_LOSS_REVIEW.md",
    ],
    "docs/acquisition": [
        "LEAD_SOURCING_SYSTEM.md", "ICP_SCORING_MODEL.md", "SECTOR_PLAYBOOKS.md",
        "OUTREACH_CADENCE.md", "MESSAGE_QUALITY_STANDARD.md",
        "SAMPLE_GENERATION_SYSTEM.md", "CHANNEL_STRATEGY.md",
        "PARTNER_ACQUISITION.md",
    ],
    "docs/sales": [
        "QUALIFICATION_RULES.md", "CALL_SCRIPT.md", "OBJECTION_HANDLING.md",
        "PROPOSAL_PROCESS.md", "CLOSING_PLAYBOOK.md", "FOLLOWUP_RULES.md",
        "SALES_METRICS.md",
    ],
    "docs/offers/revenue_sprint": [
        "OFFER.md", "PRICING.md", "SCOPE.md", "FAQ.md", "PROPOSAL_TEMPLATE.md",
        "TERMS.md", "ONE_PAGER.md",
    ],
    "docs/offers/managed_pilot": [
        "OFFER.md", "PRICING.md", "SCOPE.md", "PROPOSAL_TEMPLATE.md", "TERMS.md",
    ],
    "docs/offers/revenue_desk": [
        "OFFER.md", "PRICING.md", "SCOPE.md", "WEEKLY_DELIVERABLES.md",
        "RENEWAL_RULES.md",
    ],
    "docs/delivery": ["DELIVERY_QUALITY_STANDARD.md"],
    "docs/delivery/revenue_sprint": [
        "DELIVERY_PLAYBOOK.md", "CLIENT_INTAKE.md", "RESEARCH_PROCESS.md",
        "LEAD_TABLE_SCHEMA.md", "SCORING_RULES.md", "OUTREACH_PACK_TEMPLATE.md",
        "REPORT_TEMPLATE.md", "QA_CHECKLIST.md", "HANDOFF_TEMPLATE.md",
        "CASE_STUDY_CAPTURE.md",
    ],
    "docs/delivery/managed_pilot": [
        "DELIVERY_PLAYBOOK.md", "WEEKLY_REPORT_TEMPLATE.md", "PIPELINE_REVIEW.md",
        "MEETING_PREP_TEMPLATE.md", "QA_CHECKLIST.md",
    ],
    "docs/delivery/revenue_desk": [
        "WEEKLY_OPERATING_LOOP.md", "CLIENT_HEALTH_SCORE.md",
        "RETENTION_PLAYBOOK.md", "RENEWAL_PLAYBOOK.md",
    ],
    "docs/trust": [
        "APPROVAL_MATRIX.md", "AUTONOMY_POLICY.md", "CLAIM_GUARD.md",
        "NO_OVERCLAIM_POLICY.md", "SAFE_LANGUAGE_LIBRARY.md",
        "DATA_RETENTION_POLICY.md", "SUPPRESSION_LIST_POLICY.md",
        "CLIENT_DATA_HANDLING.md", "INCIDENT_RESPONSE.md",
        "PUBLIC_REPO_SAFETY.md", "PUBLIC_PRIVATE_BOUNDARY.md", "AI_GOVERNANCE.md",
        "AGENT_BOUNDARIES.md", "WORKFLOW_RISK_CLASSIFICATION.md",
        "EVIDENCE_SYSTEM.md", "AUDIT_POLICY.md",
    ],
    "docs/finance": [
        "BILLING_POLICY.md", "PAYMENT_RULES.md", "INVOICE_WORKFLOW.md",
        "REFUND_POLICY.md", "MRR_DEFINITION.md", "CASH_CONTROL.md",
        "CAPITAL_ALLOCATION.md", "FINANCIAL_DASHBOARD.md",
    ],
    "docs/client_success": [
        "ONBOARDING.md", "WEEKLY_REPORT_TEMPLATE.md", "CLIENT_HEALTH_SCORE.md",
        "CLIENT_TIERING.md", "FEEDBACK_LOOP.md", "RETENTION_PLAYBOOK.md",
        "UPSELL_PLAYBOOK.md", "RENEWAL_PLAYBOOK.md",
    ],
    "docs/product": [
        "PRODUCT_PRINCIPLES.md", "ROADMAP.md", "FEATURE_INTAKE.md",
        "BUILD_DEFER_KILL.md", "PRODUCTIZATION_ENGINE.md", "RELEASE_POLICY.md",
        "ENGINEERING_METRICS.md", "ENGINEERING_HEALTH_REVIEW.md",
        "CUSTOMER_FEEDBACK_LOOP.md", "BUG_TRIAGE.md",
    ],
    "docs/content": [
        "CONTENT_STRATEGY.md", "FOUNDER_VOICE.md", "LINKEDIN_SYSTEM.md",
        "X_SYSTEM.md", "CASE_STUDY_SYSTEM.md", "SECTOR_REPORT_SYSTEM.md",
        "PROOF_LIBRARY.md",
    ],
    "docs/learning": [
        "LEARNING_ROUTER.md", "COMPANY_MEMORY.md", "EXPERIMENT_SYSTEM.md",
        "EXPERIMENT_LOG.md", "WEEKLY_INTELLIGENCE_REVIEW.md", "WIN_LOSS_REVIEW.md",
        "MESSAGE_PERFORMANCE.md", "SECTOR_PERFORMANCE.md", "PRICING_LEARNING.md",
        "AGENT_EVALS.md", "MONTHLY_STRATEGY_UPDATE.md",
    ],
    "docs/people": [
        "ROLE_MAP.md", "HIRING_TRIGGERS.md", "SDR_SCORECARD.md",
        "DELIVERY_ANALYST_SCORECARD.md", "OPS_MANAGER_SCORECARD.md",
        "CONTRACTOR_ONBOARDING.md", "DELEGATION_RULES.md",
    ],
    "docs/agents": [
        "AGENT_REGISTRY.md", "AGENT_EVALUATION.md", "AGENT_PERMISSIONS.md",
        "AGENT_HANDOFFS.md", "AGENT_LOGGING.md",
    ],
    "docs/ai_management": [
        "AI_SYSTEM_INVENTORY.md", "AI_RISK_REGISTER.md", "AI_EVALUATION_POLICY.md",
        "AI_HUMAN_OVERSIGHT.md", "AI_CHANGE_MANAGEMENT.md",
        "AI_INCIDENT_RESPONSE.md", "AI_SUPPLIER_POLICY.md",
    ],
    "docs/control_plane": [
        "CONTROL_PLANE_ARCHITECTURE.md", "COMPANY_STATE_SCHEMA.md",
        "CEO_BRIEF_SPEC.md", "DECISION_ENGINE.md", "ACTION_ROUTER.md",
        "APPROVAL_ROUTING.md", "RISK_ENGINE.md", "SYSTEM_SCORECARD.md",
        "LEARNING_ROUTER.md",
    ],
    "docs/ops": [
        "OPERATING_CADENCE.md", "AUTONOMOUS_CADENCE.md", "OPERATING_LOOPS.md",
        "OPERATING_SIGNALS.md", "OPERATING_METRICS_CONTRACT.md",
        "SYSTEM_OWNERS.md", "ESCALATION_MATRIX.md", "BOTTLENECK_DETECTOR.md",
        "PRIORITY_ENGINE.md", "SELF_IMPROVING_PLAYBOOKS.md", "SOP_INDEX.md",
    ],
    "docs/partners": [
        "PARTNER_STRATEGY.md", "PARTNER_PROFILE.md", "REFERRAL_TERMS.md",
        "WHITE_LABEL_RULES.md", "PARTNER_ONBOARDING.md", "PARTNER_SCORECARD.md",
    ],
    "docs/investor": [
        "DATA_ROOM_INDEX.md", "COMPANY_OVERVIEW.md", "METRICS.md", "ROADMAP.md",
        "FINANCIAL_MODEL.md", "MARKET_THESIS.md", "RISK_REGISTER.md",
        "PITCH_DECK_OUTLINE.md",
    ],
    "docs/brand": [
        "BRAND_GUIDELINES.md", "LOGO_USAGE.md", "COLORS.md", "TYPOGRAPHY.md",
        "TONE_OF_VOICE.md", "PRESENTATION_STYLE.md", "WEBSITE_STYLE.md",
        "COMMERCIAL_ASSETS.md",
    ],
    "docs/api": [
        "API_OVERVIEW.md", "AUTHENTICATION.md", "ENDPOINTS.md", "WEBHOOKS.md",
        "ERROR_CODES.md",
    ],
    "docs/deployment": [
        "ENVIRONMENT_VARIABLES.md", "RAILWAY_DEPLOYMENT.md", "SUPABASE_SETUP.md",
        "MONITORING.md", "INCIDENT_RUNBOOK.md",
    ],
}

READINESS = {
    "readiness": ["OPERATING_READINESS_LEVELS.md"],
    "readiness/gates": [
        "gate_00_founder_clarity.md", "gate_01_offer.md", "gate_02_delivery.md",
        "gate_03_product.md", "gate_04_trust.md", "gate_05_sales.md",
        "gate_06_first_client.md", "gate_07_retainer.md", "gate_08_scale.md",
        "gate_09_autonomous_company_os.md",
    ],
    "readiness/checklists": [
        "public_repo_checklist.md", "private_boundary_checklist.md",
        "revenue_sprint_checklist.md", "delivery_qa_checklist.md",
        "trust_checklist.md", "company_os_checklist.md",
    ],
    "readiness/scorecards": [
        "founder_os_scorecard.md", "revenue_os_scorecard.md",
        "delivery_os_scorecard.md", "trust_os_scorecard.md",
        "product_os_scorecard.md", "learning_os_scorecard.md",
        "company_os_scorecard.md",
    ],
}

DEMOS = {
    "demos/revenue_sprint_demo": [
        "README.md", "demo_leads.csv", "demo_report.md", "demo_outreach_pack.md",
    ],
    "demos/lead_intelligence_demo": [".gitkeep"],
    "demos/company_brain_demo": [".gitkeep"],
    "demos/demo_data": [".gitkeep"],
}

EVALS = {
    "evals/datasets": [
        "lead_scoring_cases.jsonl", "message_quality_cases.jsonl",
        "no_overclaim_cases.jsonl", "trust_guard_cases.jsonl",
    ],
    "evals/rubrics": [
        "lead_scoring_rubric.md", "message_quality_rubric.md",
        "proposal_quality_rubric.md", "trust_guard_rubric.md",
    ],
    "evals/results": [".gitkeep"],
}

SCRIPTS = {
    "scripts": [
        "verify_full_ops.py", "verify_docs_complete.py", "verify_architecture.py",
        "verify_public_safety.py", "verify_private_boundary.py",
        "verify_stage_status.py", "verify_company_os.py", "verify_founder_os.py",
        "verify_strategy_os.py", "verify_revenue_os.py", "verify_acquisition_os.py",
        "verify_sales_os.py", "verify_offer_readiness.py", "verify_delivery_os.py",
        "verify_delivery_readiness.py", "verify_trust_os.py",
        "verify_trust_readiness.py", "verify_finance_os.py",
        "verify_client_success_os.py", "verify_product_os.py",
        "verify_content_os.py", "verify_learning_os.py", "verify_agents_os.py",
        "verify_ai_management.py", "verify_control_plane.py",
        "verify_brand_readiness.py", "verify_landing_page.py",
        "export_company_os_status.py", "generate_ceo_brief.py",
        "generate_weekly_review.py", "smoke_inprocess.py", "seo_audit.py",
        "run_evals.py",
    ],
}

TESTS = {
    "tests": ["__init__.py"],
    "tests/unit": [
        "__init__.py", "test_scoring.py", "test_claim_guard.py",
        "test_approval_matrix.py", "test_suppression.py", "test_decision_engine.py",
        "test_action_router.py", "test_risk_engine.py",
    ],
    "tests/integration": [
        "__init__.py", "test_health_api.py", "test_pricing_api.py",
        "test_demo_request.py", "test_moyasar_webhook.py",
        "test_report_generation.py", "test_ceo_brief_generation.py",
    ],
    "tests/contract": [
        "__init__.py", "test_openapi_contract.py", "test_public_endpoints.py",
    ],
    "tests/e2e": [
        "__init__.py", "test_revenue_sprint_flow.py",
        "test_demo_to_proposal_flow.py", "test_company_os_flow.py",
    ],
    "tests/trust": [
        "__init__.py", "test_no_overclaim.py", "test_never_auto_execute.py",
        "test_public_safety.py", "test_safe_language.py", "test_private_boundary.py",
    ],
}

TEMPLATES = {
    "templates": [
        "client_report_template.md", "proposal_template.md",
        "weekly_review_template.md", "daily_ceo_brief_template.md",
        "board_pack_template.md", "case_study_template.md",
    ],
}


def collect_public_manifest() -> dict[str, list[str]]:
    manifest: dict[str, list[str]] = {"": list(PUBLIC_TOP_LEVEL_FILES)}
    manifest[".github/workflows"] = list(GITHUB_WORKFLOWS)
    manifest[".github/ISSUE_TEMPLATE"] = list(GITHUB_ISSUE_TEMPLATES)
    manifest[".github"] = ["pull_request_template.md"]
    for group in [
        API_PACKAGE, DB_PACKAGE, MIGRATIONS, CONTROL_PLANE, OPERATING_INTELLIGENCE,
        DEALIX_PACKAGE, INTEGRATIONS, LANDING, APPS_WEB, DOCS, READINESS,
        DEMOS, EVALS, SCRIPTS, TESTS, TEMPLATES,
    ]:
        for d, files in group.items():
            manifest.setdefault(d, []).extend(files)
    return manifest


# ---------------------------------------------------------------------------
# Private repo manifest
# ---------------------------------------------------------------------------

PRIVATE_MANIFEST = {
    "": [
        "README.md", "OPS_STATUS.md", "DEALIX_STAGE_STATUS.md",
        "DEALIX_EXECUTION_LEDGER.md", "PRIVATE_DATA_POLICY.md",
        "verify_private_ops.py", "verify_private_ops_integrity.py",
    ],
    ".github/workflows": ["private-ops-checks.yml"],
    "founder": [
        "daily_brief.md", "ceo_dashboard.md", "weekly_ceo_review.md",
        "monthly_strategy_review.md", "board_pack.md", "decision_queue.md",
        "decision_log.md", "approvals_waiting.md", "focus_queue.md",
        "risk_log.md", "founder_time_log.md",
    ],
    "strategy": [
        "quarterly_plan.md", "strategic_bets.md", "competitor_notes.md",
        "market_notes.md", "moat_review.md", "growth_model_notes.md",
    ],
    "pipeline": [
        "pipeline_tracker.csv", "lead_sources.md", "outreach_queue.md",
        "followups.md", "objections.md", "win_loss_log.md", "suppression_notes.md",
    ],
    "sales": [
        "dm_templates.md", "call_scripts.md", "closing_playbook.md",
        "objections_log.md", "offer_experiments.md",
    ],
    "sales/proposal_notes": [".gitkeep"],
    "sales/call_notes": [".gitkeep"],
    "clients/_template": [
        "intake.md", "proposal.md", "sow.md", "delivery_report.md",
        "qa_checklist.md", "handoff.md", "feedback.md", "renewal.md",
    ],
    "clients/client_name_private": [
        "intake.md", "proposal.md", "contract_or_sow.md", "delivery_report.md",
        "qa_checklist.md", "handoff.md", "feedback.md", "health_score.md",
        "renewal.md",
    ],
    "revenue": [
        "mrr_tracker.csv", "cash_collected.csv", "pipeline_value.csv",
        "pricing_experiments.md", "revenue_dashboard.csv",
    ],
    "revenue/invoices": [".gitkeep"],
    "revenue/payments": [".gitkeep"],
    "revenue/receipts": [".gitkeep"],
    "delivery/active_sprints": [".gitkeep"],
    "delivery/reports": [".gitkeep"],
    "delivery/research": [".gitkeep"],
    "delivery/qa": [".gitkeep"],
    "delivery/handoffs": [".gitkeep"],
    "delivery/case_studies_private": [".gitkeep"],
    "trust": [
        "approval_log.csv", "suppression_list.csv", "claim_approval_log.csv",
        "export_log.csv", "data_incidents.md", "sensitive_actions.md",
        "risk_exceptions.md",
    ],
    "content": ["published_log.csv"],
    "content/drafts": [".gitkeep"],
    "content/case_study_notes": [".gitkeep"],
    "content/proof_library": [".gitkeep"],
    "content/sector_insights": [".gitkeep"],
    "prompts": [
        "founder_brief_agent.md", "lead_finder_agent.md", "enrichment_agent.md",
        "scoring_agent.md", "pain_hypothesis_agent.md", "message_agent.md",
        "followup_agent.md", "proposal_agent.md", "delivery_report_agent.md",
        "qa_agent.md", "trust_guard_agent.md", "learning_agent.md",
    ],
    "people": ["hiring_pipeline.csv", "delegation_log.md"],
    "people/role_scorecards": [
        "sdr_scorecard.md", "delivery_analyst_scorecard.md",
        "ops_manager_scorecard.md", "engineer_scorecard.md",
    ],
    "people/contractor_notes": [".gitkeep"],
    "legal": [
        "nda_template.md", "sow_template.md", "dpa_template.md", "msa_template.md",
        "terms_review.md", "legal_questions.md",
    ],
    "partners": [
        "partner_pipeline.csv", "referral_terms.md", "partner_scorecard.csv",
    ],
    "partners/partner_notes": [".gitkeep"],
    "learning": [
        "experiment_log.md", "weekly_intelligence_review.md",
        "monthly_learning_review.md", "win_loss_review.md",
        "message_performance.csv", "sector_performance.csv", "pricing_learning.md",
        "productization_candidates.md",
    ],
    "finance": [
        "monthly_finance_review.md", "cash_plan.md", "expenses.csv",
        "runway_estimate.md", "capital_allocation_review.md",
    ],
    "weekly_reviews": ["template.md"],
}


# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

def py_module_stub(path: str) -> str:
    name = Path(path).stem
    parent = Path(path).parent.name
    return (
        f'"""\n{parent}.{name} — module stub.\n\n'
        f'This module is part of the Dealix Master Tree. It is a placeholder\n'
        f'that the corresponding verify_*.py script asserts exists. Replace with\n'
        f'real implementation as the system matures.\n"""\n'
    )


def md_doc_stub(path: str) -> str:
    title = Path(path).stem.replace("_", " ").title()
    return (
        f"# {title}\n\n"
        f"> Status: DRAFT — placeholder created by the Master Tree generator.\n\n"
        f"## Purpose\n\n"
        f"Document the policy, playbook, template, metrics, owner, approval level,\n"
        f"verify script, and evidence path for **{title}**.\n\n"
        f"## Owner\n\nFounder / CEO\n\n"
        f"## Approval Level\n\nFounder approval required for any change.\n\n"
        f"## Metrics\n\nTBD\n\n"
        f"## Evidence\n\nTBD\n\n"
        f"## Last Reviewed\n\nNot yet reviewed.\n"
    )


def yaml_register_stub(path: str) -> str:
    name = Path(path).stem
    return (
        f"# {name}\n"
        f"# Register file — populated incrementally as policy hardens.\n"
        f"version: 0.1\n"
        f"register: {name}\n"
        f"entries: []\n"
    )


def html_landing_stub(path: str) -> str:
    name = Path(path).stem.replace("-", " ").title()
    return (
        "<!doctype html>\n"
        "<html lang=\"en\">\n"
        "<head>\n"
        "  <meta charset=\"utf-8\" />\n"
        "  <meta name=\"viewport\" content=\"width=device-width,initial-scale=1\" />\n"
        f"  <title>{name} — Dealix</title>\n"
        "</head>\n"
        "<body>\n"
        f"  <h1>{name}</h1>\n"
        "  <p>Placeholder page rendered by the Master Tree generator.</p>\n"
        "</body>\n"
        "</html>\n"
    )


def svg_logo_stub(path: str) -> str:
    name = Path(path).stem
    return (
        f"<!-- Dealix logo placeholder: {name} -->\n"
        "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 200 60\">\n"
        "  <rect width=\"200\" height=\"60\" fill=\"#0B0F19\"/>\n"
        "  <text x=\"100\" y=\"38\" font-family=\"sans-serif\" font-size=\"24\" "
        "fill=\"#fff\" text-anchor=\"middle\">Dealix</text>\n"
        "</svg>\n"
    )


def csv_stub(path: str) -> str:
    name = Path(path).stem
    return f"# {name}\n# header,placeholder\nplaceholder,0\n"


def jsonl_stub(path: str) -> str:
    return json.dumps({"id": 1, "case": "placeholder", "expected": "TBD"}) + "\n"


def yml_workflow_stub(path: str) -> str:
    name = Path(path).stem
    return (
        f"name: {name}\n"
        "on:\n"
        "  workflow_dispatch: {}\n"
        "jobs:\n"
        "  noop:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        "      - run: echo \"placeholder workflow\"\n"
    )


def issue_template_stub(path: str) -> str:
    name = Path(path).stem
    return (
        f"name: {name.replace('_', ' ').title()}\n"
        f"description: Issue template for {name}\n"
        f"labels: [{name}]\n"
        f"body:\n"
        f"  - type: textarea\n"
        f"    id: description\n"
        f"    attributes:\n"
        f"      label: Describe the issue\n"
        f"    validations:\n"
        f"      required: true\n"
    )


def verify_script_stub(path: str) -> str:
    name = Path(path).stem
    return (
        '#!/usr/bin/env python3\n'
        f'"""{name} — verification script stub."""\n'
        'from __future__ import annotations\n'
        'import sys\n'
        'from pathlib import Path\n\n'
        'REPO = Path(__file__).resolve().parent.parent\n\n'
        'def main() -> int:\n'
        f'    print("[OK] {name} placeholder check passed")\n'
        '    return 0\n\n'
        'if __name__ == "__main__":\n'
        '    sys.exit(main())\n'
    )


def test_stub(path: str) -> str:
    name = Path(path).stem
    return (
        f'"""{name} — placeholder test."""\n'
        'def test_placeholder():\n'
        '    """Replace with real assertion once the unit is implemented."""\n'
        '    assert True\n'
    )


# Routing table: extension or special filename -> renderer
def render(rel_path: str) -> str:
    p = Path(rel_path)
    suffix = p.suffix.lower()
    name = p.name
    stem = p.stem
    posix = p.as_posix()

    if name == ".gitkeep":
        return ""
    if name == "pull_request_template.md":
        return (
            "## Summary\n\n- [ ] What changed?\n- [ ] Why?\n\n"
            "## Tests\n\n- [ ] Unit\n- [ ] Trust\n- [ ] Verify scripts\n\n"
            "## Checklist\n\n- [ ] No PII / client data in diff\n"
            "- [ ] No claims unsupported by evidence\n- [ ] Docs updated\n"
        )
    if posix.startswith(".github/ISSUE_TEMPLATE/") and suffix == ".yml":
        return issue_template_stub(posix)
    if posix.startswith(".github/workflows/") and suffix in {".yml", ".yaml"}:
        return yml_workflow_stub(posix)
    if posix.startswith("scripts/") and stem.startswith("verify_") and suffix == ".py":
        return verify_script_stub(posix)
    if posix.startswith("scripts/") and suffix == ".py":
        return verify_script_stub(posix)  # generic CLI stub is fine
    if posix.startswith("tests/") and suffix == ".py" and stem.startswith("test_"):
        return test_stub(posix)
    if suffix == ".py":
        return py_module_stub(posix)
    if suffix == ".yaml" or suffix == ".yml":
        return yaml_register_stub(posix)
    if suffix == ".md":
        return md_doc_stub(posix)
    if suffix == ".html":
        return html_landing_stub(posix)
    if suffix == ".svg":
        return svg_logo_stub(posix)
    if suffix == ".csv":
        return csv_stub(posix)
    if suffix == ".jsonl":
        return jsonl_stub(posix)
    if name == "LICENSE":
        return "MIT License\n\nCopyright (c) Dealix\n"
    if name in {".gitignore", ".dockerignore", ".editorconfig"}:
        return f"# {name} — placeholder\n"
    if name == "Procfile":
        return "web: uvicorn api.main:app --host 0.0.0.0 --port $PORT\n"
    if name == "Makefile":
        return (
            ".PHONY: verify test\n\n"
            "verify:\n\tpython scripts/verify_full_ops.py\n\n"
            "test:\n\tpytest -q\n"
        )
    if name in {"railway.json", "railway.toml"}:
        return "# placeholder\n"
    if name == "alembic.ini":
        return "# alembic placeholder\n"
    if name in {"pyproject.toml", "requirements.txt", "requirements-dev.txt"}:
        return "# placeholder dependency manifest\n"
    if name in {"Dockerfile", "docker-compose.yml"}:
        return "# placeholder container manifest\n"
    if name.startswith(".env"):
        return "# placeholder env example\n"
    if name == ".gitleaks.toml":
        return "title = \"gitleaks-config-placeholder\"\n"
    if name == ".pre-commit-config.yaml":
        return "repos: []\n"
    if name == ".secrets.baseline":
        return "{}\n"
    return f"# {name} — placeholder\n"


# ---------------------------------------------------------------------------
# Filesystem driver
# ---------------------------------------------------------------------------

def apply_manifest(
    root: Path, manifest: dict[str, list[str]], *, check_only: bool = False
) -> tuple[int, int, list[str]]:
    created = 0
    skipped = 0
    missing: list[str] = []
    for relative_dir, files in manifest.items():
        directory = root / relative_dir if relative_dir else root
        if not check_only:
            directory.mkdir(parents=True, exist_ok=True)
        for filename in files:
            target = directory / filename
            if target.exists():
                skipped += 1
                continue
            if check_only:
                missing.append(str(target.relative_to(root)))
                continue
            content = render(str(target.relative_to(root)))
            target.write_text(content, encoding="utf-8")
            created += 1
    return created, skipped, missing


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true",
        help="Report missing files without creating them.",
    )
    parser.add_argument(
        "--private", type=Path, default=None,
        help="Also apply the private-ops manifest at this path.",
    )
    parser.add_argument(
        "--root", type=Path, default=REPO_ROOT,
        help="Target root for the public manifest (default: repo root).",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    public_manifest = collect_public_manifest()
    created, skipped, missing = apply_manifest(
        args.root, public_manifest, check_only=args.check,
    )
    if args.check:
        if missing:
            print(f"[MISSING] {len(missing)} files missing from public tree:")
            for m in missing[:50]:
                print(f"  - {m}")
            if len(missing) > 50:
                print(f"  ... and {len(missing) - 50} more")
            return 1
        print("[OK] Public tree is complete.")
    else:
        print(f"[OK] Public tree: created={created} skipped(existing)={skipped}")

    if args.private is not None:
        p_created, p_skipped, p_missing = apply_manifest(
            args.private, PRIVATE_MANIFEST, check_only=args.check,
        )
        if args.check:
            if p_missing:
                print(f"[MISSING] {len(p_missing)} files missing from private tree:")
                for m in p_missing[:50]:
                    print(f"  - {m}")
                return 1
            print("[OK] Private tree is complete.")
        else:
            print(
                f"[OK] Private tree: created={p_created} skipped(existing)={p_skipped}"
            )

    return 0


if __name__ == "__main__":
    sys.exit(main())
