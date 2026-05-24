# Dealix Missing Systems

What is **not yet** implemented, with explicit reasons. If something is
not on this list and not green in `DEALIX_IMPLEMENTATION_AUDIT.md`,
that's a contradiction the next CI run will catch.

## Purpose

Surface gaps honestly. The next item on this list is, by definition,
the next thing to build.

## Owner

Founder. Edited only after `verify_everything.py` confirms a gap.

## Cadence

- Re-evaluated every CI run.
- Re-prioritized in the CEO weekly review.

## Categories

- **Missing**: file or system does not exist.
- **Empty**: file exists but is below the minimum size threshold.
- **Partial**: file exists but missing structural sections / keywords.
- **Unwired**: file exists but no Makefile / workflow / verifier calls it.
- **Unsafe**: a guard is missing (live send, banned claim, no
  approval, etc.).
- **Blocked**: cannot be implemented until an upstream decision is made.

## Open Gaps

| Priority | Category | Layer | Item | Why it matters | Owner | Target |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | Wiring | github_actions | `.github/workflows/dealix-everything.yml` must be **required** on `main` via GitHub branch protection | Without required status, `make everything` failing locally is invisible at merge time | Founder | First admin window |
| P2 | Process | ai_governance | Quarterly NIST AI RMF + ISO 42001 self-audit minutes not yet appended to `docs/governance/RUNTIME_GOVERNANCE.md` | Reviewer-visible signal of ongoing governance | Founder | Next quarterly cycle |
| P3 | Frontend | live_send_safety | Frontend approvals page (`/ops/approvals`) must surface a "kill switch ON" banner when `WHATSAPP_ALLOW_LIVE_SEND=true` | Defense-in-depth — every operator can see the state at a glance | Founder | First feature window |
| P4 | Eval | eval_gate | `evals/personal_operator_cases.jsonl` + `revenue_os_cases.jsonl` should be enrolled into `verify_eval_gate.py` (currently it only checks YAML suites) | Catch shrinkage on JSONL eval sets too | Founder | Next eval review |
| P5 | Docs | customer_success_os | `data/customers/` schema not yet documented in a runbook | Customer success doc references it but the schema is implicit | Founder | First customer signed |

## How To Use This List

1. Take the top open gap.
2. Build the smallest thing that makes its verifier exit 0.
3. Move the row out of "Open Gaps" into "Closed Gaps" below with the
   commit SHA.
4. Run `make everything` to confirm.

## Closed Gaps

| Date | Priority | Item | Commit |
| --- | --- | --- | --- |
| 2026-05-24 | P0 | Manifest, verifier suite, policy, registries, founder OS docs, audit reports, Makefile targets, GitHub workflow | (initial Audit-First Remediation Layer commit) |

## Verification

```bash
make everything
```

If `verify_everything.py` exits 0 and this file still lists open gaps,
the list is stale — refresh it from the verifier output.
