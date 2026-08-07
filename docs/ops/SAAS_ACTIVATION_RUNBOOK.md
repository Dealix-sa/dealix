# Dealix SaaS Activation Runbook

## Positioning

Dealix is a Saudi B2B AI Company OS: a governed operating layer that connects company data, revenue workflows, approvals, proof, and AI agents. It complements the customer CRM and operational tools rather than replacing them.

## Repository readiness

Repository readiness requires both backend and browser-journey gates.

```bash
python scripts/verify_saas_foundation.py --json
pytest -q --no-cov \
  tests/test_deployment_identity_runtime.py \
  tests/test_saas_onboarding_contract.py \
  tests/test_saas_foundation_verifier.py \
  tests/test_saas_web_journey_contract.py

cd apps/web
npm ci
NEXT_PUBLIC_DEALIX_API_BASE=https://api.example.invalid npm run typecheck
NEXT_PUBLIC_DEALIX_API_BASE=https://api.example.invalid npm run build
```

A `READY` verifier result plus successful focused tests and web build prove only repository contracts. They do not prove production domains, credentials, migrations, email delivery, payments, or protected routes.

## Verified repository contracts

- tenant model and tenant-scoped operational records;
- canonical tenant RBAC, refresh sessions, MFA, and password reset;
- SAR plans, subscriptions, invoices, seats, feature flags, and usage records;
- public self-serve plan discovery and signup;
- automatic JWT session creation after signup;
- browser customer routes authenticated through Bearer JWT without exposing a shared platform API key;
- tenant context derived from the authenticated user, not `x-tenant-id` supplied by the browser;
- single-use, expiring, hashed team invitations;
- invitation roles restricted to canonical tenant roles;
- per-invitation approval plus operator-level email policy;
- manual invite-link recovery when email is disabled or fails;
- one canonical compatibility implementation for both onboarding and legacy auth invite paths;
- runtime release identity sourced from Vercel/Railway before generic build fallbacks;
- audit, PDPL consent, suppression, payment-evidence, proof, and approval-first outbound records.

## Canonical customer lifecycle

1. The browser loads only `free`, `starter`, and `growth` plans from `/api/v1/onboarding/plans`.
2. A company creates a tenant through `/api/v1/onboarding/signup`.
3. Dealix creates standard tenant roles and assigns the first user `tenant_admin`.
4. Dealix creates the selected subscription and plan-derived feature flags.
5. The browser logs in through `/api/v1/auth/login`, stores the access and refresh tokens, and opens the customer dashboard.
6. Dashboard data is fetched with the Bearer token; tenant scope comes from the validated JWT user.
7. The administrator completes the onboarding wizard.
8. Team invitations are created as hashed, expiring, single-use records with seat-limit enforcement.
9. Email delivery occurs only when the administrator approves that invitation and `EMAIL_ALLOW_LIVE_SEND` is enabled by the operator.
10. Usage, payments, proofs, approvals, and audit events remain tenant-scoped.

## Canonical deployment architecture

- Vercel project `dealix-web`: Next.js frontend rooted at `apps/web`.
- Railway: FastAPI, workers, PostgreSQL, migrations, and `api.dealix.me`.
- Frontend environment:

```text
NEXT_PUBLIC_DEALIX_API_BASE=https://api.dealix.me
```

`NEXT_PUBLIC_API_URL` remains a temporary compatibility alias. Never expose `API_KEYS`, `ADMIN_API_KEYS`, payment secrets, or provider credentials through `NEXT_PUBLIC_*` variables.

## Production activation sequence

### Gate 1 — Railway backend (#898)

Required non-secret evidence:

- a valid Railway project deployment credential is installed;
- the deployment workflow exits successfully;
- `alembic upgrade head` completes once through the governed deployment path;
- `/healthz`, `/version`, and `/api/v1/meta` return HTTP 200;
- their `git_sha` matches Railway deployment metadata;
- invalid payment-webhook signatures remain rejected.

### Gate 2 — Protected-route trust (#884)

