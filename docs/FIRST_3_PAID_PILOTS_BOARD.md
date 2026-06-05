# Dealix — First 3 Paid Pilots Board — لوحة أول 3 تجارب مدفوعة
<!-- Owner: Founder | Effective: 2026-06-05 | العربية أولاً -->

> **الهدف:** 3 تجارب مدفوعة (499 SAR) خلال أول 30 يوماً.
> الأسماء أدناه placeholders — لا أسماء حقيقية ولا PII في هذا الملف.

---

## 1. مخطط صف المرشَّح — Prospect Row Schema

| الحقل | EN | مثال صيغة |
|-------|----|-----------|
| company_name | اسم الشركة (مُجهَّل في النسخة العامة) | `<شركة-أ>` |
| decision_maker | صاحب القرار (دور لا اسم) | `<مؤسس / مدير مبيعات>` |
| pain | الألم | `<متابعة صفقات عبر واتساب>` |
| channel | القناة | `دخول دافئ / إحالة / LinkedIn` |
| relationship_level | مستوى العلاقة | `بارد / فاتر / دافئ` |
| offer_rung | درجة العرض | `[0] / [1] 499 SAR` |
| next_action | الإجراء التالي | `رسالة دافئة يدوية` |
| date | التاريخ | `2026-06-05` |

---

## 2. مراحل خط التجربة — Pilot Stage Columns

```
prospect → diagnostic → 499 sprint sold → proof pack delivered → upsell decision
مرشَّح → تشخيص → بيع sprint 499 → تسليم proof pack → قرار الترقية
```

| company (placeholder) | المرحلة الحالية | offer_rung | next_action | date |
|-----------------------|------------------|------------|-------------|------|
| `<شركة-أ>` | prospect | [0] | `<رسالة دافئة يدوية>` | `<YYYY-MM-DD>` |
| `<شركة-ب>` | diagnostic | [0]→[1] | `<حجز مكالمة 30د>` | `<YYYY-MM-DD>` |
| `<شركة-ج>` | prospect | [0] | `<إحالة من عميل>` | `<YYYY-MM-DD>` |

> صفوف فارغة للقالب فقط. تُملأ يدوياً، وتبقى مُجهَّلة إن نُشرت.

---

## 3. تتبّع الهدف — 3 Paid Pilots Tracker

| Pilot | الحالة | proof level | ملاحظة |
|-------|--------|-------------|--------|
| Pilot 1 | `<prospect>` | `<L2/L3>` | — |
| Pilot 2 | `<prospect>` | `<L2/L3>` | — |
| Pilot 3 | `<prospect>` | `<L2/L3>` | — |

أول 30 يوماً يكفي **L2/L3** (انظر [`CLAIMS_REGISTER.md`](CLAIMS_REGISTER.md)).

---

## 4. حساب القمع — Funnel Math (أسبوعياً)

| المرحلة | العدد الأسبوعي | EN |
|---------|----------------|----|
| مرشَّحون جدد | 20 | 20 new prospects |
| رسائل دافئة يدوية | 10 | 10 warm manual messages |
| ردود | 3 | 3 replies |
| مكالمات | 2 | 2 calls |
| عرض | 1 | 1 offer |
| إغلاق | 0.5–1 | 0.5–1 close |

> **قاعدة:** إذا لم تأتِ ردود → **أصلِح الرسالة / ICP، ولا تزد الحجم.**
> If no replies → fix message/ICP, do **NOT** increase volume.
> لا cold WhatsApp ولا scraping ولا mass-send. كل رسالة دافئة وبموافقة يدوية.

---

روابط: [`POSITIONING_AND_ICP.md`](POSITIONING_AND_ICP.md) · [`CLAIMS_REGISTER.md`](CLAIMS_REGISTER.md) · [`LAUNCH_GO_NO_GO.md`](LAUNCH_GO_NO_GO.md) · [`MASTER_LAUNCH_ROOM.md`](MASTER_LAUNCH_ROOM.md)

*No guaranteed claims · Missing data = insufficient_data · القيمة التقديرية ليست قيمة مُتحقَّقة.*
