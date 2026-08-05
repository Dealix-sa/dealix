# Dealix — Level Max System Spec

This directory hosts the **sovereign reference** for Dealix as a complete
system. Treat it as the source of truth — code in
[`dealix/control_plane/`](../../dealix/control_plane/) is built to match,
sentence by sentence.

## Files

- [`DEALIX_LEVEL_MAX_SYSTEM_SPEC_AR.md`](./DEALIX_LEVEL_MAX_SYSTEM_SPEC_AR.md) — **canonical Arabic spec**, sections 51–80.
- [`DEALIX_LEVEL_MAX_SYSTEM_SPEC_EN.md`](./DEALIX_LEVEL_MAX_SYSTEM_SPEC_EN.md) — English mirror, kept aligned with AR.

## The system in one line

> **Dealix is a sovereign control plane that turns signals into governed
> execution, measurable outcomes, reusable assets, and scalable revenue.**

Strongest condensed form:

```
Sami Sovereign Layer
→ Identity & Access
→ Data Classification
→ Context Feed
→ Policy Engine
→ Approval Center
→ Hermes Orchestrator
→ Agent Runtime
→ Tool Gateway
→ Outcome Graph
→ Asset Library
→ Money/Product/Partner/Market Engines
→ Scale/Kill Board
→ Platform/API/Marketplace/Ventures
```

## Tests

The Python implementation of every section is verified by:

```
tests/control_plane/
├── test_sovereignty_and_identity.py        # §51–52
├── test_policy_approval_audit.py           # §58–60
├── test_security_modes_and_incidents.py    # §64–65
├── test_agent_and_tool_runtime.py          # §61–63
├── test_commercial_and_loops.py            # §66–75
└── test_facade_end_to_end.py               # §79–80 (ControlPlane facade)
```

Run with:

```bash
python -m pytest tests/control_plane/ --no-cov
```

## HTTP surface

See [`api/routers/control_plane_os.py`](../../api/routers/control_plane_os.py)
for read-only snapshot endpoints under `/api/v1/control-plane/`.
