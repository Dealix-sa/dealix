# Dealix — Human Approval Policy / سياسة الموافقة البشرية

**Status:** canonical · **Owner:** Founder · **Updated:** 2026-06-06
**Principle:** No autonomous external action. A human (the founder, or a named
approver) approves before anything leaves Dealix infrastructure toward a third
party. لا فعل خارجي تلقائي — موافقة بشرية قبل أي إرسال.

---

## 1. What always requires approval / ما يتطلّب موافقة دائماً

| Action | Approver | Recorded in |
|---|---|---|
| Any outbound message (WhatsApp / email / DM) | Founder | Approval Center + outreach queue |
| Publishing any Proof Pack externally | Founder | Approval Center (`approval_status`) |
| Using a customer name / logo / metric publicly | Founder | requires `consent_for_publication=True` per event |
| Sending a proposal / quote | Founder | sales ledger |
| Onboarding a new data source | Founder | signed Source Passport |
| Any irreversible / destructive data op | Founder | governance ledger |

---

## 2. The approval gate / بوابة الاعتماد

```text
draft created  ──►  approval_status = "approval_required"
                         │
                 founder reviews
                         │
        ┌────────────────┴────────────────┐
   approved                            rejected
        │                                  │
 action may proceed              draft archived, no send
 (logged with approver +         (reason logged)
  timestamp)
```

- Default state of every draft is `approval_required`.
- Nothing transitions to "sent/published" without an explicit approval record
  carrying **who** approved and **when**.

---

## 3. What is never auto / ما لا يكون تلقائياً أبداً

- No auto-send of any external message.
- No autonomous outreach campaigns.
- No publishing without consent **and** approval (both, not either).
- No "agent acts on its own" — every agent action that touches a third party
  is a draft until approved.

---

## 4. Roles / الأدوار

| Role | May draft | May approve | May send |
|---|---|---|---|
| AI agent / sub-agent | yes | no | no |
| Delivery operator | yes | no | no |
| Founder | yes | yes | yes (after approval) |

Each workflow has a **named owner on both sides** (Dealix side + customer
side) — non-negotiable on agent identity.

---

## 5. Audit / التدقيق

- Approvals, rejections, consents, and sends are append-only ledger entries.
- The outreach approval queue (`reports/revenue/outreach_approval_queue.md`)
  is the working surface; the ledger is the record.
- Companion: [`CLAIMS_REGISTER.md`](CLAIMS_REGISTER.md),
  [`../PROOF_PACK_V6_STANDARD.md`](../PROOF_PACK_V6_STANDARD.md).
