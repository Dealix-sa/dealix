# Live Send Safety Gate

The Live Send Safety verifier (`scripts/verify_live_send_safety.py`)
is the gate every outbound integration must pass before the env-level
"live send" switch can be flipped.

## What it does

1. Loads `registries/integration_registry.yaml`.
2. For each integration with `direction: outbound`:
   - confirms `frontend_direct_call_allowed: false`
   - confirms `approval_required` is set
   - confirms `requires_audit_write: true` (warns otherwise)
   - confirms `live_send_enable_flag` and `mock_mode_flag` are named
     for WhatsApp / Email / Moyasar
3. Scans `apps/web/**/*.{ts,tsx,js,jsx}` for:
   - secret names (`MOYASAR_SECRET_KEY`, `GREEN_API_TOKEN`,
     `GREEN_API_INSTANCE_ID`, `SMTP_PASSWORD`, `HUBSPOT_ACCESS_TOKEN`,
     `JWT_SECRET_KEY`, `GROQ_API_KEY`)
   - direct URLs to `api.green-api.com`, `api.moyasar.com`,
     `api.hubapi.com`, `graph.facebook.com`
4. Greps the wider repo for references to:
   `approval_queue`, `suppression`, `WHATSAPP_MOCK_MODE`,
   `WHATSAPP_ALLOW_LIVE_SEND`, `WHATSAPP_DAILY_LIMIT`.
   Missing references become WARN, not FAIL — they hint that a gate
   may be unimplemented.
5. Writes `/tmp/dealix_live_send_safety.PASS` on PASS. The
   production-env verifier reads this marker to allow
   `WHATSAPP_ALLOW_LIVE_SEND=true`.

## How to read a failure

- `frontend_leak:<file>:<line>`: a secret name or forbidden URL was
  found in the frontend bundle. Move the call to a server route under
  `api/internal/`.
- `integration[<id>]_kill_switches`: `live_send_enable_flag` or
  `mock_mode_flag` was missing in the registry. Add both.
- `integration[<id>]_approval`: outbound integration has no
  `approval_required`. Add it (A1, A2, or escalate).
- `integration[<id>]_audit`: WARN that `requires_audit_write` is
  false. Set it true unless the integration is read-only research.

## How to certify a brand-new integration

1. Add a block in `registries/integration_registry.yaml` with both
   kill switches and `frontend_direct_call_allowed: false`.
2. Route all calls through `api/internal/integration_gate.py`.
3. Add the secret names to `docs/security/RAILWAY_SECRET_HANDLING.md`.
4. Add the kill switches to
   `docs/security/LIVE_INTEGRATION_KILL_SWITCHES.md`.
5. Run `make live-send-safety` and ensure PASS.
6. Run `make production-certification` and ensure rollup is PASS.
