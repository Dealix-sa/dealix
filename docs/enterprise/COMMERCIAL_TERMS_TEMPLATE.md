# Dealix — Commercial Terms — Template — قالب الشروط التجارية

> **Template only — not a legal contract.** This document is the structural template Dealix uses to assemble Commercial Terms for an enterprise engagement. Final contractual language is produced under legal review and executed by both parties. Customer-specific values replace the placeholders below.
>
> **قالب فقط — ليس عقدًا قانونيًا.** هذه الوثيقة قالب يستخدمه ديلكس لتجميع الشروط التجارية للارتباطات المؤسسية. الصياغة العقدية النهائية تُنتج بمراجعة قانونية ويوقّعها الطرفان. تُستبدل القيم الخاصة بالعميل بدلًا من المحجوزات أدناه.

---

## 1. Parties & Scope — الأطراف والنطاق

- **Provider:** Dealix (Saudi Arabia).
- **Customer:** [Customer A / شركة عميل أ].
- **Engagement reference:** [ENG-ID].
- **Scope memo:** Attached as Schedule 1; this template defers to the scope memo for activity boundaries.
- **Workflows in scope:** [Workflow A, B, C] — as enumerated in the Agent Registry v1.

**AR.** الطرفان: ديلكس و[شركة عميل أ]. مرجع الارتباط: [ENG-ID]. مذكرة النطاق مُلحَقة كجدول 1، ويُحال إليها لتحديد حدود النشاط. سير العمل ضمن النطاق محصور بما هو مُدرَج في سجل الوكلاء v1.

---

## 2. Pricing Tiers — فئات التسعير

| Component | Cadence | Range (SAR) | Notes |
|---|---|---|---|
| Discovery Week | one-time | per Offer Catalogue | Output: Discovery Memo + 60-day roadmap |
| Agentic Control Plane Setup | one-time | per Offer Catalogue | Sponsor-signed gate at Phase 1 exit |
| Governance OS Retainer | monthly | per Offer Catalogue | Includes Evidence Pack cadence + board reporting |
| Workflow Build (per workflow) | one-time | scoped per workflow | Founder approval if data class is Regulated |
| Expansion (post Day 90) | per workflow | scoped per workflow | Routed through Expansion Playbook |

Pricing ranges reference `/home/user/dealix/docs/business/OFFER_CATALOG.json`. Final figures are filled at signature.

**AR.** المراجع للنطاقات في كاتالوج العروض، والأرقام النهائية تُدرج عند التوقيع.

---

## 3. Payment Terms — شروط الدفع

- **Currency.** Saudi Riyal (SAR) by default. Other currencies require Founder approval.
- **Setup.** 50% on signature; 50% on Phase 1 exit gate confirmation.
- **Retainer.** Monthly in advance, due on the first business day of each month.
- **Workflow Build.** 40% on workflow scope sign-off; 40% on runtime governance activation; 20% on Evidence Pack delta delivery.
- **Late fee.** 2% per month after 30 days net.
- **Refunds.** No retroactive refunds. Disputes are resolved by re-scoping or by an additional Evidence Pack at no charge.

**AR.** العملة الافتراضية الريال السعودي. التأسيس 50/50 عند التوقيع وبوابة المرحلة الأولى. الاشتراك شهريًا مقدمًا في أول يوم عمل. بناء سير العمل 40/40/20. غرامة تأخير 2٪ شهريًا بعد 30 يومًا صافيًا. لا استرداد بأثر رجعي.

---

## 4. Data Residency Commitments — التزامات إقامة البيانات

- **Default.** KSA residency for storage, processing, and audit logs for KSA customer engagements.
- **Cross-border.** Any deviation requires Founder-class approval and is recorded in the Approval Center with a documented purpose.
- **Customer audit right.** The Customer may inspect residency posture quarterly and on request.
- **Customer data classes.** Public, Internal, Customer-Tenant, Regulated, Secret — handled per the Data Boundaries policy.

**AR.** الإقامة الافتراضية داخل المملكة، وأي انحراف باعتماد المؤسس وتوثيق غرضه. للعميل حق التفتيش ربعيًا وعند الطلب. فئات البيانات تُعامل وفق سياسة الحدود.

---

## 5. Kill-Switch SLA — مستوى خدمة مفتاح الإيقاف

- **Invocation channel.** The Customer's executive sponsor may invoke the kill switch on any agent or tool through the documented channel.
- **Freeze time.** Within five minutes of invocation, the affected agent or tool ceases to operate across all in-flight invocations.
- **Evidence delta.** A kill-switch event automatically produces an Evidence Pack delta entry within one business day.
- **Drill cadence.** Quarterly end-to-end drill, results recorded.

**AR.** للراعي التنفيذي تفعيل مفتاح الإيقاف عبر القناة الموثّقة. التجميد خلال خمس دقائق على كل النداءات الجارية. إضافة دليل خلال يوم عمل واحد. تدريب ربعي موثّق.

---

## 6. Evidence Pack Delivery Cadence — دورة تسليم حقيبة الأدلة

- **Per engagement.** Evidence Pack v1 at Phase 2 exit gate.
- **Quarterly.** Delta + refresh, founder-signed, delivered to the executive sponsor.
- **Event-driven.** Delta on any S0 or S1 incident within five business days of resolution.
- **Format.** Standardized per `EVIDENCE_PACK_SAMPLE.md` plus structured JSON outcome graph.

**AR.** الإصدار الأول عند بوابة المرحلة الثانية. ربعي مع تحديث وتوقيع المؤسس. حدثي عند أي حادثة S0 أو S1 خلال خمسة أيام عمل من الإغلاق. التنسيق وفق العيّنة المُعتمدة + رسم النتائج بصيغة JSON.

---

