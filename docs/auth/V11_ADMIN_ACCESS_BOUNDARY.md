# V11 Admin Access Boundary

## Internal routes

These pages contain operational data and should not be served to the public web in production:

- `/crm`, `/crm/*`
- `/operator`
- `/review-queue`
- `/outreach-lab`
- `/followups`
- `/command-center`, `/war-room`, `/pipeline`, `/kpi-finance`
- `/proof-vault`, `/deals`, `/quotes`, `/revenue`
- `/launch`
- `/client-portal/*` (except `/client-portal/demo`)

## Demo mode

When `NEXT_PUBLIC_DEMO_MODE=true`, internal routes render with **DEMO** badges and read from `business/_data/*.json`. No production traffic should run with this flag set.

## Production auth model

Two options, both supported by code already in `api/security/`:

1. **OIDC** (`oidc.py`): customer-supplied IdP. Recommended for enterprise.
2. **SAML 2.0** (`saml.py`): for customers that mandate SAML.

In both cases:
- MFA enforced (`mfa.py`, `mfa_policy.py`).
- SCIM provisioning ready (`scim.py`).
- Privileged actions logged via `privileged_audit.py`.

## Limitation

The Next.js admin pages currently rely on demo data files in the repo. Persistent production auth requires:
1. Wiring the customer IdP.
2. Pointing data fetches at the customer's database, not `business/_data/`.
3. Adding the middleware in `apps/web/middleware.ts`.

This is documented honestly. It is not pretended to be production-ready today.

## Env vars

- `DEALIX_ADMIN_PASSWORD` — basic-auth fallback until IdP is wired.
- `DEALIX_ADMIN_TOKEN` — token shared with operator scripts.
- `NEXT_PUBLIC_DEMO_MODE` — `true` for demo / development, omitted in production.
