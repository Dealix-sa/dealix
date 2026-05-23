# Founder Command Layer

## Purpose

Give Sami one control layer to operate Dealix as a company, not as
scattered scripts and documents.

## Core Screens

1. CEO Command Center
2. Sales Cockpit
3. Approval Center
4. Worker Health
5. Trust Center
6. Finance Center
7. Distribution Center
8. Delivery Center
9. Retention Center
10. Proof Center

## Founder Principle

Sami should approve and decide.

The system should research, score, draft, route, remind, report, and
escalate.

## Daily Founder Questions

- What is the one top action today?
- Which outreach needs approval?
- Which follow-up is overdue?
- Which reply needs a sample?
- Which sample needs a proposal?
- Which proposal needs payment follow-up?
- Which trust risk blocks execution?
- Which worker failed?
- What moved cash today?

## Rule

If a screen does not help approve, sell, collect, deliver, retain, prove,
or reduce risk, it is not P0.

## P0 Founder Routes

| Route             | Page                  | Source of truth                      |
| ----------------- | --------------------- | ------------------------------------ |
| `/ceo`            | CEO Command Center    | CEO Summary Worker                   |
| `/sales-cockpit`  | Sales Cockpit         | Sales Funnel Worker                  |
| `/approvals`      | Approval Center       | Approval Queue Worker                |
| `/workers`        | Worker Health         | Worker Health Worker                 |
| `/trust`          | Trust Center          | Trust Flags Worker                   |
| `/finance`        | Finance Center        | Finance Summary Worker               |
| `/distribution`   | Distribution Portfolio| Distribution Portfolio Worker        |

## Trust Plane Discipline

- The founder frontend never bypasses the Trust Plane.
- Every external-impacting action requires an approval class
  (`A0` / `A1` / `A2` / `A3`) and an explicit human decision.
- No screen should send a message, charge a card, or change shared state
  without an explicit founder action recorded in the audit log.
