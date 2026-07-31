# Improvement backlog — INDEX

Seeded by the first `improve` audit against commit `2ec6a6c`
(`.claude/skills/improve/`). Second pass (`/improve deep`, 2026-07-31,
commit `aae97bc`) audited the whole repo for sellability/trust/security/
tests/tech-debt/docs/direction across `api/`, `core/`, `db/`, `dealix/`,
`company/`, `auto_client_acquisition/`, `apps/web/`. Findings are vetted
(every `file:line` re-read before listing). This is a living backlog —
refresh with `/improve reconcile`.

## Priority order

| # | Plan | Category | Effort | Confidence | Wave | Status |
|---|------|----------|--------|-----------|------|--------|
| 002 | [Provider registry freshness guard](002-provider-registry-freshness-guard.md) | doctrine/DX | S | HIGH | maintenance | ✅ DONE (this PR) |
| 003 | [Catalog the verify_*.py scripts](003-verify-scripts-catalog.md) | docs/DX | S | HIGH | maintenance | ✅ DONE |
| 001 | [`__future__` annotations on governance rule mirrors](001-governance-rules-future-annotations.md) | tech-debt | S | MED | maintenance | ✅ DONE |
| 004 | [Refresh CLAUDE.md's stale launch status](004-refresh-claude-md-launch-status.md) | doctrine | S | HIGH | maintenance | 🆕 planned |
| 005 | [Reconcile contradictory offer-ladder pricing](005-reconcile-offer-ladder-pricing.md) | doctrine/commercial-os | S | HIGH | maintenance | 🆕 planned |
| 006 | [Remove guaranteed-outcome language](006-remove-guaranteed-outcome-language.md) | doctrine | S | HIGH | maintenance | 🆕 planned |
| 007 | [Fix kpi_dashboard.py mock-data mislabeling](007-fix-kpi-dashboard-mock-data-label.md) | correctness/doctrine | S | HIGH | maintenance | 🆕 planned |
| 008 | [Wire IP-allowlist + privileged-audit middleware](008-wire-enterprise-security-middleware.md) | security | S | HIGH | maintenance | 🆕 planned |
| 009 | [Sanitize exception detail leak in main.py](009-sanitize-exception-detail-leak.md) | security | S | MED | maintenance | 🆕 planned |
| 010 | [Strengthen the required CI test gate](010-strengthen-required-ci-test-gate.md) | tests | M | HIGH | maintenance | 🆕 planned |
| 011 | [Archive dead root-level wave-checkpoint scripts](011-archive-dead-root-scripts.md) | tech-debt | M | HIGH | maintenance | 🆕 planned |
| 012 | [Fix frontend silent error-swallowing (HR page)](012-fix-frontend-silent-error-swallowing.md) | correctness/tests | M | HIGH | maintenance | 🆕 planned |
| 013 | [auto_client_acquisition dead-module inventory + guard](013-dead-module-inventory-and-freshness-guard.md) | direction/tech-debt | M | HIGH | maintenance | 🆕 planned |
| 014 | [Refresh stale canonical docs](014-refresh-stale-canonical-docs.md) | docs | M | HIGH | maintenance | 🆕 planned |

## Dependency notes
- 005 and 014 both touch pricing/business-model docs — land 005 first
  (it names `CLAUDE.md` as the single source of truth), then 014 can point
  `docs/DEALIX_BUSINESS_MODEL.md` at the same canonical table without
  redoing the reconciliation.
- 004 and 014 use the same "staleness stamp" pattern — either order is fine,
  they touch disjoint files (`CLAUDE.md` vs `docs/`).
- 010 depends on nothing but should land after 006/007 conceptually (no
  file overlap, just thematically: tighten the trust signals before
  tightening the gate that vouches for them).
- 013 is intentionally scoped to inventory + a freshness guard, not
  module-by-module wiring/retiring decisions — those decisions are a
  separate, larger follow-up backlog once the founder reviews the catalog
  013 produces.
- 011 should land before or independently of 013 — they touch disjoint
  directories (repo root vs `auto_client_acquisition/`).
- All 004-014 are otherwise independent; each can be executed on its own
  branch/worktree per the skill's "one plan per branch" rule.
- All three original plans (001-003) are independent; each can be executed on its own branch.
- 002 landed directly in this PR (see `scripts/ops/check_provider_registry_freshness.py`
  + `tests/test_provider_registry_freshness.py`). Kept here as the canonical
  worked example of a closed audit→plan→execute→verify loop.
- 003 landed on `claude/dealix-continuation-checkpoint-nxtihl`: repo had drifted
  to 58 `verify_*.py` scripts (not 57 as originally audited) — the builder scans
  the glob dynamically so the drift didn't block execution, just updated the
  count. See `scripts/ops/build_verify_catalog.py` +
  `docs/ops/VERIFY_SCRIPTS_CATALOG.md` + `tests/test_verify_catalog.py`.
- 001 landed on `claude/dealix-continuation-checkpoint-nxtihl`: mechanical,
  no behavior change — the 4 doctrine guard tests it names
  (`test_no_cold_whatsapp.py`, `test_no_guaranteed_claims.py`,
  `test_no_linkedin_automation.py`, `test_no_scraping_engine.py`) still pass
  unchanged.

## Deferred findings — real, but too large for a single mechanical plan
Recorded here (not as plan files) so `/improve reconcile` doesn't re-discover
them from scratch; each needs a founder sequencing decision before it can be
broken into executable plans.
- **`docs/` structural sprawl** — 3,163 files, 93 numeric-prefixed top-level
  dirs with colliding numbers/concepts (`04_data_os` vs `06_data_os`,
  `06_llm_gateway` vs `09_llm_gateway`, `05_client_os` vs `11_client_os`,
  `10_agents` vs `16_agents`), 60+ version-suffixed docs (`V5_`–`V16_`), 20+
  `WAVE3_`–`WAVE17_` artifacts never archived/consolidated. Plan 014 fixes
  the two most-load-bearing stale docs only. A full `docs/` reorg needs the
  founder to decide a target taxonomy first — an executor guessing one
  would just create a different sprawl.
- **`apps/web` route/page sprawl** — ~130 routes with overlapping "control
  room" naming variants (`war-room`, `command-center`, `cmd-v2`, `dx3`,
  `iv4`, `x5`, `a14`, `s9`, `t10`, `z8`) and several pages
  (`trust-control`, `commercial-launch`, `service-catalog`,
  `client-delivery`) that render build-time-fixed snapshot objects
  (`lib/*-snapshot.ts`) styled as live dashboards. Needs a founder decision
  on which "control room" variant is canonical before any page can be
  safely retired — deleting the wrong one would remove a page someone
  actually uses.
