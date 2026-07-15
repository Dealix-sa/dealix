# Public / Private Boundary

## Purpose
Keep the public Dealix repository safe to share with anyone, and keep operating data, leads, clients, and revenue in the private ops repository.

## Owner
Sami / Trust owner.

## Review Cadence
Weekly, and on every new file pattern.

## Repositories
- **Public**: `dealix` (this repo). Code, doctrine, playbooks, templates, verifiers.
- **Private**: `dealix-ops-private`. Real leads, real clients, real revenue, approvals, decision logs.

## Files Allowed in Public Repo
- Source code (`api/`, `core/`, `dealix/`, `dealix_cli/`, `scripts/`).
- Doctrine and playbooks under `docs/`.
- Templates and example schemas with synthetic data only.
- Tests with synthetic fixtures.
- CI workflows.

## Files NOT Allowed in Public Repo
- Real lead lists, real client names linked to revenue, real contact info.
- Real revenue numbers, invoices, payment receipts, bank details.
- Personally identifiable information (PII) of any kind.
- Founder approval logs and decision logs.
- Secrets, API keys, credentials, tokens.

## Hard Rules
1. Any file whose name matches sensitive patterns (e.g. `*real*.csv`, `*pii*`, `*private*`, `*.env`, `*.key`) is blocked from public commits via `.gitignore` and pre-commit checks.
2. If a PII leak is suspected, run `scripts/run_secret_scanning.py` (or equivalent), rotate any exposed secret, and log the incident.
3. Any sample data in public repo must be clearly synthetic (e.g. `name: "Sample Co"`, `email: "lead@example.com"`).

## Process
- Before pushing, run the public safety check.
- If unsure whether a file is public-safe, treat it as private.

## Linked Systems
- docs/trust/TRUST_CONTROL_SYSTEM.md
- .gitleaks.toml
- .gitignore
- .secrets.baseline

## Last Reviewed
2026-05-23
