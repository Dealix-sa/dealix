# Dealix Sale-Ready Pack — Operating Guide

## Purpose

Convert one real company context into an internal, evidence-backed sales package without publishing fixed prices, generating an unsupported quote, claiming ROI, or contacting the customer.

## Inputs

The builder accepts account JSON containing:

- company identity and sector;
- named buyer persona;
- business problem and impact hypothesis;
- responsible owner;
- available process or data sources;
- bounded pilot willingness;
- baseline and target metric;
- pilot scope, exclusions, checkpoints, acceptance criteria, proof requirements, and stop rule;
- value inputs supplied or verified by the customer.

## Outputs

The generated draft-only pack contains:

1. account context;
2. buyer persona and buying outcomes;
3. problem statement and impact hypothesis;
4. qualification result and route;
5. recommended Dealix offer;
6. bounded pilot scope;
7. success metrics;
8. value hypothesis with missing inputs;
9. proof plan;
10. risks and assumptions;
11. approval items;
12. the single safest next step.

## Qualification behavior

- **Qualified:** all minimum discovery inputs exist and no prohibited request is present.
- **Uncertain:** the company and problem are known, but discovery inputs or pilot boundaries are missing. Route only to a mini diagnostic.
- **Not qualified:** unsafe, illegal, unverifiable, guaranteed-outcome, uncontrolled outbound, or ownerless requests are declined or referred.

## Commercial doctrine

- Discovery precedes a quote.
- Pricing remains quote-only.
- Scope and commercial terms require approval.
- External send requires approval.
- Scope changes require requoting.
- Discounts and payment terms require approval.
- Revenue requires payment proof.
- Delivery requires completion proof.
- Customer value requires a baseline and evidence.
- A value hypothesis is not an ROI claim.

## Command

```bash
python scripts/commercial/build_sale_ready_pack.py \
  --input data/commercial/account.example.json \
  --output reports/commercial/sale_ready_pack.json
```

The command performs no network request, customer contact, quote issuance, payment action, or production mutation.

## Sales use

Use the pack before discovery follow-up, proposal drafting, negotiation, pilot kickoff, or renewal. It should allow a founder or salesperson to answer six questions consistently:

1. Is this company qualified?
2. Who is the real buyer and what outcome matters?
3. Which Dealix offer is the narrowest credible entry point?
4. What exactly is in and out of the pilot?
5. How will progress, delivery, and value be proven?
6. What approval is needed before the next external action?

## Company value coverage

The current Dealix operating model can be sold around:

- market and company intelligence;
- opportunity qualification and sales execution;
- proposals, approvals, and commercial control;
- onboarding and cross-department handoffs;
- delivery checkpoints and exception management;
- adoption, customer health, and support risk;
- proof of delivery and customer value;
- renewal and expansion readiness;
- Saudi market-access and partner motions;
- governed AI, source authority, auditability, and approval-first automation.
