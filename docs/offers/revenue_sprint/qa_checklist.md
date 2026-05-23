# QA Checklist — Revenue Sprint Deliverable

> Run **before** anything leaves Dealix. The verifier
> `scripts/verify_tier2_delivery.py` requires this list to be fully checked
> for any active delivery.

## Accuracy

- [ ] Every claim is sourceable (link, file, or screenshot saved).
- [ ] No invented numbers.
- [ ] Customer names spelled correctly throughout.
- [ ] Currency, units, and dates are consistent (SAR, day/month/year).
- [ ] Tables sum to what the text says they sum to.

## Scope

- [ ] Deliverable matches the `client_intake.md` named outcome.
- [ ] No work added outside scope without a written change request.
- [ ] Out-of-scope section in the intake is unchanged.

## Tone

- [ ] No "leading", "world-class", "synergy", "exciting".
- [ ] No future-tense promises about Dealix capabilities not yet shipped.
- [ ] No internal jargon the client did not use first.

## Safety

- [ ] No private data from another client referenced.
- [ ] No secrets (API keys, passwords, tokens) in the file.
- [ ] PDPL-sensitive fields redacted unless explicitly cleared.
- [ ] Approval to send logged in `trust/approval_log.csv`.

## Format

- [ ] Renders cleanly on phone (no horizontal scroll).
- [ ] Tables not wider than 4 columns.
- [ ] File saved at `clients/<client>/<artefact>.md`.

## Sign-off

- Reviewer (must not be the producer):
- Date:
- Verdict: `<go | hold | no>`

If verdict is anything other than `go`, the deliverable does not leave Dealix.
