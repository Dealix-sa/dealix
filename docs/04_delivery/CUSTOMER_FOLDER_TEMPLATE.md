# Customer Folder Template

> **Status:** CANONICAL · **Owner:** Founder · **Last reviewed:** 2026-06-05
>
> Copy this structure into `customers/<customer_name>/` at the start of each Sprint.

---

## Files

### `00_intake.md`
```
company:
industry:
contact_role:
sales_flow:
delivery_flow:
top_5_opportunities:
current_offer:
followup_examples:
pain_points:
approval_contact:
consent: (yes/no + date)
data_collected: (list — must be minimum only)
```

### `01_revenue_map.md`
Where opportunities and follow-up break. Fields: `source, analysis, assumptions,
confidence, recommendation, approval_required, next_action`.

### `02_client_brain.md`
Account memory: requested / promised / delivered / waiting / renewal risk /
expansion opportunity.

### `03_followup_pack.md`
Follow-up **drafts** (never auto-sent). Each marked `approval_required: true`.

### `04_offer_upgrade.md`
How to strengthen the current offer. Recommendation + confidence.

### `05_proof_register.md`
Evidence that exists, evidence missing, what is safe to publish (with approval).

### `06_approval_register.md`
What in the customer's flow needs human approval, and who approves.

### `07_executive_command_brief.md`
The decision brief — see `EXECUTIVE_BRIEF_TEMPLATE.md`.

### `08_next_30_days.md`
Next execution steps with owners; 30-day view.

---

## Rules

- Every file uses the seven standard fields where applicable.
- Collect only minimum data; record consent in `00_intake.md`.
- Mark every customer-facing draft `approval_required: true`.
- Nothing in this folder is published or sent without approval.
