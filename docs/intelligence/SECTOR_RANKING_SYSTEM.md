# Sector Ranking System | نظام ترتيب القطاعات

## Purpose | الغرض
Rank Saudi B2B sectors by how attractive they are for Dealix *right now*. Drives
where the Distribution War Machine spends its weekly attention budget.

This system never sells; it only ranks and drafts.

## Target sectors | القطاعات المستهدفة
1. **ERP / CRM Implementers** — SAP, Oracle, Odoo, Microsoft Dynamics, Salesforce partners
2. **Cybersecurity** — MSSPs, SOC providers, GRC consultancies, IAM specialists
3. **B2B Agencies** — performance, brand, content, PR, design ops shops
4. **Logistics / Industrial** — 3PL, last-mile, fleet, warehousing, industrial automation
5. **Consulting / Digital Transformation** — management consultancies, DX advisories
6. **SaaS** — Saudi-origin or KSA-localized B2B SaaS vendors
7. **Enterprise Services** — managed IT, professional services, outsourcing
8. **High-Ticket B2B Providers** — anyone with > SAR 50k average deal size

## Inputs | المدخلات
- Trigger event feed (per sector)
- Hiring velocity (job posts mentioning sales/CS/revenue roles)
- Funding & tender announcements
- Public buyer activity (RFPs, expansions)
- Win/loss feedback from Dealix CRM
- Founder weekly sector calibration notes

## Outputs | المخرجات
- `sector_rank` table: sector_id, heat_score, trend, top_3_triggers, top_5_accounts
- Weekly **Sector Heat Digest** (draft → founder approves → posted internally)
- Per-sector outbound budget allocation suggestion

## Scoring dimensions | أبعاد التقييم
| Dimension | Weight | Notes |
|---|---|---|
| Trigger density | 25% | events in last 30d / # tracked accounts |
| Buyer clarity | 15% | % accounts with named decision maker |
| Average deal potential | 20% | estimated from public signals (no commitments) |
| Dealix proof fit | 15% | do we have relevant samples/case studies |
| Outreach channel openness | 10% | LinkedIn/email/form availability |
| Trust risk | 10% | regulatory, political, reputational |
| Founder strategic preference | 5% | manual overlay |

## Sector states | حالات القطاع
- **Hot** (heat >= 70): allocate top outbound capacity
- **Warm** (40–69): standard cadence
- **Cold** (< 40): nurture only, no new outbound
- **Frozen** (manual flag): paused by founder, audit row required

## Data source | مصدر البيانات
`intelligence.sectors`, `intelligence.trigger_events`, `crm.accounts`,
`partners.referrals`, founder calibration notes.

## Approval class | فئة الموافقة
- A1: internal heat-score refresh
- A2: any externally visible sector ranking (blog, deck, partner share)
- A3: ranking that names a specific competitor or a regulated body

## Trust gate | بوابة الثقة
- No claim of guaranteed revenue per sector
- All ranking factors cite their evidence row
- No personal data exposed in sector rollups
- Policy snapshot attached to every digest

## Owner | المالك
Founder approves the weekly heat digest. Worker runs daily refresh.

## Worker name
`intelligence.sector_ranker`

## KPI | المؤشرات
- Hot-sector → proposal conversion rate (rolling 90d)
- Hot-sector → paid client conversion rate
- # founder overrides per week (should trend down)
- Stale-signal % per sector (should stay < 10%)

## Failure mode | حالات الفشل
- One sector dominates because of a single noisy publisher
- Hiring data scraped from a deprecated source
- Trigger duplication inflating heat

## Recovery path | مسار الاسترداد
- Cap per-source contribution to a sector's heat at 40%
- Require 2+ independent sources for any heat jump > 15 points
- Auto-quarantine sector and notify founder if anomaly detected
