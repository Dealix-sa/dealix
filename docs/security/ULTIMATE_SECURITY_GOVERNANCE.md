# Ultimate Security Governance

> Production-grade controls on a founder-led company.
> The main branch is production. Nothing merges without green gates.

---

## 1. Purpose

Define the security and governance controls that keep Dealix **safe to operate** at the same speed it operates.

This document is the security companion to:
- `docs/trust/ULTIMATE_TRUST_PLANE.md` (runtime governance)
- `docs/engineering/ULTIMATE_OBSERVABILITY_DORA.md` (deploy quality)
- `docs/data/ULTIMATE_DATA_PLATFORM.md` (data residency + privacy)

---

## 2. Required controls

These controls are non-negotiable. If any is broken, the team stops shipping until it is restored.

### 2.1 Branch protection on `main`
- `main` is protected.
- No direct push by anyone.
- Pull request required.
- At least one reviewer.
- Required status checks (§4) must be green.
- Force-push: disabled.
- Branch deletion: disabled.
- Linear history: required.
- Conversation resolution required before merge.

GitHub's branch protection / rulesets enforce this; the configuration lives alongside the repo.

### 2.2 Required status checks
The following checks must pass on every PR to `main`:
- `ci` (lint, type-check, unit tests).
- `codeql` (SAST).
- `dealix-ultimate-level` (blueprint integrity — this is what `make ultimate-level` runs).
- `frontend-build`.
- `backend-tests`.
- `migration-check` (when DB migrations are touched).
- `eval-gate` (when prompt templates or model wiring are touched).
- `prompt-output-safety` (prompt-injection + refusal + overclaim suites must pass for affected templates).

### 2.3 Secret scanning
- GitHub secret scanning enabled (push protection mode).
- `gitleaks` / `detect-secrets` run pre-commit and in CI.
- Any high-severity finding blocks merge.
- Found secrets are rotated within 24 hours and a postmortem is filed.

### 2.4 Dependency review
- GitHub Dependency Review on every PR.
- License policy: deny GPL-3.0 unless explicit founder approval; deny unmaintained packages (no release in 24 months).
- Vulnerabilities sev-high or above block merge.

### 2.5 SAST
- CodeQL (workflow already present).
- Bandit on Python code (via `make security`).
- Findings tracked; no high-severity finding survives a release.

### 2.6 Prompt / output safety checks
- Prompt-injection suite must pass for any prompt template touched in the PR.
- Output schema is enforced at runtime; CI runs a fixture set against the schema.
- Failed safety check blocks merge.

### 2.7 AI eval checks
- Regression suite ≥ 98% pass rate on the latest run.
- Refusal suite 100% pass.
- No regression on the `no_overclaim` suite.

### 2.8 Frontend build checks
- `npm ci` + `npm run build` must succeed.
- Bundle-size budget enforced (delta > +5% requires a justification comment).

### 2.9 Backend test checks
- Unit + integration tests green.
- Coverage delta on `dealix/trust/`, `dealix/security/`, `dealix/intelligence/` must not be negative.

### 2.10 Migration checks
- Forward migration applies cleanly to a fresh DB and to a copy of staging.
- Down migration applies cleanly.
- No destructive change (drop column, drop table) without `-- DESTRUCTIVE` comment and founder approval in the PR.

### 2.11 Deploy smoke tests
- Post-deploy smoke runs the `scripts/post_redeploy_verify.sh` 22-point verifier.
- A non-green smoke is a failed deploy and triggers rollback.

### 2.12 Rollback plan
- A documented rollback procedure exists.
- The previous container is retained and addressable.
- A `make rollback` (or equivalent runbook step) restores the previous version in ≤ 15 minutes.

---

## 3. Access control

### 3.1 Roles
- **Founder** — full access.
- **Trusted Engineer** — code repo access; read-only on `/finance`, `/audit`, `/evals`; cannot approve A2/A3.
- **Trusted Operator** — read-only on the console; cannot edit suppression or approval-class overrides.
- **External Partner** — sandboxed access to their own portal (Phase 9).

### 3.2 Authentication
- Founder + Trusted Engineer + Trusted Operator: SSO + MFA on every login.
- API tokens: scoped, expiring, rotatable.
- No shared accounts.

### 3.3 Authorization
- Default deny.
- Every endpoint declares the roles allowed.
- Every state-changing action records the actor.

### 3.4 Provisioning + deprovisioning
- Access changes are PRs reviewed by the founder.
- Departure triggers a same-day revocation across GitHub, cloud, console, integrations.

---

## 4. Supply chain

- Dependencies pinned to specific versions (`requirements.txt`, `package-lock.json`).
- Reproducible builds: `pip-compile`, `npm ci`, `Dockerfile` deterministic where possible.
- SBOM generated per release (CycloneDX); attached to the release.
- Build provenance attested via GitHub OIDC (when promoted to GA).

---

## 5. Data security

- Encryption at rest: managed Postgres + object storage default encryption.
- Encryption in transit: TLS 1.2+ for all inbound + outbound traffic.
- PII fields (`contacts.email`, `contacts.phone_e164`) encrypted with per-tenant keys.
- Backups encrypted with separate keys.
- Region: KSA-default; cross-region transfers require a documented data-boundary exception.

---

## 6. Logging & audit

- Application logs: structured JSON; per-actor, per-trace.
- Security logs: every authn, authz, secret rotation, access change.
- Audit logs: `audit_events` table (see Data Platform). Append-only; never updated, never deleted.
- Log retention: 90 days hot, 365 days warm, archive thereafter.

---

## 7. Incident response

The trust-plane incident procedure (`docs/trust/ULTIMATE_TRUST_PLANE.md` §9) applies for trust incidents. Security incidents follow the same shape:

1. **Contain** — disable affected access; rotate affected secrets; isolate affected accounts.
2. **Triage** — capture timeline and trace ids.
3. **Notify** — founder, plus customer if their data is involved, plus regulator if legally required.
4. **Correct** — patch; ship a regression test; update the policy.
5. **Postmortem** — within 7 days, stored under `docs/security/postmortems/`.

---

## 8. Vulnerability management

- Dependabot (or equivalent) enabled.
- Sev-critical: patch within 24h.
- Sev-high: patch within 7d.
- Sev-medium: patch within 30d.
- Public disclosure: per `SECURITY.md` in this repo.

---

## 9. Third-party providers

- Each provider is listed in `docs/security/providers.md` with:
  - What data we send them.
  - Where their service runs.
  - The DPA status.
  - The contractual subprocessors.
- Adding a provider is a founder decision and writes an audit entry.

---

## 10. Backup & recovery

- Backups: daily, encrypted, tested.
- Restore drill: at least quarterly; the restore time is published in `/security`.
- A backup that has never been restored is not a backup.

---

## 11. Compliance posture

Dealix is not a regulated entity by default, but operates as if it were:

- Privacy: PDPL (KSA) baseline.
- Data residency: KSA-default.
- AI risk management: NIST AI RMF mapping in `docs/trust/ULTIMATE_TRUST_PLANE.md` §6.
- LLM-specific risks: OWASP LLM Top 10 mapping in `docs/trust/ULTIMATE_TRUST_PLANE.md` §7.

The roadmap to a formal certification (ISO 27001, SOC 2) is **deferred** until Dealix has the cash to fund it and the customers to require it.

---

## 12. Production rule

> **Main branch is production. Nothing merges without green gates.**

This rule is enforced by:
- Branch protection on `main`.
- Required status checks (§2.2).
- This document, reviewed and updated at least once per quarter.

If any control above is found bypassed, the bypass itself is a Sev1 incident.
