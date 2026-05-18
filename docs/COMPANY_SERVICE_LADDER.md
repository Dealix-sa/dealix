# Dealix Company Service Ladder

> One offer per maturity stage. Each rung unlocks ONLY when the prior
> rung has shipped real evidence (per `docs/V12_1_TRIGGER_RULES.md`).

## The ladder

> Catalog-of-record is the 7-offer registry in `COMMERCIAL_WIRING_MAP.md` §1
> (`auto_client_acquisition/service_catalog/registry.py`). This table is the
> maturity narrative on top of it — registry prices are authoritative.

| Rung | Offer | `service_id` | Price (SAR) | Trigger to unlock NEXT rung |
|---|---|---|---|---|
| 0 | Free Mini Diagnostic | `free_mini_diagnostic` | 0 (free) | 3 diagnostics delivered |
| 1 | 7-Day Revenue Proof Sprint | `revenue_proof_sprint_499` | **499** | 1 paid pilot fully delivered + customer-confirmed Proof Pack |
| 2 | Data-to-Revenue Pack | `data_to_revenue_pack_1500` | 1,500 | 3 paid pilots in same sector |
| 3 | Growth Ops Monthly | `growth_ops_monthly_2999` | 2,999 /mo | 3+ months of consecutive paid retainer |
| — | Support OS Add-on | `support_os_addon_1500` | 1,500 /mo | add-on; attaches to rung 3+ |
| 4 | Executive Command Center | `executive_command_center_7500` | 7,500 /mo | proven retainer + executive-confirmed value reports |
| 5 | Agency Partner / Custom AI Build | `agency_partner_os` | custom (governed estimate) | 3 paid pilots delivered + signed permission to publish |

## Rung 0 — Free Mini Diagnostic (entry)

- **Promise:** 1-page bilingual diagnostic in 24-48 hours.
- **Inputs needed:** 6 questions (per `dealix_diagnostic.py`).
- **Output:** 3 opportunities + 1 message draft + 1 risk + service recommendation.
- **Hard rule:** NO Pilot offer until Diagnostic is in customer's hands.

## Rung 1 — 7-Day Revenue Proof Sprint (first paid product)

- **Promise:** 10 opportunities + drafts + follow-up plan + Proof Pack draft.
- **Price:** 499 SAR (= 49,900 halalah). DO NOT change without ≥ 3 paid pilots.
- **Payment:** Moyasar **test mode** OR bank transfer. Live charge blocked.
- **Refund window:** 7 days from delivery.
- **Hard rule:** No `auto-send`, no guarantee, no fake metric in Proof Pack.

## Rung 2 — Data-to-Revenue Pack

- **Promise:** Cleaned data + scored opportunities + drafts turned into a repeatable revenue workflow.
- **Price:** 1,500 SAR (registry-of-record).
- **Hard rule:** Cannot upsell from 499 → Data Pack without a customer-approved Proof Pack from rung 1.

## Support OS Add-on (attaches to rung 3+)

- **Promise:** Governed operations support layer on top of an active monthly engagement.
- **Price:** 1,500 SAR / month. Not a standalone rung — an add-on only.
- **Hard rule:** Cannot sell without an active rung 3+ retainer.

## Rung 3 — Growth Ops Monthly

- **Promise:** Recurring monthly engagement; full Daily Command Center as the customer's daily console.
- **Price:** 2,999 SAR / month (registry-of-record).
- **Hard rule:** Cannot offer until ≥ 3 months of continuous delivery for an existing customer (i.e. retainer history exists in your private vault).

## Rung 4 — Executive Command Center

- **Promise:** Executive-tier monthly operating layer with executive-confirmed value reports.
- **Price:** 7,500 SAR / month (registry-of-record).
- **Hard rule:** Cannot offer without a proven monthly retainer and executive-confirmed value reports.

## Rung 5 — Agency Partner / Custom AI Build

- **Promise:** Co-branded Mini Diagnostic for the partner's clients, or a custom AI build scoped per engagement.
- **Price:** custom — governed estimate range per engagement; never a fixed published number.
- **Hard rule:** NO white-label / NO revenue-share / NO exclusivity until ≥ 3 paid pilots delivered (per `partnership_os/partner_motion.py`).

## Forbidden across all rungs

- ❌ Skipping rungs (e.g. Diagnostic → Monthly without Pilot)
- ❌ Adding a "Custom Enterprise" tier without ≥ 6 months retainer history
- ❌ Promising a tier with metrics the customer didn't supply
- ❌ Public mention of a customer name without signed permission
- ❌ Live charge / cold outreach / scraping at any rung

## Bilingual one-liner

**Arabic:** سُلَّم خدمات بسيط — كل درجة تفتح فقط بعد دليل حقيقي من الدرجة السابقة.
**English:** Simple service ladder — each rung unlocks ONLY after real evidence from the rung below.
