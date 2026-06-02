# خط أنابيب الشركاء — Partner Pipeline

**جزء من:** Dealix Market Production OS — انظر docs/market_os/MARKET_PRODUCTION_OS_AR.md
**النوع:** قالب تشغيلي — صفوف نموذجية (placeholder) تُستبدل بشركاء حقيقيين.
**المالك:** المؤسس (سامي) + عمليات الشركاء
**يقرأ القواعد من:** docs/partnerships/PARTNER_CHANNEL_OS_AR.md · docs/partnerships/REFERRAL_PROGRAM_AR.md · docs/partners/PARTNER_PACKAGES.md
**التشغيل:** schemas/ (بنية الحقول) · data/partners/ runtime (البيانات الحيّة)
**آخر تحديث:** 2026-06-02

---

## كيف يُستخدم

- صفّ واحد لكل شريك أو إحالة نشطة.
- ابدأ مرناً: الهدف الأوّلي **إحالة واحدة أو pilot واحد** قبل التعميق.
- المراحل: تواصل أوّلي → اجتماع → إحالة → تشخيص → عرض → مدفوع → تعميق.
- لا تُحتسب أي عمولة قبل `payment_confirmed`.

## جدول الـ Pipeline (صفوف نموذجية)

| الشريك | النوع | المرحلة | leads متوقَّعة | الاقتسام | الخطوة التالية |
|--------|-------|---------|----------------|----------|-----------------|
| [الشريك 1] | وكالة تسويق | تواصل أوّلي | [تقديري] | رسم إحالة 10–20% | حجز اجتماع 15 دقيقة |
| [الشريك 2] | مكتب محاسبة | إحالة | [تقديري] | اقتسام إيراد | تشخيص مجاني للعميل المُحال |
| [الشريك 3] | منفّذ CRM | عرض | [تقديري] | هامش تنفيذ | إرسال نطاق Data-to-Revenue Pack |

> هذه صفوف توضيحية فقط. استبدلها بشركاء حقيقيين. الأرقام «المتوقَّعة» تقديرية لا موعودة.

## ملاحظات الحوكمة

- لا أسماء عملاء بدون مصدر مُوثَّق؛ لا بيانات شخصية حسّاسة في الجدول.
- أي تواصل خارجي نيابةً عن العميل يتطلّب موافقة المؤسس.
- البيانات الحيّة تُدار في data/partners/ runtime وفق بنية schemas/.

## الخطوة التالية

افتح صفّاً واحداً لأقرب شريك واقعي، حدّد نموذج الاقتسام من docs/partnerships/PARTNER_CHANNEL_OS_AR.md، وحدّث المرحلة أسبوعياً.

## English summary

A template tracker for the partner channel. One row per active partner or referral, starting flexible toward a first goal of one referral or pilot. Columns: partner, type, stage, expected leads (estimated, never promised), split, next step. Rows are illustrative placeholders to be replaced by real partners. Stages run Initial Contact → Meeting → Referral → Diagnostic → Proposal → Paid → Deepen. No commission accrues before `payment_confirmed`. Governance: no customer names without a documented source, no sensitive personal data in the table, founder approval for any external send on a customer's behalf. Live data is managed in data/partners/ runtime following the field structure in schemas/.

---

القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
