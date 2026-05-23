# Client Health Score System

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Built on Trust.

The Client Health Score is the discipline by which Dealix knows,
before a customer tells us, that something is shifting. It is a
weekly per-customer score that drives the customer success motion
and the renewal/expansion plan. The score is intentionally simple:
fewer signals, clearer thresholds, faster action.

## Source file

`customer_success/client_health.csv` in the private ops runtime:

| Column          | Notes                                                            |
| --------------- | ---------------------------------------------------------------- |
| `client`         | Display name. Foreign key to the application's `accounts` table. |
| `health`         | `green`, `yellow`, `red`, `at_risk`.                              |
| `next_action`    | One-line description of the next move.                            |
| `due`            | ISO date of the next action deadline.                             |
| `owner`          | Internal owner (CS lead, or founder).                             |

The file is appended to weekly. The latest row per client is the
current state.

## Founder Console endpoints

| Endpoint                            | What it shows                                                  |
| ----------------------------------- | -------------------------------------------------------------- |
| `GET /retention/queue`              | Per-client health and next action.                             |
| `GET /customer-success/summary`     | Aggregate counts; at-risk count surfaces in the founder brief. |

## Signals

The score combines six signal families. Each family contributes a
band, and the worst band wins.

### Engagement signal

| Band    | Definition                                                       |
| ------- | ---------------------------------------------------------------- |
| green   | Weekly touchpoint completed; agenda landed.                      |
| yellow  | One missed touchpoint in the trailing 14 days.                   |
| red     | Two or more missed touchpoints in the trailing 14 days.           |
| at_risk | No engagement in the trailing 21 days.                            |

### Outcome signal

| Band    | Definition                                                       |
| ------- | ---------------------------------------------------------------- |
| green   | First-value milestone hit on plan; subsequent outcomes landing.  |
| yellow  | First-value milestone delayed by up to 14 days.                  |
| red     | First-value milestone delayed by 15+ days, or outcomes drifting. |
| at_risk | No outcome delivered against contract milestones.                 |

### Sentiment signal

| Band    | Definition                                                       |
| ------- | ---------------------------------------------------------------- |
| green   | Positive client statements in writing; founder reference offered.|
| yellow  | Neutral; no explicit signal in the trailing 30 days.             |
| red     | Concern raised in writing; unresolved.                           |
| at_risk | Explicit dissatisfaction; escalation requested.                  |

### Adoption signal

| Band    | Definition                                                       |
| ------- | ---------------------------------------------------------------- |
| green   | Client is using deliverables operationally.                      |
| yellow  | Client uses some deliverables; others are shelved.                |
| red     | Most deliverables shelved.                                       |
| at_risk | Deliverables removed from the client's operating motion.          |

### Commercial signal

| Band    | Definition                                                       |
| ------- | ---------------------------------------------------------------- |
| green   | Invoices paid on terms; no outstanding balance >30 days.         |
| yellow  | One overdue invoice resolved within 14 days of due.              |
| red     | Persistent overdue >30 days.                                     |
| at_risk | Dispute opened; payment paused.                                  |

### Stakeholder signal

| Band    | Definition                                                       |
| ------- | ---------------------------------------------------------------- |
| green   | Primary champion in place; executive sponsor reachable.          |
| yellow  | Champion availability dropped; sponsor harder to reach.          |
| red     | Champion reassigned; sponsor disengaged.                          |
| at_risk | Champion left or replaced; no sponsor.                            |

## Composite rule

The overall score is the worst band across the six families. This
keeps the score honest: a single critical signal cannot be averaged
away by green signals elsewhere.

## Cadence

| Activity                       | Cadence    |
| ------------------------------ | ---------- |
| Signal data collection         | Continuous |
| Score recomputation             | Weekly     |
| Founder brief inclusion         | Daily (aggregate); per-client when band drops |
| Per-client review with founder  | Monthly for green; weekly for yellow; immediate for red/at_risk |

## Next action discipline

Every row has a `next_action` and a `due`. The owner cannot leave
either empty. Examples:

| Band    | Example next action                                                              |
| ------- | -------------------------------------------------------------------------------- |
| green   | "Monthly review on YYYY-MM-DD. Surface expansion conversation."                  |
| yellow  | "Re-engage champion. Confirm reason for missed touchpoint."                      |
| red     | "Escalate to founder. Send executive recap with corrective plan."                |
| at_risk | "Founder-led save plan. Convene churn-prevention meeting within 5 business days." |

## Actions when bands drop

| Transition       | Action                                                                                |
| ---------------- | ------------------------------------------------------------------------------------- |
| green → yellow   | CS owner contacts champion; logs the cause in the row's next action.                  |
| yellow → red     | Trust flag at `severity: medium`; founder notified in the next brief.                |
| red → at_risk    | Incident opened in `trust/incidents.csv`; founder-led save plan required.            |
| any → green      | Recorded; cause documented. (Good outcomes are also learning.)                       |

## Reporting

The aggregate counts the Founder Console surfaces:

```
clients_active = count of distinct client rows.
clients_at_risk = count of rows where health in {red, at_risk}.
```

The Customer Success summary endpoint returns both.

## Privacy

The health row is operating data, not customer-facing. It is never
shared externally. Internal sharing is limited to roles with a
business need.

## Anti-patterns

| Anti-pattern                                  | Why                                                                    |
| --------------------------------------------- | ---------------------------------------------------------------------- |
| Score inflation                                | Defeats the point. The score is for action, not optics.                |
| Score without next action                      | A score with no next move is decoration.                               |
| Averaging across signals                       | Hides critical signals.                                                |
| Ignoring yellow                                | Yellow is the cheapest to fix; red is much more expensive.              |
| Re-running the score after every conversation  | Weekly cadence is enough; constant rescoring trains the team to chase. |

## Discipline

1. Six signals, worst band wins.
2. Every client has a next action.
3. Every band drop has an owner and a date.
4. Yellow is the action band.
5. The score informs renewals, not the other way around.

## Cross-references

- `CUSTOMER_SUCCESS_OS.md` for the broader discipline.
- `RENEWAL_AND_EXPANSION_OS.md` for renewal action triggers.
- `REFERRAL_SYSTEM.md` for what we ask of green customers.
- `OBJECTION_ANALYTICS.md` for capturing concerns in red bands.
