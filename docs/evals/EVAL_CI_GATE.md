# Eval CI Gate

## Purpose
Make AI quality a required release gate.

## Eval Suites
- no-overclaim
- approval classification
- sensitive data leakage
- prompt injection
- Arabic quality
- lead scoring consistency
- proposal quality
- evidence use

## CI Rule
Any PR that changes agents, prompts, scoring, outreach, or proposals must run evals.

## Pass Criteria
- no A3 bypass
- no guaranteed claims
- no secret leakage
- no suppressed lead outreach
- no public proof without approval
