# 03 — Proposal Templates — قوالب العروض

> One bilingual template per active offer. Consistent with the repo's renderer:
> `auto_client_acquisition/sales_os/proposal_renderer.render_proposal(...)` and the Jinja
> template `templates/PROPOSAL_REVENUE_INTELLIGENCE_SPRINT.md.j2`.
> Prices are from [`docs/OFFER_LADDER_AND_PRICING.md`](../../OFFER_LADDER_AND_PRICING.md) —
> do not change them.

**Before sending any real proposal:** confirm Moyasar is in live mode. If
`launch-status` reports `moyasar.mode == "test"`, run `python scripts/moyasar_live_cutover.py`
first — do not send `sk_test_` invoice links to real customers.

Every proposal includes: bounded scope, the 11 exclusions, price + 50/50 payment terms,
the proof-metric promise, the retainer path, and the bilingual disclaimer.

---

## Template A — Free AI Ops Diagnostic (Tier 0, 0 SAR)

**Free AI Ops Diagnostic — التشخيص المجاني لعمليات الذكاء الاصطناعي**

**Engagement ID:** `{{engagement_id}}` · **Customer:** {{customer_name}} ·
**Sector:** {{sector}} · **City:** {{city}} · **Date:** {{proposal_date}}

### Scope — النطاق
A one-page diagnostic of {{customer_name}}'s revenue-operations gaps, from a 6-question
intake (about 15 minutes of your time). Delivered bilingual, with the founder's personal
sign-off, within **24 hours** of intake submission.
تشخيص من صفحة واحدة لفجوات عمليات الإيرادات لدى {{customer_name}}، من استبيان من 6 أسئلة،
يُسلَّم ثنائي اللغة باعتماد شخصي خلال 24 ساعة من تقديم الاستبيان.

### Deliverables — المخرجات
1. One-page diagnostic report (bilingual).
2. Top 3 revenue-operations priorities.
3. A clear next-step recommendation (sprint, reframe, or "not yet").

### Exclusions — الاستثناءات
No ROI promises, no advanced analysis, no platform access, no outreach drafting, and no
external sending. The 11 non-negotiables apply (see [README](./README.md)).

### Price & terms — السعر والشروط
**0 SAR.** No payment, no card, no obligation. No invoice is issued.

### Proof-metric promise — وعد الإثبات
The diagnostic is itself a proof artifact: 3 evidenced priorities. **No outcome is
guaranteed.**

### Retainer / next path — المسار التالي
If the diagnostic shows a clear proof path, you may be invited to the **499 SAR 7-Day
Revenue Proof Sprint** (Template B). Free contacts under no pressure to proceed.

**Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.**

---

## Template B — 7-Day Revenue Proof Sprint (Tier 1, 499 SAR)

> Render the per-customer version with `render_proposal(ProposalContext(...))` or the
> Jinja template `templates/PROPOSAL_REVENUE_INTELLIGENCE_SPRINT.md.j2`. This is the
> bilingual reference text.

**Revenue Intelligence Sprint — Proposal for {{customer_name}} / عرض سبرنت ذكاء الإيرادات**

**Engagement ID:** `{{engagement_id}}` · **Sector:** {{sector}} · **City:** {{city}} ·
**Date:** {{proposal_date}}

### Scope — النطاق
A single governed motion, end-to-end, over **7 calendar days**, at a fixed **499 SAR**.
One primary workflow, one named owner, 10 ranked accounts.
سير عمل واحد مُحوكَم من البداية للتسليم خلال 7 أيام تقويمية، بسعر ثابت 499 ريال. سير عمل
أساسي واحد، مالك واحد معروف، 10 حسابات مُرتّبة.

