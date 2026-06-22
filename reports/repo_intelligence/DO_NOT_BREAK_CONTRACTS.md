# Dealix DO_NOT_BREAK_CONTRACTS.md

**Date:** 2026-06-23

These contracts must not be broken by any PR.

## Safety contracts

1. **No automatic external send.**
   - Test: `tests/test_no_auto_send.py`
   - Script: `scripts/verify_no_auto_external_send.py`
   - Default env: `EXTERNAL_SEND_ENABLED=false`, `OUTBOUND_MODE=draft_only`

2. **No fake clients, testimonials, or guaranteed ROI.**
   - Test: `tests/test_no_guaranteed_revenue_claims.py`
   - Register: `dealix/registers/no_overclaim.yaml`

3. **WhatsApp live send requires opt-in and approved template.**
   - Policy: `app/outbound/policy_gate.py::can_send_whatsapp`
   - Conditions:
     - `EXTERNAL_SEND_ENABLED=true`
     - `WHATSAPP_SEND_ENABLED=true`
     - `WHATSAPP_ALLOW_LIVE_SEND=true`
     - `WHATSAPP_SEND_MODE=template_only`
     - `contact.whatsapp` exists
     - `whatsapp_opt_in=true`
     - `whatsapp_opt_out=false`
     - approved template exists
     - `message.status=approved`
     - daily limit not exceeded

4. **Email live send requires unsubscribe, suppression list, verified target, approval, source_url, and rate limits.**
   - Policy: `app/outbound/policy_gate.py::can_send_email`
   - Conditions:
     - `EXTERNAL_SEND_ENABLED=true`
     - `EMAIL_SEND_ENABLED=true`
     - `OUTBOUND_MODE=controlled_live`
     - `contact.email` exists
     - `email_opt_out=false`
     - `source_url` exists
     - `verification_status=approved_to_send`
     - `message.status=approved`
     - unsubscribe present
     - no fake ROI/testimonials
     - daily limit not exceeded

## Ledger contracts

5. **Prospects ledger must include:**
   - `company_name`, `sector`, `city`, `website`, `source_url`, `verification_status`, `confidence`, `recommended_product`, `pain_hypothesis`, `owner_decision`

6. **Outreach log must include:**
   - `company_name`, `email`, `channel`, `status`, `draft_path`, `owner_decision`

7. **No committing real target lists or generated reports.**
   - `.gitignore` covers `data/outreach/`, `reports/`, `outbox/`, `ledgers/private/`

## Env contracts

8. **`.env.example` must keep all live-send flags false.**
   - `EXTERNAL_SEND_ENABLED=false`
   - `EMAIL_SEND_ENABLED=false`
   - `WHATSAPP_SEND_ENABLED=false`
   - `WHATSAPP_ALLOW_LIVE_SEND=false`
   - `SMS_SEND_ENABLED=false`
   - `OUTBOUND_MODE=draft_only`

9. **`.env.production.example` (when created) must keep safe defaults.**

## Build/test contracts

10. **`python -m compileall -q scripts api app dealix` must pass.**
11. **P0 safety tests must pass:**
    - `tests/test_p0_launch_stabilization.py`
    - `tests/test_no_auto_send.py`
    - `tests/test_no_guaranteed_revenue_claims.py`
12. **Frontend build must pass OR exact blocker documented.**

## Code organization contracts

13. **Do not create new modules with overlapping names unless the old one is archived.**
    - e.g., do not create a second `revenue/` or `brain/` folder; reuse `scripts/revenue/` and `scripts/brain/`.

14. **Generated artifacts go to `reports/`, `outbox/`, `data/outreach/` and must not be committed.**

## PR contract

15. **Every PR must:**
    - Have a clear title and scope
    - Include tests or a documented reason for no tests
    - Pass `verify_no_auto_external_send.py`
    - Include a final report
    - Not push directly to `main`
