# Dealix Design OS Max Utilization Playbook

## Goal

Apply the merged Dealix Agent Skills Pack and Open Design-inspired Design Command Room OS across the highest-value Dealix workstreams.

This playbook turns the design system and project-level skills into repeatable operating outputs.

## Operating principle

Use the same loop everywhere:

```text
Signal -> Brief -> Draft artifact -> Claims review -> Safety review -> Approval -> Handoff -> Proof
```

## Highest-value domains

| Domain | Artifact | Owner | Outcome |
|---|---|---|---|
| Revenue | Revenue Command Room | Founder / sales operator | Know who to contact, follow up, propose, and approve today |
| CEO decisions | Founder War Room | Founder | Know the highest-value decision and risk today |
| Client delivery | Client Delivery OS | Delivery owner | Move client from intake to proof pack |
| Sales | Sales Deck | Founder / BD | Explain Dealix clearly to qualified prospects |
| Website | Landing Page | Product/marketing | Convert prospects into discovery/pilot conversations |
| Client proof | Client Proof Pack | Delivery / trust owner | Show what was validated and what happens next |
| Client growth | Client Growth Operator | Growth operator | Prepare channel actions without uncontrolled live sending |
| Company intelligence | Company Brain | Founder | Turn operating signals into action-ready decisions |

## Daily operating flow

1. Run or inspect revenue/company/delivery signals.
2. Generate one draft artifact from the relevant template.
3. Review claims and assumptions.
4. Review external-send implication.
5. Assign owner and approval state.
6. Hand off to sales, product, delivery, or frontend.
7. Store proof in `reports/design/` or the related domain report folder.

## Weekly operating flow

Every week, generate:

- Revenue Command Room artifact
- Founder War Room artifact
- Sales Deck draft for one target sector
- Landing Page draft for one offer
- Proof Pack draft for one client or demo workflow

## What not to do

- Do not mark artifacts as client-ready without review.
- Do not claim guaranteed revenue or ROI.
- Do not imply live outbound is enabled.
- Do not copy external product runtimes into Dealix.
- Do not ship generated UI into production without engineering review.

## Commands

```bash
make design-os-list
make design-os-generate TYPE=revenue-command-room
make design-os-generate TYPE=founder-war-room
make design-os-generate TYPE=client-proof-pack
make design-os-all
make test-design-os
```

## Definition of success

Dealix benefits from the Design OS when every commercial/product workstream can produce a reviewed artifact that makes the next action clearer:

```text
one artifact -> one decision -> one action -> one proof trail
```
