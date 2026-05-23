# Trust Guardian Agent

Agent id: `trust_guardian`.

## Role

Sit between every draft and the approval queue. The guardian:

* Runs the eval gate's safety suites on the draft.
* Checks the suppression list.
* Verifies that an evidence reference is present for A2 actions.
* Emits a `trust_flag` for any suspicion.

## Outputs

* `trust/trust_flags.csv` — open + resolved flags.

## Failure-closed posture

If the guardian crashes, the approval queue still works but the
founder sees the worker heartbeat go red in `/workers`. That is
deliberate: better to slow down approvals than to skip the safety pass.
