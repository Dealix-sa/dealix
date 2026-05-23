# Dealix Maturity Model

Five levels. Honest, observable per level.

| Level | Name | Verifiable when |
|---|---|---|
| 0 | Sketch | files exist, nothing runs |
| 1 | Wired | `make sovereign-operating-stack` passes |
| 2 | Bootstrapped | `make bootstrap-runtime` ran on host; smoke test passes |
| 3 | Live drafts | workers are producing artefacts; approval queue has rows |
| 4 | Live revenue | `cash_collected.csv` has rows tied to approved A2 actions |
| 5 | Sovereign | all of the above + monthly restore drill + signed audit log |

Today we are aiming at **Level 1** with this commit. Level 2+ require
the founder to run the manual steps in
`docs/ops/CLAUDE_CODE_EXECUTION_REPORT.md`.
