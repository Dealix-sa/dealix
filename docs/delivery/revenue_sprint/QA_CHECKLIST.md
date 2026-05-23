# QA Checklist — Revenue Sprint

Run before any artifact leaves Dealix.

## Lead quality
- [ ] Every row has a source URL.
- [ ] Every row has an ICP score and a one-sentence reason.
- [ ] No duplicates.
- [ ] No exclusion-list entries.
- [ ] No suppression-list entries.
- [ ] Cities and sectors match the intake.

## Message quality
- [ ] Every sample message passes `MESSAGE_QUALITY_STANDARD.md`.
- [ ] Each sample message is tied to a named lead in the table.
- [ ] No guaranteed-outcome claims.
- [ ] No banned phrases from `docs/trust/CLAIM_GUARD.md`.

## Report quality
- [ ] Executive summary fits five bullets.
- [ ] Method section explains sources and exclusions.
- [ ] One concrete next step is named.
- [ ] Arabic and English versions match in content.

## Client relevance
- [ ] Sector frame matches the intake.
- [ ] "Good lead" definition is honored.
- [ ] Out-of-scope is reproduced verbatim from the proposal.

## Evidence
- [ ] All sources resolvable.
- [ ] All claims attributed.
- [ ] Sensitive data redacted where required.

## Sign-off
- [ ] Internal reviewer signed.
- [ ] Founder signed (first three sprints, then sampled).

## Rule
A missing checkbox stops delivery. No verbal "it's fine".
