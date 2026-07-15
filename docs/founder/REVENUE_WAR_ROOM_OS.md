# Revenue War Room OS

## Doctrine Anchor
- Non-negotiables touched: #1 (approval before external action), #2 (no value claim without evidence), #5 (no proof-level overclaiming).
- Frozen decisions touched: golden chain as default execution path, approval-first for external action.

## Purpose

Force Dealix to convert activity into revenue decisions on a fixed cadence. The war room is the founder's daily and weekly forcing function for closing loops, killing what is not working, and doubling down on what is.

## Daily Questions

Each business day, before opening anything new, answer:

- What moves cash today?
- What follow-up is overdue?
- Which proposal needs payment follow-up?
- Which positive reply still has no sample?
- Which sector is showing signal?
- What should we stop?

These six questions are the daily war-room agenda. The cockpit (`docs/control_plane/SALES_COCKPIT_SYSTEM.md`) surfaces the records that answer them.

## Weekly Decisions

Once per week:

- **Double down** on the sector or channel that produced qualified replies or cash.
- **Kill** the weakest channel or motion from the past two weeks.
- **Improve** the message, sample, or proposal that is losing somewhere measurable.
- **Adjust** price up or down based on the pricing yield review (`docs/finance/PRICING_YIELD_MANAGEMENT.md`).
- **Ship** a sample or asset that unblocks a stalled positive reply.
- **Push** the proposal that has waited too long for payment / PO.
- **Ask** for one referral from the strongest active client.

## Core Rules

- No week closes without one revenue decision being recorded.
- A "we are working on it" status is not a decision.
- A decision is: change X, by Y date, expecting Z signal, with the result recorded.
- Every decision is logged with a source-evidence link to the data that drove it.
- A decision that turned out wrong is documented as such; lessons go into the playbook.
- The war room never produces outcome promises; it produces commitments to actions Dealix controls.

## Cadence

| Cadence | What happens | Surface |
|---------|--------------|---------|
| Every business day | Daily founder digest opens, the six daily questions are answered, the cockpit is cleared | `make v5-digest`, `daily_digest.yml` |
| End of week | Weekly review: each channel scored, one decision per channel category | weekly review note |
| End of month | Monthly board-level KPI review | `docs/founder/BOARD_LEVEL_KPI_STACK.md` |

## Runtime Wiring

- Daily founder digest: `.github/workflows/daily_digest.yml`, `make v5-digest`.
- Daily snapshot: `.github/workflows/daily_snapshot.yml`, `make v5-snapshot`.
- Founder daily brief script: `scripts/dealix_founder_daily_brief.py`.
- Founder strongest ops daily: `.github/workflows/founder_strongest_ops_daily.yml`.
- Weekly autonomous ops: `.github/workflows/founder_autonomous_ops_weekly.yml`.
- Existing war room artifacts (cross-link): `docs/ops/DEALIX_REVENUE_WAR_ROOM_AR.md`, `docs/ops/REVENUE_WAR_ROOM_30_DAY_TRACKER.yaml`, `docs/ops/FOUNDER_REVENUE_DAY_ONE_AR.md`.

## Metrics

| Metric | Target | Source |
|--------|--------|--------|
| Weeks closed with at least one recorded revenue decision | 100% | weekly review notes |
| Daily digest opened and acted on | every business day | `AuditLogRecord` per panel |
| Decisions revisited as "wrong" within 30 days | tracked, no shame; drives learning | weekly review notes |
| Proposals that aged past 14 days without payment / PO follow-up | 0 in any given week | revenue events |

## Cross-Links

- `docs/control_plane/SALES_COCKPIT_SYSTEM.md`
- `docs/founder/BOARD_LEVEL_KPI_STACK.md`
- `docs/distribution/DEALIX_DISTRIBUTION_OS.md`
- `docs/distribution/EXPERIMENT_ENGINE.md`
- `docs/finance/PRICING_YIELD_MANAGEMENT.md`
- `docs/ops/DEALIX_REVENUE_WAR_ROOM_AR.md`
- `docs/ops/REVENUE_WAR_ROOM_30_DAY_TRACKER.yaml`
- `docs/transformation/01_doctrine_lock.md`

## Open Items

- The end-of-week review note has no template; we use the daily digest plus ad-hoc notes today.
- A canonical "decisions log" file or table that the weekly review writes to does not yet exist.
- The link from a war-room decision to the experiment registry (when the decision is "run experiment X") is informal.
