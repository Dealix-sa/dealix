# Dealix — Data Handling Policy
# سياسة التعامل مع البيانات

**Version:** 1.0 | PDPL-Aware | All agents and humans must comply.

---

## Core Principles

1. **Sample data first.** Never work with production data until sandbox is proven and founder approves.
2. **No production API without approval.** Gate G06 — founder must explicitly approve production access.
3. **No secrets in the repository.** API keys, passwords, and credentials are NEVER committed to Git.
4. **Least privilege.** Request only the minimum access needed. Never request full system access when read-only suffices.
5. **Audit logs required.** All significant actions must be logged with timestamp, actor, and action — no PII in logs.
6. **No PII in logs.** Personal data never goes into logs. If PII is present, redact before logging.
7. **Data stays in client environment.** For data sovereignty clients, all processing stays within their infrastructure.
8. **No external training.** Client data is never used to train AI models. This is non-negotiable.

---

## Data Classification

| Level | Examples | Handling |
|-------|----------|----------|
| Public | Company name, sector, public announcements | No restrictions |
| Internal | Workflow data, process maps, anonymized samples | Encrypt in transit, access logged |
| Confidential | Client business data, contracts, financial data | Encrypted storage, limited access, audit log |
| Restricted | Client PII, legal case data, medical admin data | Sovereign environment only, never logged, explicit consent required |

---

## PDPL Compliance Checklist

- [ ] Data processing agreement (DPA) in place for any client data
- [ ] Purpose limitation: data used only for agreed workflow automation
- [ ] Storage limitation: client data not retained beyond project scope
- [ ] Access control: only necessary personnel access client data
- [ ] Breach procedure documented (see INCIDENT_RESPONSE.md)
- [ ] Client has been informed of AI use in their workflows

---

## What Agents Can Do With Data

| Action | Allowed |
|--------|---------|
| Analyze anonymized sample data | Yes (no approval) |
| Analyze production data in client sandbox | Yes (with founder approval) |
| Store client data in Dealix systems | No (unless DPA signed) |
| Use client data to train models | Never |
| Share client data with third parties | Never (without explicit DPA) |
| Log PII | Never |

---

## Secrets Management

- All API keys go to Railway environment variables or equivalent secrets manager
- Never commit secrets to Git (enforced by pre-commit hooks)
- Rotate credentials if compromised — immediately
- All credentials are documented in a separate secure vault (not in this repo)

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
