# Workflow Runtime Design

Every Dealix workflow has:

## 1. Trigger

What starts it?

## 2. Input

What data/files are required?

## 3. AI Step

What does AI produce?

## 4. Governance Check

What must be checked?

## 5. Human Review

Who approves?

## 6. Output

What is delivered?

## 7. Proof Event

What evidence is logged?

## 8. Next Action

What happens after?

---

## Example: Lead Scoring Workflow

```text
Trigger: client uploads lead file
Input: CSV + ICP
AI Step: score accounts
Governance: source + PII + claims risk
Human Review: delivery owner reviews top 50
Output: ranked account list
Proof Event: accounts scored + data quality
Next Action: outreach draft or pilot
```

---

## Document Standard Compliance

## Purpose
Defines this operating document's role inside Dealix Company OS.

## Owner
Sami (Founder). Reassign to the responsible operator when one is named.

## Review Cadence
Weekly until stable, then monthly.

## Inputs
- Relevant company data and signals.
- Founder decisions and customer evidence.

## Outputs
- Operating guidance, decisions, or templates produced by this document.
- Evidence captured for verification.

## Rules
- Must support revenue, delivery, trust, learning, or founder leverage.
- Must not introduce unsupported claims.
- Must preserve public/private boundaries.

## Metrics
- Completion status of the actions this document drives.
- Impact on revenue, delivery, trust, or founder leverage.

## Evidence
- Linked workflow, file, test output, customer interaction, or decision log.

## Last Reviewed
2026-05-23
