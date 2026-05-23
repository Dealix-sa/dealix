# Dealix Market Entry Operating Stack

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Saudi B2B Revenue Operating System.

Built on Trust · Driven by Growth · Closing Deals · Focused on Results · Global Mindset, Local Impact.

This document is the meta-overview that ties together every operating
layer Dealix uses to enter the Saudi B2B market: brand, positioning,
intelligence, product, revenue motion, delivery, finance, customer
success, and trust. Each pillar has its own dedicated documentation;
this file links them into a single stack and explains the seams.

## The stack

```
                ┌─────────────────────────────────────────────┐
                │              Trust Plane                     │
                │   policy + registry + eval + audit           │
                │   (docs/trust/, policies/, registries/, evals/) │
                └──────────────────────┬──────────────────────┘
                                       │
                                       │ governs every layer below
                                       ▼
   ┌──────────────────────────────────────────────────────────────────┐
   │                          Brand Layer                              │
   │   Wordmark "DEALIX" + tagline "INTELLIGENT DEALS. REAL GROWTH."   │
   │   (docs/positioning/, docs/brand/)                                │
   └──────────────────────┬────────────────────────────────────────────┘
                          │
   ┌──────────────────────▼──────────────────────────────────────────┐
   │                       Positioning Layer                          │
   │   Saudi B2B Revenue Operating System                              │
   │   (docs/positioning/DEALIX_POSITIONING.md,                        │
   │    docs/positioning/SAUDI_B2B_NARRATIVE.md)                       │
   └──────────────────────┬──────────────────────────────────────────┘
                          │
   ┌──────────────────────▼──────────────────────────────────────────┐
   │                       Intelligence Layer                          │
   │   Sector map + ICP segmentation + sector ranking                  │
   │   (docs/intelligence/SAUDI_B2B_MARKET_MAP.md,                     │
   │    docs/intelligence/ICP_SEGMENTATION_SYSTEM.md,                  │
   │    docs/intelligence/SECTOR_RANKING_SYSTEM.md)                    │
   └──────────────────────┬──────────────────────────────────────────┘
                          │
   ┌──────────────────────▼──────────────────────────────────────────┐
   │                        Product Layer                              │
   │   Offer ladder + productization candidates                        │
   │   (docs/product/DEALIX_PRODUCT_LADDER.md)                          │
   └──────────────────────┬──────────────────────────────────────────┘
                          │
   ┌──────────────────────▼──────────────────────────────────────────┐
   │                       Revenue Layer                               │
   │   Revenue Factory OS + Sample Factory + Proposal Factory           │
   │   (docs/revenue/REVENUE_FACTORY_OS.md,                             │
   │    docs/revenue/SAMPLE_FACTORY.md,                                 │
   │    docs/revenue/PROPOSAL_FACTORY.md)                              │
   └──────────────────────┬──────────────────────────────────────────┘
                          │
   ┌──────────────────────▼──────────────────────────────────────────┐
   │                       Delivery Layer                              │
   │   Sprint OS + Handoff & QA + Customer Onboarding                   │
   │   (docs/delivery/ULTIMATE_DELIVERY_OS.md, etc.)                    │
   └──────────────────────┬──────────────────────────────────────────┘
                          │
   ┌──────────────────────▼──────────────────────────────────────────┐
   │                       Finance Layer                               │
   │   Finance OS + Revenue Recognition + AI Unit Economics             │
   │   (docs/finance/...)                                               │
   └──────────────────────┬──────────────────────────────────────────┘
                          │
   ┌──────────────────────▼──────────────────────────────────────────┐
   │                  Customer Success Layer                           │
   │   Health scoring + Renewal/Expansion + Referrals                   │
   │   (docs/customer_success/...)                                      │
   └─────────────────────────────────────────────────────────────────┘
```

The trust plane sits above every layer. The data and runtime layers
sit underneath. Nothing in this stack operates without the trust
plane's consent.

## Pillar map

