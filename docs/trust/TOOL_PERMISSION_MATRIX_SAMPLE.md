# Dealix — Sample Tool Permission Matrix — مصفوفة صلاحيات الأدوات (نموذج)

> Bilingual sample. Rows are tools; columns are agents; cells declare `allowed | approval_required | denied`. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.

---

## العربية

### الغرض
يفرض هذا المرجع ما يستطيع كل وكيل استدعاءه. الافتراض الأساسي **deny**؛ لا أداة تعمل ما لم تكن مسموحة صراحةً.

### الترميز
- `allowed` — مسموح بدون موافقة.
- `approval_required` — مسموح بعد موافقة مالك مُسمّى.
- `denied` — ممنوع منعًا باتًا.

### المصفوفة (نموذج)

| tool \\ agent | triage-inbox-01 | draft-quote-01 | evidence-pack-01 | outbound-reply-01 | billing-action-01 |
|---|---|---|---|---|---|
| classify | allowed | allowed | denied | allowed | denied |
| summarize | allowed | allowed | allowed | allowed | denied |
| render_template | denied | allowed | denied | allowed | denied |
| hash_context | denied | denied | allowed | denied | denied |
| fetch_audit | denied | denied | allowed | denied | allowed |
| draft_message | denied | denied | denied | approval_required | denied |
| send_external_email | denied | denied | denied | approval_required | denied |
| send_external_whatsapp | denied | denied | denied | approval_required | denied |
| mutate_crm_record | denied | approval_required | denied | denied | denied |
| mutate_invoice_status | denied | denied | denied | denied | approval_required |
| run_shell | denied | denied | denied | denied | denied |
| web_scrape | denied | denied | denied | denied | denied |

### قواعد الفرض
1. أي تعديل على خلية يولّد إدخالًا في AI Run Ledger.
2. خلايا `approval_required` تستوجب اسم المُوافق ووقت الموافقة.
3. خلايا `denied` لا تُتجاوز بواسطة دور تقني — الاستثناء يُعالَج بإصدار سياسة جديد.
4. مراجعة فصلية لكامل المصفوفة، ومراجعة فورية عند أي حادث.

---

## English

### Purpose
This matrix enforces what each agent is allowed to call. Default is **deny**; no tool runs unless explicitly allowed.

### Codes
- `allowed` — runs without approval.
- `approval_required` — runs only after a named owner approves.
- `denied` — never allowed.

### Matrix (sample)

| tool \\ agent | triage-inbox-01 | draft-quote-01 | evidence-pack-01 | outbound-reply-01 | billing-action-01 |
|---|---|---|---|---|---|
| classify | allowed | allowed | denied | allowed | denied |
| summarize | allowed | allowed | allowed | allowed | denied |
| render_template | denied | allowed | denied | allowed | denied |
| hash_context | denied | denied | allowed | denied | denied |
| fetch_audit | denied | denied | allowed | denied | allowed |
| draft_message | denied | denied | denied | approval_required | denied |
| send_external_email | denied | denied | denied | approval_required | denied |
| send_external_whatsapp | denied | denied | denied | approval_required | denied |
| mutate_crm_record | denied | approval_required | denied | denied | denied |
| mutate_invoice_status | denied | denied | denied | denied | approval_required |
| run_shell | denied | denied | denied | denied | denied |
| web_scrape | denied | denied | denied | denied | denied |

### Enforcement Rules
1. Any cell change generates an AI Run Ledger entry.
2. `approval_required` cells must record approver identity and timestamp.
3. `denied` cells are not bypassable by any technical role — exceptions require a new policy revision.
4. Quarterly full-matrix review; immediate review after any incident.

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
