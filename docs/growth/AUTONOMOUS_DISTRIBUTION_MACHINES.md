# Autonomous Distribution Machines

"Autonomous" inside Dealix means **autonomous drafting and queueing**.
External actions remain founder-approved.

## 1. The autonomy boundary

- ✅ Autonomous: pulling intelligence, scoring, drafting, scheduling
  into the queue, retrying inside the queue.
- ❌ Not autonomous: sending email, posting on LinkedIn, sending
  WhatsApp, submitting a contact form to a third party, calling a
  payment API, committing to pricing.

Every machine in the war machine is autonomous **up to** the queue and
**not after** it.

## 2. Standard machine contract

```yaml
purpose:        what business outcome this machine improves
inputs:         names + sources + freshness window
outputs:        ledger file + schema
source:         provider list + fallback policy
approval_class: per-message | per-cadence | per-segment | per-campaign
trust_gate:    where in the flow the approval happens
owner:          named agent role (distribution_operator, etc.)
worker:         orchestrator job name
KPI:            primary + guard
failure_mode:   what can go wrong
recovery_path:  what happens when it does
kill_switch:    how to disable in one command
audit:          which ledger captures runs
```

All machines under `docs/growth/*MACHINE.md` declare this contract.
Verifiers in `scripts/verify_growth_system.py` enforce that the
sections exist.

## 3. Registry

The list of registered machines lives in
`data/private_ops_seed/growth/distribution_machines.csv`. The verifier
checks that each row maps to a `*MACHINE.md` doc and that the doc
contains all of the contract sections.

## 4. Hard refusals

These machines refuse to run, even with approval, when:

- the **kill switch** is engaged for the agent or for the segment;
- a **PDPL flag** marks the account or segment as opt-out;
- the **brand guardian** marks the draft as a voice violation;
- the **trust guardian** flags missing source / consent fields.

## 5. Cross-machine guardrail

A single account cannot appear in > 1 outbound queue per week. The
queue layer enforces deduplication across machines so we never look
like a multi-channel spam operation.
