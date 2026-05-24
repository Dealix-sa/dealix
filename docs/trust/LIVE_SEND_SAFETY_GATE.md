# Live Send Safety Gate

The hard rules that govern any external message Dealix ever sends.

## Purpose

Make accidental external messaging structurally impossible. A bug, a
misconfigured environment variable, or an over-eager agent must not be
enough to message a customer.

## Owner

Founder. The gate is reviewed quarterly and after every incident.

## Cadence

Continuous. The gate is verified by every CI run.

## Source of Truth

- This document.
- `policies/dealix_control_policy.yaml` (machine-readable rules).
- `scripts/verify_live_send_safety.py` (the verifier that proves it).

## Required Guards

A path that produces an external message must pass **all** of these:

1. **approval** — the message is queued at `/ops/approvals` and a human
   has approved it.
2. **policy** — the message passes the rules in
   `policies/dealix_control_policy.yaml` (no banned claims, no
   suppressed recipient, etc.).
3. **audit** — an `audit_events` row is written *before* the send.
4. **suppression** — the recipient is checked against the suppression
   list and rejected if matched.
5. **daily_limit** — the daily cap (`50` by default) is not exceeded.
6. **mock_mode** — when `DEALIX_LIVE_SEND_MOCK=1` (the default in dev
   and CI), the call is intercepted and only the audit row is written.
7. **kill_switch** — a single env var (`WHATSAPP_ALLOW_LIVE_SEND` for
   WhatsApp, equivalent for email) can disable the whole path.

If any guard is missing, the send path is broken and CI fails via
`scripts/verify_live_send_safety.py`.

## Inputs

- Approved message
- Verified recipient
- Suppression-list snapshot
- Today's send counter

## Outputs

- An `audit_events` row written *before* the network call
- A `send_log` row written *after* the response
- A retry queue entry on failure (never a silent drop)

## KPI

- 0 sends without an approval row
- 0 sends to a suppressed address
- 0 days with > daily_limit sends
- 0 banned claims in any sent message

## Trust Boundary

External sending is the most consequential thing this codebase can do.
Defense in depth is the rule:

- the policy is in code (`dealix_control_policy.yaml`),
- the verifier proves it (`verify_live_send_safety.py`),
- the runtime enforces it (approval queue + suppression check),
- the kill switch backstops it (`WHATSAPP_ALLOW_LIVE_SEND=false`),
- and CI blocks any change that erodes any of the above.

## Failure Mode

- A new send path is added that bypasses the queue → caught by
  `verify_live_send_safety.py`'s ban on `send_whatsapp_direct` etc.
- The kill switch is flipped on without paired approval+audit → CI
  fails (`ungated_live_send_flag`).
- A banned claim slips into a message body → caught by
  `verify_prompt_output_quality.py`.

## Recovery Path

1. The failing verifier names the file and the offending pattern.
2. Replace the direct call with the approval-queue API.
3. Re-run `make verify-live-send-safety`.

## Verification

```bash
make verify-live-send-safety
python scripts/verify_everything.py --layer live_send_safety
```

## Next Action

Before turning on any live-send flag, confirm `make
verify-live-send-safety` exits 0 today, not last week.
