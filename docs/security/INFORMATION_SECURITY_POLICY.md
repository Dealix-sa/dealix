# سياسة أمن المعلومات — Information Security Policy

**الإصدار:** 1.0 | **تاريخ النفاذ:** 2026-05-31 | **مالك السياسة:** المؤسس
**دورة المراجعة:** سنوية أو عند أي تغيير جوهري

---

> **هذه السياسة مُصمَّمة لحماية عملاء Dealix وبياناتهم وفق متطلبات PDPL وأفضل الممارسات الدولية**
> **This policy is designed to protect Dealix clients and their data in accordance with PDPL requirements and international best practices**

---

## ١. الغرض من السياسة ونطاقها — Policy Purpose & Scope

### العربية

تُحدد هذه السياسة الحد الأدنى من ضوابط أمن المعلومات المعمول بها في Dealix. تسري على جميع الأنظمة والبيانات والعمليات والموظفين المرتبطين بالمنصة، بما يشمل المقاولين الخارجيين ومعالجي البيانات من الأطراف الثالثة.

**النطاق يشمل:**
- جميع بيانات العملاء المعالَجة عبر منصة Dealix.
- الأنظمة السحابية والبنية التحتية (Railway، AWS S3، قواعد البيانات).
- نماذج الذكاء الاصطناعي وبوابة LLM.
- المستندات الداخلية وحزم الإثبات (Proof Packs).
- جميع العاملين بعقد عمل أو تعاقد مع Dealix.

**النطاق لا يشمل:** بيانات العملاء المخزَّنة بالكامل في بيئات العميل الخاصة خارج منصة Dealix، ما لم يكن لـ Dealix وصول مباشر إليها.

### English

This policy defines the minimum information security controls in effect at Dealix. It applies to all systems, data, processes, and personnel connected to the platform, including external contractors and third-party data processors.

**Scope includes:**
- All client data processed through the Dealix platform.
- Cloud systems and infrastructure (Railway, AWS S3, databases).
- AI models and the LLM gateway.
- Internal documents and Proof Packs.
- All employees and contractors engaged by Dealix.

**Scope excludes:** Client data stored entirely in the client's own environment outside the Dealix platform, unless Dealix holds direct access to it.

---

## ٢. تصنيف البيانات — Data Classification

### العربية

تُصنَّف جميع البيانات في Dealix وفق أربعة مستويات. يتحمل كل موظف مسؤولية التصنيف الصحيح لكل بيانات يتعامل معها.

| المستوى | التسمية العربية | التسمية الإنجليزية | أمثلة | متطلبات الحماية |
|---|---|---|---|---|
| 1 | سري للغاية | Highly Confidential | بيانات PII الخاصة بالعملاء، فواتير ZATCA XML، بيانات الدفع، كلمات المرور | تشفير AES-256 في مرحلة التخزين (مخطط Q3 2026)، TLS 1.3 أثناء النقل، وصول RBAC صارم |
| 2 | سري | Confidential | بيانات الأعمال الداخلية، درجات DQ Score، درجات صحة الإيرادات، سجلات التدقيق | وصول محدود بالدور الوظيفي، لا مشاركة خارجية دون موافقة |
| 3 | داخلي | Internal | الوثائق التشغيلية، حزم Proof Pack بعد التسليم، بروتوكولات الاجتماعات | وصول الفريق الداخلي فقط، لا نشر علني |
| 4 | عام | Public | المحتوى التسويقي، ملخصات دراسات الحالة المُجهَّلة | لا قيود على النشر، مراجعة جودة قبل النشر |

### English

All Dealix data is classified under four levels. Every employee is responsible for correctly classifying data they handle.

**Level 1 — سري للغاية | Highly Confidential:** Client PII, ZATCA XML invoices, payment data, credentials. Requires AES-256 encryption at rest (planned Q3 2026), TLS 1.3 in transit, strict RBAC access.

**Level 2 — سري | Confidential:** Internal business data, DQ Scores, revenue health scores, audit logs. Restricted to role-based access; no external sharing without approval.

**Level 3 — داخلي | Internal:** Operational documents, Proof Packs post-delivery, meeting notes. Internal team access only; not for public distribution.

