# Ultimate Architecture Map

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Founder Console (Next.js)                    │
│  /ceo  /sales-cockpit  /approvals  /workers  /trust  /finance       │
│  /distribution  /delivery  /retention  /proof  /control-plane       │
│  /audit  /evals  /product  /security  /sovereign                    │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
                  X-Dealix-Internal-Token (production)
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│              FastAPI app  /api/v1/internal/* (this repo)            │
│  api/routers/internal/founder_console.py                            │
└────────────────┬─────────────────────────────────┬─────────────────┘
                 │                                 │
                 ▼                                 ▼
       api/internal/runtime_reader        api/internal/policy_adapter
                 │                                 │
                 ▼                                 ▼
   /opt/dealix-ops-private/**         policies/dealix_control_policy.yaml
                                       registries/agent_registry.yaml
                                       evals/gates/dealix_agent_eval_gate.yaml

           ▲                                       ▲
           │                                       │
   ┌───────┴─────────┐                ┌───────────┴────────────┐
   │ Worker scripts  │                │  Eval Guardian +       │
   │ scripts/run_*   │                │  Trust Guardian        │
   └─────────────────┘                └────────────────────────┘
```

Three flows:

* **Read flow:** browser → internal API → runtime_reader → CSV/JSON.
* **Approval flow:** browser → internal API → policy adapter → append to
  approval_decisions.csv.
* **Worker flow:** scheduler → worker script → runtime_reader → CSV/JSON
  + worker_state heartbeat.
