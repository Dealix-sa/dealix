# SDAIA AI Compliance Operating Notes

## Purpose
This document maps Dealix operating behavior to practical AI governance expectations for Saudi enterprise sales.

## Governance Position
Dealix uses AI to analyze, suggest, structure, and draft.
Dealix does not position AI as an autonomous decision-maker.

## Required Operating Controls

### 1. Human Oversight
- [x] Founder or reviewer approval before sensitive outbound
- [x] Draft queues remain visible before send
- [x] Brain outputs are framed as inputs to a human decision process

### 2. Transparency
- [x] AI-generated content is reviewable
- [x] Decision context is visible through metrics, assumptions, and next actions
- [x] Message templates and conversation flows are observable in the system

### 3. Accountability
- [x] Decision and risk records can be tied to owners
- [x] Approval actions are explicit
- [x] System defaults bias toward control rather than automation

### 4. Risk Management
- [x] Outbound defaults remain restricted
- [x] Failed message and webhook events are trackable
- [x] Operational risks can be logged in Brain OS

### 5. Fairness and Appropriate Use
- [x] Signals and scoring should focus on business context, not protected personal characteristics
- [x] Teams should review prompts, drafts, and selection logic periodically
- [x] No deceptive claims or fabricated outcomes

## WhatsApp Governance Notes
- Use official Cloud API only
- Keep webhook verification enabled
- Keep template lifecycle visible
- Do not enable live outbound broadly without documented approval policy

## Commercial Guidance
Describe Dealix as:
- governed
- reviewable
- approval-gated
- compliance-aware

Do not describe Dealix as:
- fully autonomous
- guaranteed compliant
- guaranteed ROI generating
- replacing management judgment