**Level 4 — عام | Public:** Marketing content, anonymised case study summaries. No distribution restrictions; quality review required before publication.

---

## ٣. التحكم في الوصول — Access Control

### العربية

- **RBAC (التحكم القائم على الأدوار):** يُمنح كل مستخدم الصلاحيات الضرورية لأداء مهامه فحسب. لا صلاحيات مفتوحة بدون مبرر موثَّق.
- **مبدأ الحد الأدنى من الامتياز:** الوصول الافتراضي هو "لا وصول"، يُرفع بناءً على طلب محدد وموافقة المؤسس أو مدير القسم.
- **تدوير مفاتيح API:** كل 90 يوماً للمفاتيح الحرجة (APP_SECRET_KEY، JWT_SECRET_KEY، ADMIN_API_KEYS). راجع [`docs/security/KEY_ROTATION.md`](KEY_ROTATION.md) للجدول الزمني الكامل.
- **المصادقة الثنائية (2FA):** إلزامية لجميع الحسابات ذات الوصول لبيانات من المستوى 1 أو 2.
- **إلغاء الوصول فوراً:** عند انتهاء عقد أي موظف أو متعاقد، تُلغى جميع صلاحياته خلال 24 ساعة.

### English

- **RBAC (Role-Based Access Control):** Each user is granted only the permissions necessary to perform their specific role. No open-ended access without documented justification.
- **Least privilege principle:** Default access is "no access," elevated on specific request with founder or department head approval.
- **API key rotation:** Every 90 days for critical keys (APP_SECRET_KEY, JWT_SECRET_KEY, ADMIN_API_KEYS). See [`docs/security/KEY_ROTATION.md`](KEY_ROTATION.md) for the full rotation schedule.
- **Two-factor authentication (2FA):** Mandatory for all accounts with access to Level 1 or Level 2 data.
- **Immediate access revocation:** Upon termination of any employee or contractor, all access credentials are revoked within 24 hours.

---

## ٤. معايير التشفير — Encryption Standards

### العربية

| السياق | المعيار الحالي | الهدف المخطط |
|---|---|---|
| البيانات أثناء النقل (In Transit) | TLS 1.3 — مُفعَّل | مستمر |
| البيانات في مرحلة التخزين (At Rest) | تشفير على مستوى قاعدة البيانات (قيد التقييم) | AES-256 — مخطط Q3 2026 |
| النسخ الاحتياطية | تشفير باستخدام BACKUP_ENCRYPTION_KEY | مستمر، دورة تدوير سنوية |
| الاتصالات الداخلية | HTTPS إلزامي | مستمر |

**ملاحظة:** معيار AES-256 لمرحلة التخزين هو هدف مخطط لـ Q3 2026 وليس ميزة مُنشَرة حالياً. لا تُذكر هذه الميزة في المواد الخارجية كواقع قائم.

### English

| Context | Current Standard | Planned Target |
|---|---|---|
| Data in Transit | TLS 1.3 — active | Ongoing |
| Data at Rest | Database-level encryption (under evaluation) | AES-256 — planned Q3 2026 |
| Backups | Encrypted using BACKUP_ENCRYPTION_KEY | Ongoing, annual rotation cycle |
| Internal communications | HTTPS mandatory | Ongoing |

**Note:** AES-256 at rest is a planned target for Q3 2026 and is not a currently deployed feature. This capability must not be described as active in any external materials.

---

## ٥. الاستجابة للحوادث — Incident Response

### العربية

تتبع Dealix منهجية خمس مراحل لإدارة الحوادث الأمنية:

**المرحلة الأولى — الكشف (Detect)**
رصد الحوادث عبر تنبيهات Sentry، وسجلات Railway، ومراجعات الوصول الدورية. أي سلوك غير اعتيادي يُصنَّف حادثة محتملة حتى يُثبَت خلاف ذلك.

**المرحلة الثانية — الاحتواء (Contain)**
عزل الأنظمة أو الحسابات المشتبه بتأثرها فوراً. تعليق وصول API المشتبه به. تفعيل إجراءات التدوير الطارئ للمفاتيح عند الاشتباه بالاختراق.

