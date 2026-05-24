# Revenue Factory

A repeatable revenue pipeline — top of funnel to paid — with explicit
stages, owners, KPIs, and exit criteria. Anything not in the factory is
luck, not revenue.

## Purpose

Standardize the path from "stranger" to "paying customer" so a single
person can run it on a typical day, and so we can find where it's
leaking.

## Owner

Founder runs it today. As headcount grows, ownership moves to a head of
revenue named in the agent registry.

## Cadence

Daily heartbeat at 06:30 Asia/Riyadh via the `daily_revenue_machine`
workflow. Weekly review during the CEO weekly review.

## Source of Truth

- Pipeline state: `data/commercial/pipeline.json`
- Stage definitions: this file, section "Stages"
- Conversion targets: section "KPI"

## Inputs

- Inbound leads (web + referrals)
- Outbound drafts queued for approval
- Discovery call notes
- Proposal status

## Outputs

- Today's "top 3 commercial actions" surfaced at /ops/founder
- Weekly pipeline conversion report
- Audit events for every external touch

## Stages

| Stage | Definition | Exit Criteria | Owner |
| --- | --- | --- | --- |
| 1 — Source | Lead identified, basic enrichment done | ICP match confirmed | Founder |
| 2 — Reach | Outreach drafted, queued for approval | Approval + send logged | Founder |
| 3 — Reply | Reply received within 14 days | Discovery call booked | Founder |
| 4 — Discover | 45-min discovery call held | Pain + budget confirmed | Founder |
| 5 — Propose | Proposal sent (gated by `claim_policy`) | Decision in 7 days | Founder |
| 6 — Close | Contract signed, payment captured | Onboarding handoff started | Founder |

## KPI

- ≥ 10 drafts queued per week
- ≥ 30% reply rate from queued drafts
- ≥ 25% discovery → proposal
- ≥ 30% proposal → close
- Pipeline coverage ≥ 3x trailing 90-day burn

## Trust Boundary

Stages 2 and 5 produce externally-visible artifacts and are A3 actions
under `policies/dealix_control_policy.yaml` — gated by approval + audit.

## Failure Mode

- Stage 2 backs up (drafts not approved) → /ops/approvals depth alarm.
- Stage 3 → 4 conversion drops > 50% week over week → war-room review.
- Banned claim found in any artifact → CI fails.

## Recovery Path

1. Surface the leaking stage in the next CEO weekly review.
2. Add or fix a verifier for that stage.
3. Update this doc with the new exit criteria.

## Verification

```bash
make business-os
python scripts/verify_everything.py --layer revenue_factory
```

## Next Action

Open `data/commercial/pipeline.json`. Confirm every active opportunity
is in exactly one stage. Move any stalled ones today.
