# Case Study Capture

> The moment a Sprint produces a result is the moment to start the case
> study. Do not wait.

## Capture Workflow

1. **At handoff**, ask: "If this produces results in 30 days, would you
   be willing to be named in a case study? We will send you the draft
   before anything is published."

2. **If yes**, log preliminary consent in
   `dealix-ops-private/content/case_study_pre_consents/`.

3. **At Day +30 from handoff**, follow up:
   - "How did the outreach pack perform? How many replies / calls /
     opportunities?"
   - Capture verbatim.

4. **At Day +60**, if results are confirmed:
   - Draft the case study using `docs/content/CASE_STUDY_SYSTEM.md`
     template.
   - Send draft to customer for written approval.

5. **Once approved**, publish per `CASE_STUDY_SYSTEM.md`.

## What we capture (always, with consent)

- Outreach pack performance numbers.
- Notable customer quotes (verbatim).
- Customer's CRM-confirmed opportunities sourced from our work.
- Sector context that makes the case study useful to a future buyer.

## What we do **not** do

- Publish numbers customer has not approved.
- Quote a customer paraphrased.
- Imply causation we cannot demonstrate.

## When the answer is "no"

- Anonymise the lessons; capture them for our own playbook.
- Do not press.
- Do not list them in `PROOF_LIBRARY.md`.

## Logging

```
- sprint_id: ...
- pre_consent_obtained: yyyy-mm-dd
- day_30_results: <link to numbers>
- day_60_decision: yes / no
- consent_letter_path: ...
- case_study_path: ...
- published_on: yyyy-mm-dd
```
