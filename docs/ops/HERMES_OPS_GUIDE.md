# Hermes Ops Guide — End-to-End Usage

The founder-facing operating manual for the Hermes orchestrator layer.
Skim it once; refer back when a step in the daily loop fails or a new
sub-agent gets wired in.

**Anchors:**
- Charter: `docs/institutional/HERMES_CHARTER.md`
- Constitution: `docs/institutional/DEALIX_CONSTITUTION.md`
- Secret rotation: `docs/ops/HERMES_SECRET_ROTATION.md`

---

## 1. The entry points

| Surface | Command / endpoint | When to use |
|---|---|---|
| CLI | `python -m dealix.hermes "<intent>"` | Local terminal, ad-hoc dispatch. |
| Slash command | `/hermes <intent>` inside Claude Code | One-shot dispatch from chat. |
| Daily script | `python scripts/hermes_daily.py` | Morning ritual; produces today's brief. |
| HTTP dispatch | `POST /api/v1/hermes/dispatch` | Trigger from n8n / WhatsApp bot / mobile / Railway cron. |
| HTTP metrics | `GET /api/v1/hermes/metrics?window_days=7` | Founder cockpit / weekly anchor counts. |
| HTTP status | `GET /api/v1/hermes/status` | Health view (provider, kill switch, guardrails). |
| Replay | `python scripts/hermes_replay.py <run_id>` | Re-dispatch a past run for debugging. |
| Smoke | `python scripts/hermes_smoke.py [--live]` | Offline + optional live provider ping. |

All surfaces share the same orchestrator, the same governance gate, and
the same audit ledger. Refusing one place refuses them all.

## 2. CLI quick reference

```bash
# Routed envelope for the engineer sub-agent
python -m dealix.hermes "refactor the FastAPI router for /leads"

# Pipeable JSON output
python -m dealix.hermes --json "produce today's founder brief"

# Customer-scoped run (writes to friction_log on refusal)
python -m dealix.hermes --customer cust_001 "run sprint day 3 for ACME"

# Doctrine-blocked request — exits with code 3 and prints the refusal
python -m dealix.hermes "send cold whatsapp blast to warm list"
```

Exit codes: `0` ok, `1` executor failure, `2` queued_for_approval,
`3` rejected, `4` kill switch, `5` usage.

## 3. Daily loop

```bash
# Print the brief
python scripts/hermes_daily.py

# Write to a gitignored markdown file (recommended for cron)
python scripts/hermes_daily.py --out data/founder_briefs/$(date -u +%Y-%m-%d)_hermes.md
```

The brief composes three dispatches (`pm_status`, `delivery_summary`,
`sales_drafts`) and renders a single markdown document with the
governance decision per dispatch and the bilingual disclaimer footer.

The brief never auto-sends. The founder copies it manually (per
Article 4 of the Constitution).

## 4. HTTP surface

```bash
# Health / config view
curl -H "X-Admin-API-Key: $ADMIN_API_KEY" \
  http://localhost:8000/api/v1/hermes/status | jq

# Dispatch (intent is the only required field)
curl -X POST http://localhost:8000/api/v1/hermes/dispatch \
  -H "X-Admin-API-Key: $ADMIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"intent": "summarize today friction signals"}' | jq
```

HTTP semantics:
- `200` approved + executor ok
- `403` rejected by doctrine (refusal body in `detail`)
- `409` kill switch active (`HERMES_KILL_SWITCH=1`)
- `500` executor crashed (orchestrator captured the error)
- Approval-required dispatches return `200` with
  `governance_decision.decision = "needs_approval"` and
  `http_hint_status = 202` in the body.

## 5. Provider routing

Two providers are supported:

```bash
# Default — Three-Gear via OpenRouter
HERMES_PROVIDER=openrouter

# DeepSeek-direct (cheaper for gear 1)
HERMES_PROVIDER=direct_deepseek
HERMES_FALLBACK_PROVIDER=openrouter
```

Gear-to-provider resolution lives in `dealix/llm/engine.py`. Models the
direct provider cannot serve (Minimax M2.5 / M2.7 on gear 2/3) fall
back to OpenRouter automatically.

## 5b. Live LLM execution

By default Hermes returns a structured envelope — useful for tests and
inspection but does not move work forward. Enable real LLM calls by:

```bash
export HERMES_LIVE_LLM=1
# Plus the active provider's key:
export OPENROUTER_API_KEY=…           # if HERMES_PROVIDER=openrouter
export DEEPSEEK_API_KEY=…             # if HERMES_PROVIDER=direct_deepseek
```

