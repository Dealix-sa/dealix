# AI Risk Register

## Purpose
Track the live risks introduced by using AI in Dealix's operating system, with mitigations.

## Current top risks

| Risk | Likelihood | Severity | Mitigation |
|---|---|---|---|
| Hallucinated stats in external content | Medium | High | Claim governance + scripted scan |
| AI sub-agent sends external message in error | Low | High | Sub-agents have no send tools |
| Customer data fed into an AI service without consent | Low | High | Approval matrix + access log |
| Prompt injection from external content | Medium | Medium | See `PROMPT_INJECTION_DEFENSE.md` |
| Model drift on auto-generated reports | Medium | Medium | Weekly human spot-check |
| Over-reliance reduces founder learning | Medium | Medium | Daily loop forces founder to read raw inputs |

## Operating rules
- AI may **assist** in drafting; only the founder **sends**.
- AI must label its outputs as AI-generated within the private tree.
- AI may not access `dealix-ops-private/` files unless granted per-task.

## Where to register a new risk
`dealix-ops-private/trust/risk_register.csv`:
- `date, risk, severity, likelihood, owner, mitigation, status`.

## Cadence
- Weekly: review while risk register has any Open SEV-2+ rows.
- Monthly: full review even if nothing flagged.

## Decommission
- A risk is closed only when a documented mitigation is in place and tested.
- Status moves: `Open → Mitigating → Mitigated → Closed`.

## Anti-patterns
- Closing a risk without testing the mitigation.
- Logging only the easy risks.
- Treating the register as documentation theater.
