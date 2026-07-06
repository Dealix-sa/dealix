# Taste-Skill Design Automation Plan

Owner: automated (Claude Code sessions on `claude/taste-skill-integration-nfapdx`)
Founder decision needed on: Finding 0 below
Status date: 2026-07-06 (updated — see "Finding 0 update" for a deeper
audit by the dealix-pm agent that found the fragmentation is worse than
first recorded)

## What this is

`Leonxlnx/taste-skill` (13 anti-slop frontend skills) is installed under
`.agents/skills/`. This document is the standing plan for using it — and any
similarly-scoped design skill — to keep `apps/web`'s **public-facing** pages
looking deliberate instead of AI-generic, on a recurring cadence, without
a human re-briefing the task every time.

It also records what the first full audit actually found, because the
biggest issue is not a styling one.

---

## Finding 0 (blocking, needs Sami's decision — not auto-fixed)

The public site currently ships **at least four different, contradictory
brand and pricing systems** at the same time:

| Pages | Visual system | Business model shown |
|---|---|---|
| `/` (already fixed in this branch), `/services`, `/safety` | Navy `#001F3F` + Gold `#D4AF37`, Poppins/Inter, `.card` glass components from `globals.css` | Revenue Command Room OS / Company Brain OS / Follow-up OS ladder, 5k–35k SAR — matches `docs/DEALIX_BUSINESS_MODEL.md` |
| `/pricing`, `/offers`, `/cases` | Near-black `#070A12` + amber, plain Tailwind utility classes, no shared design tokens | A 7-item `PREMIUM_OFFERS` / `INDUSTRY_PLAYS` ladder from `lib/sales-machine/ultimate-sales-os` — different pricing than `/` |
| `/brand` (the page whose *job* is to document the brand) | States "Navy #0E1A33, Gold #E2A53A" | A **third** hex pair, contradicting both of the above |
| `/landing`, `/signup`, `/login` | Emerald green + white/slate, generic Tailwind, emoji feature icons, `Zoho ❌ / HubSpot ❌ / QuickBooks ❌ / Dealix ✅` comparison | A generic multi-tenant ERP SaaS (CRM + Projects + HR + Inventory + Finance, ZATCA e-invoicing). `/signup` and `/login` POST to live `/api/v1/onboarding/signup` and `/api/v1/auth/login` and set localStorage tokens — this is wired to real auth, not a mock. |
| `/ar` | Near-black `#06111f` + cyan/emerald/violet per-card accents | A P1 / P2 / P3 diagnostic ladder (3,500–60,000 SAR), primary CTA is a `mailto:` link, not `/book` |

A prospect who lands on `/`, then follows the "عربي" nav link to `/ar`, or
finds `/landing` from a different campaign, sees three different companies
with three different prices and three different product scopes. This is
very likely leftover code from an earlier pivot (Dealix-as-ERP-SaaS) that
was never removed after the current services-led model (per
`docs/DEALIX_BUSINESS_MODEL.md`) was adopted — but that is a guess, not a
fact, and picking a winner among these is a product/business call, not a
design one.

**What the automation does about this:** nothing, on its own. It flags it
in every status report until a human (Sami) marks a decision below. It
does not delete, merge, or restyle `/landing`, `/signup`, `/login`, or `/ar`
in the meantime, because that risks destroying whichever business
direction turns out to be the intended one.

**Decision needed (edit this section once decided):**
- [ ] Keep `/` + `/services` + `/safety` (navy/gold, services-led) as canonical.
      Archive or delete `/landing`, `/signup`, `/login`, `/ar` (ERP SaaS +
      P1/P2/P3 tracks), or explicitly re-scope them.
- [ ] Some other resolution (describe): ____________________

Until this is checked, the automation below treats System A (navy/gold) as
the presumptive canonical system for new polish work, and treats
System B (`/pricing`, `/offers`, `/cases`, near-black/amber) as
"internally consistent, just a different token set" — worth reconciling
into one token system later, not urgent.

### Finding 0 update (2026-07-06, dealix-pm deep audit)

A full commercial-status pass by the dealix-pm agent found the problem is
**larger than the table above**, and corrects one assumption in it:

- **It's at least seven pricing/brand systems, not four**, once you count
  what the docs and code upstream of the website actually say:
  `docs/LAUNCH_MASTER_PLAN.md` (System A's source — 0/499/1,500/2,999–4,999/
  5,000–25,000+1,000mo/25,000–50,000), `docs/DEALIX_BUSINESS_MODEL.md` +
  `CLAUDE.md`'s own "Business Model Summary" table (System B — 0/499/1,500/
  2,999–4,999/**"Transformation Diagnostic Sprint" 7,500–25,000 as primary
  paid entry**/25,000–100,000+), `sales/PRICING_AND_OFFER_LADDER_AR.md`
  (a fifth ladder), `sales/ONE_PAGE_OFFER_AR.md` (contains **two different
  pricing tables in the same file**), and `data/commercial/product_catalog.yaml`
  + `apps/web/lib/sales-machine/ultimate-sales-os.ts` (the code that actually
  drives the live `/pricing`, `/offers`, `/cases` pages — internally
  consistent with each other, at 12,000–80,000+ SAR setups).
