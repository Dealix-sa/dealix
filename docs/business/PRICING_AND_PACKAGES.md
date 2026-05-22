# Dealix — Pricing & Packages (Saudi B2B)

> **STATUS (2026-05-22):** Superseded by [docs/strategy/FULL_OPS_STRATEGY.md](../strategy/FULL_OPS_STRATEGY.md). The Pilot Lite/Standard/Pro (499/999/1,500 SAR) tiers below differ materially from the new canonical ladder (Signal Sample 199 SAR → Sprint Starter 2,500 / Growth 4,500 / Premium 7,500 → Managed Pilot 9,500–25,000 → Retainer 5,000–20,000/mo). Retained for historical context. Live code/landing pricing is not changed by this banner; see [docs/strategy/RECONCILIATION.md](../strategy/RECONCILIATION.md). Also: the phrase "PDPL compliance" in the line below should now read "PDPL-aware" per the no-overclaim register in the new strategy.

Pricing in SAR. All packages assume PDPL compliance + opt-out + human approval for first 30 days.

## Tier 1: Managed Pilot (cash-positive in 7 days)

**Sami runs Dealix manually for 7 days; customer pays a small entry fee, then upgrades.**

| | Pilot Lite | Pilot Standard | Pilot Pro |
|---|---|---|---|
| **Price** | 499 SAR | 999 SAR | 1,500 SAR |
| **Duration** | 7 days | 7 days | 7 days |
| **Leads handled** | up to 10 | up to 25 | up to 50 |
| **Channels** | website form + WhatsApp inbound | + email | + phone call routing |
| **Daily report** | end-of-day | morning + evening | live dashboard |
| **Refund window** | 3 days | 5 days | 7 days |

**Why it works:** customer risks the price of a coffee dinner, sees real Arabic responses inside 24h. Conversion to paid Starter: target 50%+.

## Tier 2: Setup Fee (one-time integration)

| | Lite | Standard | Advanced |
|---|---|---|---|
| **Price** | 1,000 SAR | 3,000 SAR | 7,500–12,000 SAR |
| **Includes** | 1 channel + 1 CRM mapping | 3 channels + CRM + Calendly | Full multi-channel + custom integrations + bilingual prompts |
| **Delivery** | 3 business days | 5 business days | 10 business days |

## Tier 3: Monthly Subscription (after pilot)

> **Code-truth alignment:** The prices below match `api/routers/pricing.py` PLANS dict. Any divergence is a bug.

| | Starter | Growth | Scale | Enterprise |
|---|---|---|---|---|
| **Price/month** | 999 SAR | 2,999 SAR | 7,999 SAR | custom |
| **Leads/month** | 200 | 1,000 | 5,000 | unlimited |
| **Channels** | 2 | 4 | all | all + private LLM |
| **Approval mode** | manual first 30 days, then mixed | mixed | mixed | mixed |
| **SLA** | 1h | 30 min | 15 min | 5 min |
| **Onboarding** | 1 hour | 2 hours | half-day | dedicated |
| **AI services bundled** | S1+S3 | S1+S3+S6+S7 | All 7 (S1-S7) | All 7 + custom |

## Tier 4: Agency / Partner Revenue Share

| Partner type | Setup | Recurring share |
|---|---|---|
| Referral partner | 0 | 10% MRR for 12 months |
| Agency reseller | 1,000 SAR setup, included in client price | 25% MRR while client active |
| Implementation partner | 2,500 SAR per setup | 15% MRR for 6 months |
| White-label (later) | 25,000 SAR | 30% MRR |

## Tier 5: Pay-per-result (post-validation)

For customers who hate subscription:

| Outcome | Price |
|---|---|
| Qualified Arabic-replied lead | 25 SAR |
| Booked demo on calendar | 150 SAR |
| Closed customer (success fee) | 5–10% of first-year contract |

## Discount + bundle rules

- Annual prepay → 2 months free.
- 3 customer referral → 1 free month.
- Saudi-flag founders → 25% off pilot.
- Sponsor a case study → 50% off month 1.

## Refund policy

- Pilot: 100% refund in window if Dealix didn't reply to a single Arabic lead.
- Subscription: 7-day money-back on first month.
- After 30 days: pro-rata.

## When to NOT discount

- 5,000+ SAR contracts where customer hasn't seen pilot proof. Make them pilot first.
- Customers asking "can you also send cold WhatsApp?" — politely decline. Dealix is inbound-only.
- Anyone asking to skip the manual approval gate in first 30 days.
