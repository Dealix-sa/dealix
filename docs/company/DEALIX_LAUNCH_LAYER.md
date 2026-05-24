# Dealix Launch Layer

Every customer-visible change ships through this layer.

## Launch types

| Type | Gate | Verifier |
|---|---|---|
| Soft launch | Warm list only (<= 20 invitees) | `scripts/verify_commercial_launch_ready.py` |
| Beta launch | Up to 100 users, no public ads | `scripts/official_launch_verify.sh` |
| Full launch | Public homepage + GTM funnel live | `scripts/verify_dealix_commercial_go_live.sh` |

## Launch gate (pre-flight)

Mandatory checks:
1. CI green on `main` for the last 24h.
2. All 26 layer verifiers PASS (`make everything`).
3. Approval queue empty of P0 items.
4. Proof Pack store backed up.
5. Moyasar in declared mode (`test` or `live`) — never mixed.

## Rollback playbook

1. Flip Railway service to the previous green deploy.
2. Revert the feature flag if applicable.
3. Audit log entry: `launch_rollback` with `reason`, `decided_by`, `evidence_link`.
4. Postmortem within 72h, published to `docs/postmortems/`.

## Comms

Launch comms drafts: `scripts/founder_launch_day_comms.py` (drafts only,
never sends; routes through approval_center).

## Verifier

`make launch-layer` aggregates the existing commercial + official launch
verifiers.

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
