# Dealix — Trust Case Study Template — نموذج دراسة حالة ثقة

> Hypothetical / case-safe template. Focus is on the trust layer, not revenue. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.

---

## العربية

### السياق
- البيئة: `{{ environment }}` (إنتاج، تجريبي).
- نوع المخاطرة المعالَجة: `{{ risk_type }}` (PII، إرسال خارجي، MCP خارجي).
- وكلاء معنيون: `{{ agents }}`.

### القبل (Before)
- الفجوة المُعرَّفة: ماذا كان قابلًا للوقوع.
- الإشارة التي رصدت الفجوة: AI Run Ledger، شكوى، تدقيق DPO.
- مستوى الحدّة المُتوقَّع: S1 / S2 / S3 / S4.

### الفعل (Action)
- إجراء Tool Permission Matrix الذي طُبِّق.
- موافقات إضافية اشتُرطت.
- مراجعة MCP (إن وُجد).
- مكوّن AI Use Policy المُحدَّث.

### المخرَج (Output)
- الحدث قبل أن يخرج: نعم/لا.
- Evidence Pack الحادث: `{{ ep_id }}`.
- تحديثات Agent Registry: `{{ list }}`.
- تحديثات Tool Permission Matrix: `{{ list }}`.

### النتيجة (Outcome) — case-safe
- Trust Incidents Avoided: 1 (هذه الحالة).
- زمن الاستجابة: من اكتشاف إلى احتواء.
- لا تسرّب PII، لا إرسال خارجي، لا ضرر سمعة.

### الدرس (Learning)
- جذر السبب الحقيقي (وليس «خطأ بشري»).
- ثغرة سياسة (إن وُجدت).
- ما الذي سيمنع تكرار الحالة؟

### التالي (Next)
- تحديث سياسة موصى به.
- تمرين Tabletop التالي يستهدف هذه الفئة.
- نشر دراسة الحالة داخليًا/خارجيًا.

### ملاحظة نشر
- لا تُذكر أسماء وكلاء حقيقيون لعملاء.
- لا أرقام PII.
- يُذكر الفئة والقطاع فقط بإذن.

---

## English

### Context
- Environment: `{{ environment }}` (prod, sandbox).
- Risk type handled: `{{ risk_type }}` (PII, external send, foreign MCP).
- Agents involved: `{{ agents }}`.

### Before
- Identified gap: what could have happened.
- Signal that surfaced the gap: AI Run Ledger, complaint, DPO audit.
- Expected severity: S1 / S2 / S3 / S4.

### Action
- Tool Permission Matrix action applied.
- Extra approvals required.
- MCP review (if any).
- AI Use Policy component updated.

### Output
- Was the event contained before it left: yes/no.
- Incident Evidence Pack: `{{ ep_id }}`.
- Agent Registry updates: `{{ list }}`.
- Tool Permission Matrix updates: `{{ list }}`.

### Outcome — case-safe
- Trust Incidents Avoided: 1 (this case).
- Response time: detection to containment.
- No PII leak, no external send, no reputational harm.

### Learning
- True root cause (not "human error").
- Policy gap (if any).
- What prevents recurrence?

### Next
- Recommended policy update.
- Next tabletop targets this class.
- Internal/external publication of the case.

### Publication Note
- No real customer agent names.
- No PII figures.
- Class and sector mentioned only with consent.

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
