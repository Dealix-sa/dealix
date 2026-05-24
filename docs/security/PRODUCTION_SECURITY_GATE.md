# Production Security Gate — بوابة أمن الإنتاج

Status: v1
Owner: Founder
Enforcement: CI required check + deploy-time check.

## 1. Purpose — الغرض

A single gate that blocks any change from reaching production unless every safety, security, and governance check is green.

بوابة واحدة تمنع وصول أي تغيير إلى الإنتاج ما لم تكن كل فحوصات السلامة والأمن والحوكمة خضراء.

## 2. Required Checks — الفحوصات المطلوبة

| Check | Source | Blocking? |
|---|---|---|
| Lint and type check | CI | yes |
| Unit tests | CI | yes |
| Integration tests | CI | yes |
| Eval gate (full safety suites) | `evals/gates/dealix_agent_eval_gate.yaml` | yes |
| Policy file parses | CI | yes |
| Agent registry validates | CI | yes |
| SBOM produced | CI | yes |
| Dependency vulnerability scan | CI | yes (P1+ fails) |
| Container image signature | CI | yes |
| Secrets scan | CI | yes |
| Migrations dry-run | CI | yes |
| Trust Guardian label on policy/registry/agent diffs | Reviewer | yes |
| Founder approval token at deploy | Deploy step | yes |

## 3. Pre-Deploy — قبل النشر

The deploy job MUST:
1. Verify the artifact hash matches the merged commit.
2. Fetch the eval gate state for that commit; refuse if not green.
3. Fetch the registry hash; refuse if it doesn't match the committed registry.
4. Verify the policy file hash; refuse on mismatch.
5. Request founder approval token (interactive or pre-issued, time-bound).
6. Write a pending deploy audit entry.

## 4. Deploy — أثناء النشر

- Migrations applied in order, with rollback on first failure.
- Health check required before flipping traffic.
- Canary at 10% for at least 10 minutes, watching error rate, p95 latency, Guardian rejects.
- Full rollout only after canary stable.

## 5. Post-Deploy — بعد النشر

- DORA tags written (deploy_id, lead_time, commit_sha).
- Smoke tests on Control Plane summary endpoint and Guardian.
- If any check fails: auto-rollback + P1 incident.

## 6. Forbidden Patterns — أنماط محظورة

- No hand-edited production state. All changes flow through PRs.
- No "hotfix" that skips the gate. The gate runs on hotfixes too.
- No environment-only secrets. Secrets live in the managed store; environments reference them.
- No bypass flags for the eval gate or Guardian in production.

## 7. Rollback — التراجع

- One-command rollback to the previous green artifact.
- Migrations: forward-compatible by default; explicit down migrations only when reviewed.
- Rollback writes a P1/P2 audit entry; counts as a change failure for DORA.

## 8. Audit — التدقيق

Every deploy emits an immutable audit entry:
- `commit_sha`, `artifact_hash`, `policy_hash`, `registry_hash`, `eval_gate_run_id`, `founder_token_id`, `deployer`, `started_at`, `ended_at`, `outcome`.

## 9. Non-Negotiables — خطوط حمراء

- Failing eval gate => no deploy.
- Failing secrets scan => no deploy.
- Missing founder approval token => no deploy.
- Missing audit entry => P0 incident.

## 10. References — مراجع

- `docs/security/BRANCH_PROTECTION_REQUIRED_CHECKS.md`
- `docs/security/INTERNAL_API_AUTH_GATE.md`
- `docs/security/ULTIMATE_SECURITY_GOVERNANCE.md`
- `docs/evals/EVAL_GATE_V1.md`
