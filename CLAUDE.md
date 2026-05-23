# CLAUDE.md — Dealix Ultimate Operating Layer

This file gives future Claude Code sessions the durable rules and the
minimum context needed to operate inside the Dealix repo without
breaking the founder-control / trust-gated model.

> Identity. Dealix is a Saudi B2B Revenue Engine and AI-native operating
> company. It must be founder-controlled, trust-gated, revenue-producing,
> auditable, and production-verifiable.

## Core business flow

market accounts → lead intelligence → scoring → outreach drafts →
approval → send/draft queue → follow-up → replies → samples → proposals
→ payment capture → delivery → retention → proof → referrals → inbound
demand → productization.

## Core operating principle

AI **prepares, researches, drafts, scores, routes, explains, and
recommends**. Workers execute deterministic internal workflows. The
**founder approves** critical moves. Trust gates external impact. Audit
records every meaningful decision.

## Never-auto-execute list (hard rules)

The following actions are **never** performed automatically by any agent
or worker, no matter how high the confidence:

- outbound send (email, WhatsApp, LinkedIn, SMS) to any real recipient
- proposal send
- pricing commit / discount / refund / contract change
- public proof publication
- sensitive data export (full lead/customer lists, PII)
- contract / refund / payment terms changes
- destructive repo operations (force push to main, history rewrite,
  branch delete of shared branches)
- modifying secrets, tokens, or production credentials

Every external-impact action requires:

1. Policy evaluation (`policies/dealix_control_policy.yaml`).
2. Founder approval (via `/approvals` in the Founder Console).
3. Audit record (`trust/approval_decisions.csv`).

## Required local checks

```
make policy-check
make agent-registry
make eval-gate
make ultimate-operating-layer
```

## Required production gates

- `DEALIX_INTERNAL_TOKEN` is set in the runtime environment.
- `DEALIX_PRIVATE_OPS` points to a writable, **non-repo** path (default
  `/opt/dealix-ops-private`).
- Frontend `apps/web` builds.
- Master verifier passes.
- GitHub workflow `dealix-ultimate-operating-layer.yml` is green.
- Branch protection requires the workflow above.

## How to run

```
make bootstrap-runtime PRIVATE_OPS=/opt/dealix-ops-private
make policy-check
make agent-registry
make eval-gate
make founder-console-v5
make control-plane-stage
make ultimate-operating-layer
make smoke-internal-api
```

## Rules for future Claude Code sessions

1. **Preserve architecture.** The repo already has 300+ routers and
   400+ docs — adapt, do not replace.
2. **No fake production-ready claims.** If a verifier did not actually
   run, do not say "PASS". Honest "skipped" beats false "PASS".
3. **No secrets in code, docs, or commits.** Use env vars and the
   `.env.example` pattern.
4. **All external-impact actions require trust + audit.** If you add a
   new agent or endpoint that touches the outside world, it MUST go
   through policy evaluation and write to the audit log.
5. **Fallback data must show `source: "fallback"`.** Never claim live
   data when serving a safe default.
6. **Prefer working small code over large broken abstractions.** It is
   better to ship a 30-line script that runs than a 500-line framework
   that does not import.
7. **Never commit private operational data.** CSVs under
   `$DEALIX_PRIVATE_OPS` are runtime state and must stay outside the
   public repo.
8. **Adapt to actual paths.** If a file already exists, update it
   instead of creating a conflicting duplicate.
9. **Be honest in final responses.** List completed, failed, skipped,
   and manual steps separately.

## Reference

- Founder Console: `apps/web/app/<page>/page.tsx`
- Internal API:    `api/routers/internal/founder_console.py`
- Runtime reader:  `api/internal/runtime_reader.py`
- Auth gate:       `api/internal/auth.py`
- Policy:          `policies/dealix_control_policy.yaml`
- Agents:          `registries/agent_registry.yaml`
- Eval gate:       `evals/gates/dealix_agent_eval_gate.yaml`
- Master verifier: `scripts/verify_ultimate_operating_layer.py`
- Smoke test:      `scripts/smoke_internal_api.py`
