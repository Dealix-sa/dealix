# Case Study Capture — توثيق دراسات الحالة

## Purpose
Define how Dealix captures sprint outcomes as case studies for marketing, with client consent and without overclaim. No fake proof, no exaggerated numbers, no PII.

## Owner
Head of Delivery (capture). Founder (publish approval).

## Inputs
- Closed sprint with handoff acknowledged.
- 30-day post-handoff outcome data (only what the client volunteers).
- Written consent from the client to publish.

## Outputs
- `docs/case-studies/case_NNN_anonymized.md` (default).
- `docs/case-studies/case_NNN_named.md` (only when written consent names the client).

## Rules (numbered)
1. No case study is published without written consent. Verbal "go ahead" does not count.
2. Default mode is anonymized. Named mode requires explicit, dated consent.
3. No claims about outcomes Dealix cannot evidence with client-shared data.
4. No invented numbers. If the client did not share outcome data, write the case as "case-safe pattern" with hypothetical illustrative figures clearly labeled.
5. No PII anywhere. No employee names. No internal account references.
6. Every published case study links to its consent record under `dealix-ops-private/consents/`.
7. Banned phrases from `docs/trust/NO_OVERCLAIM_POLICY.md` are scanned at publish time.

## Metrics
- Consent capture rate per closed sprint: target ≥ 50%.
- Published case studies per quarter.
- Banned-phrase scan hits at publish: 0.

## Cadence
Capture conversation at 30-day post-handoff. Quarterly publish batch.

## Evidence (paths)
- `docs/case-studies/case_NNN_*.md`
- `dealix-ops-private/consents/case_NNN_consent.pdf`

## Verifier
Founder approves each publication. Head of Delivery verifies consent file exists.

## Runtime Command
`make case.draft SPRINT=<ID>` — drafts an anonymized case skeleton from the sprint folder.

## Capture flow

**Step 1 — Trigger.** At 30 days post-handoff, the delivery lead opens a 20-minute case-capture conversation with the client. The conversation is framed as a learning conversation, not a marketing ask.

**Step 2 — Data gathering.** We ask what the client did with the pack, which rows progressed, what surprised them, what could be improved. We capture only what the client volunteers. We do not push for numbers they are uncomfortable sharing.

**Step 3 — Consent ask.** Separate from data gathering. We ask: would the client be willing to be referenced in an anonymized case study? If yes, we send a one-page consent form. The form names what will be shared, the publication channel, and the right to withdraw.

**Step 4 — Drafting.** Anonymized cases use sector + size band + geography only. Named cases require the named-consent form. Drafts are reviewed by the client before publish.

**Step 5 — Scan and publish.** The draft is scanned for banned phrases and PII. The founder approves. The case is published with a link to the consent record path (private).

## Anonymization rules

- Sector and sub-sector: published.
- Country and region band: published.
- Employee band: published.
- Revenue band: published only with consent.
- Company name: published only with named consent.
- Individual names: never.
- Internal contract values: never.
- Outcome figures: only what the client shared, labeled as client-reported.

## Operating substance
Case studies are evidence assets, not marketing assets. When a buyer reads a Dealix case study, they should be able to verify (through the labeled methodology) what is fact and what is illustrative. That is why the "case-safe pattern" labeling exists for cases without shared outcome data.

We do not invent. We do not borrow numbers from one client to dress up a different case. We do not write composite cases as if they were a single client. The audit trail starts at the consent file.

Hypothetical case studies (where the client has not yet shared outcome data, or where we are demonstrating a methodology in the absence of a real engagement) are labeled at the top of the file: "Hypothetical / case-safe template". The illustrative numbers, if any, are labeled the same way.

The 30-day capture conversation is also a learning input. The patterns we hear feed `docs/learning/WIN_LOSS_REVIEW.md` regardless of whether a case study results.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
