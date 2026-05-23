# Trigger Event System | نظام الأحداث المحفزة

## Purpose | الغرض
Detect, score, and route real-world business events that increase the probability
that a Saudi B2B account will buy *now*. Every trigger becomes a draft, never an
auto-send.

## Inputs | المدخلات
- Job-post feeds (sales, marketing, ops, executive roles)
- Funding & investment news
- M&A and ownership changes
- Tender / RFP publications
- Leadership moves (LinkedIn, press)
- Product launches and market expansions
- Saudi regulatory updates (Vision 2030 program waves)
- Office openings, geographic expansion
- Public hiring sprees (5+ open roles in 30 days)

## Outputs | المخرجات
- `intelligence.trigger_events` rows: event_id, account_id, type, source_url,
  detected_at, freshness, confidence, persona_match, draft_pack_id
- Daily trigger digest for founder (top 25)
- Drafts queued into Outbound, ABM, or Partner machines

## Trigger types & default urgency | أنواع المحفزات
| Type | Default urgency | Notes |
|---|---|---|
| New CRO / Head of Sales hire | High | revenue mandate fresh |
| Funding round announced | High | budget unlocked |
| New office in KSA | High | localization need |
| Job posts for 5+ sales roles | High | scaling pain |
| New ERP / CRM rollout | Medium | revenue tooling churn |
| Leadership departure | Medium | replacement window |
| Tender published | Medium | procurement window |
| Public case study published by them | Low | proof signal |

## Confidence scoring | تقييم الثقة
- Source authority (official, press, social) → weight
- Number of independent sources → weight
- Recency (< 14d > 14-30d > 30-90d > stale)
- Cross-check against account record

Final confidence = 0-100. Drafts only generated if confidence >= 60.

## Decision rules | قواعد القرار
- High urgency + A-priority account → ABM Strategic Account Machine
- High urgency + B-priority account → Outbound Draft Machine, top of queue
- Medium urgency → Outbound Draft Machine, normal queue
- Low urgency → Nurture Machine
- Confidence < 60 → quarantine, founder review

## Data source | مصدر البيانات
`intelligence.trigger_events`, `intelligence.accounts`, founder watchlists.

## Approval class | فئة الموافقة
- A1: trigger ingestion, scoring, routing to draft queue
- A2: any draft that goes external
- A3: triggers from regulated sectors / government

## Trust gate | بوابة الثقة
- Every trigger has a verifiable source URL
- No trigger fabrication, no inferred events without evidence
- Freshness gate: triggers older than 60 days drop out of high-urgency routing
- Policy snapshot + audit row per ingestion batch

## Owner | المالك
Founder reviews daily digest. Worker handles ingestion + routing.

## Worker name
`intelligence.trigger_engine`

## KPI | المؤشرات
- Trigger-to-reply rate (rolling 30d)
- Trigger-to-proposal rate (rolling 90d)
- Median time from event → draft queued
- % triggers with verifiable source (must be 100%)

## Failure mode | حالات الفشل
- Duplicate triggers from multiple sources inflating urgency
- Source URL becomes dead before draft is approved
- Hiring data scraped from a stale board

## Recovery path | مسار الاسترداد
- Dedupe by (account_id, type, week)
- Re-verify source at draft-approval time; if dead, founder asked to confirm
- Source-health audit weekly; deprecate dead sources
