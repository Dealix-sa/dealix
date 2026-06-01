# Human Approval Matrix — مصفوفة الموافقة البشرية

**Version:** 1.0 | **Owner:** Founder | **Effective Date:** 2026-06-01 | **Review:** Quarterly

Cross-links: [AI_USAGE_POLICY.md](AI_USAGE_POLICY.md) | [../06_APPROVAL_GATES.yml](../06_APPROVAL_GATES.yml) | [../01_CLAUDE.md](../01_CLAUDE.md) | [INCIDENT_RESPONSE.md](INCIDENT_RESPONSE.md)

---

## Purpose — الغرض

This matrix defines which actions require human approval, who approves them, and the SLA for that approval. Every AI agent in Dealix checks this matrix before taking any external action.

تحدد هذه المصفوفة الإجراءات التي تتطلب موافقة بشرية، من يوافق عليها، والوقت المعياري لتلك الموافقة. كل وكيل ذكاء اصطناعي في ديليكس يراجع هذه المصفوفة قبل أي إجراء خارجي.

---

## Approval Levels — مستويات الموافقة

| Level — المستوى | Approver — المُوافِق | Available — متاح |
|---|---|---|
| **L0** | Auto-approved — no human review needed | Always |
| **L1** | Founder — before action | During working hours; async within same day |
| **L2** | Founder — before action, written confirmation required | Within 24 hours |

---

## Action → Approval Matrix — مصفوفة الإجراء → الموافقة

### Growth and Outreach Actions | إجراءات النمو والتواصل

| Action — الإجراء | Approval Required | Approver | SLA | Notes |
|---|---|---|---|---|
| Generate outreach draft (internal only) | No — L0 | Auto | Instant | Draft sits in queue, does not send |
| Send first outreach email to a new company | Yes — L1 | Founder | Same day | Every first email reviewed and approved individually |
| Send follow-up email (approved sequence) | Yes — L1 | Founder | Same day | Batch review of sequence drafts acceptable |
| Send LinkedIn connection request | Yes — L1 | Founder | Same day | Manual only — founder or designated person executes |
| Send LinkedIn direct message | Yes — L1 | Founder | Same day | Manual only — no automation |
| Send WhatsApp message (opt-in contact) | Yes — L1 | Founder | Same day | Approved template required |
| Publish LinkedIn post | Yes — L1 | Founder | Same day | |
| Resume a paused outreach channel | Yes — L2 | Founder | 24 hours | Only after root cause is resolved |

### Sales and Pricing Actions | إجراءات المبيعات والتسعير

| Action — الإجراء | Approval Required | Approver | SLA | Notes |
|---|---|---|---|---|
| Generate proposal draft (internal) | No — L0 | Auto | Instant | Proposal sits as draft until reviewed |
| Share proposal with client | Yes — L1 | Founder | Same day | |
| Quote any price to a client | Yes — L1 | Founder | Same day | Written quote only — no verbal |
| Offer a discount | Yes — L1 | Founder | Same day | Max 15% without written sign-off |
| Extend special payment terms | Yes — L2 | Founder | 24 hours | Written exception required |
| Accept a new project outside standard offer tiers | Yes — L2 | Founder | 24 hours | |

### Delivery and Technical Actions | إجراءات التسليم والتقني

| Action — الإجراء | Approval Required | Approver | SLA | Notes |
|---|---|---|---|---|
| Run analysis on anonymized sample data | No — L0 | Auto | Instant | |
| Run analysis on client production data | Yes — L1 | Founder | Same day | DPA must already be signed |
| Request API credentials from client | Yes — L1 | Founder | Same day | |
| Access production system (read-only) | Yes — L1 | Founder | Same day | Logged in CLIENT_ACCESS_MATRIX.md |
| Access production system (write access) | Yes — L2 | Founder | 24 hours | Explicit written approval required |
| Deploy to client staging environment | Yes — L1 | Founder | Same day | |
| Deploy to client production environment | Yes — L2 | Founder | 24 hours | |
| Modify a live client system | Yes — L2 | Founder | 24 hours | |
| Grant a new team member access to client data | Yes — L2 | Founder | 24 hours | |

### Data and Compliance Actions | إجراءات البيانات والامتثال

| Action — الإجراء | Approval Required | Approver | SLA | Notes |
|---|---|---|---|---|
| Delete client data | Yes — L2 | Founder | 24 hours | Confirm retention period elapsed; notify client |
| Return client data package | Yes — L1 | Founder | Same day | Log return method and date |
| Share client data with a sub-contractor | Yes — L2 | Founder | 24 hours | Sub-processor notification per DPA |
| Process personal data (PII) | Yes — L2 | Founder | 24 hours | DPA must cover this processing |
| Report an incident to client | Yes — L1 | Founder | Within 24h of breach | Do not delay to investigate first |

### Financial Actions | الإجراءات المالية

| Action — الإجراء | Approval Required | Approver | SLA | Notes |
|---|---|---|---|---|
| Generate invoice draft | No — L0 | Auto | Instant | |
| Send invoice to client | Yes — L1 | Founder | Same day | |
| Issue a credit note or refund | Yes — L2 | Founder | 24 hours | |
| Sign or accept new commercial contract | Yes — L2 | Founder | 24 hours | |

---

## What Agents Do When Approval is Pending — ما يفعله الوكيل أثناء انتظار الموافقة

When an action requires human approval and approval has not yet been received:

1. Agent drafts the action and queues it with status "pending_approval"
2. Agent notifies founder via priority brief with action description, recommended timing, and relevant context
3. Agent waits — does not execute the action
4. If the SLA window passes without response, agent sends a reminder notification only — it still does not execute
5. Approval must be explicit (approve / reject) — no action defaults to auto-approved after silence

---

## Override Policy — سياسة التجاوز

No agent can override this matrix. If a scenario arises that is not covered by this matrix, the default is: **Require L1 founder approval before proceeding.**

لا يمكن لأي وكيل تجاوز هذه المصفوفة. إذا نشأ موقف غير مشمول في هذه المصفوفة، الافتراضي هو: **طلب موافقة المؤسس (L1) قبل المتابعة.**

---

> **Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة**
