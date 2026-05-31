# قائمة تسليم السبرنت — Sprint Delivery Checklist
## سبرنت ذكاء الإيرادات (499 ريال) — 7 أيام

> **الغرض / Purpose:** قائمة تشغيلية يومية للمؤسس لإتمام سبرنت ذكاء الإيرادات بسبعة أيام كاملة. كل يوم يحتوي على بوابة نجاح/إخفاق؛ لا يبدأ اليوم التالي إلا بعد اجتياز البوابة.
>
> A day-by-day founder checklist for completing the 499 SAR Revenue Intelligence Sprint. Each day carries a pass/fail gate — the sprint does not advance without the gate passing.
>
> **مرجع متقاطع / Cross-references:** [SPRINT_DELIVERY_PLAYBOOK.md](../03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md) · [DIAGNOSTIC_DELIVERY_SOP.md](../03_commercial_mvp/DIAGNOSTIC_DELIVERY_SOP.md) · [PDPL_RETENTION_POLICY.md](./PDPL_RETENTION_POLICY.md) · [APPROVAL_POLICY.md](../05_governance_os/APPROVAL_POLICY.md)

---

## بوابة ما قبل السبرنت — Pre-Sprint Gate (APPROVAL_FIRST)

لا تبدأ أي عمل قبل اجتياز هذه البوابة كاملةً.
No work begins before every item below is confirmed.

- [ ] العقد موقَّع من الطرفين وإيداع المبلغ مؤكَّد (499 ريال). / Contract signed by both parties; 499 SAR payment confirmed.
- [ ] جواز المصدر (Source Passport) مكتمل: `owner`, `source_type`, `allowed_use`, `pii_flag`, `sensitivity`, `retention_days`. / Source Passport completed with all required fields.
- [ ] نموذج موافقة PDPL مُوقَّع من العميل قبل استلام أي بيانات. / PDPL data-processing consent signed by client before any data is received.
- [ ] مالك سير العمل مُحدَّد بالاسم من جانب العميل (غير قابل للتفاوض). / Named workflow owner confirmed on the client side — non-negotiable.
- [ ] جلسة الإطلاق (45 دقيقة) مجدولة ومؤكدة. / 45-minute kickoff session scheduled and confirmed.
- [ ] **موافقة المؤسس مُسجَّلة** قبل إرسال أي اتصال خارجي. / **Founder approval logged** before any external communication is sent.

**بوابة البدء / Start gate:** جميع البنود أعلاه = نعم. / All items above = YES. If any item is NO, the sprint does not begin.

---

## اليوم الأول — Day 1: تدقيق البيانات وقياس خط الجودة الأساسي / Data Audit + DQ Score Baseline

**الهدف:** إنشاء سجل الأدلة الأساسي وقياس جودة البيانات.
**Goal:** Establish the evidence baseline and measure data quality.

- [ ] استلام ملف بيانات العميل بالقناة المعتمدة (رفع آمن، لا WhatsApp). / Client data file received via approved channel (secure upload, not WhatsApp).
- [ ] تسجيل معرّف المشروع في سجل المشاريع: `engagements/<engagement_id>/`. / Engagement ID registered; folder `engagements/<engagement_id>/` created.
- [ ] تشغيل معاينة الاستيراد (قراءة بدون تعديل) وتوثيق عدد السجلات والحقول. / Import preview run (non-destructive read); record count and field list documented.
- [ ] حساب درجة جودة البيانات (DQ Score) على الأبعاد الستة: الاكتمال، الصحة، التفرد، الاتساق، التوقيت، المطابقة. / DQ Score computed across six dimensions: completeness, validity, uniqueness, consistency, timeliness, conformance.
- [ ] تسجيل درجة DQ الأساسية في سجل الإثبات: `proof_ledger.dq_baseline`. / DQ baseline recorded in proof ledger: `proof_ledger.dq_baseline`.
- [ ] فحص امتثال ZATCA المرحلة الثانية: هل بيانات الفواتير/المعاملات مُنسَّقة وفق معايير الفاتورة الإلكترونية؟ / ZATCA Phase 2 compliance scan: are invoice/transaction fields formatted per e-invoicing requirements?