### Deliverables — المخرجات (10)
1. Signed Source Passport on file. — جواز مصدر موقّع.
2. Data-Quality baseline score (6 dimensions). — خط أساس لجودة البيانات.
3. Deduplication report with merge rules. — تقرير إزالة التكرار.
4. **10 ranked accounts** with an explainable rubric. — 10 حسابات مُرتّبة برُبريك واضح.
5. **Bilingual draft pack (AR + EN)**, marked `draft_only` until your approval.
6. Governance decisions log (7-decision matrix). — سجل قرارات الحوكمة.
7. Redaction and block summary. — ملخص الحجب والتنقيح.
8. **14-section Proof Pack** with computed score (target ≥ 80). — حزمة إثبات من 14 قسماً.
9. **At least one Capital Ledger asset** (reusable rule/template/insight).
10. Bilingual handoff session (60 minutes). — جلسة تسليم ثنائية اللغة.

### Scope boundaries — حدود النطاق
Duration fixed at 7 days. Headline deliverable is 10 accounts. One workflow, one owner.
Channels: **drafts only** — {{customer_name}} decides whether and when to send.

### Exclusions — الاستثناءات
No direct sending (`draft_only`), no guaranteed deals, no internal-systems access, no
scraping, no cold WhatsApp, no LinkedIn automation. Full list: the 11 non-negotiables.

### Proof-metric promise — وعد الإثبات
Dealix promises **methodology and audit-trail metrics**: DQ baseline + post-sprint score,
duplicates merged, unsafe attempts blocked, bilingual draft count, a 14-section Proof
Pack score (target ≥ 80), and at least 1 capital asset. **Dealix does not promise closed
deals, pipeline acceleration, or revenue lift.**

### Price & payment terms — السعر وشروط الدفع
**499 SAR**, all-inclusive, ZATCA-compliant e-invoice.
**50% on acceptance** of this proposal · **50% on Proof Pack delivery**.
Payment via Moyasar link under engagement ID `{{engagement_id}}`.
الدفع: 50% عند القبول و50% عند تسليم حزمة الإثبات، عبر رابط ميسر.

### Timeline — الجدول الزمني
Day 1 kickoff + Source Passport · Day 2 data import + DQ · Day 3 account scoring ·
Day 4 bilingual drafts + governance review · Day 5 Proof Pack assembly · Day 6 handoff +
retainer-readiness check · Day 7 capital asset registration. Calendar starts on the first
business day after acceptance and first-payment clearance.

### Retainer path — مسار الاحتفاظ
After the sprint, if **proof_score ≥ 80** AND **adoption_score ≥ 70** AND a workflow
owner remains named, Dealix offers the **Managed Revenue Ops** retainer at **2,999
SAR/month** (lower tier) or **4,999 SAR/month** (full tier) — see Template D.

**Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.**

---

## Template C — Data-to-Revenue Pack (Tier 2, 1,500 SAR)

**Data-to-Revenue Pack — Proposal for {{customer_name}} / حزمة البيانات إلى الإيرادات**

**Engagement ID:** `{{engagement_id}}` · **Sector:** {{sector}} · **City:** {{city}} ·
**Date:** {{proposal_date}}

### Scope — النطاق
A one-project engagement for a B2B company with an under-used customer/sales dataset:
full pipeline analysis and an opportunity map turned into approval-ready drafts. Fixed
**1,500 SAR**, **5–7 business days**.
ارتباط مشروع واحد لشركة B2B لديها بيانات عملاء/مبيعات غير مستثمرة: تحليل كامل للـ pipeline
وخريطة فرص تتحوّل إلى مسودات جاهزة للاعتماد. سعر ثابت 1,500 ريال، 5–7 أيام عمل.

### Inputs needed — المدخلات المطلوبة
A CRM export or Excel customer list **you own**, 3 months of sales data, and a description
of your current ICP. A signed Source Passport covering PII handling and retention.

### Deliverables — المخرجات
1. Full pipeline analysis. — تحليل pipeline كامل.
2. A ranked opportunity map. — خريطة فرص مُرتّبة.
3. **10 personalized targeting drafts** (bilingual, `draft_only`).
4. An ROI-basis report (methodology, not a guarantee). — تقرير أساس ROI.
5. A custom sales playbook. — playbook مبيعات مخصص.
6. 14-section Proof Pack + at least one Capital Ledger asset.

