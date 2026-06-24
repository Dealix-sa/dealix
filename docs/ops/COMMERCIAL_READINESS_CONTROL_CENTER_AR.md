# Dealix Commercial Readiness Control Center

## القرار التنفيذي

هذه الطبقة تحوّل Dealix من مجموعة أنظمة وأفكار إلى روتين تجاري يومي يمكن للمؤسس تشغيله بثلاث نتائج واضحة:

1. ما الذي نبيعه اليوم؟
2. من نستهدف اليوم؟
3. ما الذي نراجعه يدويًا قبل أي إجراء خارجي؟

## القاعدة غير القابلة للكسر

Dealix يولّد مسودات وقرارات وتقارير، لكنه لا يرسل خارجيًا افتراضيًا.

القيم الآمنة الافتراضية:

```env
EXTERNAL_SEND_ENABLED=false
EMAIL_SEND_ENABLED=false
WHATSAPP_SEND_ENABLED=false
WHATSAPP_ALLOW_LIVE_SEND=false
SMS_SEND_ENABLED=false
OUTBOUND_MODE=draft_only
```

## المنتجات التجارية المعتمدة كبداية

| المنتج | الهدف | أول مخرج مدفوع |
|---|---|---|
| Revenue Command Room OS | ضبط الإيراد والمتابعة | تقرير فرص + قائمة متابعة + dashboard |
| Company Brain OS | قرار إداري يومي | daily decision + future radar |
| WhatsApp / Inbox Follow-up OS | إنقاذ المتابعات الضائعة | follow-up queue + ردود مراجعة |
| AI Trust & Compliance OS | تشغيل AI بشكل آمن | policy + approval gates + data handling SOP |
| Client Delivery OS | تسليم العميل باحتراف | intake + scope + proof pack |

## روتين المؤسس اليومي

```bash
make commercial-day
```

الناتج المتوقع:

- `reports/commercial/latest.md`
- `reports/commercial/latest.json`
- قائمة أولويات اليوم
- رسائل draft-only
- ملاحظات جاهزية الإنتاج
- مخاطر قبل الإرسال

## Definition of Done

لا يعتبر Dealix جاهزًا تجاريًا إلا إذا تحققت الشروط التالية:

- يوجد عرض واضح لكل منتج.
- يوجد follow-up sequence قابل للمراجعة.
- يوجد opt-out في أمثلة البريد.
- يوجد منع صريح للـfake ROI والـfake testimonials.
- يوجد source_url وverification_status لأي target.
- يوجد owner_decision قبل الإرسال.
- يوجد proof pack لكل عميل.
- لا يوجد live outbound افتراضيًا.

## طريقة البيع الأولى

ابدأ بـDiagnostic أو 7-Day Sprint، وليس SaaS عام.

العرض الأول المقترح:

> خلال 7 أيام نبني لك Revenue Command Room يوضح الفرص الساخنة، المتابعات المتأخرة، العروض التي تحتاج دفع، وأول 10 next actions للإدارة.

## ما لا نبيعه الآن

- لا نبيع وعود دخل مضمونة.
- لا نبيع إرسال واتساب عشوائي.
- لا نبيع CRM كامل من الصفر قبل proof.
- لا نبيع SaaS عام قبل 3–5 عملاء تجريبيين.

## التشغيل على Railway

الإنتاج يبقى على Railway مع `DATABASE_URL` من Postgres reference، و`/healthz` كمؤشر حياة. إرسال live لا يفتح إلا لاحقًا كـControlled Live Outbound PR منفصل.
