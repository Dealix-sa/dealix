# AI-Native Company Architecture

Dealix is built so the AI does the work and the founder does the
decisions. The shape of the system reflects that.

```
┌──────────────────────────────────────────────────────┐
│  Founder Console (apps/web)                          │
│  /ceo /sales-cockpit /approvals /workers /trust ...  │
└──────────────┬───────────────────────────────────────┘
               │  fetch /api/v1/internal/*
               ▼
┌──────────────────────────────────────────────────────┐
│  Internal API (api/routers/internal/founder_console) │
│  auth gate + policy adapter + runtime reader         │
└──────────────┬───────────────────────────────────────┘
               │  read / append CSV + JSON
               ▼
┌──────────────────────────────────────────────────────┐
│  Private runtime (/opt/dealix-ops-private)           │
│  intelligence / outreach / approvals / trust /       │
│  sales / finance / runtime / distribution / evals    │
│  product / security / founder                        │
└──────────────────────────────────────────────────────┘
               ▲
               │  workers + agents (kill-switched)
               │
┌──────────────────────────────────────────────────────┐
│  Agent OS (registries/agent_registry.yaml)           │
│  20 declared agents, A0/A1/A2 only, eval-gated       │
└──────────────────────────────────────────────────────┘
```

Three properties of this shape:

1. **Founder writes are the only writes that move money.** Every other
   write either updates internal state or appends to the audit log.
2. **The trust boundary is enforced in code.** Policy classes are loaded
   from YAML on startup and the policy adapter fails closed.
3. **The runtime is portable.** Today CSV + JSON; tomorrow Postgres —
   the reader is the only file that has to change.
