# Model Router Strategy

The router (`dealix/strategy_execution/model_router.py`) is **advisory** — it
plans which tier handles a task; it makes no live call and reads no secret in this
repo. A real client would resolve config/keys at call time on a private worker.

| Task | Tier | Where it runs |
|------|------|---------------|
| short internal classification | local_small | Ollama (private) |
| outreach draft | hosted_quality | provider-with-auth (draft-only) |
| long market report | hosted_quality | provider or vLLM GPU (private) |

Safety: no LLM in the production API, private-network worker only, no committed
keys, no public endpoints.
