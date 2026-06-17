---
description: Run the verification + launch-readiness gates for the current PR
---

# /dealix-verify

Run the verification layer for whatever PR is in flight.

## Steps
1. Identify the current PR from the Execution Board.
2. Run that PR's verification commands exactly as listed in the blueprint (e.g. `npm run build`,
   positioning checker, claims checker, launch-readiness checker, relevant tests).
3. Check the PR's Definition-of-Done line by line.
4. Confirm the 11 non-negotiables still hold (no regressions).

## Output
- Verification table: command → expected → actual → PASS/FAIL.
- DoD checklist result.
- Verdict: READY-FOR-FOUNDER-APPROVAL / NOT-READY (with the exact blocker).
- Never claim PASS without showing the command output.
