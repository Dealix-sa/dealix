# Feature Intake

> The single front door for "we should build X".
> No build starts without an intake row.

## Intake Schema

```
intake_id | requested_at | source | feature_name | one_line | strategy_filter_pass | size | status
```

- **source**: `founder` · `customer` · `agent` · `incident` · `advisor`
- **strategy_filter_pass**: which test passed (1=Revenue Sprint, 2=Retainer, 3=Trust, 4=Proof, 5=Founder Leverage) — or `NONE`
- **size**: XS / S / M / L / XL (see `KILL_DEFER_BUILD_RULES.md`)
- **status**: `intake` · `triaged` · `building` · `shipped` · `deferred` · `killed`

## Active Intake Log

```
INT-001 | 2026-05-23 | founder  | Trust modules (approval_matrix, claim_guard, policy_engine)            | 3   | M   | building
INT-002 | 2026-05-23 | founder  | Founder Brief generator (CSV → Daily Brief MD)                          | 5   | M   | intake
INT-003 | 2026-05-23 | founder  | Sector playbook automation (from shipped sprints)                       | 4   | M   | intake
INT-004 | 2026-05-23 | founder  | Managed Ops monthly cycle templates                                     | 2   | S   | intake
INT-005 | 2026-05-23 | founder  | claim_guard hardening (more banned-language patterns + tests)           | 3   | S   | intake
```

## Intake Template

Use this for every new request:

```yaml
intake_id: INT-NNN
requested_at: YYYY-MM-DD
source: founder | customer | agent | incident | advisor
feature_name: short noun phrase
one_line: |
  What this feature does, in one sentence the founder can read in 5 seconds.
problem_it_solves: |
  What's broken or missing without it.
who_is_affected: |
  Specific role / sector / count.
strategy_filter_pass: NONE | 1 | 2 | 3 | 4 | 5  # which Strategy Filter test does it pass?
estimated_size: XS | S | M | L | XL
estimated_cost: hours / SAR / both
success_metric: |
  How we'll know it worked. Measurable. Time-bound.
kill_switch: |
  When we'd stop. Specific condition.
trust_implications: |
  Any approval matrix, claim_guard, or suppression impact.
status: intake
```

## Triage Process

1. Daily Brief surfaces new intake rows
2. Founder triages in 5 min per row:
   - If `strategy_filter_pass: NONE` → DEFER with revisit date
   - If pass but no `success_metric` → return for sharpening
   - If pass + complete → move to `triaged`
3. Triaged + sized M or larger → goes to Weekly CEO Review for build/defer decision
4. Triaged + sized S or XS → founder can move to `building` directly

## Anti-Patterns (reject at intake)

- "Wouldn't it be cool if..." (no, kill at intake)
- Vague success metric ("it'll be useful")
- Missing kill switch
- Size XL (not allowed this quarter)
- Conflicts with existing rule in `DEALIX_DECISION_RULES.md`
- Skips strategy filter

## What Happens When Customer-Requested

- Capture verbatim in intake
- Founder responds within 48 hr ("we logged, we're thinking, here's our framework")
- Even if rejected, customer hears back with reasoning
- Aggregate 3+ same-request from different customers → re-evaluate

## Status Transitions

```
intake → triaged → building → shipped
                ↓
              deferred → (revisit date) → triaged or killed
                ↓
              killed
```

## Storage

- Public log here (without customer names)
- Detailed customer requests in `clients/{client}/feature_requests.md` (private)

## Review Cadence

- Daily: triage new intake rows
- Weekly: review building items + decide M+ sized items
- Monthly: review deferred backlog (what's been deferred too long?)
- Quarterly: kill anything that's been deferred 90+ days without revisit

## What This Refuses

- Building without intake
- Intake without triage
- Triage without decision
- Decision without ledger entry
