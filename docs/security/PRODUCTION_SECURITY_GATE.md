# Production Security Gate

The Production Security Gate is the last set of checks a change passes before it reaches production. A change that fails the gate does not deploy.

**Source of truth:** CI pipeline config + this doc
**Owner:** Engineering Lead
**Trust gate:** A2 — gate rules are policy; changes require founder approval.

## Required checks

| Check | Purpose | Failure |
|-------|---------|---------|
| Static analysis | Catch obvious bugs and security smells | Block |
| Dependency scan | Detect vulnerable libraries | Block on high-severity |
| Secret scan | Detect inline secrets | Block |
| Tests | Unit + integration + contract | Block on red |
| Eval gate | `evals/gates/dealix_agent_eval_gate.yaml` | Block on agent fail |
| Schema-compatibility check | Output schema changes are backward compatible or coordinated | Block on break |
| Policy-version pin | Policy version referenced in code matches deployed policy | Block on mismatch |
| Migration safety | DB migrations are forward-only and reversible | Block on unsafe |
| Audit-log emission | Code paths that should log do log | Block on omission |
| Founder approval | For changes touching trust plane, finance, or policy | Block until approved |

## Approval matrix

| Change type | Approval |
|-------------|----------|
| Internal-only, no policy change | Engineering Lead |
| Trust Plane touch | Founder (A2) |
| Policy change | Founder (A2) + eval suite expansion |
| Finance touch | Founder (A2) |
| External-surface touch | Founder (A2) |

## Deploy windows

- **Default:** business hours, Riyadh time, Sunday-Thursday.
- **Hotfix:** any time with named approver.
- **Frozen:** during quarter close (last 3 business days of each quarter) or active P0 incident.

## Rollback

Every deploy carries a rollback plan. If a deploy raises a P0 alarm within 30 minutes, automatic rollback is the default. The default can be overridden only by the founder.

## OWASP / NIST posture

- **LLM05 Supply chain.** Dependency scanning + pinned versions + SBOM.
- **Govern / Manage.** Required checks codify governance into CI; rollback codifies management.

## Failure modes

- **Gate bypass:** a deploy reaches production without passing the gate. Detection: deploy audit. Recovery: rollback; CI rule strengthened; root cause filed.
- **Stale check:** a check certifies behaviour that has since changed. Detection: weekly diff. Recovery: refresh, re-run.
- **Alarm-suppression deploy:** a deploy that hides existing alarms. Detection: alarm coverage diff. Recovery: revert.

## Recovery path

If gate integrity is in doubt, deploys freeze until the gate is recertified. Hotfixes require explicit founder approval per fix.

## Metrics

- Gate pass rate per PR (target: high, with meaningful failures).
- Time from commit to production (DORA lead time).
- Rollback rate (DORA change-failure rate).
- Bypass incidents (target: 0).

## Disclaimer

The gate is a quality and security check, not a guarantee of correctness. Estimated value is not Verified value.
