# Revenue Sprint — QA Checklist

> Run end-to-end on Day 6. Cannot ship without all boxes checked.

## Prospect List

- [ ] 50 rows present (no fewer)
- [ ] All rows have non-empty company, sector, buyer name, buyer role
- [ ] All fit scores ≥ 60
- [ ] All scores have breakdown (no unbacked numbers)
- [ ] Source URL present for every row (no anonymous data)
- [ ] No row matches a suppression-list entry
- [ ] No row is a competitor or prior incident
- [ ] No row contains pre-revenue companies (auto-suppressor)
- [ ] 5 random rows manually spot-checked (real company, real buyer)
- [ ] CSV file opens cleanly; PDF renders without missing fields

## Message Variants

- [ ] 3 Arabic + 3 English variants present
- [ ] Each variant ≤ 600 characters (LinkedIn-safe)
- [ ] No banned language ("synergy", "10x", "guaranteed", "industry-leading", etc.)
- [ ] Each variant has personalization slots labeled clearly
- [ ] Each variant has a single clear CTA
- [ ] Each variant includes an opt-out cue
- [ ] claim_guard.py pass on every variant
- [ ] Founder approved on each variant

## Objection Responses

- [ ] 3 objections × 2 framings = 6 in Arabic + 6 in English
- [ ] Each response addresses the actual objection (no deflection)
- [ ] No new promises in the responses (no scope creep)
- [ ] No claims that aren't in the evidence pack
- [ ] Founder approved

## Evidence Pack

- [ ] Sources used: full list with URLs + access dates
- [ ] Methodology page: one page, plain language
- [ ] Sanitization notes: what was cleaned, why
- [ ] Exclusions: what was left out + why
- [ ] Approval log: every approval timestamp during Sprint
- [ ] No client confidential data leaks into pack
- [ ] PDF renders cleanly

## Handoff Doc

- [ ] All deliverables linked
- [ ] All open items noted (or "none")
- [ ] Recommended next steps section filled
- [ ] Trust statement included verbatim
- [ ] Founder reviewed
- [ ] Storage path confirmed in private repo

## Trust Gates

- [ ] suppression.py check pass on every prospect row
- [ ] claim_guard.py pass on every artifact (messages, objections, report, sample artifacts)
- [ ] No client-specific data appears in the public repo
- [ ] Approval log complete and committed to `trust/approval_log.csv` (private)

## Logistics

- [ ] Handoff call scheduled
- [ ] Calendar invite includes deliverables link
- [ ] Day-7 reminder set
- [ ] Case study capture template ready for live handoff
- [ ] Pipeline stage move staged: `paid` → `delivered`

## Failure Handling

If any box can't be checked:
- Identify the gap
- Estimate fix time
- If < 24 hr: fix and re-run QA
- If > 24 hr: notify client proactively + log L2 miss
- Never ship with unchecked boxes

## Owner

Founder runs QA. No agent or contractor can sign off QA this quarter.

## Signoff

```
QA run on: {date}
QA passed by: {founder}
claim_guard run: {commit hash + timestamp}
Suppression check: {timestamp}
Final approval: {timestamp}
```

## What QA Refuses

- Soft passes ("close enough")
- Skipped boxes ("not applicable" without a written reason)
- Self-attestation without spot-checks
- Shipping while QA fails
