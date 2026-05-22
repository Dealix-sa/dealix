# Strategy Reconciliation Log

**Date:** 2026-05-22
**Trigger:** Founder Full-Ops Strategy decision installed at [`FULL_OPS_STRATEGY.md`](FULL_OPS_STRATEGY.md).
**Scope:** Identify every prior strategy / positioning / pricing / roadmap doc in this repo, decide how to reconcile, record action taken.

**Action types:**
- **banner** — added a `> **STATUS (2026-05-22):** Superseded by ...` banner near the top. Content kept for historical context.
- **see-also** — added a `> **See also (strategy source of truth, 2026-05-22):** ...` link near the top. Doc remains operational/technical and is NOT superseded.
- **link-only** — README/index updated to point to new strategy folder; no banner on the doc itself.
- **no-change** — reviewed and not touched.
- **conflict-flagged** — material contradiction with new strategy; flagged here for founder decision before any further action.

---

## Files touched

### Banner added (superseded but retained)

| File | Why superseded |
|------|----------------|
| `docs/OFFER_LADDER_AND_PRICING.md` | Prior 6-rung ladder (Free Diagnostic → 499 Sprint → 1,500 Pack → Managed Ops → Command Center → Partner OS) is materially different from the new Signal Sample → Sprint Starter/Growth/Premium → Managed Pilot → Retainer → Dealix OS ladder. |
| `docs/pricing.md` | Legacy bespoke 12K–40K setup + 3K–12K retainer pricing predates both the prior ladder and the new strategy. |
| `docs/PRICING_AND_PACKAGING_V6.md` | V6 catalog (Diagnostic / 499 Starter / 1.5K–3K Data-to-Revenue / 2,999/mo Executive Growth OS / 3K–7.5K Partnership Growth). |
| `docs/PRICING_STRATEGY.md` | Founder Operator (299–999/mo) + Growth OS tiers — replaced by the new ladder. |
| `docs/business/PRICING_AND_PACKAGES.md` | Pilot Lite/Standard/Pro at 499/999/1,500 SAR — materially different price points from the new ladder. Also uses "PDPL compliance" language flagged by the no-overclaim register. |
| `docs/POSITIONING_AND_ICP.md` | "AI Operations Radar" positioning superseded by "Saudi revenue operations machine"; 3 ICP sectors now explicit. |
| `docs/COMPETITIVE_POSITIONING.md` | Earlier competitive frame; superseded narrative now in the new strategy. |
| `docs/PRODUCT_ROADMAP.md` | Phase-based roadmap superseded by horizon-based 48h / 7d / 30d / 60d / 90d roadmap. |
| `docs/business/DEALIX_COMMERCIAL_STRATEGY_AR.md` | Prior "10-layer / 7-offer" commercial framing replaced by 5 Engines + 10 Super Systems. |
| `docs/strategy/90_DAY_PLAN.md` | Superseded by `ROADMAP_30_60_90.md` in same folder. |
| `docs/strategy/12_MONTH_ROADMAP.md` | Year horizon will be revisited post-day-90; near-term horizon now lives in `ROADMAP_30_60_90.md`. |
| `docs/strategy/CEO_STRATEGY.md` | Earlier CEO thesis superseded by founder's full-ops strategy. |
| `docs/strategy/DEALIX_FULL_OPS_MASTER_PLAN_AR.md` | Prior "Revenue Expansion System / 12 machines" framing replaced by "5 Engines + 10 Super Systems". |
| `docs/strategy/GO_TO_MARKET.md` | GTM superseded by §GTM Strategy of the new doc (3 priority sectors: agencies / ERP-CRM-billing / contracting-B2B-services). |
| `docs/00_foundation/DEALIX_POSITIONING.md` | Positioning stub superseded by the new strategy's bilingual statement. |

### "See also" link added (operational, not superseded)

| File | Reason |
|------|--------|
| `AGENTS.md` | Operational agent contract. The 11 non-negotiables remain authoritative; new strategy is consistent with them. |
| `DEALIX_READINESS.md` | Readiness gates remain the operational quality bar. |
| `DEALIX_COMPANY_OPERATIONAL_STATE.md` | Live operational state report. |
| `DASHBOARD.md` | Operating dashboard skeleton; new strategy's Founder Command Center section maps to it. |
| `QUICK_START.md` | GitHub bootstrap quickstart — purely procedural. |

