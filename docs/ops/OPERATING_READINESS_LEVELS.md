# Operating Readiness Levels

> The level chart used by `DEALIX_IMPLEMENTATION_AUDIT.md`. Each system in
> Dealix has a level from L0 (missing) to L5 (producing market evidence). The
> audit script computes the level mechanically.

## Levels

### L0 — Missing
Required file or directory is not on disk.
- **Symptom:** audit prints `Missing required file:` or `Missing verifier:`.
- **Unlock:** create the file with the minimum content described in
  `DEALIX_IMPLEMENTATION_AUDIT.md::Core Systems`.

### L1 — File exists
Path resolves but content is empty or trivially short (< 100 bytes).
- **Symptom:** audit prints `Too short or empty:`.
- **Unlock:** put real operating content in. Each required doc has a
  template inline in this audit guide.

### L2 — File has operating content
File exists and is long enough, but is not yet verified by a verifier.
- **Symptom:** audit passes structure but no `verify_*.py` runs against the file.
- **Unlock:** add or wire up the matching verifier in
  `scripts/audit_dealix_implementation.py::VERIFY_SCRIPTS`.

### L3 — Verified by script
A verifier script exists and exits 0 against the file's content.
- **Symptom:** `python scripts/verify_<name>.py` prints `PASS: ...` and exits 0.
- **Unlock:** none — L3 is the public goal.

### L4 — Used in private ops
Private-ops audit (`audit_private_ops.py`) confirms artefacts referencing
the public doc exist and are non-empty.
- **Symptom:** public is green, private audit prints PASS.
- **Unlock:** run the related private ops loop (`make daily`, `make stage`, etc.).

### L5 — Producing market evidence
Real-world signal: leads, DMs, samples, proposals, payment attempts. Verified
by **row counts** in the private logs.
- **Symptom:** private audit prints `Lead count: ≥ 25`, `Revenue actions: ≥ 25`,
  delivery reports exist.
- **Unlock:** follow `DEALIX_30_DAY_EXECUTION_PLAN.md`.

## How to read the audit output

```
== Dealix Public Implementation Audit ==
Missing required file: docs/founder/GO_NO_GO_DECISION_SYSTEM.md   <- L0
Too short or empty: docs/learning/LEARNING_LOOP.md               <- L1
Verifier failed: scripts/verify_tier1_revenue.py                 <- L2 -> L3 blocked
...
IMPLEMENTATION AUDIT FAILED:
- Missing required file: docs/founder/GO_NO_GO_DECISION_SYSTEM.md
- Too short or empty: docs/learning/LEARNING_LOOP.md
- Verifier failed: scripts/verify_tier1_revenue.py
```

Fix top-down: missing → empty → failing verifier → market evidence.

## Why levels are mechanical, not editorial

The whole point of this system is to **defeat the bias that says "we built it"
when only the doc exists**. A level is not awarded by the founder writing it
down. A level is awarded by a script printing PASS. Editorial language about
maturity is forbidden in the audit output for that reason.

## Related

- `DEALIX_IMPLEMENTATION_AUDIT.md` — the level table.
- `scripts/audit_dealix_implementation.py` — the computation.
- `docs/founder/GO_NO_GO_DECISION_SYSTEM.md` — how levels gate decisions.
