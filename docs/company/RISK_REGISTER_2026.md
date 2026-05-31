# سجل المخاطر 2026 — Dealix # Risk Register 2026 — Dealix

> يُراجَع هذا السجل شهرياً — آخر مراجعة: 2026-05-31
> This register is reviewed monthly — last reviewed: 2026-05-31

**الغرض / Purpose:** توثيق مركزي للمخاطر التشغيلية والاستراتيجية لعام 2026 مع استراتيجية التخفيف والمالك والحالة. هذا المستند مكمّل للملخص التنفيذي في [`RISK_REGISTER.md`](RISK_REGISTER.md).

Central documentation of operational and strategic risks for 2026 with mitigation strategy, owner, and status. This document extends the executive summary in [`RISK_REGISTER.md`](RISK_REGISTER.md).

**مقياس الدرجات / Scoring Scale:**

| الاحتمالية / Probability | التأثير / Impact | الدرجة / Score |
|--------------------------|-----------------|---------------|
| عالية × عالية / High × High | — | 9 |
| عالية × متوسطة / High × Medium | — | 6 |
| متوسطة × عالية / Medium × High | — | 6 |
| متوسطة × متوسطة / Medium × Medium | — | 4 |
| منخفضة × عالية / Low × High | — | 3 |
| منخفضة × متوسطة / Low × Medium | — | 2 |

---

## R01 — الاعتماد على المؤسس / Founder Dependency

**نقطة فشل واحدة / Single Point of Failure**

| الحقل / Field | القيمة / Value |
|--------------|---------------|
| الفئة / Category | تشغيلي / Operational |
| الاحتمالية / Probability | عالية / High |
| التأثير / Impact | عالٍ / High |
| الدرجة / Score | 9 |
| المالك / Owner | المؤسس / Founder |
| الحالة / Status | قيد المعالجة / Mitigating |
| آخر مراجعة / Last Reviewed | 2026-05-31 |

**استراتيجية التخفيف / Mitigation:**

- جميع إجراءات التسليم موثّقة في checklists قابلة للتفويض (راجع [`SPRINT_DELIVERY_PLAYBOOK.md`](../03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md)).
- مشغّل التوظيف الأول محدّد بوضوح في [`HIRING_TRIGGERS.md`](HIRING_TRIGGERS.md): 3+ مشاريع متزامنة مع تكرار نفس الـ checklist.
- نسخ احتياطية لجميع المعرفة التشغيلية في هذا المستودع.
- All delivery procedures documented in delegatable checklists.
- First hire trigger defined in [`HIRING_TRIGGERS.md`](HIRING_TRIGGERS.md): 3+ concurrent projects with repeated checklist shape.
- All operational knowledge backed up in this repository.

---

## R02 — تفويت موعد ZATCA Phase 2 Wave 8 لأحد العملاء / ZATCA Wave 8 Deadline Miss for a Client

| الحقل / Field | القيمة / Value |
|--------------|---------------|
| الفئة / Category | امتثال / Compliance |
| الاحتمالية / Probability | متوسطة / Medium |
| التأثير / Impact | عالٍ / High |
| الدرجة / Score | 6 |
| المالك / Owner | المؤسس / Founder |
| الحالة / Status | قيد المعالجة / Mitigating |
| آخر مراجعة / Last Reviewed | 2026-05-31 |

**استراتيجية التخفيف / Mitigation:**

- إبلاغ جميع العملاء المؤهلين بمتطلبات Wave 8 في الأسبوع الأول من Q3 2026.
- إنشاء قائمة تحقق Wave 8 مخصصة لكل عميل مؤهل وإغلاقها قبل الأسبوع 7.
- التوضيح الكتابي للعميل بأن الامتثال الكامل يتطلب مشاركته الفعلية في توفير البيانات.
- Notify all eligible clients of Wave 8 requirements in Week 1 of Q3 2026.
- Create a per-client Wave 8 checklist and close it before Week 7.
- Written client acknowledgment that full compliance requires their active data participation.

---

## R03 — فقدان عميل رئيسي قبل تعافي نقاط الصحة / Key Client Churn Before Health Score Recovery

| الحقل / Field | القيمة / Value |
|--------------|---------------|
| الفئة / Category | إيرادي / Revenue |
| الاحتمالية / Probability | متوسطة / Medium |
| التأثير / Impact | عالٍ / High |
| الدرجة / Score | 6 |
| المالك / Owner | المؤسس / Founder |
| الحالة / Status | مفتوح / Open |
| آخر مراجعة / Last Reviewed | 2026-05-31 |

