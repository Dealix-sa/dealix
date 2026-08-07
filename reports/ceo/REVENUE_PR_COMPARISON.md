# Revenue PR Comparison

Goal: choose one canonical Revenue Loop path. Do not merge duplicates.

| PR | Draft | Mergeable | Title | Files | URL |
|---:|---|---|---|---:|---|
| #711 | True | CONFLICTING | feat(wave-2): Revenue Engine v2 — daily commercial pack generation | 9 | https://github.com/Dealix-sa/dealix/pull/711 |
| #726 | True | CONFLICTING | feat(outreach): daily Arabic email targeting system — 30 Saudi ICPs + Gmail runner | 6 | https://github.com/Dealix-sa/dealix/pull/726 |
| #732 | False | CONFLICTING | Resolve pr 727 | 91 | https://github.com/Dealix-sa/dealix/pull/732 |
| #739 | False | CONFLICTING | feat(outreach): daily Arabic email targeting system — 30 Saudi ICPs +… | 6 | https://github.com/Dealix-sa/dealix/pull/739 |

## File surfaces

### PR #711

- `.github/workflows/revenue_day.yml`
- `.gitignore`
- `company/brand/DEALIX_BRAND_SYSTEM_V2.md`
- `company/finance/COMMERCIAL_RULES_V2.md`
- `company/revenue_engine/REVENUE_ENGINE_V2.md`
- `company/revenue_engine/revenue_engine_v2.py`
- `company/sales/REVENUE_PLAYBOOK_V2.md`
- `company/site/WEBSITE_CONVERSION_MAP_V2.md`
- `scripts/dealix_revenue_day.sh`

### PR #726

- `.gitignore`
- `Makefile`
- `auto_client_acquisition/email/daily_targeting.py`
- `data/saudi_icp_targets.json`
- `scripts/gmail_daily_outreach.py`
- `tests/test_gmail_daily_outreach.py`

### PR #732

- `.github/workflows/ci.yml`
- `.gitignore`
- `Makefile`
- `api/routers/cost_tracking.py`
- `api/routers/customer_webhooks.py`
- `api/routers/platform_meta.py`
- `api/routers/pricing.py`
- `api/routers/referral_program.py`
- `api/routers/sector_intel.py`
- `api/routers/tenant_theming.py`
- `api/routers/webhooks.py`
- `api/security/api_key.py`
- `auto_client_acquisition/governance_os/approval_matrix.py`
- `auto_client_acquisition/governance_os/draft_gate.py`
- `auto_client_acquisition/governance_os/forbidden_actions.py`
- `auto_client_acquisition/orchestrator/durable_workflow.py`
- `auto_client_acquisition/personal_operator/llm_brief.py`
- `auto_client_acquisition/runtime_safety_os/incident_detection.py`
- `auto_client_acquisition/runtime_safety_os/post_mortem.py`
- `business/playbooks/REPLY_PLAYBOOK.md`
- `data/commercial/icp_segments.yaml`
- `data/commercial/pain_to_offer.yaml`
- `data/commercial/pricing_rules.yaml`
- `data/commercial/product_catalog.yaml`
- `data/outreach/FOUNDER_RUNBOOK.md`
- `data/outreach/README.md`
- `data/outreach/TARGET_RESEARCH.md`
- `data/outreach/outreach_log.template.csv`
- `data/outreach/saudi_target_intake.template.csv`
- `data/outreach/sector_pitches.json`
- `data/templates/proposal_command_center_ar.md`
- `data/templates/proposal_delivery_os_ar.md`
- `data/templates/proposal_revenue_os_ar.md`
- `data/templates/proposal_review_os_ar.md`
- `db/models.py`
- `dealix/commercial_ops/revenue_learning_loop.py`
- `dealix/reliability/idempotency.py`
- `dealix/revenue_ops_autopilot/postgres_store.py`
- `docs/SEO_AUDIT_REPORT.json`
- `frontend/.env.local.example`
- `frontend/src/app/[locale]/partners/commissions/page.tsx`
- `frontend/src/components/shared/CommandPalette.tsx`
- `frontend/src/lib/commands/registry.ts`
- `frontend/src/lib/hooks/usePartners.ts`
- `frontend/src/lib/hooks/usePayments.ts`
- `frontend/src/lib/hooks/usePricing.ts`
- `frontend/src/lib/notifications/service.ts`
- `frontend/src/lib/onboarding/steps.ts`
- `frontend/tsconfig.json`
- `landing/architecture.html`
- `landing/case-study-template.html`
- `landing/dpa.html`
- `landing/launch-status.html`
- `landing/pricing.html`
- `landing/sector-report-realestate-sample.html`
- `landing/system-status.html`
- `presentations/company-profile/dealix-company-profile.html`
- `presentations/company-profile/dealix-company-profile.pdf`
- `reports/contracts/.gitkeep`
- `reports/customer_reports/.gitkeep`
- `reports/meetings/.gitkeep`
- `reports/pilot_reports/.gitkeep`
- `scripts/customer_experience_audit.sh`
- `scripts/dealix_command_room.py`
- `scripts/dealix_content_engine.py`
- `scripts/dealix_contract_generator.py`
- `scripts/dealix_customer_monthly_report.py`
- `scripts/dealix_daily_ops.py`
- `scripts/dealix_meeting_agenda.py`
- `scripts/dealix_outreach_kit.py`
- `scripts/dealix_outreach_tracker.py`
- `scripts/dealix_pilot_report.py`
- `scripts/dealix_proposal_generator.py`
- `scripts/dealix_renewal_tracker.py`
- `scripts/dealix_weekly_gtm_review.py`
- `scripts/integration_upgrade_verify.sh`
- `scripts/merge_research_targets.py`
- `scripts/ultimate_upgrade_verify.sh`
- `tests/launch/test_vertical_scorer.py`
- `tests/test_article_13_compliance.py`
- ... plus 11 more files

### PR #739

- `.gitignore`
- `Makefile`
- `auto_client_acquisition/email/daily_targeting.py`
- `data/saudi_icp_targets.json`
- `scripts/gmail_daily_outreach.py`
- `tests/test_gmail_daily_outreach.py`

## Executive recommendation

- If #732 is the cleaned resolution of #727, prefer #732 as canonical.
- Extract useful copy/targets from #739/#726 only if not duplicated.
- Extract architecture from #711 only if it improves `company-day` / revenue loop.
- Do not merge multiple competing daily outreach systems.
- Keep outbound as draft/review-first unless controlled-live gates pass.
