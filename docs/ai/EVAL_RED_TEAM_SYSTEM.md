# Eval & Red-Team System

> Quality evals and adversarial drills. Both gate release. Findings live in audit.

## 1. Eval suites

| Agent | Suite |
|---|---|
| Brand Guardian | Voice eval, visual conformance, bilingual symmetry |
| Growth Strategist | Scoring stability, explainability, false positives |
| Distribution Operator | Brand-pass, suppression honour, personalisation accuracy |
| Content Strategist | Voice, claim-evidence, bilingual |
| Offer Architect | Rung-fit precision |
| Performance Analyst | Trend detection precision |
| Trust Guardian | Suppression honour, prompt-injection resilience |
| Finance Copilot | Numbers-cite-source, language conformance |
| Delivery Copilot | QA-list adherence |

## 2. Cadence

- Per-change: relevant suite runs in CI.
- Weekly: full suite + red-team drill.
- On incident: targeted regression eval.

## 3. Red team

- Adversarial inbound payloads (prompt injection).
- Brand vandalism attempts (asset replacement, voice corruption).
- Trust gate bypass attempts.
- Suppression list spoofing.

## 4. Block-on-fail

A failing eval blocks the change. Bypass requires founder approval and an audit entry explaining the rationale.

## 5. Reporting

- Weekly eval scorecard surfaced in the daily brief.
- Monthly red-team report to the founder.
- Findings tracked in `evals/` and audit log.