**المرحلة الثالثة — التقييم (Assess)**
تحديد نطاق الحادث: ما البيانات المتأثرة؟ ما تصنيفها؟ هل تشمل بيانات شخصية بموجب تعريف PDPL؟ هل تشمل فواتير ZATCA؟

**المرحلة الرابعة — الإخطار (Notify)**
- **داخلياً:** إشعار فوري للمؤسس.
- **العملاء المتضررون:** إشعار خلال 48 ساعة من التأكيد.
- **الهيئة الوطنية لحماية البيانات (متطلب PDPL):** الإخطار خلال **72 ساعة** من اكتشاف الاختراق الذي يطال بيانات شخصية — وفق المادة (40) من نظام حماية البيانات الشخصية.

**المرحلة الخامسة — الاستعادة (Recover)**
استعادة الخدمة من آخر نسخة احتياطية موثوقة. توثيق الحادث كاملاً في سجل الحوادث. إجراء مراجعة ما بعد الحادث خلال 7 أيام لتحديد الثغرة وإصلاحها.

### English

Dealix follows a five-phase methodology for managing security incidents:

**Phase 1 — Detect:** Incidents are detected via Sentry alerts, Railway logs, and periodic access reviews. Any anomalous behaviour is classified as a potential incident until disproven.

**Phase 2 — Contain:** Immediately isolate affected systems or accounts. Suspend suspected API access. Trigger emergency key rotation procedures where compromise is suspected.

**Phase 3 — Assess:** Determine incident scope: which data is affected? What is its classification? Does it include personal data under PDPL definition? Does it include ZATCA invoices?

**Phase 4 — Notify:**
- **Internal:** Immediate notification to the founder.
- **Affected clients:** Notification within 48 hours of confirmation.
- **National Data Management Office (PDPL requirement):** Notification within **72 hours** of discovering a breach involving personal data — per Article 40 of the Personal Data Protection Law.

**Phase 5 — Recover:** Restore service from the last verified backup. Fully document the incident in the incident log. Conduct a post-incident review within 7 days to identify and remediate the root cause.

---

## ٦. مخاطر الأطراف الثالثة — Third-Party Risk

### العربية

- **موافقة معالج البيانات الفرعي:** أي طرف ثالث يُعالج بيانات عملاء Dealix يجب أن يحصل على موافقة مسبقة من المؤسس ويُوثَّق في سجل معالجي البيانات الفرعية.
- **التزام PDPL المادة (29):** جميع المعالجين الفرعيين يُلزَمون بالتوقيع على اتفاقية معالجة بيانات تتضمن التزامات PDPL المكافئة لالتزامات Dealix.
- **مراجعة سنوية:** تُراجع قائمة المعالجين الفرعيين سنوياً مع تجديد اتفاقيات المعالجة عند انتهائها.
- **معالجو البيانات الحاليون (بصفة تقديرية مرحلية):** Railway (استضافة)، AWS S3 (تخزين النسخ الاحتياطية)، Sentry (رصد الأخطاء)، PostHog (تحليلات المنتج)، Moyasar (معالجة المدفوعات).

### English

- **Sub-processor approval:** Any third party that processes Dealix client data must receive prior founder approval and be documented in the sub-processor register.
- **PDPL Article 29 compliance:** All sub-processors are required to sign a data processing agreement containing PDPL obligations equivalent to Dealix's own obligations.
- **Annual review:** The sub-processor list is reviewed annually with data processing agreements renewed upon expiry.
- **Current data processors (indicative, subject to change):** Railway (hosting), AWS S3 (backup storage), Sentry (error monitoring), PostHog (product analytics), Moyasar (payment processing).

---

## ٧. أمن الذكاء الاصطناعي ونماذج اللغة الكبيرة — AI/LLM Security

### العربية

