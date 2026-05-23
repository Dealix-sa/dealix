# Release Policy

How Dealix ships product changes safely.

## Pre-release
- Tests pass in CI.
- Documentation updated (one-page user note).
- Claim Guard pass on any user-facing copy.
- Approval recorded for any A2 change.

## Release
- Feature flag where possible.
- Rollout to a small cohort first when the change is user-visible.
- Monitor for the first 24 hours.

## Post-release
- Status note in the next weekly client report if it affects clients.
- Update `ROADMAP.md` to move the item to "shipped".
- Capture lessons in `EXPERIMENT_LOG.md` if it was a test.

## Rollback
- Roll back if any of: data loss, customer-visible regression, security or trust signal.
- Roll back is not a failure. It is the point of having a release policy.

## Rule
Boring releases are safe releases. Heroics are an anti-pattern.
