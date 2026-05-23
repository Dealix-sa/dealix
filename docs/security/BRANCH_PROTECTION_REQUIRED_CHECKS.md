# Branch Protection and Required Checks

Branch protection is the codified rule that no change reaches `main` without passing the required checks and the required reviews. This doc enumerates them.

**Source of truth:** branch protection config in Git host + this doc
**Owner:** Engineering Lead
**Trust gate:** A2 — protection rules are policy; changes require founder approval.

## Protected branches

| Branch | Protection |
|--------|-----------|
| `main` | Full protection: required checks, required reviews, signed commits |
| `release/*` | Full protection plus founder approval |
| `policy/*` | Full protection plus founder approval and eval suite expansion |

Other branches are unrestricted but cannot merge into protected branches without going through the gate.

## Required CI checks

These checks are listed in `docs/security/PRODUCTION_SECURITY_GATE.md`. The branch protection layer simply makes them required:

- Static analysis.
- Dependency scan.
- Secret scan.
- Tests (unit + integration + contract).
- Eval gate.
- Schema-compatibility check.
- Policy-version pin.
- Migration safety.
- Audit-log emission.

A red check blocks merge. No "merge despite failure" path is configured.

## Required reviews

| Change scope | Required reviewers |
|--------------|--------------------|
| Default | One engineer |
| Trust Plane | Engineering Lead + Founder |
| Policy as Code | Engineering Lead + Founder |
| Agent Registry | Engineering Lead + Founder |
| Schema (output) | Engineering Lead (with consumer notification) |
| Migration | Engineering Lead + Database owner |
| Public surface | Marketing Lead + Founder |

A self-approval is not permitted.

## Signed commits

All commits to protected branches must be signed with verified keys. Unsigned commits are blocked at push.

## Force-push

Force-push to protected branches is prohibited. History is append-only.

## Failure modes

- **Reviewer fatigue:** rubber-stamp reviews. Detection: review-time and comment-density audit. Recovery: rotate reviewers; founder review.
- **Required-check rot:** a check is silently disabled or deleted. Detection: weekly config audit. Recovery: restore; root cause.
- **Bypass:** a commit reaches `main` without the required path. Detection: post-merge audit. Recovery: revert; investigate.

## Recovery path

If branch protection has been bypassed, the founder triggers a freeze: no merges accepted until the audit closes and protection is recertified.

## Metrics

- Merges to protected branches per week.
- Required-check pass rate.
- Reviewer comment density.
- Bypass incidents (target: 0).

## Disclaimer

Branch protection codifies process; it does not guarantee correct code. Estimated value is not Verified value.