- **`apps/web` has zero automated tests** — no Jest/Vitest/Playwright
  config exists at all. Plan 012 fixes one concrete bug this gap allowed
  through, but choosing and standing up a test framework for ~150
  components/pages is a tooling decision for the founder, not something to
  bootstrap as a side effect of one bug fix.
- **`tests/` full-suite promotion to required CI** — plan 010 promotes only
  the 8 doctrine guard tests. Promoting the remaining ~764 files needs a
  prior pass to find and fix (or explicitly skip) any currently-failing/
  flaky tests hidden behind the `optional` + `--maxfail=25` diagnostic step
  today — that audit is its own plan once 010 lands and the CI history is
  observed for a cycle.

## Rejected findings (recorded so they don't resurface)
- **[GI-01] `!scripts/lib/` / `!apps/web/lib/` gitignore negations** — looked like
  the same broken-parent bug as `.claude/`, but the parent dirs (`scripts/`,
  `apps/web/`) are **not** wholesale-ignored, so re-inclusion works
  (`git check-ignore scripts/lib/... ` → trackable). By-design. Not a finding.
- **[FUT-02] `from __future__ import annotations` missing repo-wide** — only
  flagged where it actually matters (see 001, scoped to the doctrine mirrors that
  are part of a guarded surface). Not raised as a blanket 1000-file sweep — that
  would be churn without evidence of harm.
