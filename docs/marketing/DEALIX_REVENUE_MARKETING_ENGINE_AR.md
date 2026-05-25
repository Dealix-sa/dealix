# Dealix Revenue Marketing Engine — وثيقة الحوكمة (AR)

> ديلكس لا يسوّق ليظهر — يسوّق ليحوّل إشارات السوق إلى فرص، الفرص إلى عروض،
> العروض إلى صفقات، الصفقات إلى دخل حقيقي، والدخل إلى بيانات وأصول تزيد قوة
> النظام كل أسبوع.

## 1. الموقع داخل ديلكس

محرك Revenue Marketing هو الطبقة الموحّدة بين:

- **Market Signal Radar** (إشارات السوق المُدخَلة بحوكمة — لا scraping).
- **Marketing Factory** (تقويم محتوى وروابط UTM ومسودات أسبوعية).
- **Approval Center + Evidence Ledger** (كل خروج خارجي بإذن المؤسس وسجل أدلة).
- **Revenue Ops Autopilot + War Room** (الـpipeline والحسابات والـops).

كل ما يُنشَأ هنا يولَد كـ **draft**. لا إرسال خارجي مباشر — يمر بـ
`/api/v1/ops-autopilot/marketing/queue-approval` ثم يُنفَّذ يدويًا.

## 2. الحلقة (Marketing Operating Loop)

```
Signal → Segment → Pain → Offer → Message → Channel →
Lead → Deal → Revenue → Outcome → Learning → Asset → Scale / Kill
```

كل خطوة لها endpoint وtable:

| الخطوة | الـ Endpoint | الجدول |
| --- | --- | --- |
| Signal | `POST /api/v1/revenue-marketing/signals` | `rm_signals` |
| Loop run (Signal → Campaign draft) | `POST /api/v1/revenue-marketing/loop/run` | `rm_campaigns` |
| Campaign create + quality gate | `POST /api/v1/revenue-marketing/campaigns` | `rm_campaigns` |
| Touch capture | `POST /api/v1/revenue-marketing/touches` | `rm_marketing_touches` |
| Attribution (payment confirmed) | `POST /api/v1/revenue-marketing/attribution/record` | `rm_revenue_attribution` |
| Experiment + Decide | `POST /api/v1/revenue-marketing/experiments/...` | `rm_marketing_experiments` |
| Funnel snapshot + bottleneck | `POST /api/v1/revenue-marketing/funnel/snapshot` | `rm_funnel_snapshots` |
| Portfolio dashboard | `GET /api/v1/revenue-marketing/portfolio/dashboard` | (مشتق) |

## 3. سُلَّم العروض (5 درجات)

البذرة في `dealix/revenue_marketing/seed.yaml`:

1. **Free** — AI Governance Checklist · Revenue Leakage Checklist
2. **Entry** — Revenue Hunter Pilot (999 ر.س) · AI Trust Diagnostic (4,999 ر.س) · Data Pack (1,500 ر.س)
3. **Core** — AI Trust Kit (12K–25K) · Monthly Revenue Command (8K–18K/شهر) · Agency White-Label Kit
4. **Expansion** — Executive PMO · Market Radar Subscription
5. **Enterprise** — Agentic Control Plane (60K–250K)

`GET /api/v1/revenue-marketing/offers/ladder` يعيد السُلَّم كاملًا
مع `money_quality` لكل عرض.

`GET /api/v1/revenue-marketing/offers/{id}/upsell-suggestion`
يقترح العرض الأقوى في الدرجة التالية تلقائيًا.

## 4. صيغة Lead Score

```
Lead Score =
  0.25 · ICP fit
+ 0.20 · pain likelihood
+ 0.20 · ability to pay
+ 0.15 · urgency
+ 0.10 · partner potential
+ 0.10 · trust fit
```

كل sub-score مُعيَّر إلى [0, 1]. الناتج 0–100 + breakdown شفاف +
`recommended_offers` تختار من السُلَّم.

```
POST /api/v1/revenue-marketing/leads/score
```

## 5. Attribution (القاعدة الذهبية: لا revenue بدون دفع)

`attribute_revenue()` يرفض بـ `ValueError` إذا `payment_confirmed=False`.
الـendpoint يرفض بـ HTTP 422.

أنواع الـ attribution المدعومة:
- `first_touch` — أول قناة تمس الـlead
- `last_touch` — آخر قناة قبل التحويل
- `multi_touch` — توزيع خطي بين كل النقاط
- `asset_influenced` — كل الأصول (checklist/template/case study) التي ظهرت في السلسلة
- `agent_influenced` — كل الوكلاء الذين ساهموا في السلسلة