**استراتيجية التخفيف / Mitigation:**

- نقاط صحة العميل تُراجَع أسبوعياً؛ أي نقاط دون 60 تستدعي مكالمة مباشرة خلال 48 ساعة.
- Proof Pack يُسلَّم في موعده كأداة إثبات قيمة ملموسة عند كل إغلاق سبرينت.
- لا عرض upsell قبل أن تتجاوز نقاط الصحة 70.
- Client health scores reviewed weekly; any score below 60 triggers a direct call within 48 hours.
- Proof Pack delivered on time as a tangible value-proof tool at every sprint close.
- No upsell proposal until health score exceeds 70.

---

## R04 — منافس يطلق منصة عمليات ذكاء اصطناعي بالعربية / Competitor Launches Arabic-Native AI Ops Platform

| الحقل / Field | القيمة / Value |
|--------------|---------------|
| الفئة / Category | سوقي / Market |
| الاحتمالية / Probability | منخفضة / Low |
| التأثير / Impact | عالٍ / High |
| الدرجة / Score | 3 |
| المالك / Owner | المؤسس / Founder |
| الحالة / Status | مفتوح / Open |
| آخر مراجعة / Last Reviewed | 2026-05-31 |

**استراتيجية التخفيف / Mitigation:**

- الميزة التنافسية في Dealix مبنية على الحوكمة والإثبات والامتثال السعودي — وليس على الميزات التقنية وحدها.
- Proof Pack الموثّق وسجل الأدلة يصعب تقليدهما في المدى القصير.
- مراقبة السوق ربع سنوياً وتحديث [`STRATEGIC_MOAT.md`](STRATEGIC_MOAT.md) عند ظهور منافس جديد.
- Dealix's competitive advantage is built on governance, verified proof, and Saudi compliance — not features alone.
- Documented Proof Pack and evidence ledger are difficult to replicate in the short term.
- Quarterly market monitoring; update [`STRATEGIC_MOAT.md`](STRATEGIC_MOAT.md) when a new competitor appears.

---

## R05 — ارتفاع تكاليف نماذج الذكاء الاصطناعي / AI Model Cost Spike

| الحقل / Field | القيمة / Value |
|--------------|---------------|
| الفئة / Category | تشغيلي / Operational |
| الاحتمالية / Probability | متوسطة / Medium |
| التأثير / Impact | متوسط / Medium |
| الدرجة / Score | 4 |
| المالك / Owner | المؤسس / Founder |
| الحالة / Status | قيد المعالجة / Mitigating |
| آخر مراجعة / Last Reviewed | 2026-05-31 |

**استراتيجية التخفيف / Mitigation:**

- بوابة LLM مع قواعد توجيه النماذج وحدود التكلفة المفعّلة (راجع [`../06_llm_gateway/COST_GUARD.md`](../06_llm_gateway/COST_GUARD.md)).
- الهامش يُراجَع عند تجاوز تكلفة الذكاء الاصطناعي 15% من قيمة المشروع (راجع [`AI_FINOPS.md`](AI_FINOPS.md)).
- عقود العملاء تتضمن بنداً صريحاً يُجيز تعديل الأسعار عند تغيّر تكاليف البنية التحتية بأكثر من 20%.
- LLM gateway with model routing rules and cost limits active (see [`../06_llm_gateway/COST_GUARD.md`](../06_llm_gateway/COST_GUARD.md)).
- Margin reviewed when AI cost exceeds 15% of project value (see [`AI_FINOPS.md`](AI_FINOPS.md)).
- Client contracts include an explicit clause permitting price adjustment when infrastructure costs shift by more than 20%.

---

## R06 — إجراء تنفيذي بموجب PDPL يطال أحد العملاء / PDPL Enforcement Action on a Client

| الحقل / Field | القيمة / Value |
|--------------|---------------|
| الفئة / Category | امتثال / Compliance |
| الاحتمالية / Probability | منخفضة / Low |
| التأثير / Impact | عالٍ / High |
| الدرجة / Score | 3 |
| المالك / Owner | المؤسس / Founder |
| الحالة / Status | قيد المعالجة / Mitigating |
| آخر مراجعة / Last Reviewed | 2026-05-31 |

**استراتيجية التخفيف / Mitigation:**

- اتفاقية DPA موقّعة مع كل عميل Managed Ops قبل بدء أي معالجة للبيانات.
- تصنيف البيانات وسياسة الاحتفاظ موثّقان في [`../04_data_os/PII_CLASSIFICATION.md`](../04_data_os/PII_CLASSIFICATION.md).
- مراجعة امتثال PDPL تُجرى مرة كل ربع سنة مع توثيق النتائج.
- DPA agreement signed with every Managed Ops client before any data processing begins.
- Data classification and retention policy documented in [`../04_data_os/PII_CLASSIFICATION.md`](../04_data_os/PII_CLASSIFICATION.md).
- PDPL compliance review conducted quarterly with documented findings.

