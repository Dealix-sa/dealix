# Delivery QA OS

> Quality gate for every artifact that reaches a customer.

## 1. QA checklist (per artifact)

- [ ] Brand check (`docs/brand/DEALIX_BRAND_VOICE.md`, brand tokens)
- [ ] Accuracy check (every number cited has a source)
- [ ] Bilingual symmetry (AR and EN ship together when applicable)
- [ ] Personalisation accuracy (every reference to the customer is correct)
- [ ] Trust check (no guaranteed-result claims; suppression honoured)
- [ ] Founder sign-off recorded
- [ ] Audit event appended

An artifact that fails any step **does not** ship.

## 2. Artifact types covered

- Samples
- Proposals
- Sprint deliverables
- Managed retainer outputs
- Proof artifacts
- Customer-facing reports

## 3. Owners

- Delivery Copilot drafts the QA checklist.
- Brand Guardian reviews voice/visual.
- Founder signs off.

## 4. Failures

A failure pattern (≥ 2 artifacts failing the same step in a week) escalates to the Performance Improvement OS.

## 5. KPI

| KPI | Target |
|---|---|
| QA-pass rate | ≥ 95 % |
| On-time delivery rate | ≥ 90 % |
| Customer NPS post-delivery | tracked monthly |