### Top-level README updates

| File | Action |
|------|--------|
| `README.md` | Added a "Strategy (source of truth)" section near the top with one-line summary + 3 links (strategy, roadmap, reconciliation). |
| `README.ar.md` | Mirror in Arabic above نظرة عامة. |

### Not touched (this round)

| File | Reason |
|------|--------|
| `DEPLOYMENT.md` | Purely operational deployment guide; no strategy claims. |
| All other `docs/**/*.md` not listed above | Either niche topical docs (security, SLO, on-call), code-adjacent design notes, or already historical. Sweep can continue in follow-up PRs if founder asks. |

---

## Conflicts flagged for founder decision

These are material contradictions that the banner alone does not resolve. **Each requires founder approval before action.**

### CONFLICT 1 — Pricing-in-code drift

- **Where:** `auto_client_acquisition/finance_os/pricing_catalog` (referenced by `docs/PRICING_AND_PACKAGING_V6.md`'s "hard rule") is reportedly the live source of truth for code-level pricing. It currently encodes the V6 catalog (Diagnostic 0 / Starter 499 / Data-to-Revenue 1.5K–3K / Executive Growth OS 2,999/mo / Partnership Growth).
- **New strategy says:** Signal Sample 0 or 199 → Sprint Starter 2,500 / Growth 4,500 / Premium 7,500 → Managed Pilot 9,500–25,000 (suggested 12,000) → Retainer 5,000–20,000/mo.
- **Action required:** Founder approval required before any code change. Per the prompt's guardrail and the non-negotiables, **this PR does NOT modify code**. A follow-up PR (engineering) is needed to update the pricing catalog after founder signs off on the migration plan.

### CONFLICT 2 — Customer-facing landing pages publish old pricing

- **Where:** `landing/pricing.html`, `landing/services.html`, `landing/annual-pricing.html`, and possibly more landing artifacts publish prior pricing tiers (multiple, including 499 SAR Sprint).
- **New strategy says:** the ladder above. Public price for Sprint Starter is now **2,500 SAR**, not 499.
- **Risk if silently changed:** customer trust + any in-flight checkouts at the 499 price point.
- **Action required:** Founder approves the landing migration plan (price change, communication to any existing pipeline, grandfathering policy). **This PR does NOT touch landing pages.**

### CONFLICT 3 — README badges / claims may overclaim

- **Where:** `README.md` (English) badges include `PDPL: native` and `ZATCA: Phase 2`. The Arabic appendix §4 of the new strategy explicitly says use **"PDPL-aware"** not "PDPL compliant" and do **not** claim ZATCA Phase 2 readiness without verified integration.
- **Action required:** Founder review — keep badges (if backed by verified integration evidence) or downgrade language. **This PR adds a Strategy section to README but does NOT change the badges.** A follow-up README pass should align badge language with the no-overclaim register.

### CONFLICT 4 — Many prior "strategy" docs in `docs/strategy/` and `docs/strategic/`

- **Where:** `docs/strategy/` has 22 files; `docs/strategic/` has ~17 more. The bannered ones above are the highest-signal; many smaller files (CEO_OPERATING_CADENCE_AR.md, CATEGORY_DESIGN.md, MARKET_MAP_SAUDI.md, etc.) reference frames superseded by the new strategy but were left untouched in this PR for scope reasons.
- **Action required:** Optional. Founder may request a follow-up sweep to banner the remaining ~30 secondary strategy docs. Not blocking.

### CONFLICT 5 — "Managed" vs "founder-assisted" language across the repo

- **Where:** Many places (landing copy, OFFER_LADDER, service catalogs) describe rungs 3+ as "Managed" services. The new strategy explicitly says anything not run manually 5× must be disclosed as **founder-assisted**, not managed.
- **Action required:** Founder approves a language-pass. Not done in this PR (would touch customer-facing material).

---

## How to extend this log

When a new prior doc is discovered or a new banner is added, append a row to the appropriate table above. **Do not remove rows** — this is an append-only history.