---

## R07 — تأخر إتمام توظيف الموظف الأول / First Hire Onboarding Delay

| الحقل / Field | القيمة / Value |
|--------------|---------------|
| الفئة / Category | الفريق / Team |
| الاحتمالية / Probability | متوسطة / Medium |
| التأثير / Impact | متوسط / Medium |
| الدرجة / Score | 4 |
| المالك / Owner | المؤسس / Founder |
| الحالة / Status | مفتوح / Open |
| آخر مراجعة / Last Reviewed | 2026-05-31 |

**استراتيجية التخفيف / Mitigation:**

- عدم إعلان الحاجة للتوظيف قبل اكتمال حزمة التهيئة (onboarding pack) الكاملة.
- الاحتفاظ بقائمة مرشحين محتملين محدّثة قبل بلوغ مشغّل التوظيف بـ 4 أسابيع.
- عقد عمل حر (Contractor) كخيار احتياطي لتجسير فجوة الطاقة التسليمية بشكل مؤقت.
- Do not begin recruitment until the full onboarding pack is complete.
- Maintain a live shortlist of potential candidates 4 weeks before the hiring trigger is reached.
- Contractor engagement as a contingency to bridge a delivery capacity gap temporarily.

---

## R08 — تأخر سداد الفواتير يضغط على التدفق النقدي / Invoice Payment Delays Causing Cash Flow Stress

| الحقل / Field | القيمة / Value |
|--------------|---------------|
| الفئة / Category | إيرادي / Revenue |
| الاحتمالية / Probability | متوسطة / Medium |
| التأثير / Impact | متوسط / Medium |
| الدرجة / Score | 4 |
| المالك / Owner | المؤسس / Founder |
| الحالة / Status | قيد المعالجة / Mitigating |
| آخر مراجعة / Last Reviewed | 2026-05-31 |

**استراتيجية التخفيف / Mitigation:**

- دفعة مقدمة 50% على جميع عقود السبرينت قبل بدء العمل.
- شروط الدفع 30 يوماً كحد أقصى مع فوائد تأخير موثّقة في العقد.
- فواتير ZATCA Phase 2 إلكترونية لضمان الامتثال وتسريع دورة الدفع.
- 50% upfront payment on all sprint contracts before work begins.
- Maximum 30-day payment terms with documented late-payment terms in the contract.
- ZATCA Phase 2 e-invoicing for all clients to ensure compliance and accelerate payment cycles.

---

## R09 — مشكلة في جودة Proof Pack تُلحق ضرراً بالسمعة / Proof Pack Quality Issue Damages Reputation

| الحقل / Field | القيمة / Value |
|--------------|---------------|
| الفئة / Category | تشغيلي / Operational |
| الاحتمالية / Probability | منخفضة / Low |
| التأثير / Impact | عالٍ / High |
| الدرجة / Score | 3 |
| المالك / Owner | المؤسس / Founder |
| الحالة / Status | قيد المعالجة / Mitigating |
| آخر مراجعة / Last Reviewed | 2026-05-31 |

**استراتيجية التخفيف / Mitigation:**

- كل Proof Pack يمر عبر قائمة تحقق جودة ثنائية اللغة قبل إرساله للعميل (راجع [`../07_proof_os/PROOF_PACK_STANDARD.md`](../07_proof_os/PROOF_PACK_STANDARD.md)).
- جميع الأرقام الإيرادية في الـ Proof Pack مُصنَّفة صراحةً كـ "تقديرية" أو "موثّقة" أو "مُتحقَّق منها".
- أي ادعاء غير موثّق يحجبه معيار [`../08_value_os/ESTIMATED_OBSERVED_VERIFIED_VALUE.md`](../08_value_os/ESTIMATED_OBSERVED_VERIFIED_VALUE.md).
- Every Proof Pack passes a bilingual quality checklist before client delivery (see [`../07_proof_os/PROOF_PACK_STANDARD.md`](../07_proof_os/PROOF_PACK_STANDARD.md)).
- All revenue figures in Proof Packs are explicitly labeled as "estimated," "observed," or "verified."
- Any unverified claim is blocked by the [`../08_value_os/ESTIMATED_OBSERVED_VERIFIED_VALUE.md`](../08_value_os/ESTIMATED_OBSERVED_VERIFIED_VALUE.md) standard.

