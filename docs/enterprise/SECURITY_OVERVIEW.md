# Dealix — Security Overview — نظرة عامة على الأمن

> **EN-primary, AR summaries.** A factual summary of Dealix security posture for enterprise procurement and risk review. Where a control is on the roadmap rather than in production, that is stated explicitly. No control is claimed that has not been implemented.
>
> **بالإنجليزية كلغة أصلية، وملخّصات بالعربية.** ملخص واقعي لوضع الأمن في ديلكس لإجراءات المشتريات ومراجعة المخاطر المؤسسية. حيث يكون الضابط في خارطة الطريق لا في الإنتاج، يُذكر ذلك صراحةً. لا ادعاء بضابط غير مُنفَّذ.

---

## 1. Identity & Access — الهوية والوصول

- Single sign-on (SSO) via the customer's identity provider (SAML 2.0 / OIDC) for all human users.
- Service accounts for agents are issued with the minimum required scope and rotated quarterly.
- Role-based access control on every administrative surface; the principle of least privilege is enforced.
- Multi-factor authentication required for any administrative role; mandatory for the Founder-approval surface.
- Session timeouts: 15 minutes idle for privileged sessions; 60 minutes for read-only.

**AR.** تسجيل دخول موحّد عبر مزوّد العميل، حسابات خدمة بأقل صلاحية وتدوير ربعي، تحكم بالأدوار في كل واجهة إدارية، مصادقة متعددة العوامل لكل دور إداري وللواجهة السيادية، ومهل جلسات قصيرة للجلسات المميّزة.

---

## 2. Secrets & Key Management — إدارة الأسرار والمفاتيح

- Credentials and tokens live in an approved vault; never in environment variables that the agent runtime can read.
- Encryption keys are managed in a customer-segregated key hierarchy.
- Rotation schedule: quarterly for tokens; annually for long-lived keys; immediate on suspected exposure.
- No secret value appears in any agent prompt, log entry, or evidence artifact — confirmed by a redaction sweep.

**AR.** أسرار في خزنة معتمدة لا في متغيرات بيئة. هرمية مفاتيح معزولة لكل عميل. تدوير ربعي للرموز وسنوي للمفاتيح طويلة الأمد وفوري عند الاشتباه. لا تظهر أي قيمة سرّ في موجّه أو سجل أو أصل دليل.

---

## 3. Data Residency & PDPL — إقامة البيانات والامتثال

- KSA-first residency is the default for KSA customer engagements: storage, processing, and audit logs remain inside Saudi Arabia.
- PDPL alignment is the default posture: lawful basis, minimization, purpose limitation, retention boundaries, data-subject rights.
- Cross-border flows require Founder-class approval and a documented purpose, logged in the Approval Center.
- Data classification (Public / Internal / Customer-Tenant / Regulated / Secret) is enforced at the tool layer and audited at runtime.

**AR.** الإقامة الافتراضية داخل المملكة لارتباطات السعودية. توافق نظام حماية البيانات افتراضيًا. تدفقات عبر الحدود باعتماد المؤسس وغاية موثّقة. تصنيف البيانات مُنفّذ على طبقة الأدوات ومُدقَّق لحظة التشغيل.

---

## 4. Tenant Isolation — عزل المستأجرين

- Logical isolation per customer tenant across data, configuration, audit logs, and agent identities.
- The MCP gateway enforces tenant scope on every tool call; cross-tenant invocation is denied at policy check.
- Sector aggregation pipelines use methodology and aggregated patterns only; no per-customer identifiers leave the tenant.

**AR.** عزل منطقي لكل مستأجر على البيانات والإعدادات والسجلات وهويات الوكلاء. البوابة تفرض حدود المستأجر على كل نداء أداة، وتُرفض النداءات العابرة. تجميع القطاعات بالمنهجية فقط.

---

## 5. Agent Runtime Sandboxing — حصر بيئة تشغيل الوكلاء

- Agents run inside a sandboxed runtime with explicit network egress allow-lists.
- No filesystem persistence outside designated, audited paths.
- Code execution by an agent is forbidden by default; exceptions are tool-scoped and Founder-approved.
- Runtime telemetry (action attempted, action allowed, action denied) is logged in real time.

**AR.** بيئة تشغيل معزولة بقوائم سماح صريحة للشبكة. لا استمرار على نظام الملفات خارج مسارات معتمدة. تنفيذ الشيفرة محظور افتراضيًا واستثناءاته مقيدة باعتماد المؤسس. تسجيل التيليمتري لحظيًا.

---

## 6. MCP Gateway — بوابة MCP

- Every external tool call passes through the MCP gateway.
- Policy enforcement at the gateway: data class checks, approval class checks, rate limits, cost ceilings.
- Tamper-evident audit log on every invocation (request hash, response hash, actor, action, target, approval reference).
- Kill switch can disable a tool for all agents within five minutes.

