# Dealix — Sample Agent Registry — سجل الوكلاء (نموذج)

> Bilingual sample. Customer populates rows during Agentic Control Plane Setup. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.

---

## العربية

### الغرض
يُعرّف Agent Registry كل وكيل AI يعمل داخل المستأجِر: من يملكه، ماذا يستطيع، ما البيانات التي يصل إليها، وما الأدوات المسموح له باستخدامها، وما درجة المخاطر.

### حقول السجل
- **agent_id** — مُعرّف ثابت داخل المستأجِر.
- **owner** — البشر المسؤول، مُسمّى.
- **capabilities** — ما يستطيع الوكيل فعله بكلمات واضحة.
- **data_scope** — مصادر البيانات المسموح بها فقط.
- **tools_allowed** — مرجع إلى Tool Permission Matrix.
- **risk_tier** — T0 منخفض / T1 متوسط / T2 مرتفع / T3 حرج.

### مثال (نموذج)

| agent_id | owner | capabilities | data_scope | tools_allowed | risk_tier |
|---|---|---|---|---|---|
| triage-inbox-01 | `{{ ops_lead }}` | تصنيف وفرز الواردات وتوجيهها لقائمة محدّدة | inbound_email, inbound_whatsapp | classify, summarize | T0 |
| draft-quote-01 | `{{ sales_lead }}` | توليد مسودّة عرض سعر داخلية | crm_accounts, pricing_table | summarize, render_template | T1 |
| evidence-pack-01 | `{{ compliance_lead }}` | بناء Evidence Pack من سجل التشغيل | run_ledger, crm_outcomes | hash_context, fetch_audit | T1 |
| outbound-reply-01 | `{{ founder }}` | إعداد ردود تُرسل بعد موافقة المالك | inbound_thread, account_brief | draft_message | T2 |
| billing-action-01 | `{{ cfo }}` | تنفيذ إجراء فوترة (مغلق افتراضيًا) | zatca_invoices | mutate_invoice_status | T3 |

### قواعد الحوكمة
1. كل وكيل يجب أن يُذكَر بمالك بشر — لا يُسمَح بـ `owner = null`.
2. كل تغيير في `tools_allowed` يستوجب مراجعة وفق [TOOL_PERMISSION_MATRIX_SAMPLE.md](TOOL_PERMISSION_MATRIX_SAMPLE.md).
3. وكلاء T2 وT3 يخضعون لموافقة لكل إجراء.
4. الانحراف يُكتشف شهريًا في تقرير الحوكمة.
5. سحب الوكيل يجري بإلغاء `tools_allowed` فورًا.

---

## English

### Purpose
The Agent Registry defines every AI agent operating inside the tenant: who owns it, what it can do, which data it can access, which tools it may call, and its risk tier.

### Fields
- **agent_id** — stable identifier within the tenant.
- **owner** — named human accountable for the agent.
- **capabilities** — plain-language description of what the agent does.
- **data_scope** — only the data sources allowed.
- **tools_allowed** — pointer into the Tool Permission Matrix.
- **risk_tier** — T0 low / T1 medium / T2 high / T3 critical.

### Example (sample)

| agent_id | owner | capabilities | data_scope | tools_allowed | risk_tier |
|---|---|---|---|---|---|
| triage-inbox-01 | `{{ ops_lead }}` | Classify and route inbound items to a defined queue | inbound_email, inbound_whatsapp | classify, summarize | T0 |
| draft-quote-01 | `{{ sales_lead }}` | Generate an internal quote draft | crm_accounts, pricing_table | summarize, render_template | T1 |
| evidence-pack-01 | `{{ compliance_lead }}` | Build an Evidence Pack from the run ledger | run_ledger, crm_outcomes | hash_context, fetch_audit | T1 |
| outbound-reply-01 | `{{ founder }}` | Prepare replies that are sent only after owner approval | inbound_thread, account_brief | draft_message | T2 |
| billing-action-01 | `{{ cfo }}` | Execute a billing mutation (closed by default) | zatca_invoices | mutate_invoice_status | T3 |

### Governance Rules
1. Every agent must have a named human owner — `owner = null` is not allowed.
2. Any change to `tools_allowed` triggers review per [TOOL_PERMISSION_MATRIX_SAMPLE.md](TOOL_PERMISSION_MATRIX_SAMPLE.md).
3. T2 and T3 agents require per-action approval.
4. Drift is detected monthly in the governance report.
5. Agent retirement is performed by revoking `tools_allowed` immediately.

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
