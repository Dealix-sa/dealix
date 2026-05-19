# Qualification Scorecard — بطاقة تقييم التأهيل

> The 8-question BANT scorecard. Fill it during or right after the discovery call. Source of truth: `auto_client_acquisition/sales_os/qualification.py`.

---

## القسم العربي

### كيف تستخدمها

لكل إشارة، ضع علامة "نعم" أو "لا". أضف الوزن إلى المجموع عند "نعم" فقط. المجموع الأقصى 100. ثم طبّق عتبات القرار.

### الإشارات الثماني

| # | الإشارة | الوزن | شكل "نعم" |
|---|---|---|---|
| 1 | pain_clear — وضوح الألم | 15 | العميل وصف تسرّباً محدداً وملموساً، لا شكوى عامة |
| 2 | owner_present — مالك حاضر | 15 | شخص مُسمّى سيملك سير العمل من جانب العميل |
| 3 | data_available — بيانات متاحة | 15 | توجد قائمة حسابات أو تصدير CRM قابل للعمل عليه |
| 4 | accepts_governance — قبول الحوكمة | 10 | العميل يقبل المسودات والاعتماد المسبق وسجل التدقيق |
| 5 | has_budget — وجود ميزانية | 10 | 499 ريال ضمن ما يستطيع العميل البدء به الآن |
| 6 | wants_safe_methods — طرق آمنة | 10 | العميل مرتاح للطرق الآمنة ولا يطلب كشطاً أو تواصلاً بارداً |
| 7 | proof_path_visible — مسار إثبات واضح | 15 | يوجد من سيستخدم المخرجات فعلياً، فيُمكن إثبات القيمة |
| 8 | retainer_path_visible — مسار احتفاظ | 10 | العميل يتصوّر تكرار العمل شهرياً |

**المجموع: ____ / 100**

### عتبات القرار

| المجموع | القرار | الإجراء |
|---|---|---|
| ≥ 85 | ACCEPT | بيع سبرنت ذكاء الإيرادات (499 ريال) |
| 70–84 | REFRAME / DIAGNOSTIC | خطوة أولى أصغر أو إعادة تأطير النطاق |
| 45–69 | DIAGNOSTIC_ONLY | تشخيص مجاني فقط، لا سبرنت بعد |
| < 45 | REFER_OUT | إحالة العميل بأدب لجهة أنسب |

### قاعدة الرفض الدوكتريني (تتجاوز النتيجة)

أي انتهاك للدوكترين يفرض **REJECT تلقائياً بغضّ النظر عن المجموع**:

- طلب واتساب بارد أو رسائل واتساب بالجملة.
- طلب مبيعات مضمونة أو نتائج مضمونة.
- طلب كشط بيانات (scraping).
- طلب أتمتة LinkedIn.
- رفض الطرق الآمنة.

عند أي من هذه: لا تُكمل التقييم — اعتذر بأدب وأنهِ التواصل، وسجّل السبب في المتتبّع.

### حقل التعبئة

```
المشروع / العميل: ________________
التاريخ: ________________
1 pain_clear (15):           نعم / لا   = ____
2 owner_present (15):        نعم / لا   = ____
3 data_available (15):       نعم / لا   = ____
4 accepts_governance (10):   نعم / لا   = ____
5 has_budget (10):           نعم / لا   = ____
6 wants_safe_methods (10):   نعم / لا   = ____
7 proof_path_visible (15):   نعم / لا   = ____
8 retainer_path_visible (10):نعم / لا   = ____
المجموع: ____ / 100
انتهاك دوكتريني؟  نعم / لا   (إذا نعم → REJECT)
القرار النهائي: ________________
```

---

## English Section

### How to use it

For each signal, mark "yes" or "no". Add the weight to the total only on "yes". The maximum total is 100. Then apply the decision thresholds.

### The 8 signals

| # | Signal | Weight | What a "yes" looks like |
|---|---|---|---|
| 1 | pain_clear | 15 | The customer described a specific, concrete leak, not a vague complaint |
| 2 | owner_present | 15 | A named person will own the workflow on the customer side |
| 3 | data_available | 15 | An account list or CRM export exists and can be worked on |
| 4 | accepts_governance | 10 | The customer accepts drafts, pre-approval, and an audit trail |
| 5 | has_budget | 10 | 499 SAR is within what the customer can start with now |
| 6 | wants_safe_methods | 10 | The customer is comfortable with safe methods and asks for no scraping or cold outreach |
| 7 | proof_path_visible | 15 | Someone will actually use the outputs, so value can be proven |
| 8 | retainer_path_visible | 10 | The customer can picture repeating the work monthly |

**Total: ____ / 100**

### Decision thresholds

| Total | Decision | Action |
|---|---|---|
| ≥ 85 | ACCEPT | Sell the Revenue Intelligence Sprint (499 SAR) |
| 70-84 | REFRAME / DIAGNOSTIC | Smaller first step or reframe the scope |
| 45-69 | DIAGNOSTIC_ONLY | Free diagnostic only, no Sprint yet |
| < 45 | REFER_OUT | Refer the customer out politely |

### Doctrine auto-reject rule (overrides the score)

Any doctrine violation forces an **automatic REJECT regardless of the total**:

- Asking for cold WhatsApp or bulk WhatsApp messaging.
- Asking for guaranteed sales or guaranteed results.
- Asking for scraping.
- Asking for LinkedIn automation.
- Refusing safe methods.

On any of these: do not finish scoring — decline politely, end the engagement, and log the reason in the tracker.

### Fill-in field

```
Engagement / Customer: ________________
Date: ________________
1 pain_clear (15):            yes / no   = ____
2 owner_present (15):         yes / no   = ____
3 data_available (15):        yes / no   = ____
4 accepts_governance (10):    yes / no   = ____
5 has_budget (10):            yes / no   = ____
6 wants_safe_methods (10):    yes / no   = ____
7 proof_path_visible (15):    yes / no   = ____
8 retainer_path_visible (10): yes / no   = ____
Total: ____ / 100
Doctrine violation?  yes / no   (if yes -> REJECT)
Final decision: ________________
```

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
