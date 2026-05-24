# Retention & Referral OS | نظام الاحتفاظ والإحالة

## Purpose | الغرض
Convert delivered work into renewed retainers, expanded scopes, and warm referrals.
Retention is where Dealix's economics actually win — and where compounding starts.

All client outreach is drafted → founder-approved → manually sent.

## Inputs | المدخلات
- Closed-out engagements from Ultimate Delivery OS
- Post-engagement client sentiment + survey results
- Renewal/expansion opportunity signals
- Referral opportunity signals (champion identified, network mapped)
- Account health (ongoing for active retainers)

## Outputs | المخرجات
- `retention.opportunities`: id, client_id, type (renewal/expansion/referral),
  signal_strength, draft_id, state
- Per-client retention plan
- Referral ask drafts (queued for founder approval)
- Quarterly retention health report

## Opportunity types | أنواع الفرص
- **Renewal** — current retainer ending in 30-60 days
- **Expansion** — adjacent scope, additional service line
- **Cross-sell** — different department of same client
- **Referral — direct ask** — client willing to recommend
- **Referral — case study** — proof event becomes a magnet
- **Referral — partner network** — partner intro through client connection

## Cadence | التواتر
- Active retainer clients: monthly check-in draft (founder reviews + sends)
- 60-day pre-renewal: structured renewal conversation drafted
- 30-day pre-renewal: renewal proposal drafted (Proposal Factory)
- Post-engagement +30 days: NPS-style draft, surfacing referral opportunity
- Post-engagement +90 days: expansion conversation drafted

## Referral ask rules | قواعد طلب الإحالة
- Only after a clear success moment (delivered milestone, positive sentiment)
- Specific ask: name 1-2 peers, ideally same sector
- No incentive language that implies financial commitment unless a written
  referral agreement exists
- Polite, low-pressure, easy to decline

## Data source | مصدر البيانات
`retention.opportunities`, `delivery.engagements`, `client.sentiment`,
`partners.referrals`.

## Approval class | فئة الموافقة
- A1: opportunity detection, draft generation, scheduling
- A2: every client outreach (check-in, renewal, referral ask)
- A3: regulated/government clients; any commercial commitment

## Trust gate | بوابة الثقة
- Referral asks never imply paid placement without written agreement
- No guarantee language in renewal/expansion drafts
- Client consent required before any proof-event publication
- Policy snapshot + audit row per draft

## Owner | المالك
Founder owns every client touch and approves every referral ask.

## Worker name
`client_success.retention_referral_os`

## KPI | المؤشرات
- Logo retention rate (rolling 12m)
- Net revenue retention (renewal + expansion - churn)
- Referrals received per active client per year
- Referral → paid client conversion rate
- Time from engagement-closeout → first referral ask

## Failure mode | حالات الفشل
- Renewal conversation starts too late, client already shopped alternatives
- Referral ask sent before a clear success moment → damages trust
- Expansion pushed when client is in a delivery red-health state

## Recovery path | مسار الاسترداد
- Renewal calendar auto-creates 60-day-before drafts
- Success-moment detector required to gate referral asks
- Expansion drafts blocked when account health is yellow or red
