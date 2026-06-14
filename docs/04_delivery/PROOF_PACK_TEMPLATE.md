# Proof Pack Template — حزمة الأدلة — The Evidence Bundle Structure

## ما هذه الوثيقة — What this is

الـ **Proof Pack** هي الغلاف النهائي لكل Sprint: الدليل المُجمَّع على ما استلمناه، حلّلناه، أنشأناه، واعتمده العميل. تعيش في `customers/{company}/10_proof_pack.md` وتُسلَّم كغلاف للحزمة الكاملة ([COMMAND_SPRINT_DELIVERY_OS](COMMAND_SPRINT_DELIVERY_OS.md)). هذه الوثيقة تعرّف أقسامها السبعة، مستويات الدليل (L1–L5)، وبوابة النشر.

> القاعدة العليا — The supreme rule: لا ادعاء بلا دليل. No proof, no claim. كل بند في الحزمة مربوط بمصدر ومستوى دليل مُصرَّح.

## الأقسام السبعة — The seven sections

كل Proof Pack تحوي هذه الأقسام بالترتيب. كل بند يحمل حقول القبول من [DELIVERY_ACCEPTANCE_CRITERIA](DELIVERY_ACCEPTANCE_CRITERIA.md).

```
# Proof Pack — {company}

## 1. What we received — ما استلمناه
- input: | source: | date: | (مصادر عامة أو ما شاركه العميل فقط — لا PII)

## 2. What we analyzed — ما حلّلناه
- analysis: | method: | source: | confidence:

## 3. What we created — ما أنشأناه
- artifact: | file: (يحيل إلى ملف في المجلّد) | proof_level: (L1–L5)

## 4. What the customer approved — ما اعتمده العميل
- item: | approved_by: | date: | (يحيل إلى 06_approval_register.md)

## 5. What became clearer — ما أصبح أوضح
- insight: | before: | after: | evidence:

## 6. What action should happen next — الإجراء التالي
- action: | owner: | due_date: | approval_required: | (يحيل إلى 07_next_action_board.md)

## 7. What can / cannot be published — ما يُنشَر وما لا يُنشَر
- publishable_without_name: yes/no
- client_name_publish: requires_written_approval
- approved_by: | date:
```

كل قسم يكون فارغًا فقط إذا صُرّح صراحةً بأنه «لا ينطبق» مع سبب. لا قسم مفقود بصمت.

## مستويات الدليل — Proof Levels (L1–L5)

كل أرتيفاكت في القسم 3 يحمل مستوى دليلًا واحدًا. المستوى يصف **مدى تحقّق الأثر**، لا جودة العمل.

| Level | المعنى — Meaning | الدليل المطلوب — Evidence required |
|---|---|---|
| **L1 — Created** | أُنشئ المُخرَج | الأرتيفاكت موجود في المجلّد |
| **L2 — Reviewed** | راجعه طرف مؤهَّل | توقيع/ملاحظة مراجعة داخلية أو من العميل |
| **L3 — Approved** | اعتمده صاحب القرار | قيد في `06_approval_register.md` |
| **L4 — Used** | استُخدم فعليًا في عمل العميل | إشارة استخدام موثّقة (لقطة، رسالة، قرار اتُّخذ) |
| **L5 — Measurable impact** | أثر قابل للقياس | رقم قبل/بعد بمصدر — تقديري حتى يتحقّق |

### قاعدة الزمن — The time rule

- **أول 30 يومًا — First 30 days:** L2/L3 كافٍ. الهدف إثبات أن العمل أُنشئ ورُوجِع واعتُمد. لا تطارد L5 مبكرًا.
- **بعد 90 يومًا — After 90 days:** طارد L4/L5. الهدف إثبات أن المُخرَج استُخدم وأنتج أثرًا قابلًا للقياس.

> L5 يبقى **تقديريًا** حتى يتحقّق برقم بمصدر. لا ضمان إيراد، لا نسبة تحويل كحقيقة — تقدير أو نمط case-safe فقط.

## بوابة النشر — The publish-permission gate

- لا اسم عميل يُنشَر بلا **موافقة مكتوبة** مسجَّلة في القسم 7 و`06_approval_register.md`.
- لا رقم سرّي للعميل يُنشَر. أنماط مُجمَّعة ومنهجية فقط.
- لا بيانات عميل تُستخدم في تدريب أي نموذج — No customer data used for model training.
- لا إجراء خارجي يواجه العميل دون موافقة المؤسس — No external customer-facing action without founder approval.

## حلقة الدليل-إلى-محتوى — The Proof-to-Content loop

عند الرغبة في تحويل تعلّم من Sprint إلى محتوى عام، استخدم **النسخة المجهّلة (anonymized-insight variant)**:

```
# Anonymized Insight — قطاع: {sector} — حجم: {band}
- pattern_observed:        # نمط مُجمَّع، لا حالة فردية
- why_it_matters:
- evidence_basis:          # منهجية مُجمَّعة، لا رقم عميل سرّي
- label: "Hypothetical / case-safe template"   # إن لم يُسمَّ عميل حقيقي
```

القاعدة: المحتوى يخرج من الدليل، لا من التمنّي. إن لم يُعتمد اسم العميل، فالحالة **مجهّلة ومُصنّفة case-safe** صراحةً. لا عميل وهمي — No fake customers.

## روابط مرجعية — Cross-links

- [COMMAND_SPRINT_DELIVERY_OS.md](COMMAND_SPRINT_DELIVERY_OS.md)
- [CUSTOMER_FOLDER_TEMPLATE.md](CUSTOMER_FOLDER_TEMPLATE.md)
- [DELIVERY_ACCEPTANCE_CRITERIA.md](DELIVERY_ACCEPTANCE_CRITERIA.md)
- [../07_proof_os/PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md)
- [../05_governance_os/APPROVAL_POLICY.md](../05_governance_os/APPROVAL_POLICY.md)

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
