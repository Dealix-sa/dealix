# Security Baseline

## Purpose
Establish the minimum non-negotiable security posture for the Dealix public repository and operational environment. This baseline is the gate Sprint 0 must satisfy before any other sprint begins.

## Scope
Applies to:
- The public Dealix repository (this repo).
- The private `dealix-ops-private/` working tree.
- The founder's local environment and any contractor with read access.

## Baseline controls
1. **Secret hygiene**
   - `.env` and any file matching `.env.*` (except `.env.example` and `.env.staging.example`) MUST be gitignored.
   - No real API keys, tokens, customer credentials, or live signing keys may be committed.
   - `git secrets` / `detect-secrets` / `gitleaks` runs in pre-commit and CI.
2. **Public/private boundary**
   - Customer data lives only in `dealix-ops-private/`.
   - The scanner `scripts/verify_public_safety_v2.py` blocks PR merges that violate this.
   - `scripts/verify_data_boundary.py` enforces that no private-only filenames leak into the public tree.
3. **Branch protection**
   - `main` is protected; merges require: passing CI, one approval, no force pushes.
4. **Dependency policy**
   - Dependencies are pinned in `requirements.txt`; security advisories monitored via GitHub Dependabot and the `dependency-review` workflow.
5. **Incident response**
   - All security events follow `docs/security/INCIDENT_RESPONSE_SYSTEM.md`.

## Required artifacts
- `SECURITY.md` (root) — public-facing disclosure contact.
- `docs/security/SECURITY_RELIABILITY_SUPPLY_CHAIN_OS.md` — full operating system.
- `docs/security/DEPENDENCY_POLICY.md` — dependency rules.
- `docs/security/INCIDENT_RESPONSE_SYSTEM.md` — incident handling.

## Verification
Run:
```
python scripts/verify_security_reliability_os.py
python scripts/verify_public_safety_v2.py
python scripts/verify_data_boundary.py
```
All three must exit 0.
