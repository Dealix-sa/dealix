# Add Commercial Readiness Control Center

## Summary

This change adds a safe, founder-led commercial readiness layer for Dealix without enabling live outbound.

## What changed

- Added Arabic Commercial Readiness Control Center docs.
- Added Commercial Product Catalog covering the first products to sell.
- Added Arabic sales foundation pack with discovery questions and objection handling.
- Added `scripts/commercial/commercial_readiness_check.py`.
- Added `scripts/commercial/generate_commercial_go_live_pack.py`.
- Added a lightweight commercial pack test.
- Adds Makefile targets after Makefile patch:
  - `make commercial-check`
  - `make commercial-pack`
  - `make commercial-day`

## Safety

Live outbound remains disabled by default:

```env
EXTERNAL_SEND_ENABLED=false
EMAIL_SEND_ENABLED=false
WHATSAPP_SEND_ENABLED=false
WHATSAPP_ALLOW_LIVE_SEND=false
SMS_SEND_ENABLED=false
OUTBOUND_MODE=draft_only
```

This layer generates only local reports/templates/ledgers. It does not send email, WhatsApp, SMS, or any external request.

## Validation

Recommended commands:

```bash
python -m compileall -q scripts/commercial
python -m pytest -q tests/test_commercial_pack.py
make commercial-check
make commercial-pack
```

## Founder next step

Run:

```bash
make commercial-day
```

Then review `reports/commercial/latest.md` and manually approve any external communication.
