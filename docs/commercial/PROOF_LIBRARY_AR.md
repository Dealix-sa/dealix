# مكتبة الأدلة — Proof Library — هيكل الإثبات ومستوياته

**مرجع:** [PRODUCT_CATALOG_AR.md](PRODUCT_CATALOG_AR.md) · [docs/07_proof_os/](../07_proof_os/) · [docs/07_proof_os/PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md) · [docs/07_proof_os/PROOF_SCORE.md](../07_proof_os/PROOF_SCORE.md)
آخر مراجعة: 2026-06-02.

---

## الغرض من هذه الوثيقة

تُحدد هذه الوثيقة الهيكل الكامل لمكتبة الأدلة في Dealix: أنواع الدليل، مستويات الإثبات L0–L5، ربط كل منتج بهدف إثبات محدّد، وقاعدة "لا دليل — لا بيع صاعد".

---

## أنواع الدليل المعتمدة

### النوع 1 — Proof Pack (حزمة الإثبات الكاملة)

**تعريف:** وثيقة منظّمة تُسلَّم مع كل مشروع كامل، تُوثّق ما بُني وما تغيّر وما يمكن قياسه.

**يشمل:**
- وصف النطاق المُنجَز مقابل النطاق المُتفق عليه.
- المخرجات الفعلية (تقارير، workflows، dashboards، مسودات).
- المؤشرات الأولية (قبل/بعد) مع تحفّظ القيمة التقديرية.
- اسم مالك العملية من جانب العميل.
- توقيع القبول من مالك القرار.

**معيار الجودة:** راجع [docs/07_proof_os/PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md).

---

### النوع 2 — Case-Safe Summary (ملخص مُجهَّل للحالة)

**تعريف:** ملخص لمشروع منجز يُوثّق النمط والمخرجات دون الكشف عن هوية العميل.

**يشمل:**
- القطاع والحجم التقريبي (مثلاً: "شركة خدمات مهنية — 30 موظف — الرياض").
- المشكلة المُحدَّدة والنطاق المُنجَز.
- المخرجات الموثّقة (بدون أرقام مطلقة غير مُثبتة).
- مدة التسليم.

**القيد:** لا أسماء، لا PII، لا أرقام إيرادية غير موثّقة.

**معيار الجودة:** راجع [docs/07_proof_os/CASE_SAFE_SUMMARY.md](../07_proof_os/CASE_SAFE_SUMMARY.md).

---

### النوع 3 — Metric with Tier (مؤشر مُصنَّف بمستوى)

**تعريف:** رقم أو مؤشر مُقترن بمستوى إثباته الصريح — لا يُقتبَس رقم بدون تصنيفه.

**التصنيف:**

| التصنيف | المعنى |
|---------|--------|
| Estimated | تقدير مبني على بيانات عيّنة — لا يُستخدم كضمان |
| Observed | مؤشر مُلاحَظ في مشروع محدد — مُقيَّد بسياقه |
| Aggregated Pattern | نمط مُجمَّع من عدة حالات — لا يُحيل لحالة بعينها |

**القيد:** كل رقم في مواد المبيعات يحمل تصنيفه. لا ادّعاء بدون تصنيف.

---

### النوع 4 — Sector Pattern (نمط قطاعي)

**تعريف:** نمط مُوثَّق من تقارير قطاعية مُجمَّعة — يُستخدم للسياق وليس للادّعاء الفردي.

**يشمل:**
- مصدر النمط (اصطناعي / مُجمَّع / مستند لمرجع خارجي).
- K-anonymity ≥ 5 على كل شريحة.
- لا إحالة لمنظمة بعينها.

**المرجع:** [docs/sector-reports/b2b_services_sample.md](../sector-reports/b2b_services_sample.md).

---

### النوع 5 — Governance/Audit Trail (مسار الحوكمة)

**تعريف:** سجل قرارات المشروع — كل قرار مُسجَّل بتاريخه وصاحبه ومبرّره.

**يشمل:**
- سجل DPA (متى وُقِّع ومن وقّع).
- سجل موافقات الإرسال (إن وُجدت).
- سجل مصدر البيانات (source registry).
- سجل المخرجات المُسلَّمة.

**المرجع:** [docs/05_governance_os/GOVERNANCE_DECISION_TYPES.md](../05_governance_os/GOVERNANCE_DECISION_TYPES.md).

---

## مستويات الإثبات L0–L5

| المستوى | الاسم | المعنى | متطلبات الترقية |
|---------|-------|--------|-----------------|
| **L0** | بلا دليل | لا يوجد تسليم موثّق — لا يُعرض بيع صاعد | ابدأ بالتشخيص |
| **L1** | عيّنة بيانات | عيّنة بيانات مُسلَّمة وموثّقة + DPA | نتيجة تشخيص مقبولة |
| **L2** | تسليم أولي | تقرير أو workflow مُسلَّم ومُراجَع من مالك القرار | Proof Pack أولي مكتمل |
| **L3** | تسليم كامل | Proof Pack كامل مع توقيع القبول | تشغيل فعلي 30+ يوم |
| **L4** | نمط متكرر | أكثر من تسليم واحد ناجح في قطاع مماثل | Case-Safe Summary متاح |
| **L5** | إثبات مرجعي | Proof Score ≥ 85 + عميل مرجعي قبل الكشف عن هويته | موافقة العميل على الاستشهاد |

