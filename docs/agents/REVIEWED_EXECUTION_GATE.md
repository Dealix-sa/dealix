# Dealix Reviewed Execution Gate

## Executive decision

Dealix adopts the **execution discipline** demonstrated by `DannyMac180/sol-advisor`; it does not copy that repository into the Dealix production runtime.

The useful pattern is:

```text
architect / parent owner
-> bounded implementer
-> parent inspection of actual diff + tests
-> fresh independent read-only reviewer
-> explicit acceptance verdict
-> review receipt
```

This closes an acceptance gap without creating another Company OS, orchestrator, approval system, proof ledger, or source of truth.

## Why this fits Dealix

Dealix already has:
- project-scoped Codex implementation agents under `.codex/agents/`;
- Dealix project skills under `.agents/skills/dealix/`;
- release, safety, ownership, proof, approval, and CI doctrine;
- multiple specialized execution surfaces that should be consolidated rather than duplicated.

Therefore the highest-value adoption is an independent acceptance layer over what exists.

## Adoption matrix

| Pattern | Decision | Dealix implementation |
|---|---|---|
| Architect owns scope and acceptance | Adopt | Parent/orchestrator writes a bounded Task Contract and decides whether evidence satisfies it |
| Scoped implementer | Adopt | Reuse `dealix-engineer`, `dealix-content`, `dealix-sales`, `dealix-delivery`, or `improve-executor` |
| Parent verifies actual diff/tests | Adopt | Mandatory changed-file/diff inspection plus parent-run verification |
| Fresh independent review | Adopt | `.codex/agents/dealix-fresh-reviewer.toml`, read-only |
| Explicit stop/redesign behavior | Adopt | Reviewer verdict `rethink`; maximum two routine fix-review cycles |
| Acceptance receipt | Adopt and extend | `REVIEW_RECEIPT` captures exact SHAs, diff scope, evidence, verdict, and blockers |
| Parallel agents | Adapt | Allowed only with non-overlapping writable file ownership |
| Separate worktrees | Pilot only | Useful for high-parallelism developer workstations; not a Dealix production dependency |
| Original Sol Advisor plugin | Pilot only | Developer workstation option after repo-native gate proves useful |
| Cross-model second opinion | Pilot only | Optional review lane; never a source of truth and never a substitute for deterministic gates |
| New general orchestrator/runtime | Reject | Existing Dealix agents/skills remain authoritative |
| Auto-merge after AI review | Reject | Merge stays a separate human-approved L5 action |
| Unlimited agent swarm | Reject | Bounded, disjoint delegation only |
| Model-name configuration treated as proof | Reject | Runtime identity/effort must be observable or recorded as `unverified` |

## Canonical reviewed-execution flow

### 1. Task Contract

Before an implementer receives work, define:
- goal;
- definition of done;
- base SHA;
- allowed and forbidden paths;
- canonical systems that must be reused;
- safety invariants;
- required verification;
- stop conditions.

### 2. Bounded implementation

Use the narrowest existing Dealix agent. The implementer does not receive authority to broaden scope silently.

Parallel tasks require a File Ownership Map and must not write overlapping paths or mutate the same source-of-truth contract concurrently.

### 3. Parent verification

The parent inspects the actual diff and reruns the authoritative focused checks. The implementer's own report is not accepted as proof.

### 4. Fresh review

The fresh reviewer receives the contract, exact diff, and verification evidence. It does not receive the implementer's persuasion narrative. It is read-only and returns:
- `ship`;
- `fix-first`;
- `rethink`.

### 5. Review Receipt

Every non-trivial reviewed change should retain:

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

### 6. Release gate

A `ship` verdict means only that independent review found no blocker in the reviewed scope. It does not authorize merge, deployment, migration, external communication, payment, publication, secret changes, or destructive operations.

## Runtime/model integrity

The reviewer configuration requests a strong reasoning model and read-only sandbox. Configuration alone is not runtime proof.

If the host cannot expose the actual child-agent model or reasoning effort, the receipt must record them as `unverified`. If fresh read-only isolation itself cannot be established, review is blocked rather than silently downgraded.

## Similar patterns worth piloting later

Once the repo-native gate has measurable value, Dealix can test optional tools that strengthen the same discipline:
- cross-model second-opinion review;
- isolated-worktree parallel execution with explicit ownership;
- receipt-based agent orchestration;
- spec-to-task systems that preserve traceability from requirement to diff to verification.

The acceptance criterion for every pilot is reduction in rework, regression rate, review latency, or founder intervention. A tool that only adds agents or dependencies without measurable improvement should be removed.

## Metrics

Track these over reviewed PRs:
- first-review `ship` rate;
- `fix-first` defects found before CI/merge;
- `rethink` rate;
- post-merge regression rate;
- number of changed files per task;
- review cycles per PR;
- unresolved-thread count at readiness;
- founder interventions per reviewed PR;
- duplicate-system findings prevented;
- mean time from Task Contract to review receipt.

## Safety boundary

The reviewed-execution gate inherits all Dealix safety doctrine. In particular:
- no live cold outbound;
- no fake proof or revenue claims;
- no hidden secrets;
- no automatic production mutation;
- no automatic merge;
- no reviewer write authority;
- no parallel source of truth.
