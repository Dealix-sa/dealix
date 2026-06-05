# Outreach Draft Lab — مختبر الدرافتات

> يبنيها: [`scripts/targeting_draft_lab.py`](../../scripts/targeting_draft_lab.py) ·
> الحوكمة: [Outreach Approval Policy](../03_governance/OUTREACH_APPROVAL_POLICY.md)

## القاعدة

النظام يُنتج **مسودات فقط** (`draft_status = needs_approval`). **لا يرسل أبدًا.**
كل مسودة: واضحة · مبنية على evidence · بدون ادعاء · بدون ضغط · فيها مخرج محدد ·
فيها **CTA واحد**.

## شروط التأهل (gate)

`eligible_for_draft()` يسمح بالمسودة فقط إذا:
- الدرجة A أو A+، و
- `targeting_score ≥ 80`، و
- `evidence_count ≥ 2`، و
- لم تُرفض من بوابة الامتثال.

## قالب الرسالة

```
السلام عليكم [الاسم]،
راجعت حضور [الشركة] بشكل سريع، وواضح أن عندكم [إشارة إيجابية]،
ولاحظت فرصة لتحسين [نقطة ضعف محتملة] خصوصًا حول [الدليل/المتابعة/القرار].
أبني Dealix كنظام تشغيل أعمال AI للشركات السعودية.
نبدأ عادة بـ Command Sprint خلال 7 أيام يطلع:
- Revenue Map
- Proof Register
- Executive Command Brief
- Next Action Board
بدون إرسال تلقائي أو وعود مبالغ فيها — فقط تشخيص وتشغيل أولي قابل للمراجعة.
يناسبك أرسل لك Diagnostic مختصر؟
```

## العبارات الممنوعة (يفرضها `validate_draft`)

- «شفنا أن عندكم مشكلة أكيدة»
- «نضمن لكم مبيعات» / «نجيب لكم عملاء»
- «نرسل واتساب تلقائي»
- «استخدمنا بيانات داخلية»
- أي صيغة ضمان (guarantee / guaranteed)

أي مسودة تحتوي عبارة محظورة **لا تُكتب أصلًا** في `drafts_for_review.md`.

## Targeting Angles

| Angle | متى |
|---|---|
| Revenue leakage | ضعف المتابعة أو CTA |
| Proof gap | ضعف الأدلة |
| Command fog | كثرة الخدمات/التوسع |
| Delivery visibility | خدمات تنفيذية |
| Client memory | تعاملات طويلة |
| AI governance | استخدام AI أو بيانات حساسة |
| Partner channel | وكالات/استشارات |

كل شركة تحصل على **angle واحد واضح** مشتقّ من أقوى `pain_signal`، لا رسالة عامة.

## روابط

- [Targeting Scorecard](TARGETING_SCORECARD.md)
- [Founder Shortlist Rules](FOUNDER_SHORTLIST_RULES.md)
- اختبارات: [`tests/test_targeting_draft_lab.py`](../../tests/test_targeting_draft_lab.py)
