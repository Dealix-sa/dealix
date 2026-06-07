# Compliance Pack — حزمة الامتثال

<!-- Arabic primary | NO_LIVE_SEND | draft_only | NOT legal advice -->

**عربي:** هذه الوثيقة إرشاد تشغيلي للتواصل التجاري في السعودية، **وليست استشارة قانونية**. اعتمدها مع مراجعة مسؤول حماية البيانات (DPO) أو محامٍ مختص قبل أي حملة. الأساس: نظام حماية البيانات الشخصية (PDPL) ولوائحه.

**EN:** This document is operational guidance for business communication in Saudi Arabia, **not legal advice**. Adopt it only with review by a Data Protection Officer (DPO) or qualified lawyer before any campaign. Basis: the Personal Data Protection Law (PDPL) and its regulations.

روابط / Links: [../../commercial/FOUNDER_PDPL_COMPLIANCE_PASS_AR.md](../../commercial/FOUNDER_PDPL_COMPLIANCE_PASS_AR.md) · [../../ops/PDPL_CLOSURE_CHECKLIST_AR.md](../../ops/PDPL_CLOSURE_CHECKLIST_AR.md) · [../04_marketer_enablement/MARKETER_FIELD_MANUAL.md](../04_marketer_enablement/MARKETER_FIELD_MANUAL.md) · [../05_outreach/OUTREACH_SCRIPTS.md](../05_outreach/OUTREACH_SCRIPTS.md) · [../08_repo_automation/REPO_AUTOMATION_SPEC.md](../08_repo_automation/REPO_AUTOMATION_SPEC.md) · [../09_dashboards/](../09_dashboards/)

---

## أساسيات PDPL للتسويق المباشر B2B / PDPL Essentials for B2B Direct Marketing

**عربي:** التواصل التجاري B2B يقوم على **أساس مصلحة مشروعة** (`legitimate_interest_b2b`) عند مخاطبة جهة عمل عبر بيانات تواصل تجارية عامة، أو على **موافقة** صريحة حين تتوفّر. التزم بـ:
- **تحديد الغرض:** اجمع واستخدم البيانات لغرض التواصل التجاري المعلن فقط.
- **تقليل البيانات:** جهة تواصل عمل فقط — لا بيانات حساسة، لا هوية وطنية.
- **الشفافية:** عرّف بنفسك والغرض في أول رسالة.

**EN:** B2B business communication rests on a **legitimate interest basis** (`legitimate_interest_b2b`) when addressing a business via public business contact data, or on explicit **consent** where available. Maintain:
- **Purpose limitation:** collect and use data only for the stated business-communication purpose.
- **Data minimization:** business contact only — no sensitive data, no national ID.
- **Transparency:** identify yourself and the purpose in the first message.

---

## معالجة الإيقاف وحفظ السجلات / Opt-out Handling and Record-keeping

**عربي:** كل رسالة تحمل سطر إيقاف واضح («رد بكلمة (إيقاف)» / «Reply STOP»). عند ورود طلب إيقاف:
- نفّذه **فوراً** ولا تكرّر التواصل.
- سجّله في `notes=opt_out` وحوّل الفرصة إلى `lost` (انظر آلة الحالة في [REPO_AUTOMATION_SPEC.md](../08_repo_automation/REPO_AUTOMATION_SPEC.md)).
- احتفظ بسجل تاريخ الطلب وقناته للمساءلة.

**EN:** Every message carries a clear opt-out line ("Reply STOP" / «رد بكلمة (إيقاف)»). When an opt-out arrives:
- Honor it **immediately** and do not contact again.
- Log it as `notes=opt_out` and move the lead to `lost` (see the state machine in [REPO_AUTOMATION_SPEC.md](../08_repo_automation/REPO_AUTOMATION_SPEC.md)).
- Keep a record of the request's date and channel for accountability.

---

## تقليل البيانات / Data Minimization

