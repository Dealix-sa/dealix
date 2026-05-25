# Dealix Acceptance & Certification System

> Internal operational certification — separate from partner certification
> (which lives in [`CERTIFICATION_SYSTEM.md`](./CERTIFICATION_SYSTEM.md)).
> This file answers a single question: **Is Dealix safe to scale right now?**

## Purpose

Certify whether Dealix is structurally complete, operational, commercially
active, and safe to scale.

## Certification Levels

### C0 — Not Ready
Missing core files, broken checks, or unsafe outputs.

### C1 — Repo Ready
Repository structure, code health, docs, schemas, and workflows pass.

### C2 — Runtime Ready
Server reports, workers, private ops contracts, and logs pass.

### C3 — Revenue Ready
Lead intelligence, outreach queues, follow-ups, samples, proposals, and
payment capture exist.

### C4 — Trust Ready
No unsafe claims, no secrets, no suppressed outreach, no external action
without approval.

### C5 — Scale Ready
Sector machines, approval center, sales cockpit, observability, evals, and
business evidence pass.

## Rule

Dealix can only scale when **C1 + C2 + C3 + C4** pass.
Dealix can only automate more when **C5** passes.

## How To Run

```
make verify-all       PRIVATE_OPS=/opt/dealix-ops-private
make certify          PRIVATE_OPS=/opt/dealix-ops-private
make verification-brief PRIVATE_OPS=/opt/dealix-ops-private
```

Outputs land in `$PRIVATE_OPS/founder/dealix_os_certification.md` and
`$PRIVATE_OPS/founder/ceo_verification_brief.md`.

## Checks → Levels

| Check | Script | Level |
|---|---|---|
| Repository Structure | `scripts/verify_repository_structure.py` | C1 |
| Code Health | `scripts/verify_code_health.py` | C1 |
| Private Ops Contracts | `scripts/verify_private_ops_contracts.py` | C2 |
| Server Runtime | `scripts/verify_server_runtime.py` | C2 |
| Revenue Runtime | `scripts/verify_revenue_runtime.py` | C3 |
| Prompt Output Quality | `scripts/verify_prompt_output_quality.py` | C4 |
| Trust Security Runtime | `scripts/verify_trust_security_runtime.py` | C4 |
| Business Evidence | `scripts/verify_business_evidence.py` | C5 |

All eight are orchestrated by `scripts/certify_dealix_os.py`, which writes
a single certification report and exits non-zero on any failure.

## CEO Rule

Any new development must answer yes to all three:

1. Did `make certify` pass?
2. Does `ceo_verification_brief.md` give a clear next action?
3. Does this development move a commercial number or reduce a real risk?

If no — defer it.
