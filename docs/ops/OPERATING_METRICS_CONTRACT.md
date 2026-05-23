# Operating Metrics Contract

Every system inside Dealix must declare, in this document, how it
measures itself. A system without a metrics contract is not a system,
it is a folder.

Every contract must define:

1. Input metric
2. Output metric
3. Quality metric
4. Risk metric
5. Review cadence

## Revenue OS
- Input: leads sourced
- Output: cash collected
- Quality: close rate
- Risk: bad-fit clients
- Cadence: daily / weekly

## Delivery OS
- Input: active clients
- Output: reports delivered
- Quality: QA pass rate
- Risk: overdue delivery
- Cadence: daily / weekly

## Trust OS
- Input: actions reviewed
- Output: risks blocked
- Quality: false negative rate
- Risk: unlogged sensitive action
- Cadence: weekly

## Product OS
- Input: customer signals
- Output: shipped features / fixes
- Quality: bug regression rate
- Risk: trust-test failures on main
- Cadence: weekly

## Learning OS
- Input: experiments run
- Output: playbook updates
- Quality: experiments with a clear decision
- Risk: repeated unaddressed loss reasons
- Cadence: weekly

## Content OS
- Input: insights drafted
- Output: posts published
- Quality: reply / inbound rate
- Risk: unverified claim published
- Cadence: weekly

## Client Success OS
- Input: deliveries shipped
- Output: retainers / upsells
- Quality: client health score
- Risk: silent churn
- Cadence: weekly

## Founder OS
- Input: decisions queued
- Output: decisions resolved with evidence
- Quality: % decisions with attached evidence
- Risk: decision backlog older than 7 days
- Cadence: daily
