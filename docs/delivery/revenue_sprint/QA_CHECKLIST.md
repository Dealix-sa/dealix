# Revenue Sprint QA Checklist

The gate that must pass before any customer-facing artifact leaves the building.

## Purpose
Block low-quality deliverables from reaching customers. Catch silent failures (missing sections, wrong customer name, ungoverned claims) before they ship.

## Owner
Sami (Founder, Delivery OS).

## Review Cadence
After every sprint. Add new items every time a failure escapes.

## Inputs
- Draft artifacts produced during the sprint.
- The Delivery Playbook.
- Governance review output.

## Outputs
- Signed QA checklist saved alongside the proof pack.
- A go / no-go decision for handoff.

## Rules
- No artifact ships with an open `FAIL`.
- Every `PASS` must have evidence (file path or line reference).
- Founder is the final signer.

---

## Checklist

### Source Passport
- [ ] Customer name correct (no placeholders).
- [ ] All data sources listed.
- [ ] Owner per source recorded.
- [ ] PII handling section completed.

### DQ Score
- [ ] Score computed with documented thresholds.
- [ ] Missing fields itemized.
- [ ] Risk callouts written in plain language.
- [ ] Numbers reproducible from raw data.

### Account Scoring
- [ ] ICP definition matches kickoff form.
- [ ] At least 50 accounts scored.
- [ ] Score formula documented.
- [ ] No duplicates.

### Outreach Pack
- [ ] 3 sequences delivered.
- [ ] Each message reads naturally in Arabic / English as appropriate.
- [ ] No unsupported claims about Dealix or the customer.
- [ ] Sender identity matches what the customer approved.

### Governance Review
- [ ] PII handling verified.
- [ ] Claims supportable by evidence.
- [ ] Autonomy levels honored throughout.
- [ ] No prohibited surfaces (L4) touched.

### Proof Pack
- [ ] All section headers present.
- [ ] Single PDF and folder both present.
- [ ] Customer name appears correctly on every page.
- [ ] Linked next-step offer included.

### Handoff
- [ ] Founder approved final pack.
- [ ] Customer notified through agreed channel.
- [ ] Retainer offer (Rung 3 or 4) included.
- [ ] Internal: `next_offer.md` written.

---

## Metrics
- Number of sprints shipped with all checks `PASS`.
- Number of escapes per quarter (items that should have been caught but weren't).
- Median time from draft to QA pass.

## Evidence
- Signed checklist per sprint in `dealix-ops-private/clients/<client>/qa_checklist.md`.
- Linked proof pack and handoff notes.

## Last Reviewed
2026-05-23
