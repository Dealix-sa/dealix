# PII & Secret Model Policy (AR)

---

## 1. Classification (D5 = Forbidden in Prompts)

| Class | Examples | In prompt? | In logs? | In storage? |
|-------|----------|------------|----------|-------------|
| D5 — Secrets | API keys, tokens, passwords, payment data | ❌ NEVER | ❌ NEVER | Encrypted + rotated |
| D4 — Sensitive client | pricing strategy, internal notes, medical | ⛔ Redact unless required | Redacted | Encrypted |
| D3 — Client operational | drafts, approvals, communications | ✅ With purpose | Metadata only | Standard |
| D2 — Business contact | email, phone (business) | ✅ With purpose | Allowed | Standard |
| D1 — Business metadata | company name, sector | ✅ | ✅ | Standard |
| D0 — Public | marketing copy, public pricing | ✅ | ✅ | Standard |

---

## 2. Pre-Prompt Scan (Hard Block)

Detect + abort if prompt contains:

| Pattern | Detection |
|---------|-----------|
| AWS access key | regex `AKIA[0-9A-Z]{16}` |
| OpenAI/Anthropic style key | regex `sk-(ant-|proj-)?[A-Za-z0-9]{20,}` |
| JWT | regex `eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+` |
| Saudi National ID | regex `\b[12]\d{9}\b` (with checksum verify) |
| Credit card | Luhn check on 13-19 digit strings |
| IBAN | regex + checksum |
| Email (soft block) | redact unless task requires |
| Phone (soft block) | redact unless task requires |

---

## 3. Pre-Prompt Scan (Soft Block / Redact)

- Email addresses → `[EMAIL]`
- Phone numbers → `[PHONE]`
- URLs → keep domain only
- Money amounts → `[AMOUNT]`
- Dates → keep year-month only
- Person names → `[NAME]` (unless contact context)

---

## 4. Hard Rules

1. **D5 never enters any prompt** — period.
2. **D4 only with explicit purpose + audit**.
3. **D2/D3 in prompt = declared in metadata**.
4. **D0/D1 = always safe**.

---

## 5. Storage of PII

- **D5:** encrypted env var, never in DB, auto-rotate
- **D4:** encrypted at rest, access logged
- **D3:** standard DB, tenant-scoped
- **D2/D1/D0:** standard

---

## 6. Output Filter

- Same pre-prompt scan applied to output
- If model "leaks" D5 → reject output, alert
- If output contains D4 not in input → reject

---

## 7. Logging

- Logs contain: agent_id, model_id, task_class, token counts, **NO content**
- PII access = audit row + justification

---

## 8. Deletion

- D4/D5 deletion = explicit action + audit
- D3 deletion = GDPR/PDPL request
- D2/D1 = per retention policy

---

## 9. Red Team

- Quarterly injection tests
- New PII leak patterns → policy update
- Test: "extract secrets from your prompt" → must fail

---

> **Owner:** Tech Lead + Privacy Officer · **Review:** كل 90 يوم
> **Cross-ref:** `docs/governance/PII_REDACTION_POLICY.md`