| Pillar              | Primary document                                                       | Owner agent             |
| ------------------- | ---------------------------------------------------------------------- | ----------------------- |
| Brand               | `docs/positioning/DEALIX_POSITIONING.md`                                | Brand Guardian.         |
| Positioning         | `docs/positioning/SAUDI_B2B_NARRATIVE.md`                               | Founder + Brand Guardian.|
| Intelligence        | `docs/intelligence/SAUDI_B2B_MARKET_MAP.md`                              | Growth Strategist.       |
| ICP / segmentation  | `docs/intelligence/ICP_SEGMENTATION_SYSTEM.md`                          | Growth Strategist.       |
| Sector ranking      | `docs/intelligence/SECTOR_RANKING_SYSTEM.md`                            | Growth Strategist.       |
| Product             | `docs/product/DEALIX_PRODUCT_LADDER.md`                                 | Offer Architect.         |
| Revenue             | `docs/revenue/REVENUE_FACTORY_OS.md`                                    | Distribution Operator + Delivery Copilot. |
| Sample factory      | `docs/revenue/SAMPLE_FACTORY.md`                                        | Delivery Copilot.        |
| Proposal factory    | `docs/revenue/PROPOSAL_FACTORY.md`                                      | Delivery Copilot.        |
| Delivery            | `docs/delivery/ULTIMATE_DELIVERY_OS.md`                                 | Delivery Copilot.        |
| Onboarding           | `docs/delivery/CLIENT_ONBOARDING_OS.md`                                 | Delivery Copilot + CS.   |
| Handoff & QA         | `docs/delivery/HANDOFF_AND_QA_SYSTEM.md`                                | Delivery Copilot.        |
| Finance             | `docs/finance/ULTIMATE_FINANCE_OS.md`                                   | Finance Copilot.         |
| Customer success    | `docs/customer_success/CUSTOMER_SUCCESS_OS.md`                          | CS Lead.                 |
| Health scoring      | `docs/customer_success/CLIENT_HEALTH_SCORE_SYSTEM.md`                   | CS Lead.                 |
| Referrals           | `docs/customer_success/REFERRAL_SYSTEM.md`                              | Partner Revenue Agent.   |
| Renewal/expansion   | `docs/customer_success/RENEWAL_AND_EXPANSION_OS.md`                     | CS Lead + Founder.       |

## The seams

| Seam                                              | Owner of the seam                       |
| ------------------------------------------------- | --------------------------------------- |
| Brand → Positioning                                | Brand Guardian + Founder.               |
| Positioning → Intelligence                         | Growth Strategist.                       |
| Intelligence → Product                            | Offer Architect + Growth Strategist.    |
| Product → Revenue                                  | Distribution Operator + Offer Architect. |
| Revenue → Delivery                                  | Delivery Copilot.                       |
| Delivery → Finance                                   | Finance Copilot.                         |
| Delivery → Customer Success                          | CS Lead.                                 |
| Customer Success → Revenue (renewal, expansion)      | CS Lead + Founder.                       |
| Every layer → Trust Plane                             | Trust Guardian + Founder.                |

A seam without an owner is a place where the stack will leak.

## How the trust plane shows up at every layer

| Layer              | Trust posture                                                             |
| ------------------ | ------------------------------------------------------------------------- |
| Brand              | No overclaim; phrasing matrix in `NO_OVERCLAIM_POLICY.md`.                |
| Positioning        | Saudi-first; no claims unsupported by proof library.                       |
| Intelligence       | Account scoring is internal; never published.                              |
| Product            | Offer ladder rungs are policy-gated for pricing.                          |
| Revenue            | No external sending without approval; A3 banned.                            |
| Delivery           | Handoff QA gate; no proof without approval.                                |
| Finance            | Pricing, terms, refunds are founder decisions.                              |
| Customer success   | Referrals and proof require consent; renewal is policy-gated.              |

## Operating cadence

| Cadence       | What happens                                                              |
| ------------- | ------------------------------------------------------------------------- |
| Daily         | Founder brief; approvals reviewed; KPI snapshot.                          |
| Weekly        | Scorecard refresh; performance review; experiment review.                  |
| Monthly       | KPI tree walk; sector rebalance; finance close; CS deep-dive.              |
| Quarterly     | Sovereign readiness review; backup drill; access control drill; offer ladder review. |

## What this stack will not do

- Operate outside the trust plane.
- Make external claims unsupported by approved proof.
- Push expansion or referrals to customers without consent.
- Bypass the founder for any A2 external action.

## The brand promise

DEALIX · INTELLIGENT DEALS. REAL GROWTH. We are the Saudi B2B
Revenue Operating System. We are built on trust. We are driven by
growth. We close deals. We focus on results. We hold a global
mindset and a local impact. The stack above is how that promise is
operational, not aspirational.

## Cross-references

- `DEALIX_FINAL_OPERATING_SYSTEM.md` (this directory) for the
  highest-level summary across every pillar.
- The trust plane docs in `docs/trust/`.
- The performance docs in `docs/performance/`.
- The runtime and data docs in `docs/runtime/` and `docs/data/`.
- The engineering docs in `docs/engineering/`.
- The security docs in `docs/security/`.
