# Approval Matrix

> Who approves what.
> An approval is a decision. Every decision needs an owner and a record.

## Approval Tiers

| Tier | Definition | Approver | Record |
|------|------------|----------|--------|
| T0 | Internal-only, reversible | Auto | Log only |
| T1 | Customer-facing draft / internal config | Founder | Queue + log |
| T2 | Customer-facing send / external publication | Founder | Queue + log + audit |
| T3 | Contract / public claim / agent autonomy change | Founder (recorded decision) | Decision queue + audit |

## What requires which tier

| Action | Tier |
|--------|------|
| Internal note, draft document | T0 |
| Add a row to a private ledger | T0 |
| Agent generates a proposal draft | T1 |
| Founder edits the draft | — |
| Founder sends the proposal | T2 |
| Founder posts a LinkedIn case study | T2 |
| Founder signs a contract | T3 |
| Founder enables a new agent capability for clients | T3 |
| Founder approves a discount > 20% | T3 |
| Founder approves a refund | T3 |
| Founder approves an exception to the Bad Revenue Filter | T3 |
| Founder approves an exception to the Autonomy Policy | T3 |

## Approval Record Format

Every T1+ approval is recorded in
`dealix-ops-private/founder/approvals_waiting.md` (queue) and, once
approved, in `dealix-ops-private/trust/approvals_log.md` (audit).

```
- id: A-yyyy-mm-dd-NN
  tier: T2
  action: "Send proposal v2 to Account X"
  evidence_link: "..."
  approver: Sami
  decided_on: yyyy-mm-dd
  outcome: approved / rejected / modified
  note: "..."
```

## Approval SLA

- T1: < 24 hours
- T2: < 24 hours
- T3: < 72 hours (uses the Go/No-Go process)

## Queue Depth Targets

- Open T1: ≤ 5
- Open T2: ≤ 3
- Open T3: ≤ 1

A queue above target is a Founder Bottleneck.
