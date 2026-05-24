# Live-integration kill switches

A kill switch is a single boolean env var that immediately blocks an
outbound integration from sending real traffic. Each switch has:

- A clear **OFF** default (safe-by-default).
- A single **canonical** check in code — never duplicated.
- A **verifier** that fails if the canonical check is missing.

## WhatsApp

| Switch | Default | Effect when ON |
|---|---|---|
| `WHATSAPP_MOCK_MODE` | `true` (safe) | `WhatsAppClient.send_text` short-circuits with `whatsapp_mock_mode_true` before any HTTP call |
| `WHATSAPP_ALLOW_LIVE_SEND` | `false` | Required *in addition to* mock-mode off for `Settings.is_live_send_allowed` to be true |

The canonical guard is `Settings.is_live_send_allowed`. Direct callers
should NEVER read `whatsapp_allow_live_send` in isolation.

`scripts/verify_live_send_safety.py` fails the build if:
- `integrations/whatsapp.py` does not check `whatsapp_mock_mode`.
- `Settings.is_live_send_allowed` is absent.
- A FastAPI router imports `integrations.whatsapp` directly (bypassing
  approval queue / `whatsapp_safe_send`).

## Email

There is no single boolean; live sending is gated by:

- `auto_client_acquisition/email/daily_targeting.py` → `daily_email_limit`.
- `auto_client_acquisition/approval_center/approval_policy.py` →
  `csm_or_founder` approval required.

To stop email sending in an incident, set `SMTP_PASSWORD=""` (or empty
the provider key for `resend`/`sendgrid`) — the client will return a
configuration error rather than send.

## Payments (Moyasar)

Webhook verification uses `hmac.compare_digest` against
`MOYASAR_SECRET_KEY`. To stop accepting webhooks, unset
`MOYASAR_SECRET_KEY` — verification will fail and `dealix/payments/moyasar.py`
will return 400.

Outbound payment creation respects
`auto_client_acquisition/agent_os/agent_registry.py:ToolCategory.CHARGE_PAYMENT_LIVE`
which is **denied** for any agent not classified as compliance/L4.

## Verifying a kill switch

```bash
make live-send-safety
```

Should print `LIVE_SEND_SAFETY_VERDICT=PASS`. Any FAIL means a switch is
missing from the code path it is supposed to gate.
