# Dealix SaaS Foundation Plan

## Executive decision

Dealix enters the market first as a **founder-led managed SaaS / AI Operating System**, then graduates into public self-serve SaaS after proof from paid pilots.

## What this PR adds

- Multi-tenant SaaS documentation.
- Tenant context and access guard contracts.
- Billing stub/manual invoice foundation.
- SaaS web shell for onboarding, app, command room, team, settings, billing, and audit.
- Safety checks proving outbound remains disabled by default.
- Commercial launch playbook and first Arabic offer.

## What this PR does not activate

- No live email sending.
- No live WhatsApp sending.
- No SMS sending.
- No automatic outbound.
- No live payment capture.
- No public self-serve signup.

## SaaS path

1. Founder-led sprint.
2. Paid beta workspaces.
3. Multi-tenant dashboard.
4. Usage and billing controls.
5. Controlled-live outbound after opt-in, approval, and compliance gates.
6. Public SaaS only after CI, Railway, tenant isolation, and billing reviews pass.

## Acceptance criteria

- Tenant context fails closed.
- Cross-tenant access is blocked by policy.
- Billing remains manual/stub-only.
- Outbound defaults remain false/draft-only.
- Commercial launch is founder-reviewed and manual-send only.

## Verdict

READY_FOR_FOUNDER_LED_COMMERCIAL_BETA.
