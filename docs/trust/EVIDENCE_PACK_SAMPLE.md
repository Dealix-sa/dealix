# Dealix — Sample Evidence Pack — حزمة الإثبات (نموذج)

> Bilingual reference. An Evidence Pack is the unit of proof that converts a claimed outcome into a verified outcome. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.

---

## العربية

### الغرض
يُوثّق Evidence Pack قرار AI واحد أو حدث إيراد واحد بشكل قابل للتدقيق. لا إيراد يُحتسب «مُتحقَّقًا» بدون حزمة كاملة.

### المكوّنات الثمانية
1. **intent** — ما الذي طلبه المستخدم أو الإجراء التشغيلي، مكتوب بلغة طبيعية.
2. **context_hash** — بصمة سياق التشغيل: الموجّهات، الإصدار، نطاق البيانات.
3. **tool_calls** — تسلسل استدعاءات الأدوات مع البارامترات (بدون PII).
4. **outputs** — المخرج النهائي للوكيل قبل أي إجراء خارجي.
5. **approvals** — قائمة المُوافقين، الأدوار، الطوابع الزمنية.
6. **audit_log** — أحداث AI Run Ledger ذات الصلة (PDPL 5/13/14/18/21/32).
7. **outcome** — الحدث المُسجَّل في النظام التشغيلي (CRM/ZATCA/Calendar).
8. **revenue_link** — رابط إلى الفاتورة أو العقد الذي ينسب الإيراد لهذا التشغيل.

### هيكل JSON (نموذج)
```json
{
  "evidence_pack_id": "ep_2026_05_25_0001",
  "tenant_id": "{{ tenant }}",
  "intent": "Draft a renewal quote for account A-127 and send after owner approval",
  "context_hash": "sha256:7c92...e3",
  "tool_calls": [
    {"tool": "summarize", "agent": "draft-quote-01", "duration_ms": 412},
    {"tool": "render_template", "agent": "draft-quote-01", "duration_ms": 88},
    {"tool": "draft_message", "agent": "outbound-reply-01", "duration_ms": 215}
  ],
  "outputs": {
    "artifact": "quote_A127_v3.pdf",
    "checksum": "sha256:ab12...f9"
  },
  "approvals": [
    {"approver": "sales_lead", "decision": "approved", "ts": "2026-05-25T09:14:22Z"}
  ],
  "audit_log": ["pdpl_art_13_consent_logged", "ai_run_ledger:run_8821"],
  "outcome": {
    "system": "crm",
    "event": "quote_sent",
    "ref": "Q-2026-0142"
  },
  "revenue_link": {
    "type": "invoice",
    "ref": "ZATCA-INV-2026-1043",
    "amount_sar": 18000,
    "verified": true
  }
}
```

### قواعد القبول
- مفقود أي حقل من الثمانية → الحزمة غير صالحة.
- `revenue_link.verified = false` → الإيراد يبقى **تقديريًا**، لا يُحسب «مُتحقَّقًا».
- لا PII في `tool_calls.params` ولا في `outputs`.
- `context_hash` ثابت قابل لإعادة الحساب.

---

## English

### Purpose
An Evidence Pack documents a single AI decision or revenue event in an auditable form. No revenue counts as "verified" without a complete pack.

### The Eight Components
1. **intent** — what the user or operational action requested, in natural language.
2. **context_hash** — fingerprint of the run context: prompts, version, data scope.
3. **tool_calls** — sequence of tool calls with parameters (PII-free).
4. **outputs** — final agent artifact before any external action.
5. **approvals** — list of approvers, roles, timestamps.
6. **audit_log** — related AI Run Ledger events (PDPL 5/13/14/18/21/32).
7. **outcome** — event recorded in the operational system (CRM/ZATCA/Calendar).
8. **revenue_link** — link to the invoice or contract that attributes revenue to this run.

### JSON Shape (sample)
```json
{
  "evidence_pack_id": "ep_2026_05_25_0001",
  "tenant_id": "{{ tenant }}",
  "intent": "Draft a renewal quote for account A-127 and send after owner approval",
  "context_hash": "sha256:7c92...e3",
  "tool_calls": [
    {"tool": "summarize", "agent": "draft-quote-01", "duration_ms": 412},
    {"tool": "render_template", "agent": "draft-quote-01", "duration_ms": 88},
    {"tool": "draft_message", "agent": "outbound-reply-01", "duration_ms": 215}
  ],
  "outputs": {
    "artifact": "quote_A127_v3.pdf",
    "checksum": "sha256:ab12...f9"
  },
  "approvals": [
    {"approver": "sales_lead", "decision": "approved", "ts": "2026-05-25T09:14:22Z"}
  ],
  "audit_log": ["pdpl_art_13_consent_logged", "ai_run_ledger:run_8821"],
  "outcome": {
    "system": "crm",
    "event": "quote_sent",
    "ref": "Q-2026-0142"
  },
  "revenue_link": {
    "type": "invoice",
    "ref": "ZATCA-INV-2026-1043",
    "amount_sar": 18000,
    "verified": true
  }
}
```

### Acceptance Rules
- Missing any of the eight fields → pack is invalid.
- `revenue_link.verified = false` → revenue stays **estimated**, not "verified".
- No PII in `tool_calls.params` or `outputs`.
- `context_hash` is stable and recomputable.

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
