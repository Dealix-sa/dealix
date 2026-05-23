# Productization Decision System

## Purpose
Decide whether a repeated workflow should become documentation, template, automation, product feature, or SaaS candidate.

## Decision Types
- Log
- Document
- Template
- Automate Internally
- Delegate
- Product Feature
- SaaS Candidate
- Kill
- Defer

## Build Criteria
A workflow can move forward if:
- repeated at least 3 times
- connected to revenue, delivery, trust, learning, or founder leverage
- has clear input/output
- has QA criteria
- risk is understood
- owner is clear

## No-Go Criteria
Do not productize if:
- only happened once
- no customer value
- no delivery value
- no revenue link
- risk is unclear
- workflow still changes every time
- automation could create external commitment

## Risk Classes
- Low: internal formatting, reports, summaries.
- Medium: lead scoring, proposal draft, client report draft.
- High: outbound copy, pricing recommendation, public content.
- Critical: payment, refund, legal, claims, sensitive data export.

## Rules
- Critical workflows are never autonomous.
- High-risk workflows require approval.
- Medium-risk workflows require QA.
- Low-risk workflows can be internally automated after testing.

## Evidence
- productization/candidates.csv
- delivery QA
- weekly learning
- client feedback
