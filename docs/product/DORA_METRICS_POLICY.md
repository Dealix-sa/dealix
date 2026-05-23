# DORA Metrics Policy

## Purpose
Measure engineering speed and stability for Dealix.

## Owner
Sami / Engineering owner.

## Review Cadence
Weekly.

## Inputs
- Git commits.
- Deployments.
- Incidents.
- Failed checks.
- Recovery time.

## Outputs
- Engineering health review.
- Bottleneck detection.
- Build/fix/defer decisions.

## Rules
Engineering should improve revenue, delivery, trust, learning, or founder leverage.
Do not optimize deployment speed at the cost of trust or data safety.
Failed production changes must produce a learning item.

## Metrics
- Deployment frequency.
- Lead time for changes.
- Change failure rate.
- Failed deployment recovery time.
- CI pass rate.
- Trust test pass rate.

## Evidence
- GitHub Actions.
- deployment logs.
- incident runbook.
- weekly engineering review.

## Last Reviewed
2026-05-23
