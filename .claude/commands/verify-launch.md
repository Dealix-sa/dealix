---
description: Run the Dealix launch verification suite and report results honestly (new vs pre-existing failures).
---

# /verify-launch

Run the verification suite and report exactly what happened.

Steps:
1. `cd frontend && npm run build && npm run lint && npm run typecheck` — capture exit codes.
2. Run each launch script if present:
   - `python scripts/verify_website_positioning.py`
   - `python scripts/verify_growth_assets.py`
   - `python scripts/verify_launch_readiness.py`
   - `python scripts/verify_governance_rules.py`
3. Output a table: command · exit status · new-failure? (this change) vs pre-existing.
4. End with a single PASS/FAIL go/no-go line.

Iron rule: never report PASS unless the command exited 0. Quote real output for any failure.
This command runs checks only — it does not fix, commit, or push.
