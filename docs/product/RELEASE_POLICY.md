# Release Policy

> How code changes go from PR to production.

## Branching

- `main` — protected, production-ready
- `claude/dealix-company-os-Yq0TX` — current Company OS development branch (this PR)
- Feature branches — `feature/{intake-id}-{slug}`
- Hotfix branches — `hotfix/{date}-{slug}`

## PR Requirements (enforced via branch protection)

- PR template completed
- Status checks green:
  - CI (`ci.yml`)
  - Dealix Company OS checks (`dealix-company-os.yml`)
  - Trust tests
  - Public safety scan
  - Security scan (`security.yml`)
- Conversation resolution required
- Branch up-to-date with main required
- Founder review required (until first hire)
- No direct push to `main` — ever

## Release Cadence

- **No fixed release cadence.** We ship when the change is ready, tested, reviewed, and adds value.
- **No batched releases.** One change per PR, shipped on merge to main.
- **Hotfixes** can ship same-day if Trust / Production-blocking severity.

## What Doesn't Ship Without Tests

Any change that:
- Touches `dealix/trust/` — Trust tests required
- Touches public claim text or templates — claim_guard tests required
- Touches `dealix/agents/` — agent eval suite must pass
- Touches data flow / persistence — integration tests required
- Touches `api/` — contract tests required

## What Doesn't Need Tests (with restraint)

- Pure docs changes
- README / CHANGELOG additions
- Cosmetic frontend (when frontend exists and is in scope)

If unsure, add tests anyway.

## Release Notes

Every meaningful release gets a CHANGELOG.md entry:
- Date
- One-line summary
- What changed (user-facing language)
- What's now possible
- Any migration notes
- Linked PR

## Rollback Plan

For every release that touches:
- Trust modules → revert PR; redeploy prior commit
- Customer-facing artifacts → pull artifact + apologize within 24 hr
- Pipeline data shape → migration script with backward compat

## Communication

- Internal: append to `DEALIX_EXECUTION_LEDGER.md`
- Customer-affecting: send notification before/after as appropriate
- Public (if material): one-line LinkedIn post per Content OS policy

## Pre-Release Checklist

- [ ] All status checks green
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] Migration / rollback plan documented (if applicable)
- [ ] Trust review (if applicable)
- [ ] Founder approval
- [ ] Ledger entry drafted

## Post-Release Checklist

- [ ] Monitor for 24 hours
- [ ] Update CHANGELOG.md
- [ ] Close intake row
- [ ] Capture learning if non-trivial
- [ ] Tell relevant customers (if customer-affecting)

## What This Refuses

- "Quick ship" without tests
- Merging with red checks "just for now"
- Force-pushing to main
- Bypassing branch protection ever
- Rolling out customer-affecting changes silently
- Releasing on Friday or weekend (Saudi work week constraint)
