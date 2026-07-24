# Dealix SaaS Activation Runbook

## Positioning

Dealix is a Saudi B2B AI Company OS: a governed operating layer that connects company data, revenue workflows, approvals, proof, and AI agents. It is not positioned as a replacement CRM.

## What repository readiness means

The repository is SaaS-foundation ready only when the deterministic verifier passes. The verifier covers:

- tenant model and tenant-scoped records;
- canonical RBAC, sessions, MFA, and password reset;
- plans, subscriptions, invoices, seats, and usage metering;
- self-serve tenant signup and onboarding profile;
- single-use hashed team invitations;
- audit, PDPL consent, suppression, and provenance records;
- payment evidence and proof reports;
- approval-first outbound records.

Run:

```bash
python scripts/verify_saas_foundation.py
pytest -q tests/test_saas_onboarding_contract.py tests/test_saas_foundation_verifier.py
```

A `READY` result proves these repository contracts. It does not prove that production domains, secrets, migrations, or protected routes are live.

## Canonical customer lifecycle

1. A company creates a tenant through `/api/v1/onboarding/signup`.
2. Dealix creates the standard tenant roles and assigns the first user as `tenant_admin`.
3. The tenant receives a plan and subscription record in SAR.
4. The administrator completes the onboarding wizard.
5. Team invitations are created as hashed, expiring, single-use records.
6. External delivery remains manual and approval-first until a reviewed transactional-email transport is enabled.
7. Usage, payments, proofs, approvals, and audit events remain tenant-scoped.

## Production activation sequence

### Gate 1 — Railway backend

Close #898 with non-secret evidence:

- valid project deployment credential installed;
- deployment workflow exits successfully;
- migration command completes;
- `/healthz`, `/version`, and `/api/v1/meta` return HTTP 200;
- invalid payment webhook signatures remain rejected.

### Gate 2 — Protected-route trust

Close #884 with non-secret evidence:

- one dedicated smoke key is accepted by Railway production;
- the identical value is stored in GitHub Actions as `DEALIX_SMOKE_API_KEY`;
- protected-route smoke passes without weakening authentication;
- no key value appears in output, issues, or logs.

### Gate 3 — Public architecture

Close #894 with non-secret evidence:

- `dealix.me` and `www.dealix.me` serve the Next.js frontend from Vercel;
- `api.dealix.me` serves the FastAPI backend from Railway;
- frontend requests use `NEXT_PUBLIC_DEALIX_API_BASE=https://api.dealix.me`;
- build status alone is never accepted as runtime proof.

### Gate 4 — Database and tenant proof

```bash
alembic upgrade head
python scripts/verify_saas_foundation.py
pytest -q tests/test_saas_onboarding_contract.py tests/test_saas_foundation_verifier.py
```

Then prove, using a disposable tenant:

- signup creates exactly one tenant, four canonical roles, one administrator, and one subscription;
- login and refresh-token rotation succeed;
- a viewer invitation can be created and accepted once only;
- a second acceptance attempt is rejected;
- tenant A cannot read or mutate tenant B data;
- seat limits include active users and pending invitations;
- audit metadata contains no credentials or invitation token.

### Gate 5 — Company OS proof

Run Dealix on Dealix first:

```bash
python scripts/commercial/run_company_os_daily.py --client dealix --mode draft-only --limit 50
python scripts/commercial/run_self_improvement_daily.py --client dealix --mode draft-only
python scripts/commercial/run_weekly_proof_pack.py --client dealix --mode draft-only
```

The canonical daily runtime must produce one priority queue, one approval queue, one proof ledger, one revenue state, and one learning report. Parallel Company OS runners must not be scheduled.

## Launch claim boundary

Allowed after repository checks pass:

> Dealix has a verified multi-tenant SaaS foundation and is prepared for controlled production activation.

Allowed only after all production gates and disposable-tenant proof pass:

> Dealix is production-ready for controlled Saudi B2B SaaS onboarding.

Never claim customer outcomes, recognized revenue, successful delivery, or production readiness without corresponding evidence.

## Rollback principles

- Roll back only the newest credential, domain, migration, or deployment change.
- Do not disable authentication or production secret validation to make smoke tests green.
- Do not expose secret values during diagnosis.
- Do not count a subscription, invoice, or payment as revenue until payment evidence is captured.
