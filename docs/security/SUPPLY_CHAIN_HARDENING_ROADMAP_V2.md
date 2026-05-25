# Supply Chain Hardening Roadmap v2

## Relationship to existing docs
Builds on:
- `docs/security/KEY_ROTATION.md` — key-rotation policy.
- `docs/security/CORS_POLICY.md` — CORS policy.
- `docs/security/RATE_LIMITS.md` — rate-limit policy.
- `.github/workflows/codeql.yml` — existing CodeQL workflow.
- `dealix/registers/technology_radar.yaml` — GitHub Rulesets ADOPT, OIDC ADOPT, Gitleaks/Bandit ADOPT.

## Purpose
Lock down the Dealix supply chain progressively. Each phase has clear entry criteria; no phase ships before the previous phase is verified.

## Phase 1
- branch protection
- required status checks
- unique workflow job names
- dependency review
- secret scanning
- push protection

## Phase 2
- OpenSSF Scorecard
- pinned GitHub Actions
- SBOM generation
- artifact signing

## Phase 3
- SLSA-aligned build pipeline
- OIDC deploy
- least-privilege tokens
- environment approvals
