# Autonomous Growth & Strategy Execution OS

An internal, draft-only execution layer. It understands Dealix strategies, plans
the day, executes **safe internal** actions (reports/queues/proof logs), and
prepares every risky action for human approval.

## Autonomy levels
- 0 observe · 1 analyze · 2 draft · 3 internal execution (**daily default**) ·
  4 repo execution · 5 external execution (**BLOCKED, not implemented**).

The engine can never reach level 5. The safety gate clamps every request to at
most level 4 and routes all external-facing work to the approval queue.

## Run
```
python scripts/commercial/run_autonomous_growth_daily.py \
    --autonomy-level 3 --mode draft-only --limit 50
```

## Strategies
Defined in `dealix/strategy_execution/strategies/*.yaml` (13 files): technical
trust, money now, revenue sprint, Saudi market access, foreign targeting, local
B2B growth, B2G readiness, content factory, proof pack, partner growth, referral
loop, SEO market reports, founder daily ops.

## Outputs (per day, gitignored)
- `reports/autonomous_growth/daily/YYYY-MM-DD.md`
- `.../actions/YYYY-MM-DD_actions.json`
- `.../approvals/YYYY-MM-DD_approvals.json`
- `.../proof/YYYY-MM-DD_proof_log.json`
- `.../content/YYYY-MM-DD_content_queue.md`
- `.../learning/YYYY-MM-DD_learning.md`

## Safety
No send, no publish, no charge, no production change. Verify with
`python scripts/commercial/verify_autonomous_growth.py`.
