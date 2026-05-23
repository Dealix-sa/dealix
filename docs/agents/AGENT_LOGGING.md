# Agent Logging

## What Every Agent Must Log

Every agent run produces a structured log entry with these fields:

| Field | Description |
|---|---|
| `agent` | Agent name from the registry |
| `version` | Prompt + model + guardrail version hash |
| `run_id` | UUID per run |
| `started_at` | ISO 8601 UTC |
| `finished_at` | ISO 8601 UTC |
| `input_ref` | Pointer to input payload (queue ID or path) |
| `output_ref` | Pointer to output artifact |
| `risk_class` | Low / Medium / High / Critical |
| `approval_required` | A0 / A1 / A2 / A3 |
| `approval_status` | pending / approved / rejected / not-required |
| `tokens_used` | (optional) for cost tracking |
| `error` | Structured error if the run failed |

## Storage

- Live logs are append-only JSONL.
- Logs are retained for at least 12 months.
- Logs containing client data are stored only in the private ops repo.

## Privacy

- No raw client PII in agent logs in the public repo.
- Public logs may carry hashed identifiers, never names or contact details.

## Use in Evaluations

The eval suites in `evals/` pull from these logs to score:
- Approval correctness (did the agent route correctly?).
- Latency.
- Failure modes.

## Use in Trust Reviews

The Trust review reads the previous 30 days of logs and looks for:
- A2 / A3 actions executed without DECISION_LOG entries.
- Trust Guard bypasses.
- Repeated schema mismatches indicating drift.
