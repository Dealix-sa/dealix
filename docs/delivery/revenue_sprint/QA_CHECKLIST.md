# QA Checklist

> Run on Day 10 of every Sprint. No handoff without all green.

## A — Lead Table

- [ ] Every A-priority account has linked evidence.
- [ ] Every B-priority account has at least one trigger evidence link.
- [ ] No duplicate legal entities.
- [ ] No accounts on the customer's "do not contact" list.
- [ ] Scoring sums to total_score (no off-by-one).
- [ ] Priority derived from score, not entered manually.

## B — Outreach Pack

- [ ] No forbidden phrases (`NO_OVERCLAIM_POLICY.md`).
- [ ] Bilingual versions say the same thing; not literal translation.
- [ ] Founder signature present.
- [ ] Each message references the specific trigger.
- [ ] Subject lines specific, not generic.

## C — Executive Memo

- [ ] One page only.
- [ ] No filler language.
- [ ] Every number tied to evidence.
- [ ] Unknowns/caveats present.
- [ ] Recommended next step is concrete (named scope + price).

## D — Customer Data

- [ ] All deliverables stored under the customer's private workspace.
- [ ] No customer data on any public surface.
- [ ] PDPL data handling is documented (lawful basis, retention).

## E — Trust

- [ ] Doctrine verifier passes.
- [ ] No guarantee language anywhere.
- [ ] No agent A3 sends without approval token.

## F — Operational

- [ ] Sprint register updated with delivery date.
- [ ] Friction-log entries created for any process pain.
- [ ] Capital asset registry incremented if applicable (e.g. consented
      quote, named referral).

## QA Outcome

```
- sprint_id: ...
- qa_run_on: yyyy-mm-dd
- result: pass / fail (named failures)
- fixed_on: yyyy-mm-dd
- founder_signoff: yyyy-mm-dd
```

## Failure Path

- Each failure becomes a fix task; the Sprint cannot hand off until all
  failures are resolved.
- A recurring failure (≥ 3 across recent Sprints) triggers a template
  review.