```
POST /api/v1/revenue-marketing/attribution/record
GET  /api/v1/revenue-marketing/attribution/dashboard
```

## 6. Money Quality Score

```
Money Quality =
  margin + repeatability + low_delivery_effort
+ upsell_potential + data_moat + partner_potential
- risk
```

النتيجة المُعيَّرة في [-1, 2] مع verdict:
- `>= 1.2` → **scale**
- `>= 0.8` → **keep**
- `>= 0.4` → **improve**
- وإلا → **kill_or_rework**

`portfolio_dashboard()` يعطي كل العروض مرتبة بالـverdict، ليسهل قرار
التوسعة/التقاعد كل أسبوع.

## 7. التجارب (A/B Experiments)

قاعدة القرار الافتراضية: **scale variant if 2x conversion vs control**.
الـAPI:

```
POST /api/v1/revenue-marketing/experiments
POST /api/v1/revenue-marketing/experiments/{id}/observe   { "variant": "a"|"b", "converted": bool }
POST /api/v1/revenue-marketing/experiments/{id}/decide
```

الـdecision لا يُفعَّل إلا بعد بلوغ `minimum_sample` في الذراعين.
ثلاث حالات صريحة: `decided_scale`, `decided_kill`, `inconclusive`.

## 8. Conversion Funnel + Bottleneck

`bottleneck_diagnosis()` يقارن المراحل بالـbaseline الصحي:

| Stage | Healthy baseline |
| --- | --- |
| visitor_to_lead | 3% |
| lead_to_qualified | 40% |
| qualified_to_call | 50% |
| call_to_proposal | 60% |
| proposal_to_win | 30% |
| win_to_payment | 90% |
| payment_to_retainer | 25% |

ويعيد `fix_hint_ar` للمرحلة الأضعف (CTA، تأهيل، Discovery، Proof Pack،
Moyasar، Value Report …).

## 9. Quality Gates (ضد الـnoise)

كل campaign لازم تحقّق:
`campaign_name, target_segment, offer_id, channel, message_angle,
cta_label_ar, success_metric, scale_kill_rule`.

كل content card لازم تحقّق:
`topic_ar, target_segment, pain, offer_id, cta_ar, channel`.

أيّ نقص → `ok=false` + `blocked_reasons[]`، ويُمنع الـqueue للموافقة.

`POST /api/v1/revenue-marketing/content/anti-vanity-review`
يكتشف vanity metrics (engagement عالي بلا leads، leads بلا calls،
calls بلا deals).

## 10. الترابط مع المنظومة الحالية

- **Marketing Factory** يظل الواجهة الأمامية للمحتوى الأسبوعي والـUTM —
  هذا المحرك يولّد المسودة، Marketing Factory يطبع `queue-approval`.
- **Evidence Ledger** (`get_autopilot_store().append_evidence`) يستقبل
  أحداث: `signal_captured`, `campaign_drafted`, `campaign_created`,
  `revenue_attributed`, `experiment_decided`.
- **War Room** يقرأ الـattributions ليبني revenue trace لكل deal.
- **Founder Cadence** اليومية والأسبوعية تستهلك `portfolio/dashboard` و
  `attribution/dashboard` لقرارات scale/kill.

## 11. تشغيل سريع

```bash
# 1) صحة الـmigration head
python3 scripts/check_alembic_single_head.py     # → 014

# 2) تشغيل الاختبارات
APP_ENV=test python3 -m pytest tests/test_revenue_marketing_engine.py -q

# 3) أمثلة curl (محليًا، مع X-Admin-API-Key)
curl -H "X-Admin-API-Key: $DEALIX_ADMIN_API_KEY" \
  http://localhost:8000/api/v1/revenue-marketing/doctrine

curl -X POST -H "X-Admin-API-Key: $DEALIX_ADMIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"signal_id":"sig_ksa_ai_adoption_trust_gap"}' \
  http://localhost:8000/api/v1/revenue-marketing/loop/run
```

## 12. القاعدة النهائية (مختصرة)

- لا حملة بلا offer.
- لا offer بلا price range.
- لا lead بلا source.
- لا deal بلا attribution.
- لا revenue بدون payment confirmed.
- لا outcome بلا learning.
- لا learning بلا قرار scale/kill.
- لا إرسال خارجي تلقائي — Approval Center أولًا.
