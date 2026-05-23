# Public Repo Safety

Rules for what may and may not live in the public Dealix repository.

## Allowed in public repo
- Process documentation (this directory).
- Templates with no real client data.
- Open-source code and infrastructure.
- Public case studies (anonymized or explicitly approved).
- Public sector reports.

## Forbidden in public repo
- Real client names, contacts, or business details without written approval.
- Real lead tables.
- Real outreach logs.
- Real payment, invoice, or revenue figures.
- Private credentials, tokens, or API keys.
- Internal pricing experiments not yet decided.

## How sensitive data is kept out
- `dealix-ops-private/` is the canonical home for sensitive operational data and is git-ignored.
- Pre-commit hooks scan for secret patterns.
- `.gitleaks.toml` and `.secrets.baseline` enforce baselines.
- Periodic audit of the public repo for accidental sensitive content.

## On accidental exposure
- Treat as an incident (`INCIDENT_RESPONSE.md`).
- Rotate any exposed credentials immediately.
- Notify affected parties when material.

## Rule
If unsure whether a file belongs public, the default is private. Move it out of `dealix-ops-private/` only after explicit review.
