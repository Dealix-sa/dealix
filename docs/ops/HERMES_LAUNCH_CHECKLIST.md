# Hermes Launch Checklist — Day 0 to Day 7

The single document the founder works through to take Hermes from PR
to live production. Each item has an owner, a verification command, and
a rollback path.

**Anchors:** [Charter](../institutional/HERMES_CHARTER.md) ·
[Ops Guide](HERMES_OPS_GUIDE.md) · [Rotation Playbook](HERMES_SECRET_ROTATION.md).

---

## Pre-flight (Day 0 — before merge)

| # | Item | Owner | Verify | Rollback |
|---|---|---|---|---|
| 0.1 | All 39 Hermes tests + 1 provider-key guard pass on PR #523 | CI | `pytest tests/hermes/ tests/test_no_provider_key_in_repo.py` | revert PR |
| 0.2 | `code-review` skill run on the PR diff with no high-confidence bugs | founder | `/code-review high` | address findings |
| 0.3 | Rotated provider keys ready (DeepSeek + OpenRouter); old keys revoked | founder | provider dashboards | revoke + reissue |
| 0.4 | Production `ADMIN_API_KEY` available and not the same as staging | founder | check Railway secrets | rotate |
| 0.5 | Repo "Workflow permissions" set to Read-and-write (one-time setting; unrelated to Hermes but unblocks Gitleaks/Codecov) | founder | GitHub repo settings → Actions | revert in UI |
| 0.6 | PR moved from draft → ready for review | founder | GitHub UI | mark draft again |

## Day 1 — merge + secrets

| # | Item | Verify |
|---|---|---|
| 1.1 | Merge PR #523 to `main` (squash recommended). | `git log main -1 --oneline` shows the merge commit |
| 1.2 | Set the following Railway env vars on the **API service**: <br>• `HERMES_PROVIDER=openrouter` <br>• `HERMES_FALLBACK_PROVIDER=openrouter` <br>• `OPENROUTER_API_KEY=…` <br>• `DEEPSEEK_API_KEY=…` (the rotated one, optional) <br>• `HERMES_DAILY_BUDGET_USD=10` (start conservative) <br>• `HERMES_KILL_SWITCH=0` <br>• `HERMES_LIVE_LLM=0` (turn live on Day 2 after preflight) | Railway → Variables tab |
| 1.3 | Trigger a no-op redeploy so the new envs load. | Railway → Deployments |
| 1.4 | `curl -H "X-Admin-API-Key: $ADMIN_API_KEY" $PROD/api/v1/hermes/status \| jq` | Returns `agent_id: hermes`, `provider: openrouter`, `kill_switch: false`. |

## Day 2 — preflight live LLM + first dispatch

| # | Item | Verify |
|---|---|---|
| 2.1 | Run preflight against staging: `python scripts/hermes_preflight.py --env staging` | All 4 checks pass. |
| 2.2 | Flip `HERMES_LIVE_LLM=1` in production. | `GET /status` does not show the kill switch active. |
| 2.3 | First live dispatch via HTTP: <br>`curl -X POST $PROD/api/v1/hermes/dispatch -H "X-Admin-API-Key: …" -H "Content-Type: application/json" -d '{"intent":"status check"}'` | `governance_decision.decision: approved`, output contains `content`. |
| 2.4 | Confirm audit row was written: `tail -n 1 var/hermes-runs.jsonl` (or check the Railway volume mount path). | Has the run_id from step 2.3. |
| 2.5 | Confirm cost accounting: `GET /api/v1/hermes/metrics?window_days=1`. | `total_runs >= 1`, `by_decision.approved >= 1`. |

## Day 3 — daily loop + cron