## 7. Change Management — إدارة التغيير

- **Scope changes** are documented as Schedule 1 amendments and signed by both parties.
- **Discount requests** follow the No-Discount-Without-Evidence-Pack rule and require Founder approval for enterprise tiers.
- **New MCP tools** pass the MCP Review Checklist and are added to the Tool Permission Matrix by Founder approval.
- **Pricing increases** at renewal require written notice 60 days in advance.

**AR.** تغييرات النطاق تُوثَّق كتعديلات للجدول 1 ويوقّعها الطرفان. طلبات الخصم وفق قاعدة لا خصم بلا حقيبة أدلة، وفي فئات المؤسسات تستوجب اعتماد المؤسس. أدوات MCP الجديدة تمرّ عبر قائمة المراجعة وتُضاف بالاعتماد. زيادات التسعير عند التجديد بإشعار 60 يومًا.

---

## 8. Exit & Data Return — الخروج وإعادة البيانات

On termination or expiry:
- Customer-Tenant data is exported to the Customer's approved storage in encrypted form within 30 days.
- Audit logs are exported with cryptographic integrity within 60 days.
- The Customer retains ownership of all assets produced for the engagement (policies, registries, matrices, evidence packs).
- Dealix retains aggregated, methodology-only patterns for sector reporting; no per-customer metrics.

**AR.** عند الإنهاء أو الانقضاء: تُصدَّر بيانات مستأجر العميل إلى تخزينه المعتمد مُشفَّرة خلال 30 يومًا. تُصدَّر سجلات التدقيق بسلامة تشفيرية خلال 60 يومًا. يحتفظ العميل بملكية الأصول المُنتجة (السياسات والسجلات والمصفوفات والأدلة). يحتفظ ديلكس بأنماط منهجية مُجمَّعة للتقارير القطاعية، بلا مؤشرات فردية للعميل.

---

## 9. Intellectual Property — الملكية الفكرية

- **Customer-specific artifacts** (policies, registries, configurations, evidence packs) belong to the Customer on payment.
- **Dealix platform IP** (control plane software, gateway, runtime, reusable patterns) remains with Dealix.
- **Joint know-how** produced during the engagement may be reused by Dealix in methodology and pattern libraries, redacted of Customer identifiers.

**AR.** أصول العميل ملكه عند الدفع. ملكية المنصة لديلكس. المعرفة المشتركة يجوز إعادة استخدامها كأنماط بعد التعمية.

---

## 10. Confidentiality — السرية

- Mutual confidentiality covers technical, commercial, and audit information shared during the engagement.
- Confidentiality survives termination for three years on commercial information and indefinitely on data-subject content.
- Sector reports use methodology and aggregated patterns only; no confidential Customer metrics are published.

**AR.** سرية متبادلة على المعلومات الفنية والتجارية والتدقيقية. تستمر ثلاث سنوات على التجارية وبلا أجل على بيانات الأشخاص. تقارير القطاعات بالمنهجية والأنماط فقط.

---

## 11. Founder-Approval Clauses — بنود اعتماد المؤسس

The following require recorded Founder approval (Dealix side: Sami; Customer side: the executive sponsor or delegated authority):

1. Discounts on enterprise tiers.
2. Scope changes that touch data boundaries, residency, or kill-switch ownership.
3. New MCP servers or external tools.
4. Cross-tenant or cross-border data flows.
5. Code execution by agents on non-sandboxed surfaces.
6. Modifications to the Tool Permission Matrix that lower an approval class.

These clauses are non-negotiable on the Dealix side.

**AR.** بنود تستوجب اعتماد المؤسس: خصومات فئات المؤسسات؛ تغييرات النطاق على الحدود والإقامة وملكية الإيقاف؛ خوادم MCP وأدوات جديدة؛ تدفقات عابرة بين المستأجرين أو الحدود؛ تنفيذ الشيفرة خارج الصندوق الرملي؛ تخفيض فئات الاعتماد في المصفوفة. غير قابلة للتفاوض من جانب ديلكس.

---

## 12. MSA Placeholder — موضع اتفاقية الإطار

A Master Services Agreement (MSA) executes between the Parties and governs:
- Governing law and jurisdiction (KSA-default).
- Limitation of liability.
- Insurance and indemnities.
- Force majeure.
- Dispute resolution path (negotiation → mediation → arbitration).

This template defers entirely to the MSA for those clauses; the MSA prevails on any conflict.

**AR.** تُبرَم اتفاقية إطار خدمات (MSA) بين الطرفين وتحكم: القانون الواجب التطبيق والاختصاص (السعودية افتراضًا)، تحديد المسؤولية، التأمين والتعويض، القوة القاهرة، ومسار النزاع (تفاوض ثم وساطة ثم تحكيم). يُحال إلى MSA عند أي تعارض.

---

## 13. Acceptance — القبول

This template is converted into a signed Commercial Terms document upon completion of:
- Scope memo (Schedule 1).
- Pricing fill-ins (Schedule 2).
- Data Boundaries amendments specific to the Customer (Schedule 3).
- Executive sponsor designation (Schedule 4).
- Founder-approval routing acknowledgement (Schedule 5).

**AR.** يُحوَّل هذا القالب إلى وثيقة شروط موقّعة عند استكمال: مذكرة النطاق (جدول 1)، تعبئة الأسعار (جدول 2)، تعديلات حدود البيانات الخاصة بالعميل (جدول 3)، تعيين الراعي التنفيذي (جدول 4)، وإقرار مسار اعتماد المؤسس (جدول 5).

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.*

Related: `/home/user/dealix/docs/business/PRICING_RULES.md` · `/home/user/dealix/docs/business/OFFER_CATALOG.json` · `/home/user/dealix/docs/enterprise/IMPLEMENTATION_PLAN.md`