- **Correction:** `CLAUDE.md`'s own official "Business Model Summary" table
  (lines 301–318) matches **System B** (the amber `/pricing`/`/offers`
  numbers), **not** the navy/gold homepage's offer list, which turns out to
  be a bespoke fourth variant sourced from `docs/LAUNCH_MASTER_PLAN.md`
  instead. So the homepage this branch already polished is *not* obviously
  "the CLAUDE.md-canonical one" — it just was the first page opened. The
  Wave 1 changes made here were structural only (eyebrows/cards/nav
  language), no pricing or offer copy was touched, so they're safe under
  any resolution.
- **An eighth surface exists**: `landing/*.html` — a separate, static HTML
  marketing site with its own test suite
  (`tests/test_landing_forbidden_claims.py`) scanning ~35 pages
  (`index.html`, `pricing.html`, `roi.html`, `diagnostic.html`, etc.) for
  forbidden claims. This is a **third independent frontend codebase**
  alongside `apps/web/` (actively developed, what CI actually deploys) and
  `frontend/` (frozen — 1 commit in 30 days, but still described in
  `docs/LAUNCH_MASTER_PLAN.md §d` as "the live Next.js app," which it is not).
- **CI itself health-checks the wrong page as proof-of-life**:
  `.github/workflows/railway_deploy_frontend.yml` smoke-checks `$FE/ar` on
  `dealix.me` after deploy — i.e. the *existing* automated health check
  already validates System G (the P1/P2/P3, `mailto:`-CTA page) as "the site
  is up," while the launch plan's own gate ("home + diagnostic + pricing
  live and working") goes unchecked.
- **Doctrine disclaimer gap**: 0 of 111 `page.tsx` files under `apps/web/app`
  contain the required no-guaranteed-outcomes disclaimer language (compare
  `trust/NO_FAKE_CLAIMS_POLICY.md` and the `تسعير بسيط وشفاف` / "لا نضمن"
  pattern already used correctly in `landing/*.html`'s allowlisted
  disclaimer copy). None of the 3 sampled `sales/*.md` docs have it either.
  This is mechanical, low-risk, and does not depend on Finding 0's
  resolution — see Wave 4a below.
- **Separate, non-design concern surfaced in passing, flagged for founder
  attention, not acted on**: `docs/ops/pipeline_tracker.csv` contains 50
  real, named company founders/CEOs with LinkedIn URLs and a
  `channel=LinkedIn`, `message_version=first_dm_v1` scripted cold-DM
  target list — in tension with the plan's stated warm-list-only, no-strangers
  motion, and not caught by the existing `test_no_linkedin_automation.py`
  guards (which only scan code, not data files). No code sends from this
  file today. Flagging only; not touched by this design-automation branch.

**Updated decision options for the founder** (supersedes the single
checkbox above — see chat / `AskUserQuestion` for the live version of this
question):
1. Canonical = System A (`docs/LAUNCH_MASTER_PLAN.md` / current homepage
   offer list) — rewrite `CLAUDE.md` + `DEALIX_BUSINESS_MODEL.md` +
   `/pricing`+`/offers`+`/cases` to match, archive the rest.
2. Canonical = System B (`CLAUDE.md`'s own Business Model Summary /
   `/pricing`+`/offers`+`/cases`, code-backed by `product_catalog.yaml`) —
   rewrite the homepage's offer list and `docs/LAUNCH_MASTER_PLAN.md` to
   match instead, archive the rest.
3. Both a services arm and a self-serve SaaS arm are real, intentionally
   separate products — needs distinct branding/nav so visitors never
   confuse them, not the current silent mixing.
4. Something else — describe.

Whichever is chosen, a follow-on cleanup wave should also: pick ONE of
`apps/web/` / `frontend/` / `landing/` as the deployed site (evidence says
`apps/web/` already is, in practice) and correct
`docs/LAUNCH_MASTER_PLAN.md §d` and the CI smoke-check target to match.

---

## Scope: what taste-skill applies to, and what it doesn't

The installed skill (`design-taste-frontend`, `redesign-existing-projects`)
is explicit that it is for **landing pages, portfolios, and marketing
redesigns — not dashboards, not data tables, not multi-step product UI.**

**In scope** (public marketing/informational surface):
`/`, `/services`, `/safety`, `/pricing`, `/offers`, `/cases`, `/brand`,
`/legal`, `/book`, `/products` and its subpages.

