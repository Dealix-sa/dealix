# Dealix Company Service Ladder

> One offer per maturity stage. Each rung unlocks ONLY when the prior
> rung has shipped real evidence (per `docs/V12_1_TRIGGER_RULES.md`).

## The 6-rung ladder

| Rung | Offer | Price | Trigger to unlock NEXT rung |
|---|---|---|---|
| 0 | Mini Diagnostic | Free or token | 3 diagnostics delivered |
| 1 | 7-Day Growth Proof Sprint | **499 SAR** | 1 paid pilot fully delivered |
| 2 | 30-Day Operating Sprint | recommended_draft | 3 paid pilots in same sector |
| 3 | Monthly Operating Layer | recommended_draft | 3+ months of consecutive paid retainer |
| 4 | Partner / Agency Co-Branded | recommended_draft | 3 paid pilots delivered + signed permission to publish |
| 5 | Custom Systems / Custom AI | recommended_draft | (top rung) — bespoke internal system |

## Rung 0 — Mini Diagnostic (entry)

- **Promise:** 1-page bilingual diagnostic in 24-48 hours.
- **Inputs needed:** 6 questions (per `dealix_diagnostic.py`).
- **Output:** 3 opportunities + 1 message draft + 1 risk + service recommendation.
- **Hard rule:** NO Pilot offer until Diagnostic is in customer's hands.

## Rung 1 — 7-Day Growth Proof Sprint (first paid product)

- **Promise:** 10 opportunities + drafts + follow-up plan + Proof Pack draft.
- **Price:** 499 SAR (= 49,900 halalah). DO NOT change without ≥ 3 paid pilots.
- **Payment:** Moyasar **test mode** OR bank transfer. Live charge blocked.
- **Refund window:** 7 days from delivery.
- **Hard rule:** No `auto-send`, no guarantee, no fake metric in Proof Pack.

## Rung 2 — 30-Day Operating Sprint

- **Promise:** 4-week operating cadence: weekly Growth + Sales + Support + Delivery + Proof.
- **Price:** **recommended_draft** until 3 paid pilots inform a real number.
- **Hard rule:** Cannot upsell from 499 → 30-day without a customer-approved Proof Pack from rung 1.

## Rung 3 — Monthly Operating Layer

- **Promise:** Recurring monthly engagement; full V12 Daily Command Center as the customer's daily console.
- **Price:** recommended_draft.
- **Hard rule:** Cannot offer until ≥ 3 months of continuous delivery for an existing customer (i.e. retainer history exists in your private vault).

## Rung 4 — Partner / Agency Co-Branded

- **Promise:** Partner gets co-branded Mini Diagnostic for their clients; Dealix gets referral.
- **Price:** recommended_draft.
- **Hard rule:** NO white-label / NO revenue-share / NO exclusivity until ≥ 3 paid pilots delivered (per `partnership_os/partner_motion.py`).

## Rung 5 — Custom Systems / Custom AI

- **Promise:** A bespoke internal system — custom design profile + custom structure/architecture blueprint + a complete bilingual internal-system specification — built under full Dealix governance.
- **Price:** recommended_draft (custom scope; 50/50 payment terms).
- **Delivery mode:** Founder-assisted / semi-automated. Tooling: `auto_client_acquisition/custom_systems_os/` · API `POST /api/v1/custom-systems/run` · CLI `scripts/dealix_custom_system.py`.
- **Deliverables include:** ≥ 1 Capital Ledger asset, a 14-section Proof Pack, and the bilingual spec — never an external send.
- **Hard rule:** NO custom system build until ≥ 3 paid pilots delivered + a documented Proof Pack + a named workflow owner. **Enforced in code** (`custom_systems_os/entry_gate.py`); there is no manual override. No full white-label, no guarantees, no live send.

## Forbidden across all rungs

- ❌ Skipping rungs (e.g. Diagnostic → Monthly without Pilot)
- ❌ Adding a "Custom Enterprise" tier without ≥ 6 months retainer history
- ❌ Custom Systems build before ≥ 3 paid pilots (gate enforced in code)
- ❌ Full white-label of the custom system / guaranteed outcomes / live send
- ❌ Promising a tier with metrics the customer didn't supply
- ❌ Public mention of a customer name without signed permission
- ❌ Live charge / cold outreach / scraping at any rung

## Bilingual one-liner

**Arabic:** سُلَّم خدمات بسيط — كل درجة تفتح فقط بعد دليل حقيقي من الدرجة السابقة.
**English:** Simple service ladder — each rung unlocks ONLY after real evidence from the rung below.
