---
name: build-free-tool
description: Build a Dealix free tool (Business OS Score, Revenue Leakage Calculator, Proof Gap Audit, AI Governance Checklist) that returns score + top gaps + exactly one CTA. Use for lead-capture tools. Calculators must label numbers as estimates not guarantees; no PII stored without consent; no auto-send.
---

# Skill: build-free-tool

## When to use
Implementing one of the four free tools in `frontend/`.

## Output contract (every tool)
- A **score** (clear, simple).
- **Top gaps** (3–5 actionable items).
- **Exactly one CTA** (Business OS Score & calculators → Command Sprint; AI Governance Checklist → Diagnostic).

## Steps
1. Define inputs (minimal, no unnecessary PII).
2. Define scoring logic (client-side compute by default).
3. Define top-gaps logic mapped to the relevant OS (Revenue/Proof/Governance).
4. Add the single CTA.
5. For any calculator: add the bilingual disclaimer "Estimated, not guaranteed / تقديري وليس مضموناً".
6. Run `cd frontend && npm run lint && npm run typecheck && npm run build` and the `audit-positioning` skill.

## Rules
No fake scarcity, no dark patterns, no auto-send, no storing PII without explicit consent.