- **لا بيانات شخصية في البرامج النصية (Prompts):** يُحظر إدخال أي بيانات تُعرِّف أشخاصاً بعينهم (PII) في برامج النماذج النصية قبل تطبيق سياسة الحجب (Redaction). راجع [`docs/06_llm_gateway/REDACTION_POLICY.md`](../06_llm_gateway/REDACTION_POLICY.md).
- **سياسة الحجب قبل النموذج:** يُطبَّق حجب PII على جميع المدخلات قبل إرسالها إلى أي نموذج لغوي.
- **حدود تكلفة الذكاء الاصطناعي (Cost Guard):** تُضبط حدود الإنفاق اليومي والشهري لكل نموذج لمنع الاستخدام غير المقصود. راجع [`docs/06_llm_gateway/COST_GUARD.md`](../06_llm_gateway/COST_GUARD.md).
- **موافقة على نشر نماذج جديدة:** تستلزم إضافة أي نموذج لغوي جديد إلى بيئة الإنتاج موافقة المؤسس والتوثيق في سجل النماذج.
- **لا تخزين للمحادثات:** لا تُخزَّن محادثات المستخدمين مع النماذج اللغوية في حالتها الخام خارج فترة المعالجة الفورية، ما لم يكن ذلك ضرورياً لأغراض التدقيق وموثَّقاً.

### English

- **No PII in prompts:** Inputting personally identifiable data into model prompts before applying the redaction policy is prohibited. See [`docs/06_llm_gateway/REDACTION_POLICY.md`](../06_llm_gateway/REDACTION_POLICY.md).
- **Pre-model redaction policy:** PII redaction is applied to all inputs before they are sent to any language model.
- **AI cost guard limits:** Daily and monthly spending limits are set per model to prevent unintended usage. See [`docs/06_llm_gateway/COST_GUARD.md`](../06_llm_gateway/COST_GUARD.md).
- **New model deployment approval:** Adding any new language model to the production environment requires founder approval and documentation in the model registry.
- **No raw conversation storage:** User conversations with language models are not stored in raw form beyond the immediate processing window unless required for audit purposes and explicitly documented.

---

## ٨. التزامات الموظفين — Employee Obligations

### العربية

- **التوعية الأمنية السنوية:** يُكمل جميع الموظفين والمتعاقدين دورة توعية أمنية سنوية. لا يُتاح الوصول لبيانات من المستوى 1 أو 2 دون إتمام الدورة.
- **سياسة المكتب النظيف:** لا تُترك وثائق تحتوي بيانات من المستوى 1 أو 2 مكشوفة على المكتب أو الشاشة عند مغادرة الموظف لمكان عمله.
- **تشفير الأجهزة:** يجب تشفير جميع أجهزة الحاسوب المحمول المستخدمة للوصول إلى بيانات المستوى 1 أو 2 باستخدام تشفير قرص كامل.
- **الإبلاغ الفوري:** يُبلَّغ عن أي حادثة أمنية محتملة أو بيانات في غير موضعها إلى المؤسس فوراً — لا يُؤجَّل الإبلاغ.
- **استخدام الأجهزة الشخصية:** يُحظر تخزين بيانات المستوى 1 على أجهزة شخصية. يُسمح بالوصول عبر المتصفح مع اشتراط 2FA.

### English

- **Annual security awareness:** All employees and contractors complete an annual security awareness session. Access to Level 1 or Level 2 data is not granted without completion.
- **Clean desk policy:** Documents containing Level 1 or Level 2 data must not be left visible on a desk or screen when an employee leaves their workstation.
- **Device encryption:** All laptops used to access Level 1 or Level 2 data must have full-disk encryption enabled.
- **Immediate reporting:** Any suspected security incident or misplaced data must be reported to the founder immediately — reporting must not be delayed.
- **Personal device use:** Storage of Level 1 data on personal devices is prohibited. Browser-based access is permitted with mandatory 2FA.

---

## ٩. التدقيق والامتثال — Audit & Compliance

### العربية

- **مراجعة الوصول الفصلية:** كل ثلاثة أشهر، يُراجع المؤسس قائمة المستخدمين وصلاحياتهم لجميع الأنظمة الحرجة. يُلغى الوصول الزائد أو غير المبرر.
- **اختبار الاختراق السنوي (مخطط):** يُخطَّط لإجراء اختبار اختراق خارجي مرة في السنة اعتباراً من السنة المالية المقبلة. النتائج تُوثَّق وتُعالَج بأولوية.
- **قائمة التحقق من PDPL:** تُراجع الامتثال لمتطلبات PDPL (نظام حماية البيانات الشخصية السعودي) كل ستة أشهر أو عند إضافة عمليات معالجة جديدة.
- **سجل نشاط الوصول:** تُسجَّل عمليات الوصول إلى البيانات من المستوى 1 تلقائياً في سجل التدقيق مع الطابع الزمني وهوية المستخدم.
- **سجل تدوير المفاتيح:** كل عملية تدوير للمفاتيح تُسجَّل في [`docs/security/key_rotation_log.md`](key_rotation_log.md).

