# Competitive Intelligence System | نظام الذكاء التنافسي

## Purpose | الغرض
Track who else is selling into the same Saudi B2B accounts Dealix targets, what
they offer, how they price (public signals only), where they win, where they lose,
and how Dealix wins on trust + Saudi-fit + delivery quality.

Outputs are internal. Nothing competitive is ever written into outbound copy
without an A2 approval and a strict accuracy gate.

## Inputs | المدخلات
- Public competitor websites, pricing pages, case studies
- LinkedIn signals (who they hire, who they target)
- Tender / RFP records where competitors appear
- Reply transcripts where buyers mention alternatives
- Partner / referral notes about head-to-head deals
- Founder field intel

## Outputs | المخرجات
- `competitive.profiles`: competitor_id, sector, offer, positioning,
  pricing_signal (public-only), strengths, weaknesses, last_updated
- Head-to-head battle cards (internal use only)
- Win/loss pattern report (rolling 90d)
- Drafted *defensive* talking points (internal coach notes)

## Categories of competitors | فئات المنافسين
1. **Direct** — other Saudi-focused B2B revenue/sales agencies
2. **Adjacent** — outbound SaaS tools, fractional CRO services
3. **Inertia** — DIY founder doing it themselves
4. **Enterprise consultancies** — McKinsey-style top-down advisory
5. **Freelancers** — individual closers / setters

## Profile fields | حقول الملف التنافسي
- Offer description (1 sentence)
- Saudi presence (yes / no / partner-only)
- Pricing signal (only what is publicly disclosed)
- Proof artifacts they publish
- Reply-based mentions per month
- Win/loss pattern vs Dealix
- Trust posture (security page, PDPL stance, contract terms publicly visible)

## Decision rules | قواعد القرار
- If a competitor appears in > 3 deal reviews in a quarter → activate battle card
- If a competitor wins > 2 head-to-head against Dealix → trigger founder review
- If a competitor's claim is unverifiable → flag, do not counter-publish

## Data source | مصدر البيانات
`intelligence.competitors`, `crm.deals.lost_reason`, anonymized
`reply.transcripts`.

## Approval class | فئة الموافقة
- A1: internal profile refresh
- A2: any battle card or competitor mention used in a customer-facing draft
- A3: anything naming a competitor in public content or press

## Trust gate | بوابة الثقة
- Never publish unverified claims about a competitor
- Never reproduce a competitor's proprietary content
- No defamatory language, no price-fixing signal exchange
- Policy snapshot + audit row on every battle card published internally
- All competitor citations must include source URL

## Owner | المالك
Founder approves all externally-facing competitive mentions.

## Worker name
`intelligence.competitive_tracker`

## KPI | المؤشرات
- # active profiled competitors
- Win rate against top-3 competitors (rolling 90d)
- # head-to-head deals where battle card was used
- Accuracy: 0 published unverifiable claims

## Failure mode | حالات الفشل
- Out-of-date pricing signal cited in a draft
- Competitor name leaked into outbound by template error
- Battle card encourages over-confident language

## Recovery path | مسار الاسترداد
- Auto-expire pricing fields after 60 days unless refreshed
- Lint outbound drafts for competitor names; require A2 if found
- Battle cards reviewed quarterly by founder
