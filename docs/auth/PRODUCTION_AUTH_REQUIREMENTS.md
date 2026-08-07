# Production Auth Requirements

## Hard requirements before going to production

1. **IdP wired**: OIDC or SAML, with customer-supplied IdP for customer-facing tenants.
2. **MFA enforced** on every admin login.
3. **Session timeout** ≤ 12 hours of inactivity.
4. **Privileged actions** logged: who, what, when, what changed.
5. **`NEXT_PUBLIC_DEMO_MODE`** is unset in production.
6. **`DEALIX_ADMIN_PASSWORD`** is unset; password-only access is not allowed.
7. **Secrets** loaded from secret manager, never from the repo.
8. **Audit log** writes are append-only.
9. **Data fetches** target the customer database, not `business/_data/`.
10. **Rate limiting** in front of every mutation endpoint.

## Soft requirements (recommended for enterprise)

- SCIM provisioning enabled.
- IP allowlist for super-admin actions.
- WAF in front of `/api/admin/*` and `/api/payments/*`.
- Quarterly access review.

## Current status

- IdP code present: OIDC + SAML stubs (`api/security/*.py`). Not yet wired to a deployed IdP.
- MFA scaffolding present (`api/security/mfa.py`). Activation gated by customer choice.
- SCIM scaffolding present (`api/security/scim.py`). Wiring is per-customer.
- Admin pages currently read `business/_data/`. Production wiring requires switching the data layer.

## Gap to close before first enterprise deal

The first enterprise deal must drive:
- Choosing an IdP (Okta / Azure AD / Google Workspace).
- Wiring it through `oidc.py` or `saml.py`.
- Migrating CRM data from `business/_data/scored_leads.json` to the customer's database.
- Wiring `apps/web/middleware.ts` to enforce the IdP session.