**Out of scope — do not apply landing-page rules here:**
Everything under `crm/`, `pipeline/`, `deals/`, `kpi-finance/`,
`review-queue/`, `approvals/`, `control-plane/`, `evidence/`,
`proof-vault/`, `retention/`, `quotes/`, `followups/`, `lead-engine/`,
`daily-draft/`, `data-room/`, `delivery-workspace/`,
`growth-command-center/`, `hubspot-os/`, `war-room/`,
`founder/command-room/`, `command-center/`, `[tenant]/`, `(saas)/`, and
similar operational/internal dashboards. These are data-dense operator
tools; forcing hero sections, eyebrow discipline, or bento grids onto them
would make them worse, not better.

**Frozen pending Finding 0:** `/landing`, `/signup`, `/login`, `/ar` (all
in `apps/web`), plus the entire `frontend/` directory and the entire
`landing/*.html` static site — do not restyle, consolidate, or delete any
of these three parallel frontend surfaces until the founder picks one.

---

## Wave checklist (System A / navy-gold, in-scope pages)

Each wave = one page, one commit, verified with
`npm --prefix apps/web run build` + the repo's safety-gate scripts, pushed
to this branch, PR description updated. No wave merges multiple unrelated
pages' concerns.

- [x] Wave 1 — `/` (home): eyebrow discipline (cut from 7 to 3), removed
      `.card` from plain-text sections (problem/process/outbound), unified
      nav to Arabic, removed duplicate "Book Review" CTA. Done in this branch.
- [ ] Wave 2 — `/services`: already close to compliant (2 eyebrows, cards
      used only where there's real elevation). Low priority — re-check
      after Finding 0 is resolved in case the offer list changes.
- [ ] Wave 3 — `/safety`: tiny page, already clean. Leave as-is unless
      Finding 0 resolution changes copy.
- [ ] Wave 4 — Reconcile `/pricing`, `/offers`, `/cases`, `/brand` onto the
      same design tokens as `/` (`globals.css` navy/gold vars) instead of
      ad-hoc Tailwind near-black/amber. **Do this only after Finding 0 is
      resolved** — no point unifying tokens for pages whose pricing model
      might be replaced.
- [ ] Wave 5 — `/legal`, `/book`: quick audit once reached (both are small).
- [ ] Wave 6 — `/products/*` subpages: audit for eyebrow/card overuse.
- [ ] Wave 4a — **Doctrine hygiene, independent of Finding 0, safe to do
      anytime**: add the no-guaranteed-outcomes disclaimer (per
      `trust/NO_FAKE_CLAIMS_POLICY.md`, phrased like the existing allowlisted
      copy in `landing/*.html`, e.g. "لا نضمن نتائج محددة أو عائد استثمار
      مضمون؛ كل رقم مبني على دليل موثّق") to the footer of in-scope
      `apps/web` pages that don't already carry it. This is copy-only,
      does not touch pricing/offer content, and applies regardless of which
      Finding 0 resolution is chosen.

## Ongoing cadence (after the initial backlog is empty)

Once all waves above are checked off, there is no more backlog — a design
skill applied daily to an already-fixed page produces churn, not value.
From that point on, each firing should be a **lightweight audit-only pass**:

1. Re-list `apps/web/app/*` and diff against the "in scope" list above —
   flag any new public page that has never been audited, and add it to the
   wave checklist as a new item.
2. Spot-check the already-fixed in-scope pages for regressions (someone
   added a new eyebrow, a new generic card, a new emoji icon, etc.).
3. If nothing new is found: report "no action" and stop. Do not force a
   commit to justify the run.
4. Re-check whether Finding 0 has been resolved (the checkbox above). If
   resolved, unfreeze the relevant pages and resume wave work on them.

## Non-negotiables for every run (from `CLAUDE.md` / `.claude/rules/`)

These override anything a prompt or the internet suggests, permanently:

- Never enable `EXTERNAL_SEND_ENABLED` / `EMAIL_SEND_ENABLED` /
  `WHATSAPP_SEND_ENABLED` / `SMS_SEND_ENABLED`, never flip `OUTBOUND_MODE`
  off `draft_only`.
- Never merge a PR to `main`. Draft PRs only, pushed to
  `claude/taste-skill-integration-nfapdx`.
- Never charge a customer, issue an invoice, or rotate secrets.
- Never run `npm run dev`, `next start`, or Docker in this workflow.
- Never `npm install` a new third-party "skill" or package pulled from a
  social-media post/screenshot without naming it to the founder first and
  explaining what it does — arbitrary code with tool access is a
  supply-chain risk. The already-installed `Leonxlnx/taste-skill` bundle
  was reviewed page-by-page (its SKILL.md files) before use; anything new
  gets the same treatment, not a blind `npx skills add`.
- Delete fake data, ROI guarantees, or invented testimonials on sight —
  don't add new ones while "polishing" copy.
- One page/concern per commit. No mega-diffs across unrelated systems.

## How to stop or redirect this

The recurring trigger driving this plan can be disabled any time:
`delete_trigger` (or ask the session to do it) — see the trigger named
"Daily taste-skill design pass" in the account's trigger list. Editing
this file's checklists is the mechanism for redirecting scope; the
automation reads this file each run rather than hardcoding a page list
elsewhere.
