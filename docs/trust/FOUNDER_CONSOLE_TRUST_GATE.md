# Founder Console Trust Gate

## Purpose
Prevent Founder Console from becoming a bypass around Dealix Trust Plane.

## Required Checks Before External Action

- approval_class
- actor
- reason
- evidence
- suppression check
- no-overclaim check
- never-auto-execute check
- audit log write

## A1 Actions
Allowed with single founder approval. Standard outreach copy, internal
content changes, reversible updates.

## A2 Actions
Require Sami approval and audit. Outreach to new sector, proposal pricing
above standard rate card, public proof publication.

## A3 Actions
Cannot be automated. Must be escalated or handled manually. Contract
amendments, refunds, public regulatory statements, takedowns.

## Forbidden From Frontend

- direct frontend external send
- direct frontend price commitment
- direct frontend proof publish
- direct frontend contract/refund action

## Rule

Frontend can request action. Trust decides whether action can proceed.
