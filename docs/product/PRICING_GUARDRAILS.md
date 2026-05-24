# Pricing Guardrails

> Pricing is a policy. Founder owns it. Agents propose, founder approves.

## 1. Guardrails per rung (SAR)

| Rung | Floor | Ceiling | Notes |
|---|---|---|---|
| 1. Free Diagnostic | 0 | 0 | Always free |
| 2. Revenue Sprint | (guardrail) | (guardrail) | Founder sets per cycle |
| 3. Managed Pilot | (guardrail) | (guardrail) | Founder sets per cycle |
| 4. Revenue Desk Retainer | (guardrail/mo) | (guardrail/mo) | Founder sets per cycle |
| 5. Founder Command Center | (guardrail/mo) | (guardrail/mo) | Founder sets per cycle |
| 6. Enterprise OS | Custom | Custom | Founder-approved |
| 7. Partner / White-label | Custom | Custom | Founder-approved |

> Numbers are intentionally left to be filled by the founder in a private `dealix/transformation/pricing_state.yaml` (not in the public repo). Drafts must say "Within Pricing Guardrails (founder review)".

## 2. Rules

- **No discount over 10 % without founder approval.**
- **No refund commitment without founder approval.**
- **No payment plan over 90 days without founder approval.**
- **No multi-year commit without explicit clause review.**
- **No price for an unproven outcome.**

## 3. Currency

- KSA: SAR.
- GCC: AED / SAR.
- Multinational: USD with KSA local tax treatment for KSA entities.

## 4. Audit

Every pricing variance request and decision is recorded in audit.

## 5. Trust posture

A proposal containing a price outside guardrails must surface in `/approvals` before customer delivery. The Proposal Factory enforces this in code.
