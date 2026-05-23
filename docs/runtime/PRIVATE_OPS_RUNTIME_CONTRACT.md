# Private-Ops Runtime Contract

The private-ops directory (`/opt/dealix-ops-private` by default) is the
filesystem layout the Founder Console internal API depends on.

## Required layout

```
<private_ops>/
├── intelligence/
│   └── lead_intelligence_base.csv
├── outreach/
│   ├── outreach_queue.csv
│   ├── conversation_log.csv
│   └── suppression_list.csv
├── approvals/
│   └── approval_queue.csv
├── trust/
│   ├── approval_decisions.csv
│   ├── trust_flags.csv
│   └── incidents.csv
├── sales/
│   └── proposal_queue.csv
├── finance/
│   ├── payment_capture_queue.csv
│   ├── cash_collected.csv
│   └── ai_unit_economics.csv
├── runtime/
│   └── worker_state.csv
├── distribution/
│   ├── channel_scorecard.csv
│   └── sector_scorecard.csv
├── evals/
│   └── eval_status.csv
├── product/
│   └── productization_candidates.csv
├── security/
│   └── security_status.csv
└── founder/
    ├── operating_scorecard.md
    └── sovereign_readiness.md
```

`scripts/bootstrap_private_ops_runtime.py` creates this tree with empty
CSVs (headers only) and idempotent .md placeholders.

## Promises

* **Never committed.** The tree lives outside the repo. Even when
  `DEALIX_PRIVATE_OPS` happens to point at a subdir of the repo (e.g.
  during local dev), the path MUST match a `.gitignore` entry.
* **Append-mostly.** Reads return safe empty structures; writes are
  appends with fixed headers.
* **Auditable.** Every "interesting" write (approval decision, incident)
  records a row with a UUID + timestamp.
