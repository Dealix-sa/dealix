# Learning Router — موجِّه التعلّم

## Purpose
Implement the 1-2-3-5-10 escalation rule: when a defect, surprise, or pattern is observed, the response escalates with frequency. Once is logged, twice is checklisted, three times is playbooked, five times becomes a template, ten times becomes automated.

## Owner
Founder. Head of Delivery enforces routing on delivery patterns.

## Inputs
- Defects from QA logs.
- Patterns from sprint folders.
- Incidents from registers.
- Operator observations.

## Outputs
- Routed action per occurrence: log, checklist add, playbook update, template create, automation request.

## Rules (numbered)
1. Every occurrence is counted in the pattern register.
2. The 1-2-3-5-10 thresholds are non-negotiable; we do not skip steps.
3. Counts are scoped: per sprint, per agent, per sector — whichever the pattern lives in.
4. Automation (at 10) follows the AI release gate.
5. The router is reviewed weekly.

## Metrics
- Patterns escalated per quarter at each tier.
- Time from occurrence to routed action.
- Reverse migrations (a pattern that proved spurious and was de-escalated).

## Cadence
Continuous. Weekly review.

## Evidence (paths)
- `docs/learning/registers/pattern_log.md`

## Verifier
Founder.

## Runtime Command
`make learning.router.count PATTERN=<id>` increments the count and prints the next-step suggestion.

## Tiers

**Tier 1 — Once. Log.** Write a one-line entry in `docs/learning/registers/pattern_log.md`. Date, scope, brief description. No further action.

**Tier 2 — Twice. Checklist add.** Add a one-line check to the most relevant checklist (QA, gate, intake). The check should catch the pattern at its earliest visible point. Update the checklist file the same week.

**Tier 3 — Three times. Playbook update.** Update the relevant playbook (`DELIVERY_PLAYBOOK.md`, `INCIDENT_RESPONSE.md`, etc.) with a documented sub-step that addresses the pattern. The update is diffed and reviewed.

**Tier 5 — Five times. Template create.** Create a reusable template or schema that prevents the pattern by structure rather than discipline. Templates live in `templates/` or in the relevant docs subtree.

**Tier 10 — Ten times. Automate.** Propose an automation that handles the pattern without human action. Automation proposal follows the AI release gate. The automation does not skip oversight; it adds an A0 or A1 layer with sampling.

## Worked example

Pattern: lead rows missing `source_captured_at` field.

- Occurrence 1 (week 4): logged. One-line entry.
- Occurrence 2 (week 6): checklist add. QA checklist gains "verify source_captured_at populated on every row".
- Occurrence 3 (week 9): playbook update. Day 2 of the delivery playbook adds explicit step "capture timestamp at row capture, not at validation".
- Occurrence 5 (week 14): template create. The lead capture form template enforces timestamp field as required.
- Occurrence 10 (week 23): automate. Capture script auto-populates timestamp at row creation; agent AG-002 validates presence; A0 scanner blocks rows without timestamp.

## Operating substance
The router exists because most service businesses respond to defects in two failed modes: either ignore them ("happens sometimes") or over-react to one incident ("we need to rebuild our process"). Both fail. The 1-2-3-5-10 rule is the middle path: ignore once, observe twice, act on three, structure on five, automate on ten.

The discipline of counting is the discipline of seeing patterns. Without a count, the third occurrence feels like the first. With a count, the third triggers a playbook update before the fourth happens.

Reverse migration is allowed but must be deliberate. A pattern that turned out to be sporadic and not systemic can be de-escalated, but only after a written argument for why the previous escalation was wrong. We do not silently undo escalations.

Automation is reserved for tier 10 because pre-tier-10 automation is premature. Below ten occurrences, we do not have enough signal to design the automation correctly. The cost of bad automation is higher than the cost of manual checklist enforcement.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
