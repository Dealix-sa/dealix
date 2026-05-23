# ABM Strategic Account Machine

**Owner:** Founder + Operations
**Source of truth:** This doc + `docs/growth/AUTONOMOUS_DISTRIBUTION_MACHINES.md`

## Purpose

The ABM (Account-Based Marketing) Strategic Account Machine runs deeper, multi-persona orchestration on a small set of named strategic accounts where a sprint outcome is high-value but a Diagnostic-by-cold-DM is unlikely to land. It coordinates research, content tailoring, multi-persona outreach (within touch caps), and partner-led intros to build access over a 90-day arc.

It is the patient, high-craft layer of the Distribution War Machine. It runs on 5-10 accounts at any time, not 50.

## Inputs

- **Strategic account list** — Tier-A accounts that score above 85 and meet additional criteria (deal size > SAR 150k, sector relevance, partner-reachability).
- **Per-account research dossier** — public-source intelligence on the account's sector, recent moves, leadership, stated priorities.
- **Multi-persona map** — Founder, Head of Sales, Head of GTM, and adjacent influencers within the account.
- **Partner network** — which partners have access into the account.

## Outputs

- **Per-account playbook** — 90-day plan with named milestones (research, soft touch, content land, intro, meeting, Diagnostic).
- **Tailored content** — sector-specific or account-specific signal piece routed via Content to Demand.
- **Coordinated multi-persona outreach** — sequenced across personas with cap-respect.
- **Partner-led intro request** when a partner has access.
- **Quarterly account review** — what worked, what stalled, next quarter's plan.

## 90-day arc structure

| Days | Phase | Action |
|---|---|---|
| 1-15 | Research and dossier | Build the account dossier; identify personas; identify partner access |
| 16-30 | Soft land | Publish or share a content piece relevant to the account's stated priorities |
| 31-45 | Partner intro | Activate partner-led intro if available; otherwise primary persona warm DM |
| 46-60 | Multi-persona | Add secondary persona touch (different angle); respect 14-day per-persona cap |
| 61-75 | Diagnostic offer | If engagement detected, offer a Diagnostic; if not, continue measured presence |
| 76-90 | Review | Quarterly review; either continue, downgrade to Tier-A standard, or park |

## Source of truth

This doc + the per-account dossier + the strategic account ledger.

## Approval class

**A2** — Founder + Operator per touch; Founder + Operator per playbook ratification at day 1.

## Trust gate

- Multi-persona orchestration respects per-persona 14-day cap.
- Total account-touch cap per quarter: 10 (across all personas combined; see `AUTONOMOUS_DISTRIBUTION_MACHINES.md` orchestration on a single account).
- All research uses sanctioned public sources only.
- Partner intros require partner consent before activation.
- Strategic account designation requires Founder sign-off.

## Owner

- **Code owner:** Operations Engineering.
- **Operational owner:** Founder + assigned ABM Operator.

## Worker script (placeholder)

`workers/abm_strategic_account_worker.py` (planned). Maintains per-account state machine, surfaces due actions, coordinates with adjacent machines.

## KPI

| Metric | Target |
|---|---|
| Strategic accounts active | 5-10 at any time |
| 90-day Diagnostic-call rate | >= 30 percent of active strategic accounts |
| 90-day Diagnostic-to-sprint rate | >= 50 percent of Diagnostic calls |
| Touch-cap compliance | 100 percent |
| Quarterly review completion | 100 percent |

## Failure mode

- Strategic account count balloons past 10; depth collapses.
- Per-persona cap is breached because operator forgets the orchestration rule.
- Partner intro is requested without partner consent.
- 90-day arc fails repeatedly; operator continues anyway out of attachment.

## Recovery path

1. Force strategic account count back to 10.
2. Re-enforce per-persona cap at the queue layer.
3. Re-verify partner consent before any future activation.
4. Park accounts that fail two consecutive 90-day arcs; revisit only on a new trigger.

## What this machine does NOT do

- It does not blanket an account with simultaneous multi-channel saturation.
- It does not bypass partner consent.
- It does not commit to engagement outcomes.

## Cross-links

- Distribution War Machine: `docs/growth/DISTRIBUTION_WAR_MACHINE.md`
- Account scoring: `docs/intelligence/ACCOUNT_SCORING_MODEL.md`
- Partner referral: `docs/growth/PARTNER_REFERRAL_MACHINE.md`
- Content to Demand: `docs/growth/CONTENT_TO_DEMAND_ENGINE.md`

## Disclaimer

Dealix does not guarantee strategic-account conversion. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
