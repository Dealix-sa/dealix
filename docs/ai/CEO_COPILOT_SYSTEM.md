# CEO Copilot

Agent id: `ceo_copilot`.

## Inputs

* `intelligence/lead_intelligence_base.csv`
* `approvals/approval_queue.csv`
* `trust/incidents.csv`
* `finance/cash_collected.csv`

## Outputs

* `founder/ceo_summary.json` — machine-readable pulse.
* Markdown recommendation for the founder's next best action.

## Constraints

* Approval class max: **A1**.
* Tools: `runtime_reader` only.
* External actions: forbidden.
* Eval suites: `no_guaranteed_claims`, `prompt_injection`, `tool_misuse`.

## How to refresh

```bash
python scripts/run_ceo_summary_worker.py
```

Writes `worker_state.csv` heartbeat and the JSON pulse.