**قاعدة الترقية:** ترقية العميل من درجة لأعلى تتطلب أن يكون مستوى الإثبات مساوياً أو أعلى من متطلبات الدرجة الجديدة.

---

## ربط المنتجات بأهداف الإثبات

| المنتج | المستوى المطلوب عند البدء | هدف الإثبات عند التسليم | نوع الدليل الناتج |
|--------|--------------------------|--------------------------|-------------------|
| Revenue Leakage Diagnostic | L1 | تقرير تشخيص مقبول — L2 | Metric with Tier + Audit Trail |
| Follow-up Recovery Workflow | L2 | Proof Pack أولي — L3 | Proof Pack + Case-Safe Summary |
| AI Revenue Ops Starter | L3 | Proof Pack كامل مع مؤشرات 30 يوم — L3+ | Proof Pack + Sector Pattern |
| Full Revenue OS | L4 | Proof Pack شامل مع audit trail كامل — L4 | Full Proof Pack + Governance Trail |
| Monthly Optimization | L3+ | تقرير شهري موثّق — يُراكَم نحو L4 | Monthly Proof Update |
| Custom Company OS | L5 | يُحدَّد في SOW — L5 | SOW-defined proof artifacts |

---

## قاعدة "لا دليل — لا بيع صاعد"

هذه القاعدة غير قابلة للتفاوض في كل مسارات Dealix:

**التطبيق العملي:**

1. لا يُعرض منتج من درجة أعلى قبل اكتمال Proof Pack من الدرجة الحالية.
2. لا تُُقتبَس نتائج تقديرية في مواد المبيعات دون تصنيف المستوى.
3. لا تُستخدم Case-Safe Summary من مشروع لم يُكتمل Proof Pack له.
4. لا يُُشار إلى نتيجة "عميل X" دون موافقة مكتوبة أو case-safe anonymization.
5. Proof Score < 60 يُوقف أي محادثة بيع صاعد حتى يُحلّ السبب.

**المرجع:** [docs/07_proof_os/PROOF_SCORE.md](../07_proof_os/PROOF_SCORE.md) — درجة 85 هي الحد الأدنى للمرجعية الكاملة.

---

## هيكل تجميع المكتبة

### المسار الزمني لبناء مكتبة الأدلة

```
مشروع 1 → Proof Pack → Case-Safe Summary → L2
مشروع 2 → Proof Pack → Case-Safe Summary → L3
مشروع 3 (قطاع مختلف) → Proof Pack → Sector Pattern → L4
مشروع 4 (نفس القطاع) → Proof Pack → Aggregated Pattern → L4
مشروع 5+ → Proof Score ≥ 85 على الأقل → L5 جاهز للمرجعية
```

### تخزين الأدلة

- كل Proof Pack يُحفظ في مجلد المشروع بالريبو.
- كل Case-Safe Summary يُوثَّق في [docs/07_proof_os/CASE_SAFE_SUMMARY.md](../07_proof_os/CASE_SAFE_SUMMARY.md) أو مجلد case-studies.
- المؤشرات المُجمَّعة تُدار في [docs/07_proof_os/PROOF_EVENTS.md](../07_proof_os/PROOF_EVENTS.md).

---

## ما لا يُدرج في مكتبة الأدلة

- أسماء عملاء حقيقيين بدون موافقة مكتوبة صريحة.
- أرقام إيرادية مُدّعاة لعميل بعينه دون Proof Pack.
- شهادات أو اقتباسات من أشخاص لم يوافقوا كتابةً.
- مقارنات مع منافسين بأسمائهم.
- أي رقم مُصنَّف بأقل من المستوى المُذكور في الاقتباس.

**المرجع:** [docs/05_governance_os/CLAIM_SAFETY.md](../05_governance_os/CLAIM_SAFETY.md).

---

## مرايا إنجليزية — English Mirror

### Proof Types Summary

| Type | Definition | Use Case | Key Constraint |
|------|-----------|----------|----------------|
| Proof Pack | Full documented delivery artifact | Upsell gate, contract close | Requires decision-owner signature |
| Case-Safe Summary | Anonymised project summary | Sales materials, prospect conversations | No names, no unverified revenue numbers |
| Metric with Tier | Number + explicit proof classification | Proposals, one-pagers | Every number must carry its tier label |
| Sector Pattern | Aggregated cross-project pattern | Context-setting, sector reports | K-anonymity ≥ 5; no single org identifiable |
| Governance/Audit Trail | Decision log with date/owner/rationale | Compliance, PDPL, due diligence | Every external-bound decision recorded |

### Evidence Levels L0–L5

| Level | Name | Meaning |
|-------|------|---------|
| L0 | No evidence | No documented delivery — no upsell conversation |
| L1 | Data sample | Sample delivered and documented + DPA signed |
| L2 | Initial delivery | Report or workflow delivered and accepted by decision owner |
| L3 | Complete delivery | Full Proof Pack with sign-off + 30+ day operation |
| L4 | Repeated pattern | Multiple successful deliveries in similar sector |
| L5 | Reference-grade | Proof Score ≥ 85 + client approved reference use |

### "No Proof → No Upsell" Rule

No higher-rung product is proposed before the current rung's Proof Pack is complete and accepted. No estimated metric is quoted without its tier label. Proof Score below 60 halts upsell conversations until the cause is resolved.

---

القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
