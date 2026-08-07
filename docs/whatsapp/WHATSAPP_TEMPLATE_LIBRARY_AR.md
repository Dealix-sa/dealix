# مكتبة القوالب — أربعة عشر قالبًا

قوالب رسائل واتساب لمحادثات **محكومة وبموافقة** — لا إرسال بارد إطلاقًا. المصدر: `data/whatsapp/templates.yaml` (يحمّلها `templates.py`). المتغيرات بصيغة `{name}`.

## قواعد النبرة

- عربي أولًا، نبرة أعمال سعودية.
- قصيرة وواضحة (≤ ٥ أسطر).
- بلا مبالغة، بلا وعود بأرقام.
- كل رقم معه مستوى دليل؛ الدفع والأسرار خارج الشات.

## القوالب

### 1. welcome — الترحيب والقائمة
```
أهلًا، أنا مساعد Dealix.
أقدر أساعدك في تشخيص المبيعات والمتابعة وتشغيل أول نظام داخل شركتك.
اختر الخطوة من القائمة.
```

### 2. assessment_start — بدء الفحص
```
تمام. بسأل أسئلة قصيرة وأقترح لك أفضل مسار.
الخطوة {step} من {total}.
```

### 3. assessment_result — نتيجة الفحص
```
جهّزت لك أفضل مسار بناءً على إجاباتك.
الجاهزية الكلية: {overall}/100.
التوصية: {offer_name_ar}.
أول خطوة: {next_action_ar}.
```

### 4. permission_request — طلب صلاحية
```
نحتاج صلاحية واحدة لإكمال الربط: {system}.
الغرض: {purpose_ar}. الخطورة: {risk}. المدة: {duration_days} يوم.
لا ترسل المفتاح هنا — أكمل عبر الرابط الآمن إن لزم.
```

### 5. missing_input — مدخل ناقص
```
ناقصنا مدخل بسيط لإكمال الخطوة: {input_ar}.
لأمان البيانات، ارفعه من الرابط الآمن.
```

### 6. draft_ready — مسودة جاهزة
```
جاهز Draft للمراجعة قبل أي إرسال:
«{draft_ar}»
اعتمد / عدّل / ارفض.
```

### 7. followup_due — متابعة مستحقة
```
تذكير: متابعة مستحقة مع {lead_ar}.
جهّزت لك مسودة — تحتاج موافقتك قبل الإرسال.
```

### 8. proposal_ready — عرض جاهز
```
جهّزت لك عرضًا مبدئيًا: {offer_name_ar}.
النطاق والسعر واضحان في الكرت — راجع واعتمد أو احجز مكالمة.
```

### 9. proof_pack_ready — حزمة إثبات جاهزة
```
جاهز Proof Pack: {proof_title_ar}.
كل رقم معه مستوى دليل — بدون مبالغة.
```

### 10. payment_handoff_ready — جاهز للدفع الآمن
```
جاهز للدفع الآمن: {offer_name_ar}.
الدفع يتم عبر رابط آمن خارج الشات، بعد موافقتك.
```

### 11. onboarding_start — بدء الإعداد
```
أهلًا بك كعميل Dealix.
نبدأ بإعداد بسيط: الصلاحيات، الملفات المطلوبة، ثم أول workflow.
```

### 12. weekly_report — التقرير الأسبوعي
```
تقريرك الأسبوعي جاهز: {period_ar}.
أهم تحسّن: {improvement_ar}. الخطوة القادمة: {next_ar}.
```

### 13. renewal_offer — عرض التجديد
```
اكتملت قيمة هذا الشهر.
أقترح الاستمرار/التوسعة بناءً على النتائج — بدون أي التزام تلقائي.
```

### 14. support_escalation — تصعيد الدعم
```
وصلت طلبك للدعم.
صنّفت المشكلة، وإذا تبغى نصعّدها لشخص الآن أخبرني.
```

## جدول الأغراض والمتغيرات

| المفتاح | الغرض | المتغيرات |
|---|---|---|
| welcome | الترحيب وفتح القائمة | — |
| assessment_start | بدء/تقدّم الفحص | step, total |
| assessment_result | عرض نتيجة الفحص والتوصية | overall, offer_name_ar, next_action_ar |
| permission_request | طلب صلاحية واحدة | system, purpose_ar, risk, duration_days |
| missing_input | طلب مدخل ناقص عبر مسار آمن | input_ar |
| draft_ready | مراجعة مسودة قبل الإرسال | draft_ar |
| followup_due | تذكير متابعة بموافقة | lead_ar |
| proposal_ready | عرض مبدئي بنطاق وسعر | offer_name_ar |
| proof_pack_ready | حزمة إثبات بمستوى دليل | proof_title_ar |
| payment_handoff_ready | دفع آمن خارج الشات | offer_name_ar |
| onboarding_start | بدء الإعداد بعد البيع | — |
| weekly_report | الموجز الأسبوعي | period_ar, improvement_ar, next_ar |
| renewal_offer | اقتراح تجديد بلا التزام تلقائي | — |
| support_escalation | استقبال طلب دعم وعرض التصعيد | — |

> العرض (rendering) آمن: المتغيرات الناقصة تبقى كما هي بلا تعطّل. نقطة `GET /templates` تُرجع المفاتيح المتاحة والمفاتيح المعيارية.

## روابط

- سياسة المحادثة: [WHATSAPP_CONVERSATION_POLICY_AR.md](WHATSAPP_CONVERSATION_POLICY_AR.md)
- كروت الموافقة: [WHATSAPP_APPROVAL_CARDS_AR.md](WHATSAPP_APPROVAL_CARDS_AR.md)
- الأمان والخصوصية: [WHATSAPP_SECURITY_PRIVACY_AR.md](WHATSAPP_SECURITY_PRIVACY_AR.md)
- النظرة الشاملة: [WHATSAPP_CLIENT_OS_AR.md](WHATSAPP_CLIENT_OS_AR.md)
