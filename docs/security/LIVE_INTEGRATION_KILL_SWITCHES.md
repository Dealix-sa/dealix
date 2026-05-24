# Live Integration Kill Switches

Each outbound integration has two switches plus a daily limit. They
exist so a single env flip stops the world.

| Integration | live_send_enable_flag | mock_mode_flag | daily_limit_env | A-class |
|---|---|---|---|---|
| WhatsApp (GreenAPI) | `WHATSAPP_ALLOW_LIVE_SEND` | `WHATSAPP_MOCK_MODE` | `WHATSAPP_DAILY_LIMIT` | A2 |
| Email (SMTP) | `EMAIL_ALLOW_LIVE_SEND` | `EMAIL_MOCK_MODE` | `EMAIL_DAILY_LIMIT` | A2 |
| Moyasar (payments) | `MOYASAR_ALLOW_LIVE_CAPTURE` | `MOYASAR_MOCK_MODE` | — | A2 / ESCALATE |
| HubSpot CRM | `HUBSPOT_ALLOW_LIVE_WRITE` | `HUBSPOT_MOCK_MODE` | — | A1 |

## Rules

1. **Defaults are safe**: `*_MOCK_MODE` defaults to true, `*_ALLOW_*`
   defaults to false. The integration gate
   (`api/internal/integration_gate.py`) interprets unset envs as the
   safe value.
2. **You cannot enable both mock and live**: the production-env
   verifier fails the build if `WHATSAPP_MOCK_MODE=true` and
   `WHATSAPP_ALLOW_LIVE_SEND=true`.
3. **Daily limit is a real number, not infinity**: the gate refuses to
   call out if the daily-limit env is set to a value the caller has
   already exhausted today.
4. **A3 is never automatic**: any A3 action requires a fresh founder
   escalation in `approval_queue.csv` with a unique decision id.
5. **Live send only after the safety gate has just passed**: the live
   send safety verifier writes `/tmp/dealix_live_send_safety.PASS` on
   green; the production-env verifier checks for that file before
   accepting `WHATSAPP_ALLOW_LIVE_SEND=true`. Re-running the gate is
   the path to flipping the switch.

## How to actually flip a switch (WhatsApp example)

```bash
# 1. Make sure the static gates are green
make production-certification

# 2. Re-run the safety verifier on its own (this writes the marker)
make live-send-safety

# 3. In Railway → Variables (UI only, never in code):
#    WHATSAPP_DAILY_LIMIT=10
#    WHATSAPP_MOCK_MODE=false
#    WHATSAPP_ALLOW_LIVE_SEND=true

# 4. Redeploy.
# 5. Verify with a single A2 send that you personally approve.
# 6. Watch private_ops/trust/audit_log.jsonl tail for the next 24h.
```

If anything looks off — even a small unexpected log line — flip
`WHATSAPP_ALLOW_LIVE_SEND=false` and walk back.

## Kill-everything switch

There isn't a single env var for it on purpose. The way to kill all
outbound sending is to set `*_ALLOW_*=false` on each integration. This
is by design: it forces an operator to acknowledge what they are
stopping, integration by integration, with an audit trail.