| # | Item | Verify |
|---|---|---|
| 3.1 | Run the daily brief locally with a real key: `python scripts/hermes_daily.py --out data/founder_briefs/$(date -u +%Y-%m-%d)_hermes.md` | Markdown brief is written; three dispatches all `approved`. |
| 3.2 | Schedule the cron on Railway (or local launchd / systemd). Suggested entry: <br>`0 5 * * * cd /app && python scripts/hermes_daily.py --out data/founder_briefs/$(date -u +\%Y-\%m-\%d)_hermes.md` | Cron log shows successful daily execution at 08:00 KSA. |
| 3.3 | Confirm the brief reaches the founder (manual copy from cron output or read from `data/founder_briefs/`). | Founder confirms receipt. |

## Day 4 — approval queue + capital ledger

| # | Item | Verify |
|---|---|---|
| 4.1 | Dispatch an external-send intent: <br>`curl -X POST $PROD/api/v1/hermes/dispatch -H "…" -d '{"intent":"send email to confirmed lead with proposal","customer_id":"cust_pilot_001"}'` | Returns `needs_approval`; response includes `approval_id`. |
| 4.2 | List pending approvals: `curl -H "…" $PROD/api/v1/approvals/pending \| jq '.cards[]'` | New card with `object_type: hermes_run`. |
| 4.3 | Approve via UI / API, watch the friction_log for the resolution event. | Approval moves to `approved`. |
| 4.4 | Run a delivery dispatch for a real customer: <br>`-d '{"intent":"build a scoring rule for the warm-list", "customer_id":"cust_pilot_001"}'` | Output contains `capital_asset_id` from `bridge_to_capital_ledger`. |

## Day 5 — observability + alerting

| # | Item | Verify |
|---|---|---|
| 5.1 | Founder cockpit panel reachable: `GET /api/v1/founder/dashboard` | Response contains `hermes_last_7d` with non-zero `total_runs`. |
| 5.2 | Cost budget alert dry-run: temporarily set `HERMES_DAILY_BUDGET_USD=0.001`, dispatch once, confirm refusal with `kind: cost_budget_exceeded`. | Confirmed. Restore budget to the real value (e.g. 10). |
| 5.3 | Kill-switch drill: set `HERMES_KILL_SWITCH=1`, dispatch once, confirm refusal with `kind: refusal` + `decision: kill_switched`. Restore. | Confirmed. |

## Day 6-7 — soak

| # | Item | Verify |
|---|---|---|
| 6.1 | Daily brief runs 2 days in a row without failure. | Cron log + brief files. |
| 6.2 | Audit ledger size growing. | `wc -l var/hermes-runs.jsonl` |
| 6.3 | No `decision: kill_switched` runs (unless intentional). | `GET /metrics?window_days=2` shows none. |
| 6.4 | No `decision: rejected` runs that surprise the founder. | If any, review the matched_rules and decide if a Charter amendment is needed (separate PR). |

## Rollback plan

| Trigger | Action | Side effects |
|---|---|---|
| Refusal rate > 30% over 24h | Investigate intents (audit ledger). Likely a copy paste issue, not Hermes. | None. |
| Cost overrun before budget catches it | Set `HERMES_KILL_SWITCH=1`; investigate offending run_ids. | All dispatch halts cleanly. |
| Live LLM provider down | Flip `HERMES_PROVIDER` between `openrouter` and `direct_deepseek`. | Latency may rise, but operations continue. |
| Doctrine violation suspected | Set `HERMES_KILL_SWITCH=1`. Open incident; never bypass the gate. | All dispatch halts. |
| Critical bug in orchestrator | Revert the Hermes integration in `api/main.py` (single line). | HTTP surface offline; CLI + daily script still work. |
| Catastrophic | Revert PR #523. | Hermes gone; old behavior restored. |

## After Day 7 — promote

If days 1-7 are clean:
- Raise `HERMES_DAILY_BUDGET_USD` to a comfortable production cap (e.g. 50).
- Wire `dealix_founder_daily_brief.py` to consume `/api/v1/hermes/metrics` instead of static counts.
- Open the next PR adding cost-tracker integration (deferred from the launch PR to keep blast radius small).

---

— No external send happens without approval. No live charge happens without approval. No bypass.
