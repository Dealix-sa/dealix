# برنامج الإحالات — Referral Program
## كيف تُسجَّل الإحالة وتُتتبَّع وتُصرف

**وحدات الكود:** `auto_client_acquisition/partnership_os/referral_store.py` · `referral_tracker.py`
**نظام القنوات:** [`docs/partnerships/PARTNER_CHANNEL_OS_AR.md`](./PARTNER_CHANNEL_OS_AR.md)
**مرجع نظام الإحالات:** [`docs/partner_os/PARTNER_REFERRAL_SYSTEM_AR.md`](../partner_os/PARTNER_REFERRAL_SYSTEM_AR.md)
**خط أنابيب الشراكات:** [`reports/partnerships/PARTNER_PIPELINE.md`](../../reports/partnerships/PARTNER_PIPELINE.md)

---

## 1 — كيف تُسجَّل الإحالة

### الخطوة 1: إنشاء كود الإحالة

عند تفعيل الشريك، يُنشأ كود إحالة فريد:

```
referral_store.create_referral_code(
    referrer_id = "<partner_id>",
    plan_required = "managed_revenue_ops_starter",
    credit_sar = <قيمة حسب الاتفاق>,
    valid_until = "<تاريخ انتهاء الصلاحية>"
)
```

الكود يأخذ الصيغة: `REF-XXXXXXXX`. يُرسَل للشريك مرة واحدة عند التفعيل.

### الخطوة 2: استخدام الكود

عندما يتواصل العميل المُحال مع Dealix، يُدخل الكود أو يذكره الشريك عند تسجيل الإحالة:

```
referral_store.redeem_referral(
    code = "REF-XXXXXXXX",
    referred_id = "<customer_id>"
)
```

هذا يُنشئ سجل `Referral` بحالة `redeemed`.

### الخطوة 3: ربط الدفعة

عند دفع فاتورة العميل المُحال:

```
referral_store.mark_invoice_paid(
    referral_id = "<referral_id>",
    invoice_id = "<invoice_id>",
    amount_sar = <المبلغ>
)
```

### الخطوة 4: إصدار الرصيد للشريك

بعد تأكيد الدفعة، يُصدر المؤسس رصيد الشريك:

```
referral_store.issue_credit(
    referral_id = "<referral_id>",
    credit_sar = <المبلغ المتفق عليه>
)
```

لا يُصدر أي رصيد دون موافقة المؤسس. هذه الخطوة دائماً يدوية.

---

## 2 — نافذة الإسناد

| الحدث | المدة القياسية |
|---|---|
| من استخدام الكود إلى أول دفعة | 90 يوماً |
| انتهاء صلاحية الكود (إن لم يُستخدم) | يُحدَّد عند الإنشاء — 180 يوماً افتراضياً |

إذا دفع العميل بعد انتهاء النافذة، يُراجَع الأمر يدوياً ويُقرّر المؤسس.

---

## 3 — جدول الرسوم

| نموذج الشراكة | قاعدة الرسوم | النطاق التوجيهي |
|---|---|---|
| إحالة فقط | نسبة من قيمة أول سبرنت أو اشتراك مدفوع | 10–20% |
| إحالة + اشتراك شهري | استمرار النسبة على الاشتراكات الناتجة | بحسب الاتفاق |
| تسليم مشترك | هامش تنفيذ؛ لا رسوم إحالة إضافية | الشريك يُسعّر بحرية |

**القواعد الصارمة:**
- لا رسوم إحالة على صفقات طوّرها Dealix باستقلالية دون جهد الشريك.
- لا رسوم على إحالات ذاتية (الشريك لا يُحيل نفسه — `self-referral` مرفوض تقنياً).
- كل صرف يستلزم موافقة المؤسس الموثّقة — لا صرف تلقائي.

---

## 4 — قواعد مكافحة الإزعاج (No-Spam Rule)

الشريك الذي يستخدم أي من الأساليب التالية يفقد كوده ويُعلَّق حسابه:

- الإرسال الجماعي لأرقام واتساب بحجة "إحالة Dealix".
- استخدام قوائم مشتراة أو مُجمَّعة لنشر كود الإحالة.
- إرسال رسائل باردة عبر أي قناة تذكر Dealix دون علاقة قائمة مع المستلم.
- أتمتة التوزيع على منصات التواصل الاجتماعي.

الإحالة الصحيحة: شريك يعرف العميل شخصياً ويُقدّمه بشكل مناسب.

---

## 5 — ما يجوز للشريك ادّعاؤه وما لا يجوز

### يجوز:
- "Dealix يُجري تشخيصاً إيرادياً مبنياً على بياناتك ويُنتج Proof Pack موثَّق."
- "النتائج تُصنَّف كفرص مُثبَتة بأدلة — ليست مبيعات مضمونة."
- "التشخيص يستغرق 7 أيام ويبدأ بسبرنت محدد السعر."

### لا يجوز:
- "Dealix يضمن زيادة مبيعاتك بنسبة X%."
- "النظام يعمل تلقائياً دون أي تدخل بشري."
- "Dealix يُرسل رسائل لعملائك نيابةً عنك دون الحاجة لمراجعتها."
- أي رقم إيرادي محدد لم يُقرّه المؤسس كتابياً.

---

## 6 — إدارة التعارض (Conflict Handling)

**حالة التعارض:** عميل محتمل يأتي من شريكين مختلفين في نفس الوقت.

**القاعدة:** أسبقية التسجيل — أول كود مُسجَّل صحيح هو المعتمَد (`redeem_referral` الأسبق). إذا جاءا في نفس اليوم، يُقرّر المؤسس يدوياً.

**حالة التجاوز:** شريك يزعم إحالة عميل لم يكن له دور فيها.
القاعدة: يتطلب المؤسس إثباتاً على الاتصال الفعلي (بريد إلكتروني أو اجتماع موثَّق). بدون إثبات، لا رسوم.

---

## English Mirror — Referral Program

**Registration flow:** partner receives a unique `REF-XXXXXXXX` code via `referral_store.create_referral_code()`. When a referred client engages, the code is redeemed via `referral_store.redeem_referral()`. Once the referred client's invoice is paid, the founder manually issues the partner credit via `referral_store.issue_credit()`.

**Attribution window:** 90 days from code redemption to first payment.

**Fee schedule (indicative, founder-approved per deal):**

| Model | Basis | Indicative Range |
|---|---|---|
| Referral only | First sprint or subscription payment | 10–20% |
| Referral + recurring | Continuation on resulting subscriptions | Per agreement |
| Co-delivery | Implementation margin, no additional referral fee | Partner prices independently |

**No-spam rule:** partners who use purchased lists, cold messaging, or broadcast distribution to spread referral codes lose their code and are suspended. A valid referral is a known contact introduced personally.

**What partners may not claim:** no guaranteed sales figures, no fully automated delivery, no sending messages to clients without review, no specific revenue numbers not approved in writing by the founder.

**Conflict resolution:** first registered code takes precedence. Same-day conflicts are resolved by founder decision. Disputed claims require documented evidence of actual contact.

---

القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
