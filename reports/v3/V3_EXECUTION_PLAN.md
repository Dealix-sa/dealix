# Dealix V3 Execution Plan

## Phase 0 — Audit & Branch Setup ✅
- Create branch `feature/dealix-commercial-os-v3-final`
- Audit repo state, list broken/weak areas
- Write audit reports

## Phase 1 — Daily Operator Flow
- Create `scripts/dealix_daily_operator.py`
- Orchestrate: secrets check → OS verify → lead import → scoring → outreach drafts → follow-ups → prospect pack → proposal → CEO brief → pipeline report → summary
- Outputs to `reports/operator/`, `business/reports/exports/`, etc.
- Update docs

## Phase 2 — Founder Dashboard Data Exports
- Create `scripts/generate_founder_dashboard_data.py`
- Output `business/_generated/founder-dashboard.json`
- Create `apps/web/lib/generated/founder-dashboard.ts` mirror
- Create API route `apps/web/app/api/company-os/founder-dashboard/route.ts`
- Update pages to use data where feasible

## Phase 3 — Lead Quality & Persuasion
- Write `business/scoring/LEAD_SCORING_MODEL.md`
- Write `business/persuasion/` libraries
- Write `business/sales-machine/` taxonomy and matching rules
- Create 8 industry OS docs under `business/industries/`
- Create `scripts/score_leads.py` and `scripts/generate_outreach_drafts.py`

## Phase 4 — Proposal & Offer Closing System
- Create `business/offers/` (7 offer files)
- Create `business/closing/` (playbooks, scripts, negotiation, deal desk, red flags)
- Improve `scripts/generate_proposal.py` and `scripts/review_proposal_quality.py`

## Phase 5 — Website Conversion Upgrade
- Build reusable components in `apps/web/components/`
- Create/update pages per plan
- Create `/book` page
- Ensure typecheck and build pass

## Phase 6 — Governance, Security, No-Spam Lock
- Create governance docs and security docs
- Create `scripts/check_no_secrets.py`
- Create `tests/test_no_auto_send.py`
- Update `scripts/verify_dealix_ultimate_os.py`

## Phase 7 — Deployment & Production Readiness
- Create `docs/deploy/` docs
- Create `scripts/post_deploy_smoke.py`
- Improve `scripts/production_readiness_check.py`
- Run readiness check

## Phase 8 — Tests & CI Finalization
- Create/update test files
- Update `.github/workflows/ci.yml` or create `dealix-ultimate-os-check.yml`
- Ensure demo mode passes without API keys

## Phase 9 — Finalize README, PR Body, Push
- Update READMEs and operator runbooks
- Write final summary and PR body
- Final checks, commit, push, create PR

## Safety Rules
- No auto-send outreach.
- All drafts require human review.
- No secrets committed.
- Demo mode works without API keys.
