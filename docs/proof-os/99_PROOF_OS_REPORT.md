# تقرير نظام أصول الإثبات | Proof OS Evidence Report

## الغرض | Purpose

**عربي:** تقرير الأدلة الذي يوثّق مكوّنات نظام أصول الإثبات وحالة تطبيقه، بما في ذلك القوالب المُولّدة آليًا والملفات المرجعية. يؤكّد التزام النظام بقواعد السلامة: الذكاء الاصطناعي يجهّز، المؤسّس يعتمد، والإجراء يدوي.

**English:** The evidence report documenting the Proof Asset OS components and implementation status, including auto-generated templates and reference files. It confirms adherence to safety rules: AI prepares, founder approves, manual action only.

---

## المكوّنات | Components

| المكوّن Component | المسار Path | الحالة Status |
|---|---|---|
| نظرة عامة Overview | `00_PROOF_ASSET_OS.md` | موثّق |
| قواعد بلا ادعاءات No-fake rules | `01_PROOF_WITHOUT_FAKE_CLAIMS.md` | موثّق |
| قالب دراسة الحالة Case template | `02_CASE_STYLE_TEMPLATE.md` | موثّق |
| قالب قبل/بعد Before/After | `03_BEFORE_AFTER_WORKFLOW_TEMPLATE.md` | موثّق |
| قواعد الإذن Permission | `04_CLIENT_PERMISSION_RULES.md` | موثّق |
| عملية الإخفاء Anonymization | `05_ANONYMIZED_PROOF_PROCESS.md` | موثّق |

---

## التوليد الآلي للقوالب | Template Generation

- السكربت: `scripts/proof_asset_template_generate.py`.
- المخرجات: `outputs/proof_assets/templates/`.
- الدور: يجهّز قوالب فارغة قابلة للتعبئة يدويًا.
- ملاحظة: السكربت **يجهّز** القوالب فقط؛ لا يرسل ولا ينشر أي شيء.

```
scripts/proof_asset_template_generate.py
  └── outputs/proof_assets/templates/
        ├── case_study_template.md
        └── before_after_template.md
```

---

## قائمة التحقق من الامتثال | Compliance Checklist

- [ ] لا مقاييس مفبركة في أي أصل.
- [ ] لا عائد مضمون أو ادعاءات غير مثبتة.
- [ ] لا أسرار أو مفاتيح API في المخرجات.
- [ ] كل أصل معتمد من المؤسّس.
- [ ] لا إرسال آلي خارجي (بريد/واتساب/لينكدإن).
- [ ] لا تجريف ولا إعلانات مدفوعة مباشرة.

---

## الخطوات التالية | Next Steps

- تشغيل سكربت توليد القوالب يدويًا عند الحاجة.
- مراجعة دورية للأصول المنشورة والتأكد من سريان الأذونات.

---

## قواعد السلامة | Safety Guardrails

الذكاء الاصطناعي يجهّز، المؤسّس يعتمد، الإجراء يدوي فقط، ولا إرسال خارجي.