**عربي:** نخزّن جهة تواصل الأعمال فقط (اسم الشركة، الدور الوظيفي، قناة تواصل عمل). **لا** نخزّن هوية وطنية، بيانات صحية أو مالية شخصية، أو أي بيانات حساسة. الأمثلة في كل وثائقنا تستخدم «Example Trading Co» بلا PII.

**EN:** We store business contact only (company name, job role, a business contact channel). We do **not** store national ID, personal health or financial data, or any sensitive data. Examples throughout our docs use "Example Trading Co" with no PII.

---

## المصادر المسموحة مقابل الممنوعة / Allowed vs Forbidden Sourcing

**عربي:**
- **مسموح:** السجلات العامة، الإعلانات الرسمية، إشارات المؤسسين المعلنة، العطاءات المنشورة — يُوثَّق في `source_type`.
- **ممنوع:** الكشط (scraping)، القوائم المشتراة، استخراج البيانات الآلي، أي مصدر غير معلن أو غير مشروع.

**EN:**
- **Allowed:** public registries, official announcements, publicly stated founder signals, published tenders — recorded in `source_type`.
- **Forbidden:** scraping, purchased lists, automated data harvesting, any undisclosed or unlawful source.

---

## سجل أساس الموافقة / Record of consent_basis

**عربي:** كل صف في [../09_dashboards/](../09_dashboards/) يحمل عمود `consent_basis`. للتواصل التجاري B2B القيمة `legitimate_interest_b2b`، وعند الموافقة الصريحة `consent`. الصف بلا `consent_basis` لا يتقدّم في القمع.

**EN:** Every row in [../09_dashboards/](../09_dashboards/) carries a `consent_basis` column. For B2B business contact the value is `legitimate_interest_b2b`; with explicit consent, `consent`. A row without `consent_basis` does not advance in the funnel.

---

## بوابة الموافقة قبل الإرسال / The Approval Gate Before Any Send

**عربي:** مبدأ **NO_LIVE_SEND**: لا تخرج أي رسالة دون موافقة بشرية مسجّلة عبر `approval_center` (`approval_status="approval_required"` افتراضاً). لا أتمتة، لا إرسال جماعي، لا تواصل بارد. التفاصيل في [OUTREACH_SCRIPTS.md](../05_outreach/OUTREACH_SCRIPTS.md).

**EN:** The **NO_LIVE_SEND** principle: no message leaves without recorded human approval via `approval_center` (`approval_status="approval_required"` by default). No automation, no bulk, no cold contact. Details in [OUTREACH_SCRIPTS.md](../05_outreach/OUTREACH_SCRIPTS.md).

---

## قائمة فحص الامتثال / Compliance Checklist

**عربي:**
- [ ] `consent_basis` مسجّل لكل شركة (B2B = legitimate_interest_b2b).
- [ ] `source_type` مصدر عام مسموح به موثّق.
- [ ] لا هوية وطنية ولا بيانات حساسة مخزّنة.
- [ ] كل رسالة تحمل سطر إيقاف وتعريفاً بالمرسل والغرض.
- [ ] موافقة `approval_center` مسجّلة قبل أي إرسال.
- [ ] طلبات الإيقاف منفّذة فوراً ومسجّلة.
- [ ] متابعة واحدة فقط ثم توقّف.
- [ ] راجعت DPO/محامٍ قبل أي حملة موسّعة.

**EN:**
- [ ] `consent_basis` recorded per company (B2B = legitimate_interest_b2b).
- [ ] `source_type` is a documented allowed public source.
- [ ] No national ID or sensitive data stored.
- [ ] Every message carries an opt-out line and identifies sender and purpose.
- [ ] `approval_center` approval recorded before any send.
- [ ] Opt-out requests honored immediately and logged.
- [ ] One follow-up only, then stop.
- [ ] DPO/lawyer reviewed before any broad campaign.

---

> القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
