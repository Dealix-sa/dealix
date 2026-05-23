# Ultimate Observability + DORA

Dealix tracks DORA metrics next to revenue metrics — neither survives
without the other.

| DORA metric | How we measure |
|---|---|
| Deployment frequency | CI workflow `dealix-sovereign-operating-stack.yml` runs on every push to the dev branch; production deploys gated by `production-smoke` workflows |
| Lead time for changes | from commit to verifier-green (GitHub Actions) |
| Change failure rate | failed CI / total CI runs on the sovereign workflow |
| Recovery time | time from a `[FAIL]` verifier run to the next `[PASS]` on the same workflow |

| Revenue metric | Source |
|---|---|
| Replies | `outreach/conversation_log.csv` |
| Proposals | `sales/proposal_queue.csv` |
| Cash | `finance/cash_collected.csv` |

The Observability Agent (registered in `agent_registry.yaml`) collects
both sets. Founder views them via the Operating Scorecard.