**بوابة اليوم الأول / Day 1 gate:**
- درجة DQ مُسجَّلة في السجل. / DQ score recorded in ledger.
- لا بيانات خارج بيئة Dealix الآمنة. / No data outside Dealix's secure environment.
- DQ < 40: توقّف — اقترح حزمة البيانات (1,500 ريال) وأرجع 80% من رسوم السبرنت وفق سياسة الاسترداد. / DQ < 40: pause — propose the 1,500 SAR Data Pack; refund 80% of sprint fee per refund policy.

---

## اليوم الثاني — Day 2: تحديد تسريبات الإيرادات وقائمة الأولويات / Revenue Leakage Identification + Priority Issue List

**الهدف:** تحديد أين تُفقَد الإيرادات المحتملة قبل الوصول إلى المبيعات.
**Goal:** Identify where potential revenue is lost before it reaches sales.

- [ ] تشغيل وحدة تسريب الإيرادات: كشف الحسابات الخاملة، الحسابات المكررة، فجوات المتابعة. / Revenue leakage module run: dormant accounts, duplicate accounts, follow-up gaps identified.
- [ ] بناء قائمة أولويات مُصنَّفة بالأدلة (ليس بالتخمين): كل بند يحمل عدد السجلات المتأثرة. / Evidence-ranked priority issue list built (not by guess): each item carries an affected record count.
- [ ] توثيق كل مشكلة بتصنيف: بيانات / عملية / نظام. / Each issue classified as: data / process / system.
- [ ] لا توصيات خارجية تُرسَل للعميل اليوم — هذه مرحلة تحليل داخلية فقط. / No external recommendations sent to client today — internal analysis phase only.
- [ ] تحديث سجل الإثبات: `proof_ledger.leakage_analysis_completed = true`. / Proof ledger updated: `proof_ledger.leakage_analysis_completed = true`.

**بوابة اليوم الثاني / Day 2 gate:** قائمة الأولويات موثَّقة في ملف المشروع بأدلة قابلة للتحقق. / Priority list documented in engagement folder with verifiable evidence.

---

## اليوم الثالث — Day 3: تقييم فجوات PDPL وتصنيف البيانات / PDPL Gap Assessment + Data Classification

**الهدف:** ضمان أن بيانات العميل مُصنَّفة ومعالجتها تتوافق مع نظام PDPL.
**Goal:** Ensure client data is classified and its processing aligns with PDPL.

- [ ] مراجعة تصنيف البيانات: أي حقول تحتوي على بيانات شخصية تعريفية؟ هل هي مُعلَّمة في جواز المصدر؟ / Data classification review: which fields contain PII? Are they flagged in the Source Passport?
- [ ] تقييم فجوات PDPL: هل غرض المعالجة محدد؟ هل موافقة معالجة البيانات DPA مُوثَّقة؟ / PDPL gap assessment: is the processing purpose defined? Is the DPA documented?
- [ ] تحقق من عدم وجود بيانات من فئة خاصة (هوية وطنية، صحة، دين) في المجموعة. في حال وجودها: إبلاغ العميل فوراً وحذف الحقل. / Verify no sensitive-category data (national ID, health, religion) is present. If found: notify client immediately and remove the field.
- [ ] توثيق الفجوات في سجل المشروع مع مسار التصحيح المقترح لكل فجوة. / Gaps documented in engagement record with a proposed remediation path for each.
- [ ] تحديث سجل الإثبات: `proof_ledger.pdpl_gap_assessment_completed = true`. / Proof ledger updated: `proof_ledger.pdpl_gap_assessment_completed = true`.

**بوابة اليوم الثالث / Day 3 gate:** صفر حقول من الفئة الحساسة بدون معالجة. أي فجوة تم توثيقها أو إغلاقها. / Zero unaddressed sensitive-category fields. Every gap is documented or closed.

---

## اليوم الرابع — Day 4: تجهيز قالب حزمة الإثبات وتثبيت الخط الأساسي للمقاييس / Proof Pack Template + Metrics Baseline Locked

**الهدف:** تأمين الخط الأساسي للمقاييس قبل بدء التحليل النهائي.
**Goal:** Lock the metrics baseline before final analysis begins.

