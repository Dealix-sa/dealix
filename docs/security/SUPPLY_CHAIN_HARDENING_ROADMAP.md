# Supply Chain Hardening Roadmap

## Doctrine Anchor
- Non-negotiables touched: #3 (no cross-tenant operational access), #4 (no production autonomy without rollback path), #5 (no proof-level overclaiming).
- Frozen decisions touched: control-plane verification scripts as release blockers.

## Purpose

Harden Dealix against software supply-chain risk in phased increments, using OpenSSF Scorecard checks and SLSA-aligned build provenance as the external reference points and the existing security toolchain as the starting position.

## Existing Security Surface

- Secret scanning: `gitleaks`, `detect-secrets`, `trufflehog`.
- Static analysis: `bandit`.
- CORS, rate limits, key rotation: documented in `docs/security/`.
- Webhook HMAC verification (Moyasar): documented in `docs/BILLING_MOYASAR_RUNBOOK.md`.
- Non-root Docker container patterns.
- Pre-commit hooks: `make pre-commit-install`, `make pre-commit-run`.
- Security scans: `make security`.

## Phased Roadmap

### Phase 1 — Required status checks and baseline scanning

- Required status checks on protected branches (CI must pass before merge).
- Dependency review on every PR.
- Secret scanning enforced.
- OpenSSF Scorecard run on a schedule against the repo, with results published.

### Phase 2 — Build hardening

- Pin GitHub Actions to commit SHA (not tag).
- Generate Software Bill of Materials (SBOM) per release.
- Sign release artifacts.
- Produce provenance for release builds.

### Phase 3 — SLSA-aligned pipeline

- SLSA-aligned build pipeline for any artifact that ships to production.
- OIDC-based deploy (no long-lived cloud credentials).
- Least-privilege GitHub tokens for every workflow.
- Environment approvals for production deploys.

## Core Rules

- Required status checks are non-negotiable on protected branches. A green CI is a precondition for merge to `main`.
- Pre-commit hooks must not be skipped (`--no-verify`) without an explicit founder approval recorded in the PR.
- Secret scanning failures block the merge.
- A release without a documented rollback path is not a release.
- A new third-party dependency requires a recorded review (license, maintenance, alternative).

## Operating Cadence

| Cadence | What happens |
|---------|--------------|
| Per PR | Dependency review + secret scan + lint + security scan |
| Weekly | Scorecard results reviewed; regressions ticketed |
| Per release | SBOM + provenance for shipped artifacts |
| Quarterly | Dependency-floor review (remove what is no longer used) |

## Runtime Wiring

- Pre-commit hooks: `make pre-commit-install`, `make pre-commit-run`.
- Security scans: `make security`.
- Existing CI workflows: `.github/workflows/`.
- Existing security docs: `docs/security/`, `SECURITY.md`.

## Metrics

| Metric | Target | Source |
|--------|--------|--------|
| PRs merged with failing required checks | 0 | branch protection logs |
| OpenSSF Scorecard score | tracked, improving | scorecard runs |
| Skipped pre-commit hooks per quarter | 0 unless founder-approved | PR review |
| Releases without SBOM (after Phase 2) | 0 | release artifacts |
| Long-lived cloud credentials in CI (after Phase 3) | 0 | secret inventory |

## Cross-Links

- `SECURITY.md`
- `docs/security/` (existing security docs)
- `docs/BILLING_MOYASAR_RUNBOOK.md` (webhook HMAC pattern)
- `docs/transformation/01_doctrine_lock.md`
- `docs/engineering/OBSERVABILITY_SLO_SYSTEM.md`

## Open Items

- OpenSSF Scorecard is referenced but not yet wired as a scheduled workflow.
- SBOM and provenance generation (Phase 2) is roadmap, not current state.
- SLSA-aligned pipeline (Phase 3) is roadmap and depends on Phase 2.
- A dependency-review allowlist policy file is not yet authored.
