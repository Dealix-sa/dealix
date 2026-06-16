# Controlled Live Outbound Runbook

## Philosophy
**No uncontrolled external send.**

External sends are allowed only when controlled by policy gates, rate limits, and human approval.

## Modes

| Mode | Meaning |
|------|---------|
| `dry` | No external sends; log only. |
| `controlled_live` | Live sends allowed only if all gates pass. |
| `live` | Live sends allowed (legacy; prefer controlled_live). |

## Required Gates
1. `EXTERNAL_SEND_ENABLED=true`
2. `OUTBOUND_MODE=controlled_live`
3. Target verified.
4. `source_url` present.
5. Message approved (`APPROVED_BY=sami`).
6. Rate limits not exceeded.
7. No fake claims.
8. No guaranteed ROI.
9. Email has unsubscribe.
10. WhatsApp has opt-in + approved template.

## Commands
```bash
make outbound-env      # check env
make outbound-dry      # dry run
APPROVED_BY=sami make outbound-live   # live send
make company-live-day  # full day
```

## First Live Send
1. Set env vars.
2. Add 1 verified contact.
3. Add 1 approved draft.
4. Run `make outbound-dry`.
5. Review output.
6. Run `APPROVED_BY=sami make outbound-live`.
7. Check events in `data/outbound/events.csv`.
