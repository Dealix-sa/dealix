# Dealix — Security Overview — نظرة الأمن

> Bilingual security overview for enterprise procurement. Not a substitute for a signed DPA. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.

---

## العربية

### 1. النموذج
نموذج Dealix الأمني مبني على ثلاث طبقات: **العزل** (مستأجِر منفصل)، **التحكم** (مصفوفة صلاحيات أدوات وموافقات)، و**التدقيق** (AI Run Ledger مع context_hash).

### 2. الهوية والوصول
- مصادقة عبر SSO/OIDC في المؤسسات.
- مفاتيح ذات أعمار قصيرة.
- صلاحيات تستند إلى أدوار، والافتراض هو **deny**.
- جلسات معزولة لكل مستأجِر.

### 3. تشفير البيانات
- **في النقل**: TLS فقط.
- **في الراحة**: تشفير على مستوى التخزين.
- مفاتيح العميل مفصولة لكل مستأجِر.

### 4. عزل المستأجِر
- قواعد بيانات منطقية معزولة.
- مفاتيح API مفصولة.
- لا مشاركة موجِّهات (prompts) بين المستأجرين.
- AI Run Ledger مفصول لكل مستأجِر.

### 5. الامتثال
- **PDPL** — مواد 5، 13، 14، 18، 21، 32 مدمجة في الكود.
- **ZATCA المرحلة 2** — حقول الفاتورة الإلكترونية مُولَّدة وفق المواصفات.
- **SDAIA** — توافق مع توجيهات حوكمة الذكاء الاصطناعي.
- **ISO 27001** — مخطط لـ H2 2027-2028.

### 6. السجلّ والمراقبة
- AI Run Ledger يسجل كل تشغيل وكيل.
- محاولات الوصول المرفوضة مُسجَّلة.
- إنذارات تشغيلية على الحدود المُعرَّفة.

### 7. سلسلة التوريد البرمجية
- التبعيات مُثبَّتة الإصدارات.
- مسح أمني دوري على المستودع.
- لا تنفيذ كود خارجي ديناميكي.

### 8. الاستجابة للحوادث
انظر [`../trust/INCIDENT_RESPONSE_SAMPLE.md`](../trust/INCIDENT_RESPONSE_SAMPLE.md).

### 9. كشف الثغرات
قناة `dpo@dealix.me`. نقدّر الإفصاح المسؤول. لا نتسامح مع شروط احتجاز.

### 10. الحدود الأمنية المنصوصة
- لا scraping.
- لا أتمتة WhatsApp/LinkedIn.
- لا إرسال خارجي بدون موافقة.
- لا تنفيذ shell من قبل وكيل.

---

## English

### 1. Model
The Dealix security model rests on three layers: **isolation** (separate tenant), **control** (tool permission matrix and approvals), and **audit** (AI Run Ledger with context_hash).

### 2. Identity and Access
- Enterprise authentication via SSO/OIDC.
- Short-lived keys.
- Role-based access; default is **deny**.
- Isolated sessions per tenant.

### 3. Data Encryption
- **In transit**: TLS only.
- **At rest**: storage-level encryption.
- Customer keys separated per tenant.

### 4. Tenant Isolation
- Logically isolated databases.
- Separated API keys.
- No prompt sharing across tenants.
- Per-tenant AI Run Ledger.

### 5. Compliance
- **PDPL** — Articles 5, 13, 14, 18, 21, 32 wired in code.
- **ZATCA Phase 2** — e-invoice fields generated to spec.
- **SDAIA** — aligned with AI governance guidance.
- **ISO 27001** — planned for H2 2027-2028.

### 6. Logging and Monitoring
- AI Run Ledger records every agent run.
- Denied access attempts logged.
- Operational alerts on defined thresholds.

### 7. Software Supply Chain
- Pinned dependency versions.
- Periodic security scan of the repository.
- No dynamic external code execution.

### 8. Incident Response
See [`../trust/INCIDENT_RESPONSE_SAMPLE.md`](../trust/INCIDENT_RESPONSE_SAMPLE.md).

### 9. Vulnerability Disclosure
Channel: `dpo@dealix.me`. Responsible disclosure honored. No retention clauses imposed.

### 10. Explicit Security Boundaries
- No scraping.
- No WhatsApp/LinkedIn automation.
- No external sends without approval.
- No shell execution by agents.

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
