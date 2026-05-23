# Delegation Rules

> What the founder can delegate, what they must keep, and how delegation actually works.

## Delegation Test (apply to every task)

1. Is this an A3/A4 action? → **Cannot delegate this quarter**
2. Is this a final approval? → **Cannot delegate**
3. Is this a strategic decision? → **Cannot delegate**
4. Is this documented in a playbook? → **Can delegate**
5. Is this routine + reversible? → **Can delegate**

## Things The Founder Must Keep (this year)

- All A3 and A4 approvals
- Pricing decisions
- Hiring decisions
- Customer escalations
- Trust incident response (with advisor)
- Public claims
- Strategic decisions (per `STRATEGY OS`)
- Final QA signoff
- Client handoff calls

## Things The Founder Can Delegate (with playbook)

- Lead sourcing volume (to SDR, under quality rules)
- Initial enrichment
- Draft generation (final approval stays with founder)
- Sample artifact production (under SAMPLE_GENERATION_SYSTEM rules)
- Routine progress updates
- Schedule management
- Process compliance auditing
- Daily Brief assembly
- Monthly close-the-books
- Contractor management (Ops Manager only)

## Delegation Has Three Levels

| Level | What founder does | What delegate does |
|---|---|---|
| L1 | Reviews every action | Acts after approval |
| L2 | Reviews batches | Acts within playbook |
| L3 | Reviews exceptions | Acts independently within playbook + escalates only red flags |

Promotion L1 → L2 → L3 happens at 30/60/90 calibration based on scorecard.

## Delegation Failure Modes

- **Founder bottleneck rebuilds** — founder approves so slowly that delegate idles. Fix: batch-approve or pre-clear common patterns.
- **Delegate over-asks** — delegate escalates everything, defeats the purpose. Fix: clarify what's in their scope.
- **Delegate under-asks** — delegate acts outside scope. Fix: re-onboard on playbook + add to red-flag list.
- **Approval drift** — over time, "rubber stamp" approvals creep in. Fix: weekly approval log spot-check.
- **Documentation lags** — playbook says one thing, practice says another. Fix: update playbook in same week as practice change.

## Delegation Discipline (founder-side)

- Resist the urge to "just do it myself" — it kills the delegation
- Resist micromanaging at L2/L3 — it kills morale and signals broken playbook
- Always log delegation decisions in `people/decisions.md`
- Always update playbook when practice evolves

## Delegation Discipline (delegate-side)

- Follow playbook until variation is explicitly approved
- Surface uncertainty (we reward asking)
- Don't pretend to know what you don't
- Don't hide mistakes
- Don't skip the trust gates

## Specific Delegation Patterns

### Lead scoring → agent (L3)
- Agent scores per `ICP_SCORING_MODEL.md`
- Founder reviews weekly distribution (sanity check)
- Founder reviews 10 random rows monthly

### Outreach draft → agent or SDR (L1 initially → L2)
- Drafts produced per `SECTOR_PLAYBOOKS.md`
- Founder reviews per-batch in first 30 days
- Move to L2 (batch-approve) after 30 days clean

### Pipeline tracker hygiene → SDR (L2 → L3)
- SDR updates per `PIPELINE_STAGES.md`
- Founder spot-checks weekly
- Move to L3 after 60 days of clean hygiene

### Sample artifact refresh → Delivery Analyst (L1 → L2)
- Analyst drafts; founder reviews + approves before library entry
- Move to L2 after 30 days of clean QA

### Daily Brief assembly → Ops Manager (L2 → L3)
- Ops Manager assembles from CSVs; founder reviews
- Move to L3 after 60 days of clean delivery (and founder still reads it)

## When To Re-Centralize

If a delegated function:
- Produces a Trust incident → revert to L1, retrain
- Misses scorecard 2 weeks running → revert to L1, coach
- Becomes the rate-limit on the company → revert + redesign the function

## What This Refuses

- "Delegation" without a playbook
- Delegating approvals to "save time"
- Delegating without scorecard
- Delegating then never reviewing (abandonment)
- Delegating in haste then re-doing in shame
