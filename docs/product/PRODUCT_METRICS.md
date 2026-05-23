# Product Metrics

> What we measure about the product itself (not revenue — that's `REVENUE_METRICS.md`).

## Engineering Health Metrics

| Metric | Target | Source |
|---|---|---|
| CI pass rate (last 30 days) | ≥ 95% | GitHub Actions |
| Time from PR open to merge | < 48 hr (S/XS); < 5 days (M) | Git history |
| Trust-test pass rate | 100% (no exceptions) | `tests/trust/` |
| Public safety scan pass rate | 100% | `verify_public_safety.py` |
| Open PR count | < 5 | GitHub |
| Stale branch count | < 10 (no branch > 30 days idle) | GitHub |

## Quality Metrics

| Metric | Target | Source |
|---|---|---|
| Bugs reported per month | ≤ 3 | issue tracker / friction log |
| Bugs fixed within 7 days | 100% (sev 1-2); 80% (sev 3) | issue tracker |
| Regression rate | < 5% (releases that need follow-up fix) | CHANGELOG analysis |
| Test coverage (modules touched) | ≥ 80% | coverage report |

## Adoption Metrics (internal — eat-the-cooking)

| Metric | Target | Source |
|---|---|---|
| Founder Daily Brief read rate | ≥ 5/7 days/week | self-attestation |
| Approval queue cleared daily | ≥ 80% same-day | `trust/approval_log.csv` |
| Execution Ledger entries per week | ≥ 10 | `DEALIX_EXECUTION_LEDGER.md` |
| Weekly CEO Review completed | weekly (no skips > 2 wks) | `weekly_reviews/` |
| Decisions logged within 24 hr | ≥ 90% | `decision_log.md` |

## Adoption Metrics (customer-facing — when applicable)

| Metric | Target | Source |
|---|---|---|
| Sprint deliverables used by client (post-handoff) | ≥ 70% deliverables actively used in 14 days | follow-up call |
| Managed Ops drafts sent by client | ≥ 80% of approved drafts | client report |
| Quarterly review attendance | 100% | calendar |

## Feature Lifecycle Metrics

| Metric | Target | Source |
|---|---|---|
| Time from intake to triage | < 48 hr | intake log |
| Time from triage to build start | < 7 days (XS/S); < 14 days (M); < 30 days (L) | intake log |
| Time from build start to ship | within size estimate ± 20% | git history |
| Killed features per quarter | ≥ 2 (focus discipline signal) | `BUILD_DEFER_KILL.md` |
| Deferred features acted on | ≥ 50% by revisit date | intake log |

## Trust + Governance Metrics (cross-link to `TRUST_OS`)

| Metric | Target | Source |
|---|---|---|
| Approval log completeness | 100% (every external action logged) | `approval_log.csv` |
| claim_guard violations caught (pre-send) | track count | logs |
| claim_guard violations missed (post-send) | 0 | incident log |
| Suppression-list breaches | 0 | incident log |
| A3-blocked actions | 0 unless test | logs |

## Anti-Metrics (we don't measure or report)

- Lines of code
- Number of features shipped (we want quality not count)
- Velocity / story points (we don't story-point)
- "Time saved by AI" (unmeasurable, vanity)
- Number of agents (more isn't better)

## Reporting Cadence

- Daily: Founder Brief includes approval queue + ledger summary
- Weekly: Weekly CEO Review includes product section
- Monthly: Board memo includes engineering health + adoption snapshot
- Quarterly: full retrospective on metrics — what should we add / drop?

## When Metrics Drift

- Health metric red for 2 weeks → escalate to Weekly CEO Review
- Quality metric red for 2 weeks → halt new features until fixed
- Trust metric red ever → halt + advisor review same day
- Adoption red → revisit whether we're really eating our cooking

## What This Refuses

- Vanity metrics
- Metrics nobody acts on
- Metrics we can't compute from our own data
- Metrics whose definition keeps shifting
