# Ultimate Architecture Map

```
┌──────────────────────────────────────────────────┐
│ Founder Console (Next.js)        apps/web/app/*  │
│   /ceo /sales-cockpit /approvals /workers ...    │
└───────────────┬──────────────────────────────────┘
                │ NEXT_PUBLIC_DEALIX_API + token
                ▼
┌──────────────────────────────────────────────────┐
│ Internal API (FastAPI)                           │
│   api/routers/internal/founder_console.py        │
│   /api/v1/internal/*                             │
└───────────────┬──────────────────────────────────┘
                │ auth: DEALIX_INTERNAL_TOKEN
                ▼
┌──────────────────────────────────────────────────┐
│ Helpers                                          │
│   api/internal/auth.py                           │
│   api/internal/runtime_reader.py                 │
│   api/internal/policy_adapter.py                 │
│   api/internal/agent_registry_reader.py          │
└───────────────┬──────────────────────────────────┘
                │ filesystem
                ▼
┌──────────────────────────────────────────────────┐
│ Private Ops Tree                                 │
│   ${DEALIX_PRIVATE_OPS}/                         │
│     intelligence / outreach / approvals /        │
│     trust / sales / finance / runtime /          │
│     distribution / evals / product / security    │
└──────────────────────────────────────────────────┘
                ▲
                │ append/update
                │
        scripts/run_*_worker.py
        scripts/update_worker_state.py
        scripts/generate_operating_scorecard.py
        scripts/bootstrap_private_ops_runtime.py
```

## Trust gate

```
agent → trust_guardian → policy_adapter.evaluate
        → approval_queue.csv
founder reviews → /api/v1/internal/approvals/{id}/(approve|reject|edit|escalate)
        → approval_decisions.csv (append-only audit)
```
