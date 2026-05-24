# Email approval gate

Mirrors `WHATSAPP_APPROVAL_GATE.md`, with email-specific differences.

## Pipeline

1. **Intake.** Draft created by an L1 or L2 agent.
2. **Approval.** CSM or founder may approve (lower bar than WhatsApp).
   See `auto_client_acquisition/approval_center/approval_policy.py`:
   `max_auto_approve_risk = "low"`.
3. **Compliance check.** `auto_client_acquisition/email/compliance.py`
   verifies CAN-SPAM / PDPL requirements (unsubscribe link, sender
   identity, opt-in provenance).
4. **Daily limit.** `auto_client_acquisition/email/daily_targeting.py`
   enforces `daily_email_limit` (default 50). Exceeding triggers a
   queued send for the next day, never a hard fail.
5. **Send.** `gmail_send.py` (or `resend`/`sendgrid` depending on
   `EMAIL_PROVIDER`). Requires OAuth token + refresh path.
6. **Audit write.** Same as WhatsApp.

## Suppression

PDPL opt-out is permanent and overrides every other state. Email
suppression list lives alongside the WhatsApp one — both share the same
canonical `enforce_consent_or_block` middleware.

## Live cutover checklist

- [ ] `EMAIL_PROVIDER` chosen and credentials present (`SMTP_USER` +
      `SMTP_PASSWORD`, or `RESEND_API_KEY`, or `SENDGRID_API_KEY`).
- [ ] `SMTP_FROM` set.
- [ ] Compliance check returns OK for a smoke message.
- [ ] Daily limit ≤ 50 for the first 7 days.
