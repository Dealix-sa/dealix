# Dealix Enterprise Readiness Pack

This pack is shared with enterprise prospects after the first qualifying call. It is not a sales brochure — every section maps to an in-repo artifact a buyer's procurement or security team can inspect.

## What Dealix is

Dealix builds business operating systems on top of the customer's existing tools (CRM, WhatsApp, reviews, reports, billing). It does not replace systems; it routes data, automates approvals, and produces proof.

## Production posture

| Area | Posture |
| --- | --- |
| Outreach | Drafts only. Human approves every outbound message. No autonomous WhatsApp / email send. |
| Payments | Provider stubs only. No card data handled. Live payments require Moyasar / Stripe credentials + signed DPA. |
| Data | Customer data stays in customer-owned systems. Dealix processes copies for the agreed scope only. |
| AI | Deterministic-first. Optional LLM-assist behind a feature flag with full audit log. |
| Identity | OIDC + SAML stubs land in `api/security/`; production rollout requires customer IdP configuration. |

## Mapped artifacts

- `SECURITY_QUESTIONNAIRE_TEMPLATE.md`
- `DATA_BOUNDARY_STATEMENT.md`
- `AI_GOVERNANCE_STATEMENT.md`
- `HUMAN_REVIEW_STATEMENT.md`
- `SERVICE_LEVEL_BOUNDARIES.md`
- `IMPLEMENTATION_ASSURANCE_PLAN.md`
- `ENTERPRISE_BUYER_FAQ_AR.md`, `ENTERPRISE_BUYER_FAQ_EN.md`
- `apps/web/app/enterprise-readiness/page.tsx`

## How buyers evaluate Dealix

1. Read `ENTERPRISE_BUYER_FAQ`.
2. Open `/enterprise-readiness` for the live posture summary.
3. Walk the 7-day workflow review during the diagnostic sprint.
4. Receive a proof report. Compare against `IMPLEMENTATION_ASSURANCE_PLAN`.
5. Sign MSA + SOW from `business/contracts/`.

## What this pack is not

Not legal advice. Not a SOC 2 attestation. Not a contractual SLA. These are operational scaffolds the founder reviews and the buyer signs off.
