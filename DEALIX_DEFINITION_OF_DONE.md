# Dealix Definition of Done

## Purpose
Define what "done" actually means at three levels: per file, per sprint, and per company milestone.

## Per file
A file is done when:
- It exists and contains real content (> 50 bytes, no template placeholders left).
- It is referenced from at least one of: the Master Blueprint, the Integration Map, or an OS doc.
- It is reachable from the relevant verifier script.
- If it is a script, it exits 0 when run with no arguments (or prints clear failure reasons and exits 1).

## Per sprint
A sprint is done when:
- All files listed in the sprint's section of `DEALIX_IMPLEMENTATION_SPRINT_PACK.md` exist.
- The sprint's verifier script exits 0.
- The relevant Make target (if any) runs and prints PASS.
- The sprint's checkboxes in `DEALIX_IMPLEMENTATION_MASTER_CHECKLIST.md` are ticked.
- The change is committed with a clear message.

## Per company milestone

### Activation milestone (Horizon 1)
- All 10 operating systems scaffolded.
- `make implementation-check` green.
- `dealix-ops-private/` working tree bootstrapped.

### First market loop milestone (Horizon 2)
- 25 leads in pipeline tracker.
- 25 founder-led DMs sent and logged.
- 3 sample packs prepared.
- 1 proposal in `sales/proposal_tracker.csv` with a follow-up date.
- 1 payment / PO / written approval pursued to a definitive outcome.

### First delivery milestone (Horizon 3)
- Intake, lead table, delivery report, QA score ≥ 75, handoff, feedback request, retainer evaluation all completed.
- Proof artifacts (with approval) registered in the content library.

### Repeatability milestone (Horizon 4)
- 3 paying customers for the same offer.
- Productization candidates documented.

### SaaS readiness milestone (Horizon 5)
- SaaS gate doc signed.
- Capital plan signed.
- Trust + finance evidence covers ≥ 3 paying customers.

## What "done" does NOT mean
- Done does not mean perfect.
- Done does not mean every feature is automated.
- Done does not mean nothing more can be improved.
- Done means: the bar is met, the artifact exists, the next step is unblocked.

## Verifying done
Run, in order:
```
python scripts/verify_implementation_sprint_pack.py
make implementation-check
```
If both pass, the implementation pack is done.
