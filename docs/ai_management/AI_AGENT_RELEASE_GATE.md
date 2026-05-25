# AI Agent Release Gate

> Before any new AI agent or material capability ships, this checklist
> must be green. Founder signs.

## When this gate applies

- A new agent is being added to `AI_SYSTEM_INVENTORY.md`.
- An existing agent moves from one autonomy tier to a higher one.
- An existing agent gains a new data class as input (e.g. starts handling
  customer PII).
- An existing agent changes model vendor or model family.

## Checklist

### Inventory & Mapping
- [ ] Added to `AI_SYSTEM_INVENTORY.md` with full schema fields filled.
- [ ] Owner named.
- [ ] Inputs and outputs defined.
- [ ] Data classes identified.
- [ ] Retention policy defined.

### Autonomy
- [ ] Autonomy tier explicitly set (default: lowest viable).
- [ ] Human-in-loop point named.
- [ ] If A2 or higher: founder has approved the pattern in writing.
- [ ] If A3: per-send approval mechanism is implemented and tested.

### Risk
- [ ] Added to `AI_RISK_REGISTER.md` with at least one risk per OWASP LLM
      category.
- [ ] Threat scenarios written in `AI_THREAT_MODEL.md`.
- [ ] Mitigations implemented (not just listed).

### Evaluation
- [ ] Evaluation suite exists under `evals/<agent_id>/`.
- [ ] Eval set covers: golden cases, adversarial cases, edge cases.
- [ ] Pass thresholds defined.
- [ ] Eval run output is green on current model + version.

### Trust
- [ ] Output reviewed against `NO_OVERCLAIM_POLICY.md`.
- [ ] Output cannot leak private data into a public surface.
- [ ] Prompt injection resilience tested (T1 from threat model).

### Operational
- [ ] Cost cap configured.
- [ ] Rate cap configured.
- [ ] Logging in place (inputs, outputs, model+version).
- [ ] Rollback path defined (how to disable in < 5 minutes).
- [ ] Monitoring alerts wired.

### Documentation
- [ ] Runbook entry written.
- [ ] User-facing capability descriptions match `SAFE_LANGUAGE_LIBRARY.md`.

## Founder Sign-Off

```
- agent_id: AI-NN
- release_gate_passed_on: yyyy-mm-dd
- founder_signature: Sami
- rollback_path: <link>
- next_review_date: yyyy-mm-dd
```

## Failure path

If any checklist item is red:

- Block release.
- Open an issue in `dealix-ops-private/founder/decision_queue.md`.
- Do not work around. Fix the underlying gap.

## Post-release Review

- 7 days after release: review logs and any escalations.
- 30 days after release: re-run evaluation suite, compare to baseline.
- 90 days after release: re-score risk register entry.
