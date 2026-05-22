# `docs/strategy/` — Dealix Commercial Strategy (Source of Truth)

**As of 2026-05-22, this directory is the source of truth for Dealix commercial strategy.**

The founder's final strategic decision — **Build Dealix as a Full-Ops Revenue Machine** — supersedes prior strategy/positioning/pricing claims published elsewhere in this repo.

---

## Canonical strategy artifacts (read in this order)

1. **[`FULL_OPS_STRATEGY.md`](FULL_OPS_STRATEGY.md)** — Executive condensed strategy, bilingual (AR primary, EN mirror). The 3-page version. Start here.
2. **[`FULL_OPS_STRATEGY_APPENDIX.ar.md`](FULL_OPS_STRATEGY_APPENDIX.ar.md)** — Founder's full original text (17 sections, Arabic, verbatim). The authoritative appendix. Use when there is doubt about wording or intent.
3. **[`ROADMAP_30_60_90.md`](ROADMAP_30_60_90.md)** — 48-hour / 7-day / 30-day / 60-day / 90-day milestones with owners, success metrics, and approval gates.
4. **[`RECONCILIATION.md`](RECONCILIATION.md)** — Every prior strategy/positioning/pricing doc in the repo: what we did to it (banner / link / no-change) and why. Flags real conflicts that need founder decision.

---

## What this supersedes

The following prior docs make strategy/positioning/pricing claims that are now historical context. They each carry a banner pointing here:

- `docs/OFFER_LADDER_AND_PRICING.md` — prior 6-rung ladder (Free Diagnostic → 499 Sprint → 1,500 Pack → Managed Ops → Command Center → Partner OS).
- `docs/pricing.md` — legacy custom-engagement pricing (12K–40K setup + 3K–12K retainer).
- `docs/PRICING_AND_PACKAGING_V6.md` — V6 catalog (Growth Diagnostic / Starter 499 / Data-to-Revenue 1.5K-3K / Executive Growth OS 2,999/mo / Partnership Growth).
- `docs/PRICING_STRATEGY.md` — Founder Operator 299–999/mo + Growth OS tiers.
- `docs/PRICING_AND_PACKAGES_V6.md` (variants) and `docs/business/PRICING_AND_PACKAGES.md` — Pilot Lite/Standard/Pro at 499/999/1,500 SAR.
- `docs/POSITIONING_AND_ICP.md` — "AI Operations Radar" positioning.
- `docs/COMPETITIVE_POSITIONING.md` — prior competitive frame.
- `docs/PRODUCT_ROADMAP.md` — phase-based roadmap.
- `docs/strategy/90_DAY_PLAN.md` — earlier 90-day plan (now superseded by `ROADMAP_30_60_90.md`).
- `docs/strategy/12_MONTH_ROADMAP.md`, `docs/strategy/CEO_STRATEGY.md`, `docs/strategy/DEALIX_FULL_OPS_MASTER_PLAN_AR.md`, `docs/strategy/GO_TO_MARKET.md` — prior strategy framings.
- `docs/business/DEALIX_COMMERCIAL_STRATEGY_AR.md` — prior commercial center.
- `docs/00_foundation/DEALIX_POSITIONING.md` and other positioning fragments.
- `DEALIX_READINESS.md`, `DEALIX_COMPANY_OPERATIONAL_STATE.md` (carry "See also" link — operational, not superseded).

See **[`RECONCILIATION.md`](RECONCILIATION.md)** for the full table with banner status per file.

---

## What this does NOT change (yet)

- **Code modules** — `auto_client_acquisition/finance_os/pricing_catalog` and any other pricing-in-code remains untouched. Code-level pricing changes require founder approval and a separate PR.
- **Customer-facing landing pages** — `landing/pricing.html`, `landing/services.html`, and other landing artifacts publish the previous pricing ladder. Updating them requires founder approval; flagged in `RECONCILIATION.md`.
- **The 11 non-negotiables in `AGENTS.md`** — unchanged. The new strategy is consistent with them and explicitly reinforces approval-first, no-overclaim, and PDPL-aware language.

---

## How to use this directory

- **Reading order for a new collaborator:** `FULL_OPS_STRATEGY.md` → `ROADMAP_30_60_90.md` → relevant section of the appendix.
- **When prior docs disagree with this directory:** this directory wins. Add a banner to the prior doc and update `RECONCILIATION.md` if not already listed.
- **When founder voice / wording is unclear:** consult `FULL_OPS_STRATEGY_APPENDIX.ar.md` (verbatim) — never re-translate the appendix.
- **For execution sequencing:** use `ROADMAP_30_60_90.md` and the TodoWrite backlog seeded by the PR that introduced this directory.

---

## Maintenance rules

1. The appendix is **frozen** — do not edit `FULL_OPS_STRATEGY_APPENDIX.ar.md` unless the founder issues a new strategy decision.
2. The executive doc (`FULL_OPS_STRATEGY.md`) may be lightly clarified for typos/links but **its substance is also frozen** until the next founder decision.
3. The roadmap (`ROADMAP_30_60_90.md`) is a living document — update milestones as they complete or change.
4. The reconciliation log (`RECONCILIATION.md`) is **append-only history** — never remove rows, only add new ones when more prior docs are discovered or banners are added.