**AR.** كل نداء أداة خارجية يمر بالبوابة. إنفاذ السياسة على البوابة: فئة البيانات وفئة الموافقة والمعدلات والسقف التكلفي. سجل تدقيق محصّن، ومفتاح إيقاف ينفذ خلال خمس دقائق.

---

## 7. Audit Logs — سجلات التدقيق

- Append-only, tamper-evident logs with cryptographic signing on a daily roll.
- Captured fields: timestamp, actor, action, target, data class, approval class, approver, payload hash, outcome reference.
- Retention: 7 years for audit logs; per Data Boundaries policy for content data.
- Logs are queryable by the Evidence Pack assembly pipeline and exposed to the customer's executive sponsor.

**AR.** سجلات للإلحاق فقط مع توقيع يومي. حقول: زمن، منفّذ، إجراء، هدف، فئة بيانات، فئة موافقة، معتمد، بصمة الحمولة، مرجع النتيجة. احتفاظ سبع سنوات للسجلات. قابلة للاستعلام من خط حقيبة الأدلة ومتاحة للراعي التنفيذي.

---

## 8. Backup & Disaster Recovery — النسخ الاحتياطي والاستعادة

- Daily encrypted backups of configuration, audit logs, and customer-scoped artifacts.
- Recovery objectives — RPO: 24 hours; RTO: 4 hours for control plane functions, 24 hours for non-critical analytics.
- Quarterly restore drills with documented outcomes filed to the Evidence Pack assembly archive.
- Geographic redundancy within the KSA residency boundary by default.

**AR.** نسخ يومي مُشفَّر للإعدادات والسجلات وأصول المستأجر. أهداف الاستعادة: نقطة 24 ساعة، زمن 4 ساعات للتحكم و24 للتحليلات. تدريبات استعادة ربعية موثّقة. تكرار جغرافي ضمن حدود الإقامة السعودية افتراضيًا.

---

## 9. Vulnerability Handling — التعامل مع الثغرات

- Inbound reports through a published security contact; acknowledged within one business day.
- Triage matrix maps severity to a fix window: S0 within 24 hours, S1 within 7 days, S2 within 30 days, S3 next release cycle.
- Coordinated disclosure with the customer's executive sponsor.
- Public security advisories are published on resolution where appropriate.

**AR.** تقارير واردة عبر جهة اتصال أمنية معلنة، إقرار خلال يوم عمل. مصفوفة فرز تربط الخطورة بنافذة إصلاح: S0 خلال 24 ساعة، S1 خلال 7 أيام، S2 خلال 30 يومًا، S3 في الإصدار التالي. إفصاح منسّق مع الراعي التنفيذي، ونشر تنبيهات عامة عند الحلّ حسب الاقتضاء.

---

## 10. Penetration Testing — اختبار الاختراق

- Cadence: **annual independent test plus on every major release**.
- Scope: agent runtime, MCP gateway, control plane administrative surfaces, customer tenant boundary.
- Findings drive corrective actions tracked to closure in the Evidence Pack archive.
- Customers may request a sanitized summary under NDA.

**AR.** سنوي مستقل + مع كل إصدار رئيسي. النطاق: بيئة الوكلاء، البوابة، واجهات التحكم، حدود مستأجر العميل. النتائج تُدار حتى الإغلاق وتُحفظ في أرشيف الأدلة. للعملاء طلب ملخّص مُعقَّم تحت اتفاقية سرية.

---

## 11. SOC 2 / ISO 27001 Posture — وضع الاعتماد

- **Status: in scope; on the roadmap. Not claimed as obtained today.**
- The control library Dealix operates against today is aligned to the families covered by SOC 2 Type II and ISO 27001 (access control, change management, incident response, vendor risk, monitoring).
- An independent third-party readiness assessment is planned. The attestation timeline is set by the founder office and will be communicated when committed.

**AR.** الحالة: في النطاق وعلى خارطة الطريق، غير مُدَّعى اليوم. مكتبة الضوابط الحالية محاذية لفئات SOC 2 Type II وISO 27001. تقييم جاهزية مستقل مخطّط، والجدول الزمني يحدّده مكتب المؤسس ويُعلَن عند الالتزام.

---

## 12. Customer Responsibilities — مسؤوليات العميل

- Maintain the customer-side identity provider and revoke access on personnel changes.
- Designate and empower an executive sponsor with kill-switch authority.
- Adopt or align with the AI Use Policy template before agent activation.
- Notify Dealix within 24 hours of any suspected incident on the customer side.

**AR.** صيانة مزوّد الهوية وسحب الصلاحيات، تعيين راعٍ تنفيذي بصلاحية مفتاح الإيقاف، اعتماد سياسة الاستخدام قبل التشغيل، وإبلاغ ديلكس خلال 24 ساعة من أي حادثة مشتبه بها لدى العميل.

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.*

Related: `/home/user/dealix/docs/enterprise/GOVERNANCE_MODEL.md` · `/home/user/dealix/docs/trust/DATA_BOUNDARIES_SAMPLE.md` · `/home/user/dealix/docs/trust/MCP_REVIEW_CHECKLIST.md`
