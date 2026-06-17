---
description: Run the Dealix launch gates and report GREEN/RED with the Per-PR Execution Contract reminder.
---

# /verify-launch

Run the `run-launch-gates` skill and report the verdict.

**Per-PR Execution Contract (restate before any PR work):**
```
I will implement PR [N] only: [NAME].
I will restate scope and list expected files BEFORE editing.
I will not touch files outside scope. I will not implement future PRs.
I will not commit or push until the founder approves.
I will not change pricing unless this PR includes pricing.
I will not change public website copy unless this PR includes copy.
I will not add dependencies unless necessary and justified.
I will run verification and NOT hide failures.
After editing: show changed files, explain each, run `git diff --stat`,
report blockers, recommend the next PR, and WAIT for approval.
```

Then run the gates and output GREEN/RED with real command output.
