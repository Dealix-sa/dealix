# ICP Segmentation System

> Defines the Ideal Customer Profile in machine-checkable terms.

## 1. Primary ICP (Tier 1)

| Dimension | Value |
|---|---|
| Geography | Kingdom of Saudi Arabia |
| Sector | One of the eight sectors in `SECTOR_RANKING_SYSTEM.md` |
| Size band | 30 - 500 FTE |
| Revenue band | 10M - 500M SAR ARR |
| Motion | Founder- or executive-led B2B sales |
| Tech stack | Operates at least one CRM and one outbound channel |
| Trust posture | Buyer-aware, AI-cautious |
| Decision maker | Founder, COO, CRO, or Head of Growth |

## 2. Secondary ICP (Tier 2)

- KSA-presence multinationals (regional HQ, 5+ FTE in KSA).
- GCC firms with material KSA revenue.

## 3. Anti-ICP

We will not engage:

- Consumer-only businesses.
- Government tenders without partner sponsorship.
- Crypto / unregulated finance.
- Any organisation on the suppression list.

## 4. Segments

| Segment | Definition | Lead offer |
|---|---|---|
| Founder-led KSA SaaS | 30-100 FTE, founder still closes | Revenue Sprint |
| KSA cybersecurity vendor | Selling into enterprise | Managed Pilot |
| KSA ERP/CRM integrator | Implementation revenue dominant | Retainer |
| B2B agency in KSA | Operating outbound for customers | White-label OS |
| KSA consulting firm | Selling transformation engagements | Revenue Desk Retainer |
| Logistics / industrial services | Account-led motion | ABM Managed Pilot |
| Saudi high-ticket B2B | Bespoke deals 250k+ SAR | Founder Command Center |
| GCC firm with KSA presence | Cross-border buyer | Enterprise OS |

## 5. Output

`growth/target_segments.csv` columns:

```
segment_id, name_en, name_ar, tier, lead_offer, ideal_size, ideal_arr, motion, status, source
```

## 6. Cadence

- Weekly refresh of segment status.
- Monthly review of segment definitions.
- Quarterly review of ICP overall.

## 7. Trust posture

ICP and segments inform recommendations, never enforce automated action.
