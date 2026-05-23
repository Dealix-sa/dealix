# AI-Native Company Architecture

```
┌────────────────────────────────────────────────────────────────┐
│  Founder Console (Next.js, apps/web)                           │
│    /ceo /sales-cockpit /approvals /workers /trust /finance     │
│    /distribution /delivery /retention /proof /control-plane    │
│    /audit /evals /product /security                            │
└────────────┬─────────────────────────────────────────┬─────────┘
             │ X-Dealix-Internal-Token                  │
             ▼                                          ▼
┌────────────────────────────┐         ┌─────────────────────────┐
│  Internal API              │◄────────│  Policy-as-Code         │
│  /api/v1/internal/...      │         │  policies/...yaml       │
│  api/routers/internal/     │         │  registries/...yaml     │
│  founder_console.py        │         │  evals/gates/...yaml    │
└─────────┬──────────────────┘         └──────────┬──────────────┘
          │                                       │
          ▼                                       │
┌────────────────────────────┐                    │
│  Private Ops Runtime       │                    │
│  $DEALIX_PRIVATE_OPS       │                    │
│  intelligence/  outreach/  │                    │
│  approvals/     trust/     │                    │
│  sales/         finance/   │                    │
│  runtime/       distribution/                   │
│  delivery/      retention/  proof/ evals/...    │
└─────────┬──────────────────┘                    │
          ▼                                       │
┌────────────────────────────┐                    │
│  Workers / Agents          │◄───────────────────┘
│  scripts/run_*_worker.py   │  (policy evaluation + audit)
└────────────────────────────┘
```

Every external-impact action traverses Policy-as-Code, founder approval,
and the audit log before anything leaves the system.