Optional safety knobs:

| Variable | Purpose | Default |
|---|---|---|
| `HERMES_DAILY_BUDGET_USD` | Refuse new live calls once estimated daily spend ≥ value (0 disables). | `0` |
| `HERMES_COST_PER_CALL_USD` | Per-call cost estimate used by the budget check. | `0.005` |

The executor injects every doctrine constraint from the envelope as the
system prompt, so the LLM is told to refuse violations even if the gate
misses something exotic. Failures (network, 4xx/5xx, JSON malformed)
return `ok=false` with `kind=live_llm_error` rather than crashing.

Idempotency: same `(date, customer_id, intent)` hashes to the same
`idempotency_key`. Use it on the caller side to detect duplicates.

## 5c. Metrics endpoint

```bash
curl -H "X-Admin-API-Key: $ADMIN_API_KEY" \
  "http://localhost:8000/api/v1/hermes/metrics?window_days=7" | jq
```

Returns counts only — `by_decision`, `by_sub_agent`, `by_provider`,
`success_runs`, `total_runs`, `ledger_size`. No PII; safe to surface
on the founder cockpit.

## 5d. Replay

```bash
python scripts/hermes_replay.py hermes_1779977174796_98ef7ddf
python scripts/hermes_replay.py --json hermes_…
```

Reads the original intent + customer from `var/hermes-runs.jsonl` and
re-dispatches with a fresh `run_id`. Useful for debugging refusals
("did my rewording survive the gate?") and for spot-checking that a
prompt change actually shifts behavior.

## 6. Kill switch

Halt all dispatch during an incident:

```bash
export HERMES_KILL_SWITCH=1
```

Every subsequent dispatch returns `decision = kill_switched` and is
mirrored into `friction_log` as a high-severity `manual_override`
event. Unset the variable once the incident is resolved.

## 7. Audit + observability

| Source | Path / table | What's there |
|---|---|---|
| Hermes audit | `var/hermes-runs.jsonl` | One row per dispatch (run_id, decision, route, output ref). |
| Friction log | `var/friction-log.jsonl` (or `DEALIX_FRICTION_LOG_PATH`) | Mirrored refusals + approval-required events, customer-scoped. |
| Approval center | `/api/v1/approvals/pending` | Drafted external sends waiting for founder click. |

Tail the audit log during a debug session:

```bash
tail -f var/hermes-runs.jsonl | jq -c '{run_id, decision: .governance_decision.decision, sub: .sub_agent}'
```

## 8. Adding a new sub-agent

1. Add a new `.claude/agents/<name>.md` definition that lists tools and
   constraints. Include a short "Hermes integration" section pointing at
   the executor module.
2. Add `dealix/hermes/agents/<name>_executor.py` that mirrors
   `pm_executor.py` — a thin envelope builder, no LLM calls inside.
3. Extend `TaskClass`, `_SUB_AGENT`, `_KEYWORD_TO_CLASS`, and
   `_TASK_GEAR_FOR_CLASS` in `dealix/hermes/router.py`.
4. Register the executor in `dealix/hermes/agents/__init__.py`.
5. Add an orchestrator test in `tests/hermes/test_orchestrator.py`
   covering both the routing and the envelope content.

The orchestrator's gate, audit, and provider routing are reused
automatically — there's nothing to wire on those layers.

## 9. Failure playbook

| Symptom | First check | Fix |
|---|---|---|
| `decision = kill_switched` | `echo $HERMES_KILL_SWITCH` | Unset after incident review. |
| `provider_resolved` not what you set | `env | grep HERMES_PROVIDER` | Restart process / shell. |
| Refusal you disagree with | `result.decision.matched_rules` | If the rule is wrong, open a separate PR amending the Charter — never bypass at the gate. |
| Live key in CI log | `tests/test_no_provider_key_in_repo.py` | Rotate now per `docs/ops/HERMES_SECRET_ROTATION.md`. |
| Daily brief shows `executor_error` | `var/hermes-runs.jsonl` last row | Reproduce locally with the printed `run_id`. |

## 10. Cron suggestion (Railway)

```cron
# 08:00 KSA = 05:00 UTC daily — produce today's brief
0 5 * * * cd /app && python scripts/hermes_daily.py --out data/founder_briefs/$(date -u +\%Y-\%m-\%d)_hermes.md
```

The brief writes to a gitignored path; the founder reads it manually.
No external send happens from cron.

---

— Hermes obeys the doctrine, ships the work, never improvises around the limits.
