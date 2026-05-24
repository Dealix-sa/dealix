# Email Approval Gate

Email sends are class **A2** (transactional notifications to a single
opted-in recipient) or **A3** (bulk / cold). Same gate as WhatsApp.

## Hard rules

1. No bulk send. Period. The system is built for one-to-one founder-
   approved messages.
2. No template that names a price, a discount, or a guarantee.
3. Every send must come through
   `api.internal.integration_gate.request_external_send(
     integration_id="email_smtp", ...)`.
4. The `From` header is `dealix_founder_email` (configured via
   `DEALIX_FOUNDER_EMAIL`). No spoofing.
5. SPF / DKIM / DMARC must be aligned before live send is enabled;
   misalignment is a deliverability incident.

## Envs

| Name | Default | Note |
|---|---|---|
| `EMAIL_MOCK_MODE` | true | Set false only after safety gate is green. |
| `EMAIL_ALLOW_LIVE_SEND` | false | Flip last. |
| `EMAIL_DAILY_LIMIT` | (unset) | Set to a small number first (5-10). |
| `SMTP_USER` | — | Provided by the email provider. |
| `SMTP_PASSWORD` | — | Provided by the email provider. Never in repo. |

## Suppression

Use the same `private_ops/outreach/suppression_list.csv`. Channel column
should be `email` for email suppressions. Any unsubscribe immediately
appends a row. The gate refuses any send to a suppressed handle.

## Audit

Same as WhatsApp: one JSON line per gate decision, recipient handle
hashed, content summary recorded (not the full body).