- [ ] فتح قالب حزمة الإثبات (14 قسم): ملء الأقسام الأولى — الاستلام، جواز المصدر، درجة DQ، تقرير إلغاء التكرار. / Proof Pack template opened (14 sections): populate first sections — intake, Source Passport, DQ score, dedupe report.
- [ ] تثبيت الخط الأساسي للمقاييس المتفق عليها مع العميل في الجلسة الافتتاحية. / Agreed-upon metrics baseline (from kickoff) locked in the engagement record.
- [ ] التحقق من أن جميع الأدلة المُجمَّعة حتى الآن قابلة للتدقيق وترتبط بمصادر بيانات موثَّقة. / All evidence gathered to date is auditable and traces to documented data sources.
- [ ] لا تقديرات للقيمة في هذه المرحلة — فقط حقائق موثَّقة. / No value estimates at this stage — documented facts only.
- [ ] تحديث سجل الإثبات: `proof_ledger.metrics_baseline_locked = true`. / Proof ledger updated: `proof_ledger.metrics_baseline_locked = true`.

**بوابة اليوم الرابع / Day 4 gate:** الخط الأساسي للمقاييس مُثبَّت ومُوقَّع في سجل المشروع. / Metrics baseline locked and committed in engagement record.

---

## اليوم الخامس — Day 5: اكتمال التحليل والنتائج وحزمة الإثبات المسوّدة / Analysis Complete + Findings Documented + Proof Pack Draft v1

**الهدف:** إنتاج مسودة حزمة الإثبات الكاملة.
**Goal:** Produce the complete Proof Pack draft.

- [ ] تشغيل وحدة ترتيب الحسابات: كل تصنيف في أعلى 10 حسابات يحمل مبرراً نصياً قابلاً للقراءة البشرية. / Account scoring module run: every top-10 ranking carries a human-readable text justification.
- [ ] توليد مسودات الإجراءات الموصى بها (ثنائية اللغة AR + EN)؛ جميع المسودات مُعلَّمة `draft_only` حتى موافقة المؤسس. / Recommended action drafts generated (bilingual AR + EN); all drafts labelled `draft_only` until founder approval.
- [ ] تشغيل قرارات الحوكمة وتوثيق كل قرار: ALLOW / REQUIRE_APPROVAL / BLOCK مع السبب. / Governance decisions run; every decision documented: ALLOW / REQUIRE_APPROVAL / BLOCK with reason.
- [ ] تجميع مسودة حزمة الإثبات v1 (14 قسم). التحقق من عدم وجود أقسام فارغة. / Proof Pack draft v1 assembled (14 sections). Verify no empty sections.
- [ ] حساب درجة الإثبات (proof_score). إذا كانت < 70: توقّف — لا تسليم؛ ابدأ مسار التصحيح. / Proof score computed. If < 70: stop — no delivery; begin remediation path.
- [ ] تحديث سجل الإثبات: `proof_ledger.proof_pack_draft_v1 = <path>`, `proof_ledger.proof_score = <score>`. / Proof ledger updated: `proof_ledger.proof_pack_draft_v1 = <path>`, `proof_ledger.proof_score = <score>`.

**بوابة اليوم الخامس / Day 5 gate:** درجة إثبات ≥ 70. جميع الأقسام الـ14 موجودة بلا فراغات. / Proof score ≥ 70. All 14 sections present with no placeholders.

---

## اليوم السادس — Day 6: المراجعة الداخلية ومراجعة المؤسس (APPROVAL_FIRST) / Internal Review + Founder Review (APPROVAL_FIRST)

**الهدف:** لا يصل أي تسليم للعميل قبل مراجعة المؤسس الكاملة وتسجيل موافقته.
**Goal:** No deliverable reaches the client before a complete founder review and logged approval.

- [ ] قراءة حزمة الإثبات من الأول للآخر بوصفك المؤسس، لا كمنتج مستعجل. / Read the Proof Pack end to end as founder — not as a product in a hurry.
- [ ] التحقق من 8 أبعاد الجودة: سلامة المصدر، شفافية DQ، قابلية شرح الترتيب، التكافؤ الثنائي اللغوي، قابلية تدقيق الحوكمة، انضباط الموافقة، اكتمال الإثبات، إيداع الأصول. / Verify all 8 QA dimensions: source integrity, DQ transparency, scoring explainability, bilingual parity, governance auditability, approval discipline, proof completeness, capital deposit.
- [ ] التحقق من أن جميع التقديرات مُعلَّمة بوضوح "تقديري" وليس "مضمون". / Verify all estimates are clearly labelled "Estimated" and not "Guaranteed".
- [ ] التحقق من عدم وجود معلومات تعريفية شخصية (PII) في مسودات التسليم خارج السياق المصرَّح به. / Verify no PII appears in delivery drafts outside permitted context.
- [ ] **تسجيل موافقة المؤسس** في سجل الحوكمة قبل الانتقال لليوم السابع. / **Log founder approval** in governance ledger before advancing to Day 7.
- [ ] إذا اكتُشفت مشاكل: تصحيح في نفس اليوم أو التمديد 48 ساعة على حساب Dealix، لا العميل. / If issues found: remediate same day or extend 48 hours at Dealix's cost, not the client's.

