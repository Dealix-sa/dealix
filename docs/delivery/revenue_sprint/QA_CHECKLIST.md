# Revenue Sprint — QA Checklist

Every customer-facing artifact in a Revenue Sprint must pass this
checklist before founder sign-off and before it ships to the
customer. The checklist is run by AI as a first pass; the founder
runs the final pass.

## Purpose
Catch quality and trust failures before they reach the customer.
The checklist exists because a single bad artifact can cost a
retainer (and a refund); the cost of running QA is always lower
than the cost of skipping it.

## Owner
Sami (Founder). AI runs the first-pass checks; founder runs the
final pass.

## Review Cadence
Per-artifact during active sprints. Checklist itself reviewed
monthly inside the Weekly CEO Review.

## Inputs
- The artifact under review (Discovery Brief, Findings, Analysis,
  Sprint Report, or Rung 3 proposal).
- The agreed scope from the Discovery Brief.
- The Source Passport for the engagement.
- The previous artifact in the sprint sequence (for continuity).

## Outputs
- A signed checklist file in `clients/<client>/qa_<artifact>.md`
  (private).
- A pass/fail decision.
- If fail: a list of required fixes with owner and ETA.

## Rules
- An artifact with any unchecked critical item does **not** ship.
- An artifact failing the same critical item twice triggers a
  playbook review.
- AI may auto-check the mechanical items; the founder must
  personally check every "Trust" and "Customer Voice" item.
- No artifact ships with placeholder content ("TBD", "TODO",
  "<insert here>").
- No artifact ships with unsourced claims or unattributed numbers.

## Metrics
- First-pass QA pass rate (target: 80%+).
- Number of artifacts shipped without QA (target: 0).
- Number of customer-reported errors post-ship (target: 0).
- Average QA time per artifact (target: under 30 min).

## Evidence
- Signed checklists in `clients/<client>/qa_<artifact>.md` (private).
- Mapping of QA fails → playbook updates in `docs/learning/`.

## Last Reviewed
2026-05-23

---

## The Checklist

### Scope
- [ ] Artifact answers the question agreed in the Discovery Brief.
- [ ] Artifact does not exceed agreed scope (no scope creep).
- [ ] Artifact stays inside the agreed offer rung.

### Evidence
- [ ] Every number has a source link or a footnote.
- [ ] Every claim has either a source or is explicitly framed as
      "our interpretation".
- [ ] Sources are listed in the Source Passport for this engagement.
- [ ] No public source is fabricated; URLs resolve.

### Clarity
- [ ] One-paragraph executive summary at the top.
- [ ] Recommendations are concrete and time-bounded (within next 30
      days).
- [ ] Charts have axis labels, units, and source.
- [ ] No jargon without a one-line definition on first use.

### Trust (Founder must personally verify)
- [ ] No customer PII outside the customer's own artifact.
- [ ] No claim about competitors that we cannot defend.
- [ ] No prediction stated as a guarantee.
- [ ] No internal Dealix process exposed that should stay private.

### Customer Voice (Founder must personally verify)
- [ ] Customer's named bottleneck is addressed by name in the
      executive summary.
- [ ] Tone matches the customer's stated preference (formal /
      conversational).
- [ ] Recommendations respect the customer's stated constraints
      (budget, timeline, team size).

### Mechanical
- [ ] File is in the agreed format (PDF / markdown / both).
- [ ] File is in the correct private folder.
- [ ] File is named per convention (`final_report_YYYY-MM-DD.md`).
- [ ] No spelling errors in headings.
- [ ] Bilingual sections (AR / EN) match content, not just translate
      machine-blindly.

### Approval
- [ ] AI first-pass complete with notes.
- [ ] Founder final-pass complete.
- [ ] A2 approval logged in `clients/<client>/founder_approval.md`.
- [ ] Customer send-time scheduled.

---

## Failure Modes To Watch
- Trust or Customer Voice items being auto-checked → discipline
  break; reset.
- Same item failing across multiple sprints → upstream playbook
  issue; fix the playbook.
- Checklist becoming theatrical (always green, problems still
  reach the customer) → add the missed item as a new check.
