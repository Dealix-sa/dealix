# Invoice Flow

## Current: Manual (via Moyasar dashboard)
1. Customer agrees to purchase
2. Create invoice in Moyasar: amount + description + customer email
3. Copy invoice URL
4. Send to customer via WhatsApp/email
5. Customer pays
6. Moyasar confirms (webhook if backend running, else dashboard)
7. Manual welcome email
8. Manual onboarding

## Future: Automated (after Railway deploy)
See `api/routers/webhooks.py` for the backend flow.

## Invoice numbering
Format: DLX-YYYY-NNNNN (sequential)

## VAT/ZATCA
Currently below threshold. Consult accountant when approaching 187,500 SAR annual.

---

## Document Standard Compliance

## Purpose
Defines this operating document's role inside Dealix Company OS.

## Owner
Sami (Founder). Reassign to the responsible operator when one is named.

## Review Cadence
Weekly until stable, then monthly.

## Inputs
- Relevant company data and signals.
- Founder decisions and customer evidence.

## Outputs
- Operating guidance, decisions, or templates produced by this document.
- Evidence captured for verification.

## Rules
- Must support revenue, delivery, trust, learning, or founder leverage.
- Must not introduce unsupported claims.
- Must preserve public/private boundaries.

## Metrics
- Completion status of the actions this document drives.
- Impact on revenue, delivery, trust, or founder leverage.

## Evidence
- Linked workflow, file, test output, customer interaction, or decision log.

## Last Reviewed
2026-05-23
