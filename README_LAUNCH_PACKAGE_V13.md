# Dealix Launch Package V13 — Consolidation & Master Merge Kit

V13 is the consolidation layer above V1–V12. Its job is not to add another isolated operating layer, but to make the full Dealix launch stack easier to merge, verify, operate, and explain.

## What V13 adds

- Master merge plan for V1–V12.
- Canonical command surface through Makefile.
- Master readiness script.
- File inventory generator.
- Migration order checker.
- Workflow inventory checker.
- Launch decision report.
- Consolidated operator guide.
- Final founder handoff pack.

## Core commands

```bash
make dealix-master-readiness
make dealix-launch-decision
make dealix-inventory
make dealix-workflows
make dealix-migrations
```

## Operating principle

V13 makes Dealix executable by reducing operational ambiguity. If a founder, operator, or engineer asks "what should I run first?" the answer starts from the Makefile and the master readiness report.
