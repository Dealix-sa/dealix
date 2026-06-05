---
description: Show the current Dealix launch status — which of the 6 PRs are done, the active gate, and the next action.
---

# /launch-status

Report the state of the Dealix launch.

Steps:
1. Read `/root/.claude/plans/vast-bouncing-raccoon.md` (the master plan) and, if it exists,
   `docs/00_platform_truth/LAUNCH_CONTROL_TOWER.md`.
2. Check `git log --oneline -15` and `git status` to infer which PRs have landed.
3. For each PR (PR1 Claude OS → PR6 Verification Gates), output: status (done / in-progress
   / not-started), its gate, and whether the gate passed.
4. End with the **single next recommended action** and the Go/No-Go line from §20 of the plan.

Read-only. Do not edit, commit, or push.
