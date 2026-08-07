# 018 — Reconcile landing/ self-serve pages to the 2-offer registry

- **Finding:** `landing/pricing.html` presents **six self-serve checkout
  tiers** with live `/checkout.html?tier=...` links — "Executive Command
  Center" (`tier=partner`, `:90`), "Scale OS" (`tier=scale`, `:105`),
  "Growth OS / Growth Ops Monthly" (`tier=growth`, `:121`), "Revenue Proof
  Sprint" (`tier=sprint`, `:136`), "Data Pack" (`tier=data_pack`, `:154-155`),
  plus "Enterprise" (`:176`, mailto). Only "Mini Diagnostic" (`:161`) has
  no checkout link, matching the registry's free entry offer. Against
  `auto_client_acquisition/service_catalog/registry.py`'s
  `commercial_status` field, exactly two offerings are commercially live
  (`free_mini_diagnostic` = `free_entry`, `revenue_command_pilot_30d` =
  `quote_only` — no public fixed price, quote after discovery); the
  registry's own docstring (registry.py:12-15) states everything else
  "remains an internal experiment... until a separate approval changes
  `commercial_status`." A visitor can currently click "إكمال الاشتراك"
  (complete subscription) on five different tiers this backend doesn't
  treat as live commercial offers. Separately, `landing/systems-catalog.html`
  (1,252 lines, ~17 cards matching the registry's `count: 17`) presents
  all 17 catalogued offerings uniformly, without visually distinguishing
  the 2 live offers from the 15 `internal_experiment` ones.
  `landing/services.html`, by contrast, already reads as largely
  compliant — its own copy states "هذه خريطة عروض Pilot وليست قائمة أسعار
  أو عقد خدمة أو ضمان أداء" (`:81`, "this is a map of Pilot offers, not a
  price list, service contract, or performance guarantee") — verify it
  stays that way rather than assuming it needs the same rework as the
  other two files.
- **Category:** doctrine / commercial-os
- **Wave:** maintenance
- **Effort:** M   **Confidence:** HIGH
- **Written against commit:** aae97bcefcf73e74aef8c75ac593238dc1ed690e

## Drift check (run first)
```bash
git rev-parse HEAD   # if != aae97bcefcf73e74aef8c75ac593238dc1ed690e, re-read the files below before editing
```

## Context (inlined)
- Files in scope: `landing/pricing.html`, `landing/systems-catalog.html`.
  `landing/services.html` gets a verification pass only (step 3) — do not
  rewrite it unless that pass finds a real problem.
- **Land plan 015 first** — it already fixed `landing/pricing.html:260`'s
  WhatsApp claim; this plan reworks the same file's broader tier
  structure afterward. Re-read the file fresh before starting (015's edit
  will have shifted some content).
- Do not guess which `tier=` slug maps to which `registry.py` offering ID
  — step 1 below makes the executor build that mapping mechanically before
  touching any markup.
- Repo convention: `landing/assets/data/services-catalog.json` is the
  synced JSON export of `registry.py` (confirmed in sync as of
  2026-07-28) — use it as a quick lookup instead of re-parsing the Python
  file for every tier name, but treat `registry.py` as the ultimate source
  of truth if the two ever disagree.

## Steps
1. Build the tier→registry mapping. For each `tier=<slug>` found in
   `landing/pricing.html` (`grep -n 'tier=' landing/pricing.html`), find
   the closest matching offering in
   `landing/assets/data/services-catalog.json` (by name or id) and record
   its `commercial_status`. Produce a short table (in the PR description
   or a scratch note, not committed) of: tier slug → matched offering id →
   commercial_status. If a tier has no plausible match in the registry at
   all (i.e., it's not a catalogued offering under any name), treat it as
   `internal_experiment` for the purposes of step 2 — a self-serve tier
   with no backing registry entry is the worst case, not a pass.
   **Gate:** mapping table produced and reviewed before any markup edit.
2. For every tier whose mapped `commercial_status` is **not**
   `free_entry` or `quote_only`, remove the self-serve checkout
   affordance and replace it with roadmap/quote language, e.g. change:
    ```html
    <a class="cta" href="/checkout.html?tier=scale" data-analytics="cta_pricing_scale">إكمال الاشتراك</a>
    ```
   to:
    ```html
    <a class="cta" href="/diagnostic.html" data-analytics="cta_pricing_scale_waitlist">تواصل معنا — غير متاح للاشتراك الذاتي حالياً</a>
    ```
   (routes interested visitors to the free diagnostic / discovery path
   instead of a live checkout for an internal-experiment offering). Do
   this per-tier, one at a time, re-verifying each `tier=` slug's mapping
   from step 1 before changing it.
   **Gate:** after all edits, `grep -c "checkout.html?tier=" landing/pricing.html`
   equals the number of tiers whose mapped status is `free_entry` or
   `quote_only` (expected: 0 or 1 — the free diagnostic doesn't need
   checkout at all, and the pilot is quote-only so it also shouldn't link
   to a self-serve checkout; confirm this expectation against the actual
   mapping from step 1 rather than assuming).
3. Check `landing/services.html` for any self-serve checkout link or fixed
   price contradicting the registry (`grep -n "checkout.html\|SAR\|ريال"
   landing/services.html`). If none found beyond what's already
   compliant, leave the file untouched and note that in the PR
   description. If a real contradiction is found, fix it using the same
   pattern as step 2.
   **Gate:** command output reviewed; file either left untouched (with a
   note) or fixed with the same before/after pattern as step 2.
4. In `landing/systems-catalog.html`, for each of the ~17 cards, add a
   visible status indicator distinguishing the 2 live offers from the 15
   internal-experiment ones — e.g. a small badge reading "متاح الآن"
   (available now) on the 2 live cards and "قيد التطوير الداخلي — غير
   متاح للطلب" (internal development — not available to order) on the
   rest, sourced from the same tier→registry mapping built in step 1
   (reuse it; do not rebuild). Do not remove any of the 17 cards — this is
   a labeling fix, not a content deletion.
   **Gate:** `grep -c "قيد التطوير الداخلي" landing/systems-catalog.html`
   → 15 (or whatever count step 1's mapping determines is
   `internal_experiment` among the cards actually present on this page —
   re-verify the exact count against the mapping, don't assume 15 if the
   page doesn't 1:1 mirror all 17 registry entries).

## Done criteria (machine-checkable)
- [ ] `grep -n "checkout.html?tier=" landing/pricing.html` → only tiers
      confirmed `free_entry`/`quote_only` in step 1's mapping remain (if
      any — the free offer plausibly needs no checkout at all)
- [ ] `landing/systems-catalog.html` visibly distinguishes live vs
      internal-experiment cards per step 4's gate
- [ ] `make full-repo-test` → all required gates PASS

## Out of scope (do not touch)
- Do not touch `apps/web/` — separate frontend.
- Do not touch `landing/checkout.html` itself (the checkout page's
  internal logic) — this plan only changes which pages link to it and how.
- Do not remove the "Mini Diagnostic" or Enterprise-by-email cards — both
  are already compliant patterns (free entry, and quote-via-email
  respectively).
- Do not invent new pricing for any `internal_experiment` offering — the
  fix is removing the self-serve affordance / adding a status label, never
  publishing a new number.

## STOP conditions
- If step 1's mapping finds that a tier's registry entry has
  `commercial_status` values this plan didn't anticipate (something other
  than `free_entry` / `quote_only` / `internal_experiment`) → STOP, report
  the new status value rather than guessing how to treat it.
- `landing/checkout.html` was confirmed test-mode-only during this audit
  (`checkout.html:27`: "🧪 وضع TEST — NO_LIVE_CHARGE"; the form always
  submits `method: 'moyasar_test'`, `checkout.html:110`) — no real charge
  is currently possible through it, so this plan's fix is a labeling/UX
  correction, not a live-money emergency. If a future drift check finds
  `checkout.html` has since gained a live payment method, STOP and
  escalate as a P0 finding before touching anything else in this plan.
- If `landing/services.html`'s verification pass (step 3) finds it is
  NOT already compliant → STOP before rewriting it wholesale; report the
  specific contradiction found and fix only that, don't assume the whole
  file needs the same treatment as pricing.html.
