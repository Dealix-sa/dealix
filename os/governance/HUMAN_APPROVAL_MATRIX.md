# Dealix — Human Approval Matrix
# مصفوفة الموافقة البشرية

**Version:** 1.0 | Canonical source: os/06_APPROVAL_GATES.yml

---

## Matrix Summary

| Action Category | Requires Founder Approval | Auto-Execute |
|----------------|--------------------------|--------------|
| Research company (public) | No | Yes |
| Build company brief | No | Yes |
| Write email draft | No | Yes |
| Build proposal draft | No | Yes |
| Score company | No | Yes |
| Classify reply | No | Yes |
| Internal QA on sample | No | Yes |
| **Send first email** | **YES** | No |
| **Send follow-up** | **YES** | No |
| **Share pricing** | **YES** | No |
| **Send proposal** | **YES** | No |
| **Request credentials** | **YES** | No |
| **Use production API** | **YES** | No |
| **Access client systems** | **YES** | No |
| **Deploy to client env** | **YES** | No |
| **Delete client data** | **YES** | No |
| Cold WhatsApp | **BLOCKED — NEVER** | Never |
| LinkedIn automation | **BLOCKED — NEVER** | Never |
| Scraping | **BLOCKED — NEVER** | Never |
| Train AI on client data | **BLOCKED — NEVER** | Never |

---

## Approval Process

1. Agent prepares the action (draft, plan, brief)
2. Action queued in Daily Brief for founder review
3. Founder reviews → approves or rejects
4. If approved → founder executes (or agent executes with explicit confirmation)
5. All approvals logged in execution log

---

## Escalation

If any agent encounters an action not covered in this matrix:
- Stop immediately
- Add to Founder Daily Brief as an escalation
- Include: what was attempted, why it stopped, options for founder
- Do not proceed until founder decides

---

## Override Authority

Only the founder can override approval requirements. No agent, no automation, no system can self-approve an action that requires human approval. This is a doctrine rule, not a preference.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
