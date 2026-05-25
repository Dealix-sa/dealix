# Dealix — Value Measurement — قياس القيمة

> Bilingual measurement model. Verified revenue vs estimated revenue is the cornerstone. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.

---

## العربية

### 1. مبدأ القياس
لا يقاس النجاح بالعدد الذي يُكتب على شريحة عرض، بل بـ **الدليل المربوط** بكل ريال يُنسب إلى الـ AI.

### 2. المؤشرات الأربعة
**(1) Verified Revenue (الإيراد المُتحقَّق)**
- التعريف: إيراد مرتبط بـ Evidence Pack بحقل `revenue_link.verified = true`.
- الحساب: مجموع `amount_sar` لكل حزمة سارية في الفترة.
- يُعرَض في تقرير المجلس **منفصلًا** عن التقديرات.

**(2) Founder Time Saved (وقت المؤسس المُوفَّر)**
- التعريف: عدد الساعات التي خُفّضت لقرارات حسّاسة عبر مسودّات + موافقات.
- الحساب: قياس قبل/بعد على مهام محدّدة.
- لا يُحوَّل إلى دولار/ريال بدون موافقة العميل.

**(3) Agent ROI**
- التعريف: لكل وكيل، (Verified Revenue المنسوب − تكلفة تشغيل الوكيل) ÷ تكلفة التشغيل.
- يُحسب شهريًا في تقرير الحوكمة.
- وكلاء T0 وT1 قد لا يكون لهم إيراد مُتحقَّق مباشر؛ يُقاسون بـ time saved.

**(4) Trust Incidents Avoided (حوادث ثقة مُحتواة)**
- التعريف: حالات أوقفها Tool Permission Matrix أو طبقة الموافقات قبل وقوع الضرر.
- الحساب: عدد محاولات `denied` + عدد الموافقات المرفوضة.
- يُعرَض كـ «حدود تشغيلية فعّالة»، لا كـ «ادّعاء أمن».

### 3. ما لا يُقاس
- معدّلات تحويل مضمونة.
- ROI مُسقَط بدون أدلة.
- «وقت موفَّر» بلا قياس قبل/بعد.

### 4. تقرير القيمة الشهري
- صفحة 1: Verified Revenue.
- صفحة 2: Estimated Pipeline (مفصول).
- صفحة 3: Founder Time Saved.
- صفحة 4: Agent ROI لكل وكيل.
- صفحة 5: Trust Incidents Avoided.
- ملحق: عيّنة Evidence Packs.

---

## English

### 1. Measurement Principle
Success is not measured by a slide number; it is measured by the **proof linked** to every riyal attributed to AI.

### 2. The Four Indicators
**(1) Verified Revenue**
- Definition: revenue tied to an Evidence Pack with `revenue_link.verified = true`.
- Calculation: sum of `amount_sar` for valid packs in the period.
- Shown in the board report **separated** from estimates.

**(2) Founder Time Saved**
- Definition: hours reduced on sensitive decisions via drafts plus approvals.
- Calculation: before/after measurement on defined tasks.
- Not converted to currency without customer consent.

**(3) Agent ROI**
- Definition: per agent, (verified revenue attributed − agent operating cost) ÷ operating cost.
- Computed monthly in the governance report.
- T0 and T1 agents may not produce direct verified revenue; measured by time saved.

**(4) Trust Incidents Avoided**
- Definition: cases that the Tool Permission Matrix or approval layer stopped before harm.
- Calculation: count of `denied` attempts plus count of rejected approvals.
- Reported as "effective operational boundaries", not as a "security claim".

### 3. What Is Not Measured
- Guaranteed conversion rates.
- Projected ROI without evidence.
- "Time saved" without before/after measurement.

### 4. Monthly Value Report
- Page 1: Verified Revenue.
- Page 2: Estimated Pipeline (separated).
- Page 3: Founder Time Saved.
- Page 4: Agent ROI per agent.
- Page 5: Trust Incidents Avoided.
- Appendix: Evidence Pack sample.

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
