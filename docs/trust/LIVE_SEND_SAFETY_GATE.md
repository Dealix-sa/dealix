# Live-send safety gate

Every outbound external action passes through the following gates, in
order. The first refusal wins; downstream gates are not consulted.

```
approval_queue
    ↓
policy_check                  ← auto_client_acquisition/approval_center/approval_policy.py
    ↓
suppression_check (PDPL)      ← opt-out list (permanent override)
    ↓
daily_limit                   ← email/daily_targeting.py / WHATSAPP_DAILY_LIMIT
    ↓
quiet_hours_check (KSA)       ← orchestrator/policies.py
    ↓
kill_switch                   ← Settings.is_live_send_allowed (must be True)
    ↓
audit_log_write               ← BEFORE adapter call
    ↓
integration_adapter           ← integrations/whatsapp.py (etc.)
    ↓
audit_log_update              ← AFTER adapter call with delivery status
```

## Code references (single source of truth)

| Gate | File |
|---|---|
| Approval queue | `auto_client_acquisition/approval_center/approval_policy.py` |
| Safe-send orchestration | `auto_client_acquisition/whatsapp_safe_send.py` |
| Consent guard | `auto_client_acquisition/safe_send_gateway/middleware.py` (`enforce_consent_or_block`, `SendBlocked`) |
| Quiet hours | `auto_client_acquisition/orchestrator/policies.py` (`is_in_quiet_hours`) |
| Kill switch | `core/config/settings.py` (`Settings.is_live_send_allowed`) |
| Integration adapter | `integrations/whatsapp.py` |

## What the verifier enforces

`scripts/verify_live_send_safety.py` runs static checks for:

- `whatsapp_mock_mode` AND `whatsapp_allow_live_send` are both consulted
  inside `integrations/whatsapp.py`.
- `whatsapp_safe_send.py` checks `approval_status`, `is_opted_out`, and
  quiet hours.
- `safe_send_gateway/middleware.py` exports `SendBlocked` and
  `enforce_consent_or_block`.
- `approval_policy.py` defines a whatsapp policy with a founder/approval
  handle.
- `dealix/payments/moyasar.py` uses `hmac.compare_digest`.
- `Settings.is_live_send_allowed` exists.
- No FastAPI router imports `integrations.whatsapp` directly.

## What it does **not** check

- That the audit log is actually written. The runtime path is responsible
  for calling the writer; the verifier cannot enforce it statically with
  confidence. Runtime tests cover this in `tests/`.
- That the actual founder pressed the approve button. That is recorded
  in the approval ledger, which the verifier cannot synthesise.

## Failure mode

If ANY gate above is missing, `make live-send-safety` exits non-zero and
`make production-certification` fails. The deploy is blocked.
