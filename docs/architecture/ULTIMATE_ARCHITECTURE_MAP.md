# Ultimate Architecture Map

```
[Founder]
    │
    ▼
[Founder Console / apps/web]
    │   (X-Dealix-Internal-Token)
    ▼
[Internal API / api/routers/internal/founder_console.py]
    │
    ├── reads → api/internal/runtime_reader.py → $DEALIX_PRIVATE_OPS/...
    ├── evals → api/internal/policy_adapter.py → policies/+registries/+evals/
    └── audits → $DEALIX_PRIVATE_OPS/trust/approval_decisions.csv

[Workers / scripts/run_*_worker.py]
    │
    └── writes → $DEALIX_PRIVATE_OPS/...
```
