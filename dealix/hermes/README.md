# Hermes — Top-Layer Agent Orchestrator

This package is the operating layer that sits above `dealix-pm` and
routes a single founder intent through doctrine-bound dispatch:

```
intent → identity → governance gate → router → executor → audit → ledgers
                                                                   ↘ friction_log
                                                                   ↘ approval_center
                                                                   ↘ capital_ledger
```

Anchored under [`docs/institutional/HERMES_CHARTER.md`](../../docs/institutional/HERMES_CHARTER.md)
and the Dealix Constitution. Honors all 11 non-negotiables; refuses
cold-WhatsApp / LinkedIn automation / scraping / fabricated proof at
the gate and writes a refusal to friction_log.

## Module layout

| File | Role |
|---|---|
| `__init__.py` | Public surface (`HermesOrchestrator`, `HermesTask`, `LiveLLMExecutor`, …). |
| `__main__.py` | CLI entry — `python -m dealix.hermes "<intent>"`. |
| `identity.py` | Agent identity + monotonic `run_id` (non-negotiable #9). |
| `governance_gate.py` | Pre-execution doctrine check. Pure logic; no side effects. |
| `router.py` | Keyword classification → `(task_class, sub_agent, gear, model)`. |
| `audit.py` | JSONL ledger at `var/hermes-runs.jsonl` + friction bridge. |
| `integrations.py` | Approval-center + capital-ledger bridges (lazy-imported). |
| `orchestrator.py` | `HermesOrchestrator.dispatch(task) -> HermesTaskResult`. |
| `live_executor.py` | Wraps an envelope executor with an actual provider call. |
| `agents/` | One envelope builder per Claude Code sub-agent. |

## Quick start

```python
from dealix.hermes import HermesOrchestrator, HermesTask
from dealix.hermes.agents import route_to_agent_executor

orch = HermesOrchestrator(executor=route_to_agent_executor)
result = orch.dispatch(HermesTask(intent="refactor the /leads router"))
print(result.decision.decision)        # → "approved"
print(result.route.sub_agent)          # → "dealix-engineer"
print(result.output["kind"])           # → "prompt_envelope"
```

Promote to live LLM:

```python
from dealix.hermes import LiveLLMExecutor

executor = LiveLLMExecutor(base_executor=route_to_agent_executor)
orch = HermesOrchestrator(executor=executor)
# HERMES_LIVE_LLM=1 + OPENROUTER_API_KEY (or DEEPSEEK_API_KEY) required.
```

## Adding a sub-agent

1. Drop `.claude/agents/<name>.md` with tools + Hermes integration hook.
2. Add `dealix/hermes/agents/<name>_executor.py` mirroring `pm_executor.py`.
3. Extend `TaskClass`, `_SUB_AGENT`, `_KEYWORD_TO_CLASS`, and
   `_TASK_GEAR_FOR_CLASS` in `router.py`.
4. Register the executor in `agents/__init__.py`.
5. Add a `tests/hermes/test_orchestrator.py` case covering routing + envelope.

Everything else (gate, audit, ledgers, provider routing) is reused.

## Tests

39 tests under `tests/hermes/` + 1 provider-key guard at
`tests/test_no_provider_key_in_repo.py`. Run dep-light:

```bash
python -m pytest tests/hermes/ --noconftest -o addopts="" -p no:cacheprovider -q
```

## Charter amendment

Per Charter §8, this module's behavior is pinned by
`tests/hermes/test_charter_pinned.py`. Any change to the Charter or to
this module's doctrine semantics requires a separate PR; do not bundle
behavior changes with feature work.

— Hermes obeys the doctrine, ships the work, never improvises around the limits.
