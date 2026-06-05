---
description: Audit the repo against the Dealix launch doctrine and the 11 non-negotiables
---

# /dealix-audit

You are auditing the Dealix repo for launch-readiness and doctrine compliance.

Do **not** edit files. Produce a report only.

## Steps
1. Read `docs/05_founder/DEALIX_FULL_COMPANY_LAUNCH_BLUEPRINT.md` (the frozen v1 plan) and
   `docs/05_founder/DEALIX_EXECUTION_BOARD.md` (current state).
2. Check the 11 non-negotiables (see CLAUDE.md → "Non-negotiables"). For each, state PASS/FAIL with evidence (file:line).
3. Check positioning: Dealix is **not** CRM/chatbot/Revenue-only. Flag any copy that reduces it.
4. Check claims: flag any guaranteed-outcome or un-sourced claim.
5. Check CTAs: every public page must route to Business OS Score, Diagnostic, or Command Sprint, with exactly one primary CTA.
6. Cross-check the Definition-of-Done for the current PR in the blueprint.

## Output
- Compliance table (rule → PASS/FAIL → evidence → fix).
- Top 5 blockers ranked by launch impact.
- Recommended next action (single sentence).