### English

- **Quarterly access review:** Every three months, the founder reviews the user list and permissions for all critical systems. Excess or unjustified access is revoked.
- **Annual penetration test (planned):** An external penetration test is planned annually beginning from the next financial year. Findings are documented and remediated on a priority basis.
- **PDPL compliance checklist:** Compliance with Saudi Personal Data Protection Law requirements is reviewed every six months or when new processing activities are added.
- **Access activity log:** Access to Level 1 data is automatically recorded in the audit log with timestamp and user identity.
- **Key rotation log:** Every key rotation event is recorded in [`docs/security/key_rotation_log.md`](key_rotation_log.md).

---

## ١٠. مراجعة السياسة وصلاحيتها — Policy Review & Authority

### العربية

- **دورة المراجعة:** تُراجع هذه السياسة سنوياً في يناير من كل عام، أو فوراً عند أي من الحالات التالية: حادث أمني جوهري، تغيير في متطلبات PDPL أو ZATCA، إضافة خطوط أعمال أو أنظمة جديدة.
- **صلاحية التعديل:** يحتفظ المؤسس بحق التعديل. أي تعديل جوهري يستلزم توقيع المؤسس وتحديث رقم الإصدار.
- **التوزيع:** تُوزَّع السياسة على جميع الموظفين والمتعاقدين عند توقيع عقودهم وعند كل تحديث جوهري.
- **السجل:** تُحفظ النسخ التاريخية في نظام التحكم بالإصدارات (Git).

### English

- **Review cycle:** This policy is reviewed annually each January, or immediately upon any of the following: a material security incident, a change in PDPL or ZATCA requirements, the addition of new business lines or systems.
- **Amendment authority:** The founder retains the right to amend. Any material amendment requires founder sign-off and a version number increment.
- **Distribution:** The policy is distributed to all employees and contractors upon signing their agreements and upon each material update.
- **Record keeping:** Historical versions are retained in version control (Git).

---

## توقيع المؤسس — Founder Sign-Off

| | العربية | English |
|---|---|---|
| الإصدار | 1.0 | Version |
| تاريخ النفاذ | 2026-05-31 | Effective Date |
| تاريخ المراجعة القادمة | يناير 2027 | Next Review Date |
| توقيع المؤسس | _________________________ | Founder Signature |
| التاريخ | _________________________ | Date |

---

## وثائق ذات صلة — Related Documents

- [`docs/security/KEY_ROTATION.md`](KEY_ROTATION.md) — جدول تدوير المفاتيح وإجراءاته
- [`docs/security/key_rotation_log.md`](key_rotation_log.md) — سجل تدوير المفاتيح
- [`docs/06_llm_gateway/REDACTION_POLICY.md`](../06_llm_gateway/REDACTION_POLICY.md) — سياسة حجب البيانات قبل النموذج
- [`docs/06_llm_gateway/COST_GUARD.md`](../06_llm_gateway/COST_GUARD.md) — حدود التكلفة
- [`docs/04_data_os/PII_CLASSIFICATION.md`](../04_data_os/PII_CLASSIFICATION.md) — تصنيف البيانات الشخصية
- [`docs/04_data_os/DATA_RETENTION_POLICY.md`](../04_data_os/DATA_RETENTION_POLICY.md) — سياسة الاحتفاظ بالبيانات
- [`docs/05_governance_os/APPROVAL_POLICY.md`](../05_governance_os/APPROVAL_POLICY.md) — بروتوكول APPROVAL_FIRST
- [`docs/02_saudi_positioning/PDPL_AWARE_LANGUAGE.md`](../02_saudi_positioning/PDPL_AWARE_LANGUAGE.md) — لغة الوعي بـ PDPL
- [`docs/company/PARTNERSHIP_PROGRAM.md`](../company/PARTNERSHIP_PROGRAM.md) — برنامج الشراكة (يشمل التزامات أمنية للشركاء)

---

*القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value*
