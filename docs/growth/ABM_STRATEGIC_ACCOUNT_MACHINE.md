# ABM Strategic Account Machine

| Field | Value |
|---|---|
| Purpose | Run bespoke plays against top-tier accounts (Tier 1 ICP, high score) |
| Inputs | account scoring, sector ranking, trigger events, partner intel |
| Outputs | `abm_account_queue.csv`, per-account play sheet |
| Approval class | Per-play founder approval |
| Trust gate | Brand, suppression, partner conflict |
| Owner | Distribution Operator + Founder |
| KPI | Pipeline coverage per Tier 1 account, cash from Tier 1 |
| Failure mode | Play misfires → captured in win/loss, no auto-retry |

## Play templates (illustrative)

| Play | When to use |
|---|---|
| Founder-to-founder | Both sides are founder-led |
| Insight pack | When a trigger event aligns with a Dealix insight |
| Partner introduction | When a partner already engages the account |
| Sector benchmark | When the account is laggard / leader in a benchmark we hold |
| Custom diagnostic | When the account asks for proof |

## Schema

```yaml
queue: abm_account_queue
fields:
  - account_id
  - play_id
  - status
  - founder_owner
  - planned_actions     # list of drafts / artifacts to produce
  - created_at
  - source
```

## Rules

- Tier 1 accounts get a named founder owner.
- No more than one active play per account at a time.
- Plays last 30-60 days; review and renew or close.
