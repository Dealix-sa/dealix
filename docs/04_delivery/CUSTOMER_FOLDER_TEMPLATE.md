# Customer Folder Template / قالب مجلّد العميل

**Use:** when a customer pays, create an isolated workspace folder at
`clients/<customer_slug>/` using this structure. One folder per customer; no
cross-customer data mixing (Client OS isolation).

---

## Folder structure / بنية المجلّد

```
clients/<customer_slug>/
├── 00_passport/
│   └── source_passport.md        # signed data-ownership declaration
├── 01_intake/
│   ├── kickoff_notes.md          # diagnostic + sprint scope
│   └── engagement.md             # engagement_id, dates, owner (both sides)
├── 02_data/
│   ├── raw/                      # client_upload / crm_export / manual_entry only
│   ├── cleaned/                  # post Data OS (DQ + dedupe)
│   └── dq_score.md
├── 03_drafts/
│   └── *.md                      # all drafts = approval_required
├── 04_governance/
│   ├── approvals.md              # who approved / when
│   ├── redactions.md             # PII redactions
│   └── consent.md                # consent_for_publication records
├── 05_proof/
│   └── proof_pack.md             # from PROOF_PACK_TEMPLATE.md
├── 06_value/
│   └── value_tier.md             # Value OS mapping + Capital OS asset id
└── README.md                     # one-screen status for this customer
```

---

## Required files at kickoff / الملفات المطلوبة عند البدء

| File | Why | Gate |
|---|---|---|
| `00_passport/source_passport.md` | data ownership is the contract | sprint does not begin without it |
| `01_intake/engagement.md` | named owner on **both** sides | agent-identity non-negotiable |

---

## Rules / القواعد

- **Isolation:** never mix two customers' data in one folder.
- **No scraped data:** `source_type` must be `client_upload`, `crm_export`, or
  `manual_entry`.
- **Drafts stay drafts:** everything in `03_drafts/` is `approval_required`
  until the founder approves (see
  [`../03_governance/HUMAN_APPROVAL_POLICY.md`](../03_governance/HUMAN_APPROVAL_POLICY.md)).
- **Retention:** honor `retention_days` from the Source Passport; delete on
  request (PDPL data-subject rights).
- **Proof gate:** `proof_score < 70` is not deliverable — remediate or
  partial-refund per [`../REFUND_SOP.md`](../REFUND_SOP.md).

---

## README.md seed (per customer)

```markdown
# <Customer> — Engagement <engagement_id>
- Status: kickoff | data | drafts | proof | delivered
- Owner (Dealix): <name>   Owner (Customer): <name>
- Source Passport: signed? yes/no
- DQ score: <n>   Proof score: <n>
- Next action (founder): <one line>
```
