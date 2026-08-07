# Improvement backlog — INDEX

Seeded by the first `improve` audit against commit `2ec6a6c`
(`.claude/skills/improve/`). Second pass (`/improve deep`, 2026-07-31,
commit `aae97bc`) audited the whole repo for sellability/trust/security/
tests/tech-debt/docs/direction across `api/`, `core/`, `db/`, `dealix/`,
`company/`, `auto_client_acquisition/`, `apps/web/`. Third pass
(2026-07-31, "Founder-360 reconciliation" — see section below) merged this
backlog with a parallel, independently-run audit thread (PRs #1005, #1009,
#1010, #1011; issue #938) into one phased sequence. Findings are vetted
(every `file:line` re-read before listing). This is a living backlog —
refresh with `/improve reconcile`.

## Priority order — by phase

**P0 — Trust, Safety, Production-Truth** (land before touching anything commercial)

| # | Plan | Category | Effort | Confidence | Wave | Status |
|---|------|----------|--------|-----------|------|--------|
| 019 | [Production-truth verifier (SHA/version/smoke)](019-production-truth-verifier.md) | doctrine/ops | M | HIGH | maintenance | 🆕 planned |
| 004 | [Refresh CLAUDE.md's stale launch status](004-refresh-claude-md-launch-status.md) | doctrine | S | HIGH | maintenance | 🆕 planned (revised — depends on 019) |
| 015 | [Remove live-WhatsApp-send claim from pricing.html](015-remove-live-whatsapp-claim-pricing-page.md) | doctrine/safety | S | HIGH | maintenance | 🆕 planned |
| 016 | [Remove personal Gmail from landing/index.html](016-remove-personal-gmail-landing-site.md) | doctrine/privacy | S | HIGH | maintenance | 🆕 planned |
| 006 | [Remove guaranteed-outcome language](006-remove-guaranteed-outcome-language.md) | doctrine | S | HIGH | maintenance | 🆕 planned |
| 007 | [Fix kpi_dashboard.py mock-data mislabeling](007-fix-kpi-dashboard-mock-data-label.md) | correctness/doctrine | S | HIGH | maintenance | 🆕 planned |
| 008 | [Wire IP-allowlist + privileged-audit middleware](008-wire-enterprise-security-middleware.md) | security | S | HIGH | maintenance | 🆕 planned |
| 009 | [Sanitize exception detail leak in main.py](009-sanitize-exception-detail-leak.md) | security | S | MED | maintenance | 🆕 planned |
| 012 | [Fix frontend silent error-swallowing (HR page)](012-fix-frontend-silent-error-swallowing.md) | correctness/tests | M | HIGH | maintenance | 🆕 planned |
| 010 | [Strengthen the required CI test gate](010-strengthen-required-ci-test-gate.md) | tests | M | HIGH | maintenance | 🆕 planned (land last in P0) |

**P1 — Commercial-Truth + Portfolio Hygiene**

| # | Plan | Category | Effort | Confidence | Wave | Status |
|---|------|----------|--------|-----------|------|--------|
| 017 | [Reconcile pricing docs to the registry model](017-reconcile-pricing-docs-to-registry.md) | doctrine/commercial-os | S | HIGH | maintenance | 🆕 planned (retires 005) |
| 018 | [Reconcile landing/ site to the 2-offer registry](018-reconcile-landing-site-to-registry.md) | doctrine/commercial-os | M | HIGH | maintenance | 🆕 planned |
| 013 | [auto_client_acquisition dead-module inventory + guard](013-dead-module-inventory-and-freshness-guard.md) | direction/tech-debt | M | HIGH | maintenance | 🆕 planned |
| 020 | [PR/branch portfolio triage tool (issue #938)](020-pr-branch-portfolio-triage-tool.md) | tech-debt/ops | M | HIGH | maintenance | 🆕 planned |

**P2 — First-Paid-Pilot Readiness + Proof**

| # | Plan | Category | Effort | Confidence | Wave | Status |
|---|------|----------|--------|-----------|------|--------|
| 021 | [Legal/compliance template pack (draft only)](021-legal-compliance-template-pack.md) | docs/legal | M | HIGH | maintenance | 🆕 planned |
| 022 | [ICP + 30-day discovery funnel operating doc](022-icp-discovery-funnel-doc.md) | docs/sales | S | HIGH | maintenance | 🆕 planned |
| 014 | [Refresh stale canonical docs](014-refresh-stale-canonical-docs.md) | docs | M | HIGH | maintenance | 🆕 planned (revised — BUSINESS_MODEL.md step dropped) |

**P3 — Repeatability / Housekeeping** (zero-urgency, sequence opportunistically)

| # | Plan | Category | Effort | Confidence | Wave | Status |
|---|------|----------|--------|-----------|------|--------|
| 011 | [Archive dead root-level wave-checkpoint scripts](011-archive-dead-root-scripts.md) | tech-debt | M | HIGH | maintenance | 🆕 planned |

**Done (earlier passes)**

| # | Plan | Category | Effort | Confidence | Wave | Status |
|---|------|----------|--------|-----------|------|--------|
| 002 | [Provider registry freshness guard](002-provider-registry-freshness-guard.md) | doctrine/DX | S | HIGH | maintenance | ✅ DONE (this PR) |
| 003 | [Catalog the verify_*.py scripts](003-verify-scripts-catalog.md) | docs/DX | S | HIGH | maintenance | ✅ DONE |
| 001 | [`__future__` annotations on governance rule mirrors](001-governance-rules-future-annotations.md) | tech-debt | S | MED | maintenance | ✅ DONE |

**Retired**

| # | Plan | Category | Status |
|---|------|----------|--------|
| 005 | [Reconcile contradictory offer-ladder pricing](005-reconcile-offer-ladder-pricing.md) | doctrine/commercial-os | 🗄️ RETIRED → see 017 |

## Founder-360 reconciliation (2026-07-31)

A second, independently-run audit thread (different branches, same repo)
converged on the same root diagnosis as this backlog by a different path.
Verified via GitHub API and direct repo reads before anything below was
planned — none of this is taken on the other thread's word alone:

- **PR #1005** (open): rewrites `CLAUDE.md`'s Business Model Summary and
  `.claude/rules/dealix-commercial-os.md`'s offer ladder from the old
  6-rung fixed-price table to the 2-offer registry-based model already
  live in code (`auto_client_acquisition/service_catalog/registry.py`:
  `free_mini_diagnostic` = `free_entry`, `revenue_command_pilot_30d` =
  `quote_only`, 15 others = `internal_experiment`). **This obsoleted
  plan 005**, which was written against the still-current stale table in
  `main`'s `CLAUDE.md` (main hasn't merged #1005 yet). 005 is retired in
  favor of 017, which fixes the *other* docs still quoting the old prices
  (`COMMERCIAL_IDENTITY.md`, `README_FOUNDER_EXECUTION.md`) without
  touching `CLAUDE.md` itself — that file belongs to #1005's branch.
- **PR #1009** (open, correctly Draft): `db/tenant_session.py` +
  `tests/test_tenant_session_binding.py` — 23 passed, 3 skipped
  (`@requires_postgres`). `db/rls_policies.py` confirms `apply_rls()` is
  never called anywhere in `api/` (AST-scan test in the same PR). Well-
  scoped and correctly gated; nothing added to this backlog for it beyond
  this cross-reference — do not activate RLS until those 3 tests are green
  on a real Postgres instance.
- **PR #1010** (open, draft): pure test extraction, CI green, no risk.
- **PR #1011** (open, draft, branch `ops/founder-360-market-truth-20260731`):
  adds the Founder-360 executive report + `action_queue`/`approval_queue`/
  `proof_log` CSVs under `docs/ops/founder-360/2026-07-31/`, and fully
  rewrites `docs/DEALIX_BUSINESS_MODEL.md` into a "Market Validation
  Edition v2.0-draft". **This obsoleted the `DEALIX_BUSINESS_MODEL.md`
  step of plan 014** — dropped from 014, kept the rest.
- **Issue #938** "Portfolio Stabilization Control Tower" (open): tracks a
  100+-open-PR backlog (confirmed via API, up from ~45 nine days earlier)
  with an explicit "no merges without founder approval" safety contract.
  Plan 020 gives it a repeatable triage tool instead of another one-off
  manual audit.
- **Two net-new findings** this backlog's earlier pass missed, now planned:
  `landing/pricing.html:260` publicly claims Starter+ includes live
  WhatsApp sending via "an approved provider" — a public promise of
  exactly the capability `WHATSAPP_ALLOW_LIVE_SEND=false` forbids by
  default (plan 015, highest severity of this reconciliation pass); and
  `landing/index.html` publishes the founder's personal Gmail in both
  schema.org structured data and the footer (plan 016).
- **Not actionable by any plan**: the Founder-360 report states a private
  scan of historical offline ZIP delivery packages (not in this git repo)
  found potential credential material, no value printed or committed.
  `security_smoke_ci.py` is clean against the tracked repo. This stays a
  standing founder-only investigation/rotation flag — no plan here
  attempts to verify or act on it.

Phase ordering rationale: P0 closes everything a founder or outside
auditor can check mechanically (including the two net-new doctrine
violations) before P1 touches anything commercial; P1 makes every public/
internal price and offer claim match the registry and gives the PR/branch
sprawl a repeatable tool; P2 builds the operational/legal scaffolding to
actually run a paid pilot; P3 is cosmetic and can land whenever convenient.

## Dependency notes
- 019 should land before 004 executes — 004's revised step reads 019's
  verifier output instead of a hand-written prose staleness stamp.
- 015 and 018 both touch `landing/pricing.html` — serialize, don't
  parallelize; 015 is a 1-line isolated doctrine fix, 018 is the broader
  page-to-registry rework.
- 017's inlined pricing table must be re-verified against
  `auto_client_acquisition/service_catalog/registry.py` at execution time
  (the source of truth), not against PR #1005's branch, since #1005 may or
  may not have merged by then.
- 022 cross-references `docs/DEALIX_BUSINESS_MODEL.md` (rewritten by
  PR #1011); if #1011 hasn't merged by execution time, inline the needed
  facts per the plan template's drift-check convention rather than a
  dangling reference.
- 013 is intentionally scoped to inventory + a freshness guard, not
  module-by-module wiring/retiring decisions — those decisions are a
  separate, larger follow-up backlog once the founder reviews the catalog
  013 produces.
- 011 should land before or independently of 013 — they touch disjoint
  directories (repo root vs `auto_client_acquisition/`).
- All 004, 006-022 are otherwise independent; each can be executed on its
  own branch/worktree per the skill's "one plan per branch" rule.
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
- **Doc-duplication is a repo-wide pattern, not isolated incidents** —
  writing plans 021 and 022 surfaced the same "N near-identical documents,
  none reconciled" shape already seen in the `docs/` structural sprawl
  item above: **5 separate DPA templates**, **4 SLA docs + 4 SLA code
  modules**, **10 incident-response hits** (4 separate `incident_response.py`
  modules alone), and **5 separate ICP documents** (one of which,
  `docs/commercial/ICP_MATRIX_AR.md`, explicitly expands to 10 broad B2B
  segments — the opposite of the narrow first-ICP discipline PR #1011
  argues for). Plans 021 and 022 each handle their own category
  (inventory + pointer-file consolidation, never a rewrite-from-scratch);
  neither attempts the others'. A founder-level decision on a repo-wide
  "one canonical doc per topic, everything else is a dated pointer"
  policy would prevent this from recurring with the next wave of work —
  that policy decision itself is out of scope for any plan here.

## Rejected findings (recorded so they don't resurface)
- **[GI-01] `!scripts/lib/` / `!apps/web/lib/` gitignore negations** — looked like
  the same broken-parent bug as `.claude/`, but the parent dirs (`scripts/`,
  `apps/web/`) are **not** wholesale-ignored, so re-inclusion works
  (`git check-ignore scripts/lib/... ` → trackable). By-design. Not a finding.
- **[FUT-02] `from __future__ import annotations` missing repo-wide** — only
  flagged where it actually matters (see 001, scoped to the doctrine mirrors that
  are part of a guarded surface). Not raised as a blanket 1000-file sweep — that
  would be churn without evidence of harm.
