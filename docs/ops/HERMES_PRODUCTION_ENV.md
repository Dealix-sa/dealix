# Hermes Production Env Reference

The exact set of variables to paste into Railway / Vercel / Render
secrets for a production launch. Nothing here is committed; every
value lives in the platform's secret store.

---

## Required (Day 1)

| Variable | Example | Source | Notes |
|---|---|---|---|
| `HERMES_PROVIDER` | `openrouter` | Operator choice | Or `direct_deepseek`. |
| `OPENROUTER_API_KEY` | `sk-or-v1-…` | <https://openrouter.ai/keys> | Only required when provider = `openrouter`. **Set a credit cap.** |
| `DEEPSEEK_API_KEY` | `sk-…` (32 hex) | <https://platform.deepseek.com/api_keys> | Only required when provider = `direct_deepseek`. |
| `ADMIN_API_KEY` | random 32+ char | `openssl rand -hex 32` | Already in place for the existing admin surface. Reused by Hermes HTTP router. |

## Highly recommended (Day 2)

| Variable | Example | Default | Notes |
|---|---|---|---|
| `HERMES_LIVE_LLM` | `1` | `0` | Flip ON after preflight succeeds. |
| `HERMES_DAILY_BUDGET_USD` | `10` | `0` (disabled) | Soft cap. Start conservative; raise after Day 7. |
| `HERMES_COST_PER_CALL_USD` | `0.005` | `0.005` | Estimate used by the budget gate. |
| `HERMES_FALLBACK_PROVIDER` | `openrouter` | `openrouter` | Used when the primary is unreachable. |
| `HERMES_AUDIT_PATH` | `/data/hermes/runs.jsonl` | `var/hermes-runs.jsonl` | Point at a persistent Railway volume; default is repo-relative and will reset on every redeploy. |

## Optional

| Variable | Example | Default | Notes |
|---|---|---|---|
| `HERMES_KILL_SWITCH` | `1` | `0` | Manual halt switch. Use during incidents. |
| `HERMES_BASE_URL` | `https://api.openai.com/v1` | provider default | Override the provider base URL (rarely needed). |
| `DEALIX_FRICTION_LOG_PATH` | `/data/friction/log.jsonl` | `var/friction-log.jsonl` | Persistent path for friction events. |

---

## Railway one-shot copy/paste

```bash
# Mark these secret in Railway UI (eye icon).
HERMES_PROVIDER=openrouter
HERMES_FALLBACK_PROVIDER=openrouter
OPENROUTER_API_KEY=<paste-rotated-key>
DEEPSEEK_API_KEY=<paste-rotated-key-or-blank>
HERMES_LIVE_LLM=0
HERMES_DAILY_BUDGET_USD=10
HERMES_COST_PER_CALL_USD=0.005
HERMES_KILL_SWITCH=0
HERMES_AUDIT_PATH=/data/hermes/runs.jsonl
DEALIX_FRICTION_LOG_PATH=/data/friction/log.jsonl
```

Trigger a no-op redeploy after pasting. Then run preflight:

```bash
python scripts/hermes_preflight.py --env production
# After it returns 0, enable live LLM:
# Toggle HERMES_LIVE_LLM=1 in Railway, then:
python scripts/hermes_preflight.py --env production --live
```

## Persistent storage caveat

The default audit ledger path (`var/hermes-runs.jsonl`) lives in the
container's working directory. On Railway, that's **ephemeral** — every
redeploy wipes it and the `GET /api/v1/hermes/metrics` window resets.

Two fixes (pick one):

1. **Mount a Railway volume** at `/data` and set
   `HERMES_AUDIT_PATH=/data/hermes/runs.jsonl`. Same for friction.
2. **Defer until Day 7**: switch the JSONL store to PostgreSQL behind
   the same `audit.write()` interface. The current code does not need
   to change; only `audit._path()` needs a different backend.

For Day 0 launch, option 1 is enough.

## Rotation reminders

- Rotate every 90 days or immediately after any exposure event.
- Playbook: [`HERMES_SECRET_ROTATION.md`](HERMES_SECRET_ROTATION.md).
- Never paste a live key into a chat, a ticket, or a screenshot.
