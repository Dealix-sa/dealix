# AI Human Oversight

> A human is in the loop. Define where, when, and how.

## Oversight Points (by autonomy tier)

| Autonomy | Oversight |
|----------|-----------|
| A0 | None at runtime. Output reviewed in aggregate via audits. |
| A1 | Founder reviews each draft before promotion. |
| A2 | Founder approves the pattern once; logs are sampled. |
| A3 | Founder approves each send. No token = no send. |
| A4 | Forbidden to agents. |

## Oversight Mechanisms

1. **Approval queues.** A1+ drafts land in
   `dealix-ops-private/founder/approvals_waiting.md` until decided.
2. **Per-send tokens.** A3 sends require a founder-issued token that
   the outbound channel verifies. No token = the send is rejected.
3. **Audit sampling.** Each week, founder samples 5 drafts and 5 sends
   and verifies them against source data.
4. **Halt control.** Any agent can be disabled in < 5 minutes via the
   rollback path declared in the release gate.

## Drill: Human Oversight Tabletop (quarterly)

Pick one scenario from the threat model and walk through:

- "An A3 message was sent without a token because the channel was
  misconfigured." — does the audit catch it within 24h?
- "An A1 draft hallucinated a funding round." — does QA Checker catch
  it? If not, why?
- "A vendor model changed behaviour overnight." — does the regression
  smoke catch it? In how long?

Time-box: 30 minutes. Output: gaps and updates to policies.

## Anti-Patterns

- "Rubber-stamp" approvals (skim, click yes).
  → Mitigation: review checklist with three forced questions per draft.
- "Auto-approve trusted patterns" (drift).
  → Mitigation: re-affirm patterns every 30 days.
- "Approvals delegated to another agent".
  → Forbidden.

## Logging

Every approval — including rejections — is logged in
`dealix-ops-private/trust/approvals_log.md`:

```
- id: A-yyyy-mm-dd-NN
  tier: T1 / T2 / T3
  artifact: "..."
  outcome: approved / rejected / modified
  decision_time_seconds: N
  reviewer: Sami
```

Approval-time outliers (too fast, too slow) are reviewed monthly.
