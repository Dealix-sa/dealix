# Marketing & Revenue Attribution — نسبة الإيراد

> Section 40. سبعة أنواع attribution، AttributionRecord schema، الأسئلة الستّ، وكيف نتتبّع.
> Module path: `dealix/growth_os/attribution/`

---

## مقدّمة — Introduction

كل ريال يدخل Dealix يجب أن يعرف من أين أتى. ليس لأغراض تسويقية، بل لتقرير ما الذي يستحقّ التوسعة وما الذي يستحقّ الإيقاف. الـ attribution هنا أداة قرار، لا أداة استعراض.

Every riyal that enters Dealix must know where it came from — not to brag, but to decide what to scale and what to kill. Attribution here is a decision tool, not a vanity tool.

---

## الأسئلة الستّ — The 6 Attribution Questions

كل صفقة تُجاب عنها بستّة أسئلة:

1. **Source.** ما الإشارة الأولى التي لفتت انتباه العميل؟
2. **Trigger.** ما الذي جعله يطلب اجتماعاً الآن؟
3. **Asset.** أي محتوى/أصل أثّر في القرار؟
4. **Channel.** عبر أي قناة وصل (GEO, ABM, partner, paid, referral)?
5. **Agent.** أي وكلاء Dealix شاركوا في التحضير؟
6. **Partner.** هل شريك معيّن أحال أو شارك؟

---

## السبع أنواع — The 7 Attribution Types

| # | النوع | متى يُستخدم | الوزن المُقترَح |
|---|---|---|---|
| 1 | First Touch | أوّل تفاعل يُسجَّل | 100% لأوّل touchpoint |
| 2 | Last Touch | آخر تفاعل قبل الإغلاق | 100% لآخر touchpoint |
| 3 | Linear | جميع touchpoints متساوية | 1/N لكل نقطة |
| 4 | Time Decay | الأقرب زمنياً للإغلاق يأخذ أكثر | منحنى exp decay |
| 5 | Position-Based (U-shape) | أوّل + أخير + باقي | 40/40/20 |
| 6 | Signal-Anchored (Dealix-native) | يربط الإيراد بـ SignalCard أصلي | 100% للإشارة + توزيع ثانوي |
| 7 | Partner-Weighted | عند وجود شريك مُحيل | حسب PartnerAgreement.commission_share |

> الافتراضي في Dealix: **Signal-Anchored + Linear secondary**. السبب: يربط الإيراد بقرار سوقي حقيقي، ويوزّع الفضل عبر الأصول المساعدة.

---

## AttributionRecord JSON example

```json
{
  "attribution_id": "ATR-2026-0231",
  "revenue_id": "REV-2026-0231",
  "deal_id": "DEAL-2026-0089",
  "model": "signal_anchored_linear_secondary",
  "source_signal": {
    "signal_id": "SIG-2026-0117",
    "signal_type": "sdaia_framework_update",
    "captured_at": "2026-05-01T08:00:00+03:00"
  },
  "trigger_event": {
    "event_type": "meeting_request",
    "requested_at": "2026-05-05T11:30:00+03:00",
    "trigger_asset_id": "CON-GEO-0004"
  },
  "touchpoints": [
    {"order": 1, "channel": "geo", "asset_id": "CON-GEO-0004", "ts": "2026-05-03T09:14:00+03:00"},
    {"order": 2, "channel": "linkedin_dm", "asset_id": "MSG-2026-0042", "ts": "2026-05-04T16:00:00+03:00"},
    {"order": 3, "channel": "meeting", "asset_id": "MTG-2026-0089", "ts": "2026-05-06T10:00:00+03:00"},
    {"order": 4, "channel": "proposal", "asset_id": "PRO-2026-0089", "ts": "2026-05-09T13:00:00+03:00"}
  ],
  "weights": {
    "signal_primary": 1.0,
    "secondary_distribution": {
      "CON-GEO-0004": 0.40,
      "MSG-2026-0042": 0.20,
      "MTG-2026-0089": 0.20,
      "PRO-2026-0089": 0.20
    }
  },
  "channel_attribution": {
    "geo": 0.40,
    "abm_direct": 0.20,
    "conversion_engine": 0.40
  },
  "agent_attribution": {
    "signal_radar_agent": 0.25,
    "message_drafter_agent": 0.25,
    "proposal_drafter_agent": 0.50
  },
  "partner_attribution": null,
  "campaign_id": null,
  "disclosures": [
    "Attribution is a model, not a fact.",
    "Dealix uses Signal-Anchored as primary; secondary weights are diagnostic."
  ]
}
```

---

## ما نتتبّعه — What We Track

| المحور | ما يُسجَّل | المصدر |
|---|---|---|
| Channel | geo / abm / partner / paid / referral / event | حقل `channel` في كل touchpoint |
| Offer | OfferCard.id | RevenueRecord.offer_id |
| Campaign | حملة محدَّدة (إن وُجدت) | PaidCampaignCard.id |
| Asset | كل أصل محتوى/رسالة | ContentAsset.id, MessageDraft.id |
| Agent | كل وكيل ساهم | AI Run Ledger (`docs/06_llm_gateway/AI_RUN_LEDGER.md`) |
| Partner | إن وُجد إحالة شريك | PartnerDealRecord.id |
| Signal | الإشارة المصدر | SignalCard.id |

---

## قواعد الإسناد — Attribution Rules

1. **لا attribution بدون touchpoint موثَّق.** كل نقطة لها timestamp ومصدر.
2. **لا تكرار double-counting.** الصفقة الواحدة لها AttributionRecord واحد.
3. **Signal أولاً.** إن وُجدت إشارة سوقيّة، تأخذ الإسناد الأوّلي.
4. **شفافيّة النموذج.** اذكر دائماً نموذج الإسناد المُستخدم.
5. **إعادة الحساب الشهريّة.** أعد توزيع الأوزان شهرياً مع touchpoints المتأخّرة.

---

## مؤشّرات قياس صحّة الإسناد — Attribution Health KPIs

- `% revenue with attribution_record` — مستهدف ≥ 95%.
- `avg touchpoints per deal` — يُراقب الاتجاه، لا قيمة مطلقة.
- `signal_anchored_share` — % صفقات لها signal_id.
- `channel_concentration` — مؤشر تنوّع القنوات (تجنّب الاعتماد على قناة واحدة).

---

## How to verify

```bash
bash scripts/growth_os_master_verify.sh
```

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
