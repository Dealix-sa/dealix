# برنامج الإحالة — Referral Program

**جزء من:** Dealix Market Production OS — انظر docs/market_os/MARKET_PRODUCTION_OS_AR.md
**المالك:** المؤسس (سامي) + عمليات الشركاء
**يبني على:** docs/partnerships/PARTNER_CHANNEL_OS_AR.md · docs/partners/PARTNER_PROGRAM.md · docs/partners/PARTNER_PACKAGES.md
**قواعد التشغيل:** dealix/config/partner_rules.yaml · التتبّع عبر schemas/ (بيانات التشغيل في data/partners/ runtime)
**آخر تحديث:** 2026-06-02

---

## الغرض

آلية إحالة **بسيطة وعادلة** تكافئ الشريك على فتح علاقة عميل حقيقية، بحوكمة واضحة وبلا ضمانات. هذا أبسط نقاط الدخول للشريك (يطابق مبدأ docs/partners/PARTNER_PROGRAM.md: «ابدأ مرناً، هدف أوّلي إحالة واحدة»).

## كيف تعمل الإحالة

1. الشريك يقدّم عميلاً حقيقياً يعرفه — لا قوائم مشتراة، لا أسماء مسحوبة آلياً.
2. تُفتح إحالة بصفّ في reports/partnerships/PARTNER_PIPELINE.md مع مصدر العلاقة.
3. العميل يدخل عبر التشخيص المجاني (0) ثمّ السلّم المعتمد.
4. عند أول دفعة مؤكَّدة (`payment_confirmed`)، يُحتسب رسم الإحالة.

## الاقتسام العادل

| الحالة | الرسم (مثال تشغيلي) |
|--------|----------------------|
| إحالة دون تنفيذ | نسبة من أول دفعة (10–20% حسب الاتفاق) |
| إحالة + تنفيذ | الشريك يحتفظ بأتعاب التنفيذ + رسم الإحالة |
| علاقة مستمرّة | اقتسام إيراد من MRR ما دام العميل نشطاً |

> النسب التفصيلية للباقات في docs/partners/PARTNER_PACKAGES.md. لا تُحتسب أي عمولة قبل `payment_confirmed`.

## الموافقة والحوكمة

- كل تواصل خارجي نيابةً عن العميل يتطلّب **موافقة المؤسس** — لا إرسال آلي.
- واتساب فقط **بعد ردّ إيجابي أو موافقة صريحة**، 1:1 (انظر docs/whatsapp/WHATSAPP_POST_REPLY_FLOW_AR.md).
- مصدر كل عميل مُوثَّق؛ لا بيانات شخصية حسّاسة في السجل.

## التتبّع (Schemas + Runtime)

- بنية السجل تتبع schemas/ (حقول قصيرة: معرّف الشريك، معرّف العميل، نوع الإحالة، الحالة، الرسم، تاريخ التأكيد).
- بيانات التشغيل الحيّة تُخزَّن في data/partners/ runtime — تُملأ عند تفعيل أول إحالة فعلية، لا قبل ذلك.

## بلا ضمانات

- لا «نضمن» عدد leads أو إيراداً للشريك؛ الرسم يُحتسب على **دفعات مؤكَّدة فقط**.
- الفرص مُثبتة بأدلة، والنتائج تقديرية لا موعودة.

## الخطوة التالية

عرّف الشريك على هذا البرنامج عبر docs/partners/PARTNER_OUTREACH_MESSAGES.md، وافتح أول إحالة في reports/partnerships/PARTNER_PIPELINE.md بهدف «دفعة مؤكَّدة واحدة».

## English summary

A simple, fair referral mechanic — the easiest entry point for a partner, matching the program principle of starting flexible toward one referral. The partner introduces a real customer they know (no purchased lists, no auto-scraped names); a row opens in reports/partnerships/PARTNER_PIPELINE.md with the relationship source; the customer enters via the free diagnostic (0) and the canonical ladder; the referral fee is computed only on the first `payment_confirmed`. Splits: referral without delivery (10–20% of the first payment), referral plus delivery (partner keeps implementation fees plus the referral fee), and ongoing relationship (revenue share on active MRR). Package percentages live in docs/partners/PARTNER_PACKAGES.md. Governance: founder approval for any external send, WhatsApp only after a positive reply or explicit consent, documented source per customer. No guarantees — fees accrue on confirmed payments only; opportunities are evidenced, results are estimated. Record structure follows schemas/; live runtime data lives in data/partners/ and is populated only when a real referral activates.

---

القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
