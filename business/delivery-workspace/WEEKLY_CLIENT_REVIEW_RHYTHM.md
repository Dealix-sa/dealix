# Weekly Client Review Rhythm

## When
Same slot every week, agreed at kickoff. 45 min default.

## Agenda
1. **What we shipped** (10 min) — completed deliverables.
2. **What we found** (10 min) — friction log updates.
3. **What we'll ship next** (10 min) — next 1-2 deliverables.
4. **What we need from you** (10 min) — open approvals, access, data.
5. **Open risks** (5 min) — review the risk register.

## Output
- Notes saved to `business/proof/exports/<client-id>/weekly-<date>.md`.
- Proof items added via `add_proof_item.py`.
- Approvals requested via `request_client_approval.py`.

## Skip policy
- 1 skipped review → warning + reschedule.
- 2 in a row → escalate to commercial owner's manager (with their permission).
- 3 in a row → SOW pauses.

## Anti-patterns
- Status theater. Don't recite what was done; show it.
- Skipping risks. Always review even if "nothing's wrong".
- Promising next week's deliverable without checking capacity.
