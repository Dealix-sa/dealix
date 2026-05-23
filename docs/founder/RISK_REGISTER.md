# Risk Register

> Every meaningful risk the company is carrying. Reviewed weekly.
> A risk that is not on this register cannot be claimed as a surprise.

## Format

```
ID | category | description | probability | impact | owner | mitigation | status
```

- **category**: `revenue` · `delivery` · `trust` · `product` · `cash` · `people` · `external`
- **probability**: low · medium · high
- **impact**: low · medium · high · existential
- **status**: `open` · `mitigated` · `accepted` · `closed`

## Current Risks

```
R-001 | cash      | Single-founder bank account — any disruption halts ops | low  | existential | founder | Secondary payment route + 60-day runway buffer    | open
R-002 | revenue   | Concentration risk — first 1–3 clients = 100% of MRR    | high | high        | founder | Diversify across 3 sectors; cap any client at 40% | open
R-003 | trust     | Public claim drift — could overclaim AI capabilities    | medium| high       | founder | claim_guard.py enforces evidence-pack rule         | mitigated
R-004 | delivery  | Founder-only delivery — bottleneck after 3 active sprints| high | high       | founder | Delivery Playbook → contractor onboarding @ 3+    | open
R-005 | product   | Tech sprawl in existing repo — distracts from revenue   | high | medium     | founder | Build-Defer-Kill enforced + Focus Policy cap      | mitigated
R-006 | people    | Founder burnout — 7-day weeks not sustainable           | high | existential | founder | Sunday-off rule + weekly review enforces pause   | open
R-007 | external  | Saudi market: regulatory shift on AI claims (PDPL, SDAIA)| low | high       | founder | Quarterly review of compliance posture            | open
```

## Risk Discipline

- Every weekly review touches this register
- A risk cannot be closed without a one-line outcome note
- A new risk discovered between reviews → log it the same day
- Any `existential` risk that goes 2 weeks without movement → escalates to founder One Focus

## When To Accept A Risk

You accept a risk when:
- Mitigation cost > expected loss
- The risk is genuinely outside your control
- You have a tripwire defined ("if X happens, here's the response")

Accepted risks must include the tripwire in the mitigation column.

## When To Move From Accepted To Mitigated

When you stop being able to articulate the tripwire, the risk needs new mitigation. Don't let "accepted" become "forgotten".
