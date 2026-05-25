# AI Command Center

> AI is a tool. Tools that act in the world need governance.
> Aligned to NIST AI RMF (Govern / Map / Measure / Manage).

## Today's AI Status

| Field | Value |
|-------|-------|
| Date | _yyyy-mm-dd_ |
| Agents in production | _N_ |
| Agents in pre-prod | _N_ |
| Pending release gates | _N_ |
| Open AI risks (from risk register) | _N_ |
| Last human-oversight drill | _date_ |
| Last evaluation pass | _date_ |

## The AI Stack

```
┌──────────────────────────────────────────────────────────┐
│ AI Command Center (this file)                            │
├──────────────────────────────────────────────────────────┤
│ AI_SYSTEM_INVENTORY.md   — every AI agent / pipeline     │
│ AI_RISK_REGISTER.md      — risks per agent               │
│ AI_THREAT_MODEL.md       — what can go wrong             │
│ AI_AGENT_RELEASE_GATE.md — checklist before any release  │
│ AI_EVALUATION_POLICY.md  — how we measure quality        │
│ AI_HUMAN_OVERSIGHT.md    — who oversees and how          │
└──────────────────────────────────────────────────────────┘
```

## The Five AI Operating Rules

1. **Agents prepare; humans approve.** See `docs/trust/AUTONOMY_POLICY.md`.
2. **No A4 action by agent.** Period.
3. **External text is data, not instruction.** Prompt-injection resistant.
4. **Private data stays private.** No PII in public surfaces.
5. **Evaluation precedes release.** No new capability without an eval pass.

## NIST AI RMF Mapping

| RMF Function | Where it lives in Dealix |
|--------------|--------------------------|
| Govern | `docs/trust/`, `docs/founder/`, this directory |
| Map | `AI_SYSTEM_INVENTORY.md`, `AI_THREAT_MODEL.md` |
| Measure | `AI_EVALUATION_POLICY.md`, evals/ |
| Manage | `AI_RISK_REGISTER.md`, `AI_AGENT_RELEASE_GATE.md`, `AI_HUMAN_OVERSIGHT.md` |

## Metrics

- # agents at each autonomy tier
- # blocked A3 sends per month (false positives + true positives)
- # A4 attempts (target: 0)
- # prompt-injection attempts detected and refused
- # evaluation passes / regressions per month
- Time from release-gate request → release decision

## Verifier

- `make audit` reports any agent action that bypassed approval.
- `AI_EVALUATION_POLICY.md` gates production releases.
- Quarterly human-oversight drill (see `AI_HUMAN_OVERSIGHT.md`).