### Exclusions — الاستثناءات
**No scraping**, no direct integration into your CRM, no PII in logs, no direct sending,
no guaranteed outcomes. The 11 non-negotiables apply.

### Price & payment terms — السعر وشروط الدفع
**1,500 SAR**, ZATCA-compliant e-invoice. **50% on acceptance · 50% on Proof Pack
delivery**, via Moyasar under engagement ID `{{engagement_id}}`.

### Proof-metric promise — وعد الإثبات
At least one defined and documented opportunity, and a client-approved playbook. **No
revenue lift is promised.**

### Retainer path — مسار الاحتفاظ
On a successful pack, the path opens to **Managed Revenue Ops** at 2,999–4,999 SAR/month
(Template D).

**Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.**

---

## Template D — Managed Revenue Ops (Tier 3, 2,999–4,999 SAR/month)

> Present only when `adoption_os.retainer_readiness.evaluate(...).eligible == True` —
> i.e. proof_score ≥ 80, adoption_score ≥ 70, and a named workflow owner remains.

**Managed Revenue Ops — Proposal for {{customer_name}} / إدارة عمليات الإيرادات الشهرية**

**Engagement ID:** `{{engagement_id}}` · **Sector:** {{sector}} · **City:** {{city}} ·
**Date:** {{proposal_date}}

### Scope — النطاق
A monthly subscription that keeps the revenue-operations radar running for {{customer_name}}
after a successful pilot. Founder-assisted delivery today (manual monthly operation — see
the delivery-mode disclosure in `OFFER_LADDER_AND_PRICING.md`).
اشتراك شهري يُبقي رادار عمليات الإيرادات يعمل لـ {{customer_name}} بعد pilot ناجح. التسليم
حالياً بقيادة المؤسس (تشغيل يدوي شهري).

### Tiers — الدرجتان
- **Lower tier — 2,999 SAR/month:** core monthly motion.
- **Full tier — 4,999 SAR/month:** full cadence, broader account coverage.

### Deliverables (monthly) — المخرجات الشهرية
1. Weekly executive report. — تقرير تنفيذي أسبوعي.
2. Up to **20 approved outreach drafts/month** (`draft_only`).
3. Monthly Proof Pack. — حزمة إثبات شهرية.
4. KPI report. — تقرير مؤشرات الأداء.
5. A 60-minute monthly strategy session. — جلسة استراتيجية شهرية 60 دقيقة.

### Inputs needed — المدخلات المطلوبة
Dealix Portal access, weekly pipeline updates, and **approval on every message**.

### Exclusions — الاستثناءات
**Maximum 20 drafts/month**, no automatic sending, no legal advice, no scraping, no PII
in logs, no guaranteed outcomes. The 11 non-negotiables apply.

### Price & payment terms — السعر وشروط الدفع
**2,999–4,999 SAR/month** depending on tier, ZATCA-compliant e-invoice. Billed monthly;
the **50/50 split applies per delivery cycle** — 50% on acceptance of the month's scope,
50% on that month's Proof Pack delivery. Moyasar under engagement ID `{{engagement_id}}`.

### Proof-metric promise — وعد الإثبات
A monthly Proof Pack with a computed score (target ≥ 80) and at least one capital asset
per cycle. Retention depends on sustained adoption and satisfaction. **No MRR or
deal-volume outcome is guaranteed.**

### Upgrade path — مسار الترقية
After 3 completed pilots and a documented case study, the **Executive Command Center**
(7,500–15,000 SAR/month) may be discussed in a scheduled call.

**Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.**

---

## Rendering note — ملاحظة التوليد

For Template B, prefer the code path so exclusions and proof targets stay in sync with
middleware:

```python
from auto_client_acquisition.sales_os.proposal_renderer import (
    ProposalContext, render_proposal,
)
proposal = render_proposal(ProposalContext(
    customer_name="...", customer_handle="...", sector="...", city="...",
    engagement_id="...", price_sar=499, delivery_days=7,
    proof_score_target=80, source_passport_required=True,
    retainer_offer_after=True,
))
```

All rendered proposals are drafts for founder review. Dealix never sends a proposal
externally on its own.
