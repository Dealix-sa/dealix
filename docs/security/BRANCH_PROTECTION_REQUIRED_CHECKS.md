# Branch Protection — Required Checks — حماية الفرع والفحوصات المطلوبة

Status: v1
Owner: Founder

## 1. Purpose — الغرض

Defines the branch protection rules and required CI checks on `main` and any release branch. No merge happens without these checks green.

يحدد قواعد حماية الفرع والفحوصات المطلوبة على `main` وأي فرع إصدار. لا دمج دون نجاح هذه الفحوصات.

## 2. Protected Branches — الفروع المحمية

- `main`
- `release/*`
- `hotfix/*`

## 3. Required Pull Request Reviews — مراجعات إلزامية

- At least one approving review.
- Founder review required on:
  - `policies/**`
  - `registries/**`
  - `evals/gates/**`
  - `docs/security/**`
  - `docs/ai/**`
  - any file under `src/dealix/guardian/**`
- "Trust Guardian" label required on PRs touching the items above.

## 4. Required Status Checks — فحوصات الحالة الإلزامية

The following checks MUST be green before merge:

| Check | What it verifies |
|---|---|
| `ci/lint` | Style and type checks |
| `ci/unit` | Unit tests |
| `ci/integration` | Integration tests |
| `ci/eval-gate` | Full safety eval suites pass per `evals/gates/dealix_agent_eval_gate.yaml` |
| `ci/policy-parse` | `policies/dealix_control_policy.yaml` parses and validates |
| `ci/registry-validate` | `registries/agent_registry.yaml` validates against schema |
| `ci/secrets-scan` | No secret patterns in diff |
| `ci/deps-scan` | No P1+ vulnerable dependencies |
| `ci/sbom` | SBOM artifact produced |
| `ci/docs-links` | Doc cross-links resolve |
| `ci/migration-dryrun` | DB migrations apply cleanly on a staging snapshot |
| `ci/security-gate` | Aggregate gate from the Production Security Gate doc |

## 5. Force Push, Deletion, History — الدفع القسري والحذف

- No force pushes to protected branches.
- No branch deletions for protected branches.
- Linear history required; merges are squash or rebase.

## 6. Signed Commits — التوقيع

- All commits to protected branches must be signed.
- Unsigned commits are rejected at push time.

## 7. CODEOWNERS — مالكو الكود

- `CODEOWNERS` file enforces founder review for the paths listed in Section 3.
- Codeowner approval counts toward the required review minimum.

## 8. Automation — الأتمتة

- Dependabot (or equivalent) updates are auto-opened but never auto-merged; they go through the same checks.
- Renovate windows scheduled outside business hours.

## 9. Drift Detection — كشف الانحراف

- A weekly job verifies the branch protection settings match this document.
- Any drift opens a P1 ticket and pages the founder.

## 10. Non-Negotiables — خطوط حمراء

- No bypass of required checks; admin-merge is disabled.
- No merge without founder review on guarded paths.
- No skipping the eval gate, ever.
- No unsigned production commits.

## 11. References — مراجع

- `docs/security/PRODUCTION_SECURITY_GATE.md`
- `docs/security/ULTIMATE_SECURITY_GOVERNANCE.md`
- `docs/evals/EVAL_GATE_V1.md`
- `docs/ai/AGENT_REGISTRY_SYSTEM.md`
