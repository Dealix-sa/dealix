# ERP / CRM Partner Playbook

> ERP and CRM vendors own the system of record. A partnership with
> them puts Dealix at the right layer of the buyer's stack.

## Who fits

- Saudi ERP implementers (SAP, Oracle, Microsoft Dynamics, Odoo).
- Local CRM vendors and Salesforce / HubSpot implementation partners.
- ERP for sectors aligned with our locked beachhead.

## Why they partner with Dealix

- They control the data pipe; Dealix adds proof-safe AI on top.
- Their customers ask "do you have AI?" — Dealix answers it
  defensibly (PDPL-native, approval-first, audit trail).
- ZATCA Phase 2 connectivity makes integration straightforward.

## Integration pattern

```
ERP/CRM  →  Dealix Lead Engine / Decision Passport
         ↓
   Proof-safe outputs  →  ERP/CRM records (with audit trail)
```

## What they offer us

- Reseller / implementation channel.
- Joint reference accounts in the beachhead sector.
- ZATCA / PDPL co-positioning at events.

## What we never do

- Promise data residency outside Saudi Arabia without explicit
  contract and customer approval.
- Modify ERP/CRM data without an approval trail.
- Compete with their existing add-on partners — we sit above, not
  beside.

## How to add an ERP/CRM partner

1. Row in `partner_pipeline.csv` with `type=erp_crm`.
2. Capture the *exact* integration scope in `next_action`.
3. Governance review for any data-flow change.
4. Pilot integration with one shared customer before scale.
