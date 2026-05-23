# Revenue Sprint QA Checklist

The hard checklist every Revenue Sprint deliverable must pass before it leaves Dealix. Failure on any item blocks delivery.

## Purpose
Make quality enforceable and auditable, not a matter of taste. Every Sprint is scored against this checklist at Day 5 (governance review) and again before handover on Day 7. Founder approval is logged only if every item passes.

## Owner
Sami (Founder).

## Review Cadence
Monthly. Checklist is updated when a customer complaint or refusal reveals a gap.

## Inputs
- The draft deliverable from Day 4.
- The Source Passport from Day 1.
- The DQ Score from Day 2.
- The Dealix doctrine.

## Outputs
- A signed checklist file per Sprint, stored in `clients/<client>_private/qa_checklist.md`.
- A pass/fail signal that gates handover.
- A friction-log entry if any item fails so the cause can be addressed.

## Rules
- No item is "soft". Every item is binary pass/fail.
- A single fail blocks handover until fixed and re-checked.
- Checklist is signed by the founder, not delegated.
- Every failure is logged in the friction log even after fixing.

## Metrics
- Pass rate at Day 5 review (target: >=80% first-pass).
- Number of items failed per Sprint (target trending down).
- Time spent in QA per Sprint (target trending down).

## Evidence
- Signed checklist file per Sprint.
- Friction log entries per failure.
- Approval log entry at Day 5.

## The Checklist

### Sources and Evidence
- [ ] Every claim in the deliverable has at least one cited source.
- [ ] Every numerical figure has a source date and a method note.
- [ ] No source is older than the offer-rung freshness rule.
- [ ] No source is from a banned domain or scraping origin.

### Doctrine compliance
- [ ] No language outside the approved Dealix vocabulary.
- [ ] No promise that exceeds the rung sold.
- [ ] No comparison to a competitor without a verified citation.
- [ ] No private operating data appears in customer-facing artifacts.

### Customer-fit
- [ ] Deliverable maps to the intake form's declared outcome.
- [ ] Account list and recommendations reflect the customer's industry, not a generic template.
- [ ] At least three customer-specific insights present (not boilerplate).

### Format and polish
- [ ] Title, summary, body, evidence appendix all present.
- [ ] No broken links.
- [ ] No internal-only notes left in the artifact.
- [ ] File names and folder structure follow the standard.

### Delivery
- [ ] Capital Asset registered in `assets/registry.csv`.
- [ ] Handover meeting scheduled.
- [ ] Customer notified with delivery template.
- [ ] Retainer eligibility evaluated and logged.

## Last Reviewed
2026-05-23
