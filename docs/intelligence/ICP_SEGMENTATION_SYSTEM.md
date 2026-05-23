# ICP Segmentation System | نظام تقسيم العميل المثالي

## Purpose | الغرض
Slice the Saudi B2B universe into clean, repeatable ICP segments so every machine
(Outbound, ABM, Nurture, Partner) speaks to the right buyer with the right proof.

ICP segmentation is internal-only intelligence. It never becomes an external message
without an A2 approval.

## Inputs | المدخلات
- Sector Ranking System output
- Account Scoring Model output
- Buyer Persona System tags
- Past won/lost deals
- Founder's strategic ICP overrides

## Outputs | المخرجات
- `icp.segments` table: segment_id, sector, sub-vertical, employee_band,
  revenue_band, geo, buyer_role, pain_cluster, proof_artifacts
- Per-segment draft pack: subject lines, opener candidates, proof bullets, CTA
- Segment quality scorecard

## Segmentation axes | محاور التقسيم
1. **Sector** — one of the 8 target sectors
2. **Sub-vertical** — e.g., ERP for retail, MSSP for banking
3. **Company size** — micro (<10), small (10-50), mid (50-250), large (250+)
4. **Saudi geo** — Riyadh, Jeddah, Eastern Province, NEOM/Tabuk, other
5. **Buyer role** — founder/CEO, CRO, head of sales, head of marketing, COO
6. **Pain cluster** — sales hiring, weak pipeline, slow proposals, weak follow-up
7. **Proof match** — which Dealix proof artifact lands hardest

## Segment lifecycle | دورة حياة القطاع
- **Draft** — created from intelligence, < 20 accounts
- **Live** — 20+ accounts, drafts queued
- **Validated** — at least 1 proposal generated
- **Proven** — at least 1 paid client
- **Retired** — < 5% reply rate over 60 days OR founder retires it

## Data source | مصدر البيانات
`intelligence.icp_segments`, `crm.accounts`, `proof.artifacts`, founder overrides.

## Approval class | فئة الموافقة
- A1: internal segment refresh, scoring updates
- A2: activating a new segment for outbound drafting
- A3: any segment touching regulated industries or government

## Trust gate | بوابة الثقة
- Each segment cites its evidence: which signals justify it
- No PII stored in segment definitions (segment is anonymized cluster)
- Buyer-role tags map to public titles only
- Policy snapshot + audit row per segment activation

## Owner | المالك
Founder approves activation. Worker maintains segment health.

## Worker name
`intelligence.icp_segmenter`

## KPI | المؤشرات
- # validated segments per month
- # proven segments (total)
- Reply-rate spread between best and worst live segment (should narrow over time)
- Segment retirement velocity (healthy churn = signal of learning)

## Failure mode | حالات الفشل
- Over-segmentation: too many micro-segments, none reach validated state
- Stale segment: hasn't been refreshed in 60 days but still drafting
- Founder override drift: too many manual segments not backed by evidence

## Recovery path | مسار الاسترداد
- Auto-merge segments with < 20 accounts after 30 days
- Auto-archive segments with 0 replies after 45 days
- Weekly founder review of all manual overrides
