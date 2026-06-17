# Customer Folder Template — مجلّد العميل القياسي — The Canonical Delivery Folder

## ما هذه الوثيقة — What this is

كل عميل مدفوع يحصل على **مجلّد تسليم واحد**. لا ملفات متناثرة، لا رسائل، لا مرفقات ضائعة. المجلّد هو مصدر الحقيقة الوحيد لكل Sprint. هذه الوثيقة تعرّف الشجرة الكاملة وملفًا لكل يوم من أيام الـ [Command Sprint Delivery OS](COMMAND_SPRINT_DELIVERY_OS.md).

بذرة جاهزة (real example seed) محفوظة تحت `customers/_TEMPLATE/`. ابدأ كل Sprint بنسخها:
`cp -r customers/_TEMPLATE customers/{company}` ثم عبّئ الملفات بالترتيب.

> القاعدة — The rule: كل ملف يحمل حقول القبول من [DELIVERY_ACCEPTANCE_CRITERIA](DELIVERY_ACCEPTANCE_CRITERIA.md). لا ملف "جاهز" قبل اكتمال حقوله.

## الشجرة الكاملة — The exact tree

```
customers/
└── {company}/
    ├── 00_intake.md                  # الاستلام — intake form responses
    ├── 01_company_intelligence.md    # ذكاء الشركة — company intelligence brief
    ├── 02_diagnostic_summary.md      # ملخّص التشخيص — diagnostic summary
    ├── 03_command_sprint_scope.md    # نطاق الـ Sprint — scope of work
    ├── 04_revenue_map.md             # خريطة الإيراد — revenue map
    ├── 05_proof_register.md          # سجلّ الأدلة — proof register
    ├── 06_approval_register.md       # سجلّ الموافقات — approval register
    ├── 07_next_action_board.md       # لوحة الإجراءات — next action board
    ├── 08_executive_command_brief.md # موجز القرار — executive command brief
    ├── 09_delivery_log.md            # سجلّ التسليم — delivery log
    ├── 10_proof_pack.md              # حزمة الأدلة — proof pack
    └── 11_upsell_recommendation.md   # توصية التوسّع — upsell recommendation
```

البذرة `customers/_TEMPLATE/` تحتوي نفس الشجرة بملفات هياكل فارغة جاهزة للتعبئة.

---

## 00_intake.md
**الغرض — Purpose:** التقاط ما قاله العميل وما دفع مقابله. نقطة الصفر.
```
# Intake — {company}
- company: 
- sector: 
- contact_role:            # دور صاحب القرار، لا اسم/PII
- paid_tier:               # Proof Deposit / Standard
- stated_problem: 
- data_shared:             # مصادر عامة فقط
- scope_confirmed_by:      # المؤسس
- date: 
```

## 01_company_intelligence.md
**الغرض:** من هي الشركة، السوق، المنافسون، نقاط الضعف التشغيلية — كل سطر بمصدر.
```
# Company Intelligence — {company}
## Market — السوق
- finding: | source: | confidence:
## Competitors — المنافسون
- finding: | source: | confidence:
## Operational gaps — نقاط الضعف
- finding: | source: | assumption: | confidence:
```

## 02_diagnostic_summary.md
**الغرض:** التشخيص التشغيلي — أين الفوضى، ما الذي يُعطّل القرار.
```
# Diagnostic Summary — {company}
## Top diagnoses — أهم 3 تشخيصات
1. observation: | source: | confidence: | impact:
## What this is costing — الكلفة التقديرية
- estimate: (تقديري) | basis:
```

## 03_command_sprint_scope.md
**الغرض:** ما هو داخل النطاق وما ليس فيه. يمنع توسّع النطاق.
```
# Sprint Scope — {company}
## In scope — داخل النطاق
- 
## Out of scope — خارج النطاق
- لا إرسال خارجي · لا واتساب جماعي · لا scraping خلف تسجيل دخول
## Approved by — اعتمدها: | date:
```

## 04_revenue_map.md
**الغرض:** أين يتسرّب الإيراد، أين الفرص المُثبتة بأدلة، الأولوية بالأثر.
```
# Revenue Map — {company}
## Leaks — مواضع التسرّب
- leak: | source: | confidence:
## Evidenced opportunities — فرص مُثبتة بأدلة
- opportunity: | evidence: | est_impact: (تقديري) | priority:
```

## 05_proof_register.md
**الغرض:** كل ادعاء قُدّم للعميل مربوط بدليل ومستوى Proof. انظر [PROOF_PACK_TEMPLATE](PROOF_PACK_TEMPLATE.md).
```
# Proof Register — {company}
| claim | source/evidence | proof_level (L1–L5) | publishable? |
|---|---|---|---|
```

## 06_approval_register.md
**الغرض:** كل إجراء خارجي أو قرار حسّاس — مَن وافق ومتى.
```
# Approval Register — {company}
| item | approval_required | approved_by | date | status |
|---|---|---|---|---|
# لا إجراء خارجي يواجه العميل دون موافقة المؤسس
```

## 07_next_action_board.md
**الغرض:** 3 إجراءات تالية مرتّبة بالأثر، لكل واحد مالك ومُهلة.
```
# Next Action Board — {company}
| # | action | impact | owner | due_date | approval_required |
|---|---|---|---|---|---|
| 1 |  |  |  |  |  |
```

## 08_executive_command_brief.md
**الغرض:** صفحة قرار واحدة لصاحب القرار. تُقرأ في 20 دقيقة.
```
# Executive Command Brief — {company}
## Situation — الوضع
## Options — الخيارات
## Recommendation — التوصية (واحدة)
## Evidence — يحيل إلى Proof Register
```

## 09_delivery_log.md
**الغرض:** سجلّ ما حدث كل يوم، الوقت المصروف، أي انحراف عن الـ SLA.
```
# Delivery Log — {company}
| day | artifact | hours_spent | sla_deviation | notes |
|---|---|---|---|---|
# هدف الإجمالي: 6–10 ساعات
```

## 10_proof_pack.md
**الغرض:** الغلاف النهائي للأدلة المُسلَّمة للعميل. الهيكل الكامل في [PROOF_PACK_TEMPLATE](PROOF_PACK_TEMPLATE.md).
```
# Proof Pack — {company}
(الأقسام السبعة: received / analyzed / created / approved / clearer / next / publishable)
```

## 11_upsell_recommendation.md
**الغرض:** توصية واحدة موثّقة لما بعد الـ Sprint، مربوطة بفجوة في Revenue Map.
```
# Upsell Recommendation — {company}
- recommended_next: 
- tied_to_gap:            # يحيل إلى 04_revenue_map.md
- evidence: 
- est_value: (تقديري) 
- approval_required: 
```

## روابط مرجعية — Cross-links

- [COMMAND_SPRINT_DELIVERY_OS.md](COMMAND_SPRINT_DELIVERY_OS.md)
- [PROOF_PACK_TEMPLATE.md](PROOF_PACK_TEMPLATE.md)
- [DELIVERY_ACCEPTANCE_CRITERIA.md](DELIVERY_ACCEPTANCE_CRITERIA.md)
- [../05_governance_os/APPROVAL_POLICY.md](../05_governance_os/APPROVAL_POLICY.md)

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
