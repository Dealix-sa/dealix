# SaaS Architecture Gate

## Purpose
Gate the moment Dealix moves from services + scripts to a SaaS surface that external customers self-serve.

## Pre-conditions (all required)
1. ≥ 3 paying customers on the same productized offer.
2. ≥ 2 documented retainer renewals.
3. ≥ 6 months of unit-economics data on the offer.
4. A clear, written description of the SaaS product (one page).
5. A capital plan signed by the founder describing how the build will be funded.
6. A trust review covering AI risk for the SaaS surface.
7. A security review of the data flows the SaaS surface will introduce.

## Architecture requirements
- Multi-tenant data isolation from day 1.
- Authentication via a vetted identity provider.
- Audit logging on all privileged actions.
- Backup + restore drill before any external billing.
- Public API only after the internal one is stable for 3 months.

## What the gate is NOT
- Not a license to abandon services.
- Not a license to mass-onboard before the product is ready.
- Not a deferral of any operating discipline.

## After the gate
- New code lives in a dedicated module (`saas/` or similar).
- New repo branch policy: SaaS PRs go through extra review.
- Founder remains accountable for incident response.

## Failure mode
If any pre-condition is missing and someone wants to start anyway: NO. Write down the reason for the urge in `productization/automation_backlog.md` and move on.
