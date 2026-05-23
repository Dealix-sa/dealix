# Dealix Autonomy Policy

Every surface inside Dealix is tagged with one of five autonomy levels. The level controls what AI can do before a human signs off.

## Purpose
Define the autonomy ladder and the rules for graduating a surface up the ladder (or demoting it after an incident).

## Owner
Sami (Founder, Trust OS).

## Review Cadence
Monthly, or immediately after any incident.

## Inputs
- Approval matrix (`docs/trust/APPROVAL_MATRIX.md`).
- Incident reports and friction log.
- Customer outcomes per surface.

## Outputs
- The autonomy ladder below.
- Surface-by-surface autonomy assignment (kept in agent configs).
- Upgrade / demotion events logged.

## Rules
- A surface starts at L0 by default.
- Promotion requires four consecutive weeks of clean operation.
- Demotion happens immediately on incident; re-promotion requires a written retro.
- L4 surfaces never see AI action of any kind.

---

## The Five Autonomy Levels

### L0 Manual
- Human does the work end-to-end. AI does not act.
- Used for: payments, bank changes, contract signatures, first-time customer interactions.

### L1 Assisted
- AI drafts, suggests, summarizes. Human edits and ships.
- Used for: outreach drafts, proposals, customer-facing reports, website copy.

### L2 Semi-Auto
- AI executes the work; human reviews before publication.
- Used for: internal research, lead enrichment, account scoring, internal dashboards.

### L3 Auto
- AI acts on a defined recipe with logged outputs; human reviews on a sample / weekly cadence.
- Used for: internal scoring jobs, internal data refreshes, internal monitoring.

### L4 Prohibited
- AI must not act on this surface, ever.
- Used for: bank transfers, password / 2FA changes, contract terms, irreversible account changes, public claims about unproven outcomes.

---

## Graduation Procedure

To promote a surface from L1 → L2 → L3:
1. Run the surface at the lower level for at least four weeks.
2. Show zero rejected outputs in the approval log over that period.
3. Founder writes a one-paragraph retro and signs it.
4. Update the surface's autonomy tag in the agent config.
5. Add an entry in the approval log marking the graduation event.

## Metrics
- Number of surfaces at each level.
- Number of graduations completed this quarter.
- Number of demotions triggered (target: low and falling).

## Evidence
- Autonomy assignments in agent configs.
- Approval log entries showing graduation events.
- Incident log linking demotions to root causes.

## Last Reviewed
2026-05-23
