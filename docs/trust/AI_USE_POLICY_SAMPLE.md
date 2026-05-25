# AI Use Policy — Sample — سياسة استخدام الذكاء الاصطناعي (عيّنة)

> **Sample — adapt to your company.** This template is provided by Dealix as a starting point. Replace bracketed entries with your own and route the final version through your legal, risk, and executive review. Adoption is the customer's decision.
>
> **عيّنة — تُكيَّف وفق الشركة.** هذا القالب من ديلكس كنقطة بدء. استبدل المحجوز بمعلوماتك ووجّه النسخة النهائية إلى المراجعة القانونية والمخاطر والتنفيذ. التبنّي قرار العميل.

---

## 1. Purpose — الغرض

To define how [Customer A / شركة عميل أ] permits the use of AI systems — including generative models, AI agents, and AI-enabled tooling — across its workforce, contractors, and automated workflows, while maintaining compliance with the Personal Data Protection Law (PDPL), customer trust, and operational sovereignty.

تحديد كيف تُجيز [شركة عميل أ] استخدام أنظمة الذكاء الاصطناعي — بما فيها النماذج التوليدية ووكلاء الذكاء الاصطناعي والأدوات المُمكَّنة بالذكاء الاصطناعي — للموظفين والمتعاقدين وسير العمل المؤتمت، مع الحفاظ على الامتثال لنظام حماية البيانات الشخصية وثقة العملاء والسيادة التشغيلية.

---

## 2. Scope — النطاق

Applies to:
- All employees and contractors of [Customer A].
- All AI agents deployed by [Customer A] or by approved vendors on its behalf.
- All AI-enabled features embedded in tooling that touches customer data or operational systems.

يشمل: جميع موظفي ومتعاقدي [شركة عميل أ]، وكل وكلاء الذكاء الاصطناعي المنشورين من قِبلها أو من قِبل موردين معتمدين بالنيابة عنها، وكل ميزات الذكاء الاصطناعي المضمّنة في الأدوات التي تلامس بيانات العميل أو الأنظمة التشغيلية.

---

## 3. Permitted Use Cases — حالات الاستخدام المسموح بها

- Drafting internal documents and reports from internal-only inputs.
- Summarizing public sources for research with explicit citation.
- Routing internal requests within approved workflows under the Runtime Governance Loop.
- Generating proposal drafts that are reviewed by a named human approver before any external delivery.
- Producing analytics on data classified as Public or Internal.

يُسمح بـ: صياغة الوثائق الداخلية، تلخيص المصادر العامة مع الاستشهاد، توجيه الطلبات الداخلية ضمن سير عمل معتمد، صياغة مسوّدات العروض بمراجعة بشرية قبل أي إرسال خارجي، وإنتاج التحليلات على بيانات مصنّفة عامة أو داخلية.

---

## 4. Prohibited Use Cases — حالات الاستخدام المحظورة

- Sending external communication on the customer's behalf without explicit written approval and an approved channel.
- Cold outreach automation (cold email, cold WhatsApp, LinkedIn automation, scraping).
- Writing to money systems (payments, refunds, ledger) without a recorded Founder-class approval.
- Sharing Regulated or Secret data with any model or tool outside the approved boundary.
- Cross-tenant data flows of any kind.
- Modification of contractual terms by an agent without a named human signatory.

يُحظر: الإرسال الخارجي بالنيابة عن العميل دون اعتماد كتابي وقناة معتمدة، أتمتة التواصل البارد، الكتابة في أنظمة المال بدون اعتماد فئة المؤسس، مشاركة البيانات المُنظَّمة أو السرية مع أي نموذج خارج الحدود المعتمدة، التدفقات العابرة بين المستأجرين، وتعديل شروط العقود بواسطة وكيل بلا موقّع بشري مُسمّى.

---

## 5. Data Classes & Boundaries — فئات البيانات والحدود

| Class | Examples | AI Handling |
|---|---|---|
| Public | Marketing pages, public reports | Free use within policy. |
| Internal | Memos, internal SOPs | Use within approved tools only. |
| Customer-Tenant | Customer-owned records | Only within the customer's tenant boundary; no cross-tenant access. |
| Regulated | PDPL personal data, financial records | Redaction required; named approver for any model exposure. |
| Secret | Credentials, keys, board materials | Never exposed to any model; vault-only access. |

---

## 6. Approval Workflow — مسار الموافقات

Sensitive actions are routed through approval classes:
- **Auto** — low-risk, policy-conformant actions; logged but not interrupted.
- **Reviewer** — actions reviewed by a named human operator before execution.
- **Founder** — actions requiring the executive sponsor (or, for Dealix engagements, Sami) before execution.
- **Board** — actions reserved for the board or risk committee.

الإجراءات الحسّاسة تمر بفئات موافقة: تلقائي، مراجع، مؤسس، مجلس.

---

## 7. Audit & Evidence — التدقيق والأدلة

Every privileged action is logged with: actor, action, target, data class, approval class, approver, timestamp, and outcome reference. Logs are retained per the residency and retention rules in the Data Boundaries document. Evidence Packs are produced per engagement and per quarterly review.

كل إجراء ذي امتياز يُسجَّل مع: المنفّذ، الإجراء، الهدف، فئة البيانات، فئة الموافقة، المُعتمد، الطابع الزمني، ومرجع النتيجة. تُحفظ السجلات وفق قواعد الإقامة والاحتفاظ، وتُصدَر حقائب الأدلة لكل ارتباط ولكل مراجعة ربعية.

---

## 8. Kill Switch & Incident Escalation — مفتاح الإيقاف وتصعيد الحوادث

- Every agent has a documented kill switch with a named owner.
- Any team member may raise an incident; on-call ownership escalates per the Incident Response runbook.
- The kill switch is exercised whenever there is reasonable doubt about an agent's behavior — the cost of pause is always lower than the cost of an unsafe action.

لكل وكيل مفتاح إيقاف بمالك مُسمّى. يحق لأي عضو رفع حادثة، ويصعّد المسؤول وفق دليل الاستجابة. يُستخدم مفتاح الإيقاف عند أي شك معقول — تكلفة الإيقاف أقل دومًا من تكلفة إجراء غير آمن.

---

## 9. Review Cadence — دورية المراجعة

- Quarterly internal review of policy, registry, and permission matrix.
- Annual third-party review (planned; on the roadmap).
- Out-of-cycle review on any S0 or S1 incident.

مراجعة ربعية داخلية، ومراجعة طرف ثالث سنوية (مُخطَّطة)، ومراجعة خارج الدورة عند أي حادثة S0 أو S1.

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.*

Related: `/home/user/dealix/docs/trust/AGENT_REGISTRY_SAMPLE.md` · `/home/user/dealix/docs/trust/TOOL_PERMISSION_MATRIX_SAMPLE.md` · `/home/user/dealix/docs/trust/INCIDENT_RESPONSE_SAMPLE.md`
