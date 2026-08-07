---
name: dealix-reviewed-execution
description: Run non-trivial Dealix implementation through a bounded architect-implementer-fresh-reviewer acceptance gate using existing Dealix agents, exact diffs, verification evidence, non-overlapping ownership, and a review receipt before merge consideration.
---

# Dealix Reviewed Execution Gate

## Purpose

Use this skill for non-trivial Dealix code, infrastructure, data-contract, security, commercial-runtime, or cross-module changes where implementation quality matters more than raw agent throughput.

This skill does **not** create another Dealix orchestrator, Company OS, Approval Center, Proof Ledger, or source of truth. It is an acceptance protocol over the existing Dealix agents and release process.

Core loop:

```text
Task Contract
-> bounded implementation
-> parent diff/test verification
-> fresh independent review
-> review receipt
-> fix or redesign if needed
-> PR readiness decision
```

## Existing agents to reuse

Prefer the narrowest existing implementer:

- `dealix-engineer` for Python, API, tests, persistence, migrations, and bounded runtime changes.
- `dealix-content` for internal/customer-safe documentation and content artifacts.
- `dealix-sales` for sales workflow artifacts and commercial logic within existing doctrine.
- `dealix-delivery` for delivery workflows, proof packs, and client execution artifacts.
- `improve-executor` only for an already-approved, bounded improvement plan.

Use `dealix-fresh-reviewer` for the final independent acceptance review. The reviewer is read-only and must never implement its own findings.

## Step 0 — Establish reality

Before implementation, inspect the actual repository state and the target branch/PR. Never rely on a historical report alone.

Minimum evidence:

```bash
git status --short
git branch --show-current
git rev-parse HEAD
git log --oneline -5
gh pr list --limit 30
```

If the work is based on an existing PR, capture its current head SHA and unresolved review threads before making decisions.

## Step 1 — Write a bounded Task Contract

The parent/orchestrator must state:

```text
task_id:
goal:
definition_of_done:
base_sha:
allowed_files_or_directories:
forbidden_files_or_directories:
canonical_systems_to_reuse:
safety_invariants:
required_tests:
stop_conditions:
```

The contract is authoritative for scope. Do not tell an implementer to "improve everything".

### Mandatory Dealix invariants

Unless a narrower rule is stricter:

- Reuse the canonical Company Brain, Opportunity/relationship contracts, Action/Draft/Approval chain, Proof/Learning contracts, and existing release tooling.
- Do not create a parallel source of truth, workflow runtime, approval system, proof ledger, CRM core, model router, or sender.
- Preserve draft-only outbound defaults and explicit approval gates.
- Never fabricate customer, revenue, delivery, proof, consent, or production evidence.
- No secrets in prompts, logs, diffs, reports, or committed files.
- Merge, production mutation, external send/publish, payment, and destructive actions remain separate L5 approvals.

## Step 2 — Delegate bounded implementation

Give the implementer the Task Contract plus only the context needed to execute it.

The implementer must:
- touch only owned files unless it reports a required scope change first;
- add or update behavior-level tests for public behavior it changes;
- preserve doctrine and source-of-truth boundaries;
- report files changed, tests run, failures, and remaining uncertainty;
- stop instead of weakening a guard to obtain green tests.

### Parallelism rule

Parallel implementation is allowed only when file ownership is **non-overlapping** and the tasks do not mutate the same state or source-of-truth contract.

Create a File Ownership Map before parallel work:

```text
worker_a: [paths]
worker_b: [paths]
shared_read_only: [paths]
forbidden_shared_writes: true
```

If two tasks need the same writable file or schema, serialize them. Never run competing writers and reconcile by guesswork later.

## Step 3 — Parent verifies the implementation independently

The parent/orchestrator must not accept the implementer's self-report as proof.

Inspect the real change:

```bash
git diff --check
git diff --name-only <base_sha>...HEAD
git diff <base_sha>...HEAD
```

Then rerun the relevant verification from the parent context. Prefer the smallest authoritative suite first, followed by required repo gates.

Typical Dealix gates include, as applicable:

```bash
python -m compileall -q api app core db dealix scripts
python scripts/verify_no_auto_external_send.py
python scripts/verify_company_intelligence_entity_ownership.py
python scripts/verify_company_launch_ready.py
python scripts/verify_railway_surfaces.py
python -m pytest -q <focused tests>
```

Do not use `|| true` when producing final acceptance evidence. A failing required command is evidence, not noise.

## Step 4 — Fresh independent review

After implementation is stable, invoke `dealix-fresh-reviewer` from a fresh context.

Provide:
- Task Contract;
- actual base/head SHAs;
- changed-file list and actual diff;
- parent-run test/check output;
- only the applicable doctrine/source-of-truth references.

Do **not** prime the reviewer with the implementer's rationale, desired verdict, or claims that the change is already correct.

The reviewer must be read-only. If fresh read-only review cannot be established, acceptance is blocked; do not silently replace it with self-review.

## Step 5 — Act on the verdict

Allowed verdicts:

- `ship`: no blocker remains; the change may proceed to normal PR readiness checks.
- `fix-first`: return only the blocking findings to the bounded implementer, then repeat parent verification and fresh review.
- `rethink`: stop patching; revisit the Task Contract or architecture because the approach is structurally wrong.

Limit routine fix/review cycles to two. If a meaningful blocker survives two cycles, default to `rethink` or split the change into a smaller slice instead of creating an endless agent loop.

## Step 6 — Require a Review Receipt

Before a non-trivial PR is considered merge-ready, preserve a receipt in the PR body/comment or a dedicated internal artifact:

```text
REVIEW_RECEIPT
base_sha:
head_sha:
changed_files_reviewed:
evidence_checked:
reviewer_runtime_observed:
reasoning_effort_observed:
verdict: ship|fix-first|rethink
findings:
unresolved_blockers:
merge_recommendation:
```

Runtime/model identity is evidence only when observable. Configuration is not proof. Write `unverified` rather than making a model-identity claim without runtime evidence.

## Step 7 — Merge remains a separate gate

A `ship` review is not permission to merge or deploy.

Before merge consideration require:
- exact-head CI terminal and acceptable;
- unresolved review threads handled;
- mergeability confirmed;
- no base drift that invalidates the review;
- the user's action-specific approval for merge.

Production deployment, secret changes, migrations, sends, publishes, payments, and destructive changes remain separate approvals even after merge.

## Review quality heuristics

A useful fresh review should prioritize:
1. correctness and regressions;
2. source-of-truth duplication;
3. authority/safety expansion;
4. tenant/provenance/approval/proof boundaries;
5. hidden failure modes and idempotency;
6. behavior-level test adequacy;
7. unnecessary complexity and scope creep.

Style-only observations never outweigh correctness blockers.

## Anti-patterns

Do not:
- add a new general orchestrator merely to run this protocol;
- accept green CI without reading the diff;
- ask the implementer to be its own independent reviewer;
- let the reviewer edit the implementation;
- spawn unlimited agents on overlapping work;
- retry the same failing approach indefinitely;
- auto-merge on reviewer `ship`;
- claim the configured reviewer model/effort actually ran unless the host exposes evidence.

## Definition of done

This skill has been applied successfully when:
- scope is explicit and bounded;
- implementation used an existing Dealix agent or direct bounded execution;
- overlapping parallel writes were prevented;
- the parent inspected the actual diff and reran required checks;
- a fresh read-only review produced `ship`, `fix-first`, or `rethink`;
- a Review Receipt exists;
- L5 actions remain unexecuted until separately approved.
