# CUSTOMER FOLDER — هيكل ملف العميل

> The standard, governed folder for every customer engagement. Keeps proof, approvals, and data
> handling auditable. Pairs with `COMMAND_SPRINT_DELIVERY.md` and `docs/03_governance/`.

## Why a standard folder

Every engagement must be **auditable**: what we claimed, what evidence backs it, what the customer
approved, and how their data is handled. A consistent folder makes the Proof Pack and the Claims
Register trivial to assemble — and makes governance review fast.

## Structure

```
clients/<customer-slug>/
├── 00_source_passport.md        # what data we have, source, allowed use, PII flags
├── 01_intake.md                 # founder inputs, scope, sector, goals (no scraping)
├── 02_market_intelligence.md    # Market Intelligence Lite (Why-Now)
├── 03_revenue_map.md            # leaks + scored opportunities
├── 04_drafts/                   # draft pack — NOTHING here is sent without approval
├── 05_approval_register.md      # every external action + approval status + approver + date
├── 06_proof_pack/               # assembled evidence (links to L0–L5)
├── 07_claims.md                 # rows mirrored into docs/03_governance/CLAIMS_REGISTER.md
├── 08_executive_brief.md        # one-screen command brief
├── 09_next_actions.md           # next action board
└── 10_upsell.md                 # honest next-rung recommendation (only if proof supports)
```

> `clients/` already exists in the repo — follow existing per-customer conventions where present.

## Rules

- **Source Passport first.** No work begins without `00_source_passport.md` (source + allowed use + PII).
- **Drafts ≠ sends.** `04_drafts/` is human-gated; nothing leaves without an Approval Register entry.
- **No customer data for model training.** See `docs/03_governance/DATA_RETENTION_POLICY.md`.
- **No name/logo/quote published** without written approval logged in `05_approval_register.md`.
- **Every claim** in `07_claims.md` is Evidence-backed / Hypothesis / Rewritten — never bare.

## Retention & deletion

Follow `docs/03_governance/DATA_RETENTION_POLICY.md`: defined retention window, deletion on request,
subprocessors disclosed.
