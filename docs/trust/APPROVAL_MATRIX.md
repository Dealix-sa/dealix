# Approval Matrix

Every action in Dealix is classified by approval level.

## Levels
- **A0** — Automatic internal action. No approval required.
- **A1** — Review recommended. Logged, executed if not held within 24 hours.
- **A2** — Explicit founder approval required before execution.
- **A3** — Never auto-execute. Founder action only, in person.

## Examples

| Action | Level |
|---|---|
| Score a new lead | A0 |
| Add a lead to the candidate table | A0 |
| Draft an outbound message | A0 |
| Send an outbound message | A1 |
| Send a proposal | A2 |
| Change pricing on a public surface | A2 |
| Change product positioning publicly | A2 |
| Issue an invoice | A2 |
| Sign a contract | A3 |
| Sign an NDA | A3 |
| Issue a refund | A3 |
| Communicate with a regulator | A3 |
| Export sensitive client data | A3 |
| Make a guaranteed revenue claim | A3 (and almost always refused) |
| Make a guaranteed compliance claim | A3 (and almost always refused) |

## Logs
- A1: logged in `dealix-ops-private/trust/action_log.csv`.
- A2: logged in `dealix-ops-private/trust/approval_log.csv`.
- A3: logged in `dealix-ops-private/trust/approval_log.csv` with founder signature note.

## Rule
The system does not protect what it does not log. Every A1, A2, A3 action is logged.