**بوابة اليوم السادس / Day 6 gate (APPROVAL_FIRST):** موافقة المؤسس مُسجَّلة في سجل الحوكمة. بدون هذا السجل لا يُسمح بالتسليم. / Founder approval logged in governance ledger. Without this record, delivery is not permitted.

---

## اليوم السابع — Day 7: جلسة التسليم للعميل وإصدار الفاتورة / Client Delivery Session + Invoice

**الهدف:** تقديم حزمة الإثبات للعميل في جلسة رسمية وإغلاق المشروع بنظام.
**Goal:** Present the Proof Pack in a formal session and close the engagement cleanly.

- [ ] جلسة التسليم: حضوري أو مكالمة فيديو مجدولة — لا تسليم عبر WhatsApp. / Delivery session: in-person or scheduled video call — no delivery via WhatsApp.
- [ ] تقديم حزمة الإثبات قسماً قسماً؛ إتاحة وقت للأسئلة بعد كل قسم رئيسي. / Present Proof Pack section by section; allow questions after each major section.
- [ ] تأكيد أن جميع التقديرات مقدّمة كأدلة، لا كضمانات مبيعات. / Confirm all estimates are presented as evidenced opportunities, not sales guarantees.
- [ ] إصدار الفاتورة وفق معايير ZATCA المرحلة الثانية والتسليم للعميل. / Invoice issued per ZATCA Phase 2 requirements and delivered to client.
- [ ] تسجيل أصل رأسمالي واحد على الأقل قابل لإعادة الاستخدام في سجل الأصول الرأسمالية. / At least one reusable capital asset registered in the Capital Ledger.
- [ ] تحديث حالة المشروع إلى `status=delivered` في سجل المشاريع. / Engagement status updated to `status=delivered` in engagement registry.

**بوابة اليوم السابع / Day 7 gate:** الجلسة مُنعقدة، الفاتورة مُصدَرة، الحالة `delivered`، الأصل الرأسمالي مُسجَّل. / Session held, invoice issued, status `delivered`, capital asset registered.

---

## ما بعد السبرنت — Post-Sprint Actions

- [ ] إذا استوفى العميل معايير الجاهزية (درجة إثبات ≥ 80، مالك سير عمل مستمر، جواز مصدر قابل للتجديد): عرض Managed Ops (2,999–4,999 ريال/شهر). / If client meets readiness criteria (proof score ≥ 80, workflow owner persists, renewable Source Passport): propose Managed Ops (2,999–4,999 SAR/mo).
- [ ] تحديث درجة صحة العميل في لوحة المتابعة. / Client health score updated in the monitoring dashboard.
- [ ] طلب الإحالة: "هل تعرف شركة أخرى تعاني من نفس التحديات؟" — سؤال مباشر، لا ضغط. / Referral ask: "Do you know another company facing the same challenges?" — direct question, no pressure.
- [ ] إعداد ملخص مجهول الهوية للحالة (case-safe summary) في `docs/case-studies/` دون ذكر اسم العميل أو أرقام الإيرادات المحددة. / Case-safe summary prepared in `docs/case-studies/` with no client name or specific revenue figures.

---

## ما لا يُتجاوز أبداً — What Must Never Be Skipped

| البند الإلزامي | السبب |
|---|---|
| درجة DQ (DQ Score) | التسليم بدون قياس جودة البيانات يُنتج ادعاءات لا يمكن التحقق منها |
| حزمة الإثبات (Proof Pack) | العميل يشتري سجل الأدلة، لا مجرد توصيات |
| مراجعة المؤسس وموافقته (APPROVAL_FIRST) | كل إجراء خارجي يتطلب موافقة مُسجَّلة قبل التنفيذ |

| Mandatory Item | Reason |
|---|---|
| DQ Score | Delivery without data quality measurement produces unverifiable claims |
| Proof Pack | The client buys the evidence record, not just recommendations |
| Founder review + approval (APPROVAL_FIRST) | Every external action requires a logged approval before execution |

---

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
