# Deployment

## Purpose
Define how Dealix code, configuration, and AI assets move from development to production safely and reversibly.

## Owner
Sami / Engineering owner.

## Review Cadence
Monthly, plus after any incident.

## Inputs
- Code changes (PRs).
- Configuration and secret changes.
- Model and prompt changes.
- Infrastructure changes.
- CI/CD signals.

## Outputs
- Deployment checklist per environment.
- Rollback procedure per environment.
- Release notes.
- Incident response playbook.

## Rules
- No deployment to production without green CI and required reviews.
- Secrets never enter the repository; they live in the secret store and are referenced by name.
- Production-affecting changes follow a documented rollback path before they go out.
- Customer-facing breaking changes require A2 founder approval and customer notice.

## Metrics
- Deployment frequency.
- Lead time from merge to production.
- Change failure rate.
- Mean time to restore.

## Evidence
- `.github/workflows/` files.
- deployment checklist in this folder.
- rollback procedure in this folder.
- incident reports.

## Last Reviewed
YYYY-MM-DD