Required non-secret evidence:

- one dedicated smoke key is accepted by Railway production;
- the identical value is stored as GitHub Actions secret `DEALIX_SMOKE_API_KEY`;
- protected-route smoke passes without weakening authentication;
- no secret value appears in output, issues, comments, or logs.

### Gate 3 — Public architecture (#894)

Required non-secret evidence:

- `dealix.me` and `www.dealix.me` serve the Next.js frontend from `dealix-web`;
- `api.dealix.me` serves the Railway FastAPI backend;
- `/signup` remains the self-serve page and is not redirected to `/book`;
- frontend signup, login, refresh, `/auth/me`, and dashboard calls reach `api.dealix.me`;
- browser bundles contain no shared platform/admin API key;
- build status alone is never accepted as runtime proof.

### Gate 4 — Database and disposable-tenant proof

Create a disposable tenant and record IDs/statuses only, never credentials or tokens.

Prove:

- plans endpoint returns only `free`, `starter`, and `growth`;
- signup creates one tenant, four canonical roles, one administrator, one subscription, and plan feature flags;
- login succeeds and refresh rotation revokes the previous refresh token;
- `/auth/me` identifies the authenticated tenant;
- dashboard returns only that tenant's data;
- tenant A cannot read or mutate tenant B data;
- a viewer invite can be accepted once only;
- a second acceptance attempt is rejected;
- active users plus pending invitations enforce the seat limit;
- `send_email=false` contacts no provider;
- provider-disabled and provider-failure paths return manual-share recovery without claiming delivery;
- audit/log data contains no password, access token, refresh token, invite token, or secret value;
- the disposable tenant and associated records can be removed through the governed cleanup procedure.

### Gate 5 — Browser proof

Against the preview/frontend project:

1. Open `/signup`.
2. Confirm plan names, prices, and limits match the plans endpoint.
3. Create the disposable account.
4. Confirm automatic login and dashboard redirect.
5. Refresh the page and confirm the session remains valid.
6. Exercise refresh-token rotation by expiring/replacing the access token in a controlled test.
7. Confirm 401/403 clears the browser session and returns to `/login`.
8. Confirm no request sends `x-tenant-id` or `X-API-Key` from the browser.

### Gate 6 — Dealix on Dealix

Run only the canonical Company OS runtime in draft-only mode:

```bash
python scripts/commercial/run_company_os_daily.py --client dealix --mode draft-only --limit 50
python scripts/commercial/run_self_improvement_daily.py --client dealix --mode draft-only
python scripts/commercial/run_weekly_proof_pack.py --client dealix --mode draft-only
```

The cycle must produce one priority queue, one approval queue, one proof ledger, one revenue state, and one learning report. No parallel Company OS runner may be scheduled. Revenue remains zero until `payment_received` evidence exists.

## Release evidence packet

Record only:

- branch/head and merged commit SHA;
- GitHub workflow run IDs and conclusions;
- Vercel/Railway deployment IDs and environment;
- migration revision before/after;
- HTTP statuses and sanitized response fields;
- disposable tenant ID and cleanup status;
- proof-pack artifact location;
- rollback decision and owner.

Do not record secret values, customer credentials, raw tokens, payment card data, or personal data beyond the minimum approved test identity.

## Claim boundary

Allowed after repository checks pass:

> Dealix has a verified multi-tenant SaaS foundation and is prepared for controlled production activation.

Allowed only after all production gates and disposable-tenant proof pass:

> Dealix is production-ready for controlled Saudi B2B SaaS onboarding.

Never claim customer outcomes, recognized revenue, successful delivery, email delivery, payment success, or production readiness without corresponding evidence.

## Rollback principles

- Roll back only the newest credential, domain, migration, deployment, or frontend release change.
- Do not disable authentication, tenant isolation, production secret validation, or payment signature checks to make smoke tests green.
- Do not expose secret values during diagnosis.
- Do not count a subscription, invoice, or payment as revenue until `payment_received` evidence is captured.
