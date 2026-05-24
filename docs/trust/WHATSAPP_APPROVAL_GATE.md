# WhatsApp approval gate

The full WhatsApp send pipeline. Every step is required; skipping any is
a deploy-blocking violation surfaced by `verify_live_send_safety.py`.

## Pipeline

1. **Intake.** A draft is created by an L1 or L2 agent. Status: `pending`.
2. **Approval.** A founder reviews via the approval centre. Status moves
   to `approved` only after explicit human action. PDPL: the approver
   must record consent provenance for the destination MSISDN.
3. **Safe-send orchestration.** `safe_send_text(...)` runs the six gates:
   - approval gate (must be `approved` + WhatsApp action type)
   - destination present (MSISDN non-empty)
   - opt-out gate (PDPL permanent override)
   - quiet-hours gate (KSA `Asia/Riyadh` window)
   - kill switch: `Settings.is_live_send_allowed`
   - then the adapter call.
4. **Adapter call.** `WhatsAppClient.send_text` re-checks
   `whatsapp_mock_mode` and `whatsapp_allow_live_send`. The first
   short-circuits with `whatsapp_mock_mode_true`. The second with
   `whatsapp_allow_live_send_false`.
5. **Audit write.** Outcome is persisted with `reason_code`, `message_id`
   (if delivered), and the approval id used.

## Refusal codes

`SafeSendResult.reason_code` values:

| Code | Cause |
|---|---|
| `approved_and_sent` | Success |
| `not_approved` | Approval missing or action type wrong |
| `missing_msisdn` | Destination empty |
| `opted_out` | PDPL permanent block |
| `quiet_hours` | Outside KSA active window — `queued_until` is set |
| `live_send_disabled` | `WHATSAPP_MOCK_MODE=true` OR `whatsapp_allow_live_send=false` |
| `client_error` | Adapter exception or Meta rejection |

## Live cutover checklist

Before flipping `WHATSAPP_MOCK_MODE=false` on Railway:

- [ ] `make live-send-safety` is PASS.
- [ ] `make production-certification` is PASS.
- [ ] Founder approval recorded in the audit log: a sign-off entry
      stating the founder has reviewed the safety report.
- [ ] `WHATSAPP_DAILY_LIMIT` set to a conservative starting value (≤ 25).
- [ ] At least one dry-run via `safe_send_text` returns a `SafeSendResult`
      with `reason_code="live_send_disabled"` (proving the kill switch
      works) before live-flag flip.
