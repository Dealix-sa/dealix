# Dealix Ultimate Commercial OS — Implementation Audit

Date: 2026-06-11
Auditor: Kimi Code CLI
Scope: Repo after first commercial OS layer

## Findings Summary

| Category | Count | Severity |
|----------|-------|----------|
| Missing scripts | 8 | Critical |
| Missing schemas | 6 | Critical |
| Missing shared library | 1 | Critical |
| Missing web pages | 4 | High |
| Broken build path | 1 | High |
| Missing tests | 6 | High |
| Weak data boundaries | 3 | Medium |
| Missing docs | 5 | Medium |

---

## 1. Missing Core Scripts

- `scripts/verify_dealix_ultimate_os.py` — does not exist. No master verification.
- `scripts/import_leads_csv.py` — exists as `scripts/import_leads.py` but it POSTs to remote API; no local CSV→JSON pipeline with backup/dedupe.
- `scripts/score_leads.py` — does not exist.
- `scripts/generate_outreach_drafts.py` — does not exist.
- `scripts/generate_proposal.py` — exists in other forms but not the V2 CLI with `--account-id`, `--offer`, `--lang`.
- `scripts/generate_daily_ceo_brief.py` — does not exist as standalone script.
- `scripts/check_no_secrets.py` — does not exist.
- `scripts/production_readiness_check.py` — does not exist.

## 2. Missing Data Schemas

- `business/_schemas/lead.schema.json` — no unified lead schema.
- `business/_schemas/account.schema.json` — no account schema.
- `business/_schemas/proposal.schema.json` — no proposal schema.
- `business/_schemas/delivery.schema.json` — no delivery schema.
- `business/_schemas/source.schema.json` — no source registry schema.
- `business/_schemas/daily_pack.schema.json` — no daily pack schema.

## 3. Missing Shared Library

- `scripts/lib/` — directory does not exist.
- Every script hardcodes its own paths; no `paths.py`, `json_store.py`, `validation.py`.

## 4. Missing Web Pages

- `apps/web/app/outreach-lab/page.tsx` — missing.
- `apps/web/app/operator/page.tsx` — missing.
- `apps/web/app/legal/page.tsx` — missing.
- `apps/web/app/pipeline/page.tsx` — missing.

## 5. Build / Type Errors

- `apps/web/node_modules` — missing. `npm run typecheck` fails with `sh: 1: tsc: not found`.
- `apps/web/package.json` scripts reference `next` and `tsc` but dependencies are not installed in this environment.

## 6. Weak Data Boundaries

- No `demo` flag on demo leads.
- No `lawful_basis_note` field on lead records.
- No `review_status` on outreach drafts.

## 7. Missing Tests

- `tests/test_lead_scoring.py` — missing.
- `tests/test_import_leads.py` — missing.
- `tests/test_draft_safety.py` — missing.
- `tests/test_proposal_generator.py` — missing.
- `tests/test_json_schemas.py` — missing.
- `tests/test_no_auto_send.py` — missing.

## 8. Missing Docs

- `docs/pdf/PDF_EXPORT_PLAN.md` — missing.
- `docs/security/SECRET_HANDLING.md` — missing.
- `docs/deploy/FRONTEND_DEPLOYMENT.md` — missing.
- `docs/deploy/BACKEND_DEPLOYMENT.md` — missing.
- `business/commercial/FIRST_100_LEADS_PLAN.md` — missing.

## Exact Files to Fix

1. Create `scripts/lib/paths.py` — central path registry.
2. Create `scripts/lib/json_store.py` — atomic write with backup.
3. Create `scripts/lib/validation.py` — lead record validator.
4. Create `scripts/lib/scoring.py` — deterministic scoring functions.
5. Create `scripts/lib/drafts.py` — safe draft generation.
6. Create `scripts/lib/slugs.py`, `dates.py`, `safety.py` — utilities.
7. Create all schema JSON files under `business/_schemas/`.
8. Create all data JSON files under `business/_data/`.
9. Rewrite/create `scripts/import_leads_csv.py`, `score_leads.py`, `generate_outreach_drafts.py`, `generate_proposal.py`, `generate_daily_ceo_brief.py`.
10. Create `scripts/update_account_stage.py`, `add_account_note.py`, `add_followup.py`, `mark_reviewed.py`, `generate_pipeline_report.py`.
11. Create web pages: `outreach-lab`, `operator`, `legal`, `pipeline`.
12. Create API route: `apps/web/app/api/health/commercial-os/route.ts`.
13. Create `connectors/` stubs.
14. Create `scripts/check_no_secrets.py`.
15. Create `scripts/production_readiness_check.py`.
16. Create tests.
17. Update `.env.example` with new placeholders.
18. Update `README.md` with operator flow.
