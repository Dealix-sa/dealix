# Dealix — Audit Log Format
# صيغة سجل التدقيق

**Version:** 1.0 | Schema: os/schemas/execution-log.schema.json

---

## Required Fields for Every Log Entry

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| log_id | string | Yes | Unique ID |
| timestamp | ISO 8601 | Yes | UTC |
| action | string | Yes | What was attempted |
| module | string | Yes | Which OS module |
| status | enum | Yes | success / failed / blocked / pending_approval |
| actor | enum | Yes | agent / founder / system |
| requires_approval | boolean | Yes | Was approval needed? |
| approval_obtained | boolean | Conditional | If requires_approval=true |
| block_reason | string | If blocked | Why it was blocked |
| governance_decision | object | Yes | Module + key decision |
| pii_present | boolean | Yes | MUST always be false |

---

## Prohibited in Logs

- Real names or emails of contacts
- Phone numbers
- Any personally identifiable information
- Client credentials or API keys
- Raw message content (summary only)
- Client financial data

---

## Sample Log Entry (JSON)

```json
{
  "log_id": "LOG-2026-06-01-001",
  "timestamp": "2026-06-01T09:00:00Z",
  "action": "send_first_email",
  "module": "approval_gate",
  "status": "pending_approval",
  "actor": "agent",
  "company": "Al Seha FM",
  "channel": "email",
  "requires_approval": true,
  "approval_obtained": false,
  "pii_present": false,
  "governance_decision": {
    "module": "approval_gate",
    "action": "send_first_email",
    "status": "pending_approval",
    "doctrine_rule": "all_external_sends_require_approval"
  },
  "metadata": {
    "draft_id": "DRAFT-001",
    "persuasion_score": 86,
    "company_tier": "A"
  }
}
```

---

## Retention

- Audit logs retained for minimum 2 years
- Logs stored in encrypted storage
- Access restricted to founder
- Logs never shared externally without legal requirement

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
