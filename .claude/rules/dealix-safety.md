# Dealix Safety Rules

## Outbound — NEVER enable live send by default

These must remain false in every session unless a controlled-live approval PR has been merged:

```
EXTERNAL_SEND_ENABLED=false
EMAIL_SEND_ENABLED=false
WHATSAPP_SEND_ENABLED=false
WHATSAPP_ALLOW_LIVE_SEND=false
SMS_SEND_ENABLED=false
OUTBOUND_MODE=draft_only
```

Allowed outputs: drafts, proposals, WhatsApp payload drafts, email drafts, approval cards, command room reports, proof packs, audit logs, classification results.

Forbidden: automatic WhatsApp/SMS/email sending, cold outbound without opt-in, LinkedIn scraping/automation, sending without founder approval.

## Secrets — NEVER commit or print

- Never commit `.env`, API keys, tokens, or credential values.
- Never print secret values in logs, tests, markdown files, or PR bodies.
- Generate secrets locally with `python -c "import secrets; print(secrets.token_hex(32))"` and paste only into Railway/GitHub Secrets UI.
- Run `python3 scripts/ops/security_smoke_ci.py` to verify no secrets leaked.

## Fake data — NEVER create

- No fake customers, fake logos, fake testimonials.
- No guaranteed ROI claims or fabricated revenue numbers.
- Use hypothesis language: "we expect", "the goal is", "we will measure".

## Production secret guard — NEVER remove

`api/main.py:_validate_production_secrets` rejects insecure production startup.
Do not weaken or remove it. If Railway fails, fix billing and env vars — not security.

## Stop conditions

Stop immediately and report if:
- A committed secret is found anywhere in the repo.
- A change would enable live outbound.
- Production secret validation would need to be removed.
- You cannot determine whether a change is safe.
