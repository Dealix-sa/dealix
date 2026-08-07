---
name: dealix-loop-operating-system
description: Design and implement Dealix operating loops for revenue, company brain, delivery, trust review, proof packs, market watch, and release stabilization with stop conditions and safety gates.
---

# Dealix Loop Operating System

## When to use

Use this skill when the user asks to:

- turn scripts into repeatable operating loops
- build a `company-day`, `revenue-loop`, `brain-loop`, `delivery-loop`, or `trust-loop`
- create loop registries, orchestrators, reports, or proof packs
- make agents work through plan, execute, verify, report, and stop cycles
- prevent infinite agent work and uncontrolled token burn

## Core idea

Dealix should not depend on one huge prompt. Dealix should run controlled loops.

A loop is a bounded operating cycle:

```text
inputs -> plan -> execute -> verify -> report -> decision -> stop or next cycle
```

## Loop registry schema

```text
Loop Name:
Goal:
Inputs:
Tools:
Agents:
Verifier:
Outputs:
Stop Condition:
Safety Gates:
Human Review Required:
Schedule:
Max Iterations:
Failure Mode:
Report Path:
```

## Recommended loops

| Loop | Purpose |
|---|---|
| Company Day Loop | Run daily Dealix operating cycle |
| Revenue Loop | Research, score, draft, follow up, and report |
| Brain Loop | Convert signals into CEO decisions |
| Delivery Loop | Move client work from intake to proof |
| Trust Review Loop | Check claims, privacy, outbound, and risks |
| Market Watch Loop | Monitor sector and competitor signals |
| Release Loop | Stabilize PRs, CI, build, and deployment |
| Proof Pack Loop | Convert work into evidence and next actions |

## Files to inspect first

```text
Makefile
scripts/
scripts/revenue/
scripts/brain/
scripts/delivery/
scripts/commercial/
scripts/outbound/
scripts/ops/
reports/
docs/ops/
docs/company/
tests/
```

## Implementation rules

- Never create an unbounded autonomous loop.
- Every loop needs max iterations.
- Every loop needs a verifier.
- Every loop needs a final report.
- Every loop needs a safe failure mode.
- Every loop that touches external actions needs human approval.
- Generated outputs should be separated from source files.

## Makefile target pattern

```make
company-day:
	python scripts/ops/run_company_day.py

revenue-loop:
	python scripts/revenue/run_revenue_day.py

brain-loop:
	python scripts/brain/run_company_brain_day.py

delivery-loop:
	python scripts/delivery/run_delivery_day.py

trust-loop:
	python scripts/outbound/verify_no_auto_external_send.py
```

Only add targets that map to real files or intentionally add the corresponding script.

## Validation commands

```bash
python -m compileall -q scripts app api dealix 2>/dev/null || true
python -m pytest -q tests/*loop* tests/*outbound* tests/*revenue* 2>/dev/null || true
make company-day || true
make revenue-loop || true
make brain-loop || true
make trust-loop || true
```

## Stop conditions

Stop and report instead of continuing if:

- git working tree has unknown user changes
- dependencies are missing and cannot be installed
- tests show runtime/syntax errors
- outbound is enabled unexpectedly
- secrets are found
- the loop would modify too many unrelated files
- the user asked for live sending without policy gates

## Definition of done

A loop is production-worthy only when it has documented goal, deterministic inputs, bounded execution, verification command, report output, audit trail, safe defaults, and human review gate where needed.

## Final response format

```text
Dealix Loop OS Status:
- loop:
- inputs:
- outputs:
- verifier:
- stop condition:
- files changed:
- commands run:
- next cycle:
```
