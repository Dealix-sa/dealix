# Revenue Ops Private — Templates

These files mirror the structure expected under `dealix-ops-private/` by the
Revenue Operations Playbook. The real folder lives **outside this repo** and
is `.gitignore`d, because it contains live pipeline, prospect names, sample
content, and proposal numbers.

## How to use

```bash
# one-time, on the founder machine
cp -R docs/templates/revenue_ops_private ~/dealix-ops-private
cd ~/dealix-ops-private
git init     # optional: keep a private git repo for this
```

Then point the CLI at it:

```bash
PRIVATE_OPS=~/dealix-ops-private make revenue-ops
```

## Layout

| Path | Purpose |
|---|---|
| `icp/icp_scorecard.csv` | Per-sector ICP test results |
| `icp/bad_fit_log.md` | Disqualified prospects + reasons |
| `acquisition/lead_sources.md` | Where leads come from |
| `acquisition/source_performance.csv` | Source-level funnel metrics |
| `acquisition/message_performance.csv` | Message-level funnel metrics |
| `sales/proposal_tracker.csv` | All proposals + follow-up state |
| `sales/proposal_notes/` | One file per proposal — context, objections |
| `pipeline/pipeline_tracker.csv` | The single source of truth for leads |
| `pipeline/win_loss_log.md` | Weekly review notes |
| `delivery/sample_quality_log.csv` | Sample pack QA log |
| `delivery/samples/` | One folder per sample pack |
| `clients/_template/` | New-client folder template |
| `experiments/market_experiments.csv` | Hypotheses + outcomes |
| `revenue/revenue_action_log.csv` | One row per revenue action per day |

## Non-negotiables (mirrors Revenue Ops Playbook)

- Every lead has a `next_action`.
- Every proposal has a `follow_up_date`.
- No guaranteed revenue claim.
- No full delivery without payment / PO / written approval.
- No public proof without approval.
