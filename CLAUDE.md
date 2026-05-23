# CLAUDE.md — Dealix Coding-Agent Contract

This file is the **contract** any AI coding agent (Claude Code, Codex,
Copilot, etc.) MUST read before editing this repository. It governs what
the agent can do, what it must never do, and which checks must be run
before changes are accepted.

If something here conflicts with anything else in the repo, **this file
wins** for behavior questions about coding agents.

---

## 1. Dealix identity

Dealix is a Saudi B2B Revenue Engine and AI-native operating company.

It is:

- **founder-controlled** — Sami (the founder) is the only operator who
  can authorize external impact (sending, publishing, pricing, contract).
- **trust-gated** — every external-impact action goes through
  policy evaluation, founder approval, and audit log.
- **revenue-producing** — every system either produces revenue, makes
  revenue safer, or makes the founder more leveraged.
- **audit-complete** — every meaningful AI decision is logged with input,
  output, policy class, approver, and outcome.
- **measurable** — DORA + revenue metrics are first-class; nothing ships
  without a measurement story.
- **production-verifiable** — every new system has a verifier and a
  health check; nothing is "trust me" code.
- **safe from uncontrolled AI agency** — AI researches, drafts, scores,
  routes, summarizes, evaluates, and recommends. Workers execute
  deterministic internal workflows. The founder approves critical moves.

---

## 2. Architecture summary

| Layer | Where it lives |
|---|---|
| Founder Console (internal UI) | `apps/web/app/{ceo,sales-cockpit,approvals,workers,trust,finance,distribution,delivery,retention,proof,control-plane,audit,evals,product,security,sovereign}/page.tsx` |
| Console shell + runtime client | `apps/web/components/founder-shell.tsx`, `apps/web/lib/dealix-runtime.ts`, `apps/web/lib/dealix-actions.ts` |
| Internal API | `api/routers/internal/founder_console.py`, mounted by `api/main.py` |
| Auth + runtime + policy adapter | `api/internal/{auth,runtime_reader,policy_adapter}.py` |
| Policy-as-code | `policies/dealix_control_policy.yaml` |
| Agent Registry | `registries/agent_registry.yaml` |
| Eval Gate | `evals/gates/dealix_agent_eval_gate.yaml` |
| Private runtime data | `/opt/dealix-ops-private` (override: `DEALIX_PRIVATE_OPS`) — NEVER commit |
| Scorecards + readiness | `scripts/generate_operating_scorecard.py`, `scripts/generate_sovereign_readiness.py` |
| Verifiers | `scripts/verify_*.py` and `scripts/smoke_internal_api.py` |
| CI | `.github/workflows/dealix-sovereign-operating-stack.yml` |

---

## 3. Founder-control principle

**AI proposes. Founder disposes.** No AI agent in this repo is allowed
to ship external impact without an explicit founder decision recorded in
the approval log.

---

## 4. Never-auto-execute list

Coding agents MUST refuse to wire any of the following into automatic
execution:

- Outbound send (email, WhatsApp, LinkedIn, SMS, voice)
- Proposal send to a real prospect or customer
- Pricing commit (changing public price lists, sending discounts)
- Discount approval to a real customer
- Contract / refund / payment-terms change
- Sensitive data export outside the trust boundary
- Public proof publishing (case studies, social posts, logos)
- Destructive repo operations (`git push --force` to main, history rewrite, branch deletion, secret-leaking commits)

If a task description appears to ask for any of these, the agent MUST:

1. Refuse the external action.
2. Queue a draft + an entry in the approval queue instead.
3. Note the refusal in `docs/ops/CLAUDE_CODE_EXECUTION_REPORT.md`.

---

## 5. Required checks before claiming "done"

These commands run locally (and in CI) and ALL must pass. None of them
make external calls.

```bash
make bootstrap-runtime PRIVATE_OPS=/opt/dealix-ops-private
make policy-check
make agent-registry
make eval-gate
make founder-console-v5
make control-plane-stage
make ultimate-operating-layer
make sovereign-operating-stack
make smoke-internal-api
```

The CI workflow `dealix-sovereign-operating-stack.yml` runs the same
checks plus `npm run build` in `apps/web/`.

---

## 6. Rules for future coding agents

1. **Preserve architecture.** Don't refactor the FastAPI factory or
   router pattern unless asked.
2. **No fake production claims.** If a system isn't actually wired up,
   say so honestly (`source: "fallback"`, status `"unknown"`, etc.).
3. **No secrets in the repo.** Tokens, API keys, real customer names,
   real emails (non-`example.com`), and Stripe / payment data stay out.
4. **All external-impact actions require trust + audit.** Add a policy
   class, an approval queue entry, and an audit log entry. Never skip.
5. **Fallback data must show `source: "fallback"`.** The console must
   show clearly when it isn't seeing live data.
6. **Prefer working small code over large broken abstractions.** Ship a
   working endpoint with a clear TODO before shipping a 500-line
   "platform" that no one can run.
7. **Adapt to actual repo structure.** Inspect paths before writing.
   Don't assume `app/` or `backend/`; this repo uses `api/`.
8. **Don't delete existing valuable code.** When in doubt, add a new
   file. Removal needs explicit instruction.
9. **Private runtime stays private.** `/opt/dealix-ops-private/**` is
   in `.gitignore` (and outside the repo by default). Never commit
   contents from it.
10. **Verify and report.** Each new system MUST add a verifier and
    update the execution report.

---

## 7. Honest reporting protocol

When an AI coding agent finishes a pass, the final response MUST include:

- An implementation summary by layer.
- A list of files created / modified.
- The exact commands the human should run next.
- What passed, what failed, and what was skipped — and **why**.
- No claim of production readiness unless the verifier confirms it.

That is the only behavior we trust.