---

## R10 — تغيير سياسة واتساب يقيّد تواصل العميل / WhatsApp Policy Change Restricting Client Communication

| الحقل / Field | القيمة / Value |
|--------------|---------------|
| الفئة / Category | سوقي / Market |
| الاحتمالية / Probability | منخفضة / Low |
| التأثير / Impact | متوسط / Medium |
| الدرجة / Score | 2 |
| المالك / Owner | المؤسس / Founder |
| الحالة / Status | مفتوح / Open |
| آخر مراجعة / Last Reviewed | 2026-05-31 |

**استراتيجية التخفيف / Mitigation:**

- Dealix لا يُرسل رسائل خارجية آلية نيابةً عن العملاء في أي سيناريو (راجع [`../02_saudi_positioning/WHATSAPP_BOUNDARY.md`](../02_saudi_positioning/WHATSAPP_BOUNDARY.md)).
- التواصل التشغيلي مع العملاء يعتمد بشكل أساسي على البريد الإلكتروني وهذا المستودع، مع واتساب كقناة ثانوية فقط.
- أي تغيير في سياسات واتساب يُراجَع خلال 5 أيام عمل لتحديث [`../05_governance_os/CHANNEL_POLICY.md`](../05_governance_os/CHANNEL_POLICY.md).
- Dealix does not send automated external messages on clients' behalf under any scenario (see [`../02_saudi_positioning/WHATSAPP_BOUNDARY.md`](../02_saudi_positioning/WHATSAPP_BOUNDARY.md)).
- Operational client communication relies primarily on email and this repository; WhatsApp is a secondary channel only.
- Any WhatsApp policy change reviewed within 5 business days to update [`../05_governance_os/CHANNEL_POLICY.md`](../05_governance_os/CHANNEL_POLICY.md).

---

## ملخص لوحة المخاطر ## Risk Board Summary

| # | الخطر / Risk | الفئة / Category | الدرجة / Score | الحالة / Status |
|---|-------------|-----------------|---------------|----------------|
| R01 | الاعتماد على المؤسس / Founder Dependency | تشغيلي / Operational | **9** | قيد المعالجة / Mitigating |
| R02 | تفويت موعد ZATCA Wave 8 / ZATCA Wave 8 Deadline Miss | امتثال / Compliance | **6** | قيد المعالجة / Mitigating |
| R03 | فقدان عميل رئيسي / Key Client Churn | إيرادي / Revenue | **6** | مفتوح / Open |
| R04 | منافس عربي للذكاء الاصطناعي / Arabic AI Competitor | سوقي / Market | **3** | مفتوح / Open |
| R05 | ارتفاع تكاليف الذكاء الاصطناعي / AI Cost Spike | تشغيلي / Operational | **4** | قيد المعالجة / Mitigating |
| R06 | إجراء PDPL تنفيذي / PDPL Enforcement | امتثال / Compliance | **3** | قيد المعالجة / Mitigating |
| R07 | تأخر توظيف الموظف الأول / First Hire Delay | الفريق / Team | **4** | مفتوح / Open |
| R08 | تأخر سداد الفواتير / Invoice Payment Delay | إيرادي / Revenue | **4** | قيد المعالجة / Mitigating |
| R09 | مشكلة جودة Proof Pack / Proof Pack Quality Issue | تشغيلي / Operational | **3** | قيد المعالجة / Mitigating |
| R10 | تغيير سياسة واتساب / WhatsApp Policy Change | سوقي / Market | **2** | مفتوح / Open |

**المخاطر التي تستدعي انتباهاً فورياً (درجة ≥ 6) / Risks Requiring Immediate Attention (Score ≥ 6):**

- **R01** — الاعتماد على المؤسس: تسريع إعداد حزمة التهيئة ومراقبة مشغّل التوظيف.
- **R02** — ZATCA Wave 8: إطلاق قائمة تحقق العملاء في الأسبوع الأول من Q3.
- **R03** — Churn العميل الرئيسي: تفعيل بروتوكول المكالمة المباشرة عند نقاط صحة دون 60.

- **R01** — Founder dependency: accelerate onboarding pack preparation and monitor hiring trigger.
- **R02** — ZATCA Wave 8: launch client checklist in Week 1 of Q3.
- **R03** — Key client churn: activate direct call protocol for health scores below 60.

---

*آخر تحديث: 2026-05-31 · مالك السجل: المؤسس · دورة المراجعة: شهرية*
*Last updated: 2026-05-31 · Register owner: Founder · Review cadence: Monthly*
