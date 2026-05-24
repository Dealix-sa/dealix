# Dealix AI Governance Overview

How Dealix manages the full lifecycle of every AI system it owns, with
explicit alignment to the **NIST AI Risk Management Framework (AI RMF
1.0)** and **ISO/IEC 42001:2023** (AI Management Systems).

## Purpose

Make sure every model, agent, and machine that influences a customer or
internal decision has:

- a named owner,
- a documented purpose,
- a risk class,
- a kill_switch,
- a required evaluation suite,
- and an audit trail.

If a layer cannot satisfy these six, it cannot ship.

## Owner

Founder. Reviewed monthly.

## Cadence

- Daily: `governance_auditor` runs `make everything`.
- Weekly: drift report rolled into the CEO weekly review.
- Monthly: governance overview review.
- Quarterly: third-party-aligned (NIST AI RMF + ISO 42001) self-audit.

## Source of Truth

- `registries/agent_registry.yaml` (every agent + safety controls)
- `registries/machine_registry.yaml` (every automated machine)
- `policies/dealix_control_policy.yaml` (policy-as-code)
- `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md`
- `docs/governance/AUTONOMY_VALIDATION_GATES.md`
- This file.

## AI Lifecycle

We treat AI systems through the standard NIST AI RMF lifecycle, mapped
to Dealix surfaces:

| Stage | NIST AI RMF function | Dealix artifact |
| --- | --- | --- |
| Map | Govern + Map | `docs/ai_governance/AI_SYSTEM_INVENTORY.md` |
| Measure | Measure | `evals/*.yaml` + `scripts/verify_eval_gate.py` |
| Manage | Manage | `policies/dealix_control_policy.yaml` + approvals queue |
| Govern (cross-cutting) | Govern | this file + governance docs under `docs/governance/` |

ISO/IEC 42001 mapping: each requirement (context, leadership, planning,
support, operation, performance evaluation, improvement) is satisfied by
the artifacts above, plus quarterly internal audit minutes appended to
`docs/governance/RUNTIME_GOVERNANCE.md`.

## Risk Classes

Aligned with `docs/governance/AI_ACTION_LEVELS.md`:

- **A1**: read-only / internal. Auto-execute allowed.
- **A2**: internal write or external draft. Audit required. Auto-execute
  allowed.
- **A3**: external action with customer impact. Approval + audit
  required. Auto-execute forbidden.

## Required Controls Per System

Every AI system listed in `AI_SYSTEM_INVENTORY.md` must declare:

- **Owner** — the human accountable.
- **Risk class** — A1 / A2 / A3.
- **Kill switch** — environment variable or feature flag that disables
  the system immediately.
- **Eval required** — boolean + reference to the eval suite.
- **Audit required** — boolean, almost always `true`.
- **Allowed write targets** — explicit allowlist.

## Trust Boundary

No AI system at Dealix sends external messages by itself. Sending is
mediated by the queue at `/ops/approvals`, governed by the live-send
safety gate.

## Failure Mode

- A new model added without registry entry → fails CI via
  `verify_agent_registry.py`.
- An eval suite shrinks below the case floor → fails
  `verify_eval_gate.py`.
- A banned claim appears in any output → fails
  `verify_prompt_output_quality.py`.

## Recovery Path

1. Stop deployment (the failing verifier blocks merge).
2. Update the registry or eval suite.
3. Re-run `make everything`.
4. Append the incident to `docs/governance/INCIDENT_RESPONSE.md` if
   customer impact was possible.

## Verification

```bash
make ai-governance
python scripts/verify_everything.py --layer ai_governance
```

## Next Action

Open `AI_SYSTEM_INVENTORY.md`. Confirm every agent in the agent registry
is also listed there. Add any that are not.
