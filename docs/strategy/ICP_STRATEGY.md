# ICP Strategy

> Who we sell to first, second, and never.
> Updated quarterly. Drives `docs/acquisition/SECTOR_PLAYBOOKS.md`.

## Tier 1 ICP (sell to first)

**Profile:**
- Saudi-headquartered company
- Revenue SAR 5M – 50M
- Founder or family CEO actively involved
- 10 – 80 employees
- Existing sales motion (even if chaotic)
- B2B (we don't do B2C this quarter)

**Sectors (Tier 1):**
1. Logistics & last-mile (high deal volume, manual quoting)
2. B2B professional services (accounting, legal-adj, recruiting)
3. Light manufacturing & distribution (long deal cycles, painful follow-up)

**Buyer titles:**
- Founder
- CEO
- Head of Sales / Sales Manager
- COO (when ops + sales report there)

**Trigger signals (buy now):**
- Recently lost a key salesperson
- Just hired or trying to hire an SDR
- Has a CRM but isn't using it
- Has > 100 leads/month with no scoring
- Reports in WhatsApp, not in a system

## Tier 2 ICP (sell to after first 3 paid sprints)

**Profile:**
- Saudi SAR 50M – 200M revenue
- Professional sales team (3 – 10 people)
- Has a CRM in use
- Has formal procurement < 60 days

**Why later:** Longer sales cycle, formal procurement adds friction. Wait until we have proof packs from Tier 1.

## Tier 3 ICP (revisit at 6 months)

- Enterprise (> SAR 200M revenue)
- Government / semi-gov entities
- GCC outside Saudi
- Family offices

## Not ICP (never, this year)

- Pre-revenue startups
- Pure B2C (e-commerce, retail)
- Crypto / unregulated finance
- Anyone asking for "AI agents to replace humans"
- Anyone with procurement > 90 days

## Fit Score (used by Acquisition OS)

Score every prospect 0–100:

| Signal | Weight |
|---|---|
| In Tier 1 sector | 25 |
| Revenue SAR 5M – 50M | 20 |
| Founder/CEO contactable | 15 |
| Has > 100 leads/month | 10 |
| Recent CRM purchase or SDR hire | 10 |
| Has English + Arabic ops | 5 |
| Existing case-study sector for us | 10 |
| Warm intro available | 5 |

Action thresholds:
- **80–100:** Personal outreach this week, founder-drafted
- **60–79:** Standard outreach next week, agent-drafted + founder-approved
- **40–59:** Newsletter / content nurture only
- **< 40:** Suppression — do not contact

This scoring is enforced by `dealix/agents/` (scoring_agent) and gated by `dealix/trust/approval_matrix.py`.

## Disqualifiers (auto-suppress)

Any one of these moves the lead to suppression list:
- Asked to be removed
- Pre-revenue
- Outside Saudi (unless Tier 3 revisit triggered)
- Government tender-only buyer
- Competitor
- Prior incident (logged in `trust/data_incidents.md`)

## Review Cadence

- Quarterly: re-score the Tier 1 sector mix based on reply rate + close rate
- Monthly: review the disqualifier list — any new patterns?
- Weekly: update the trigger signals based on what actually got a "yes"

## What This Strategy Refuses

- "Anyone with budget" — no, fit first
- "Let's chase enterprises for big logos" — no, not this quarter
- "Let's do free pilots to get logos" — no, we charge 499 SAR minimum
- "Let's expand to GCC for volume" — no, depth before breadth
