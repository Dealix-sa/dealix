# Ultimate Architecture Map

> The flows that move data, decisions, AI calls, and code through Dealix.
> Every request, lead, agent call, and deploy travels through one of these four flows. If your change does not fit one of them, the change is in the wrong layer.

---

## 1. Request Flow (how a human action becomes a system effect)

```
Founder Console
   │
   ▼
Internal API  ─────────────►  Auth Gate  ──┐
                                            │
                                            ▼
                                       Trust Gate  ──┐
                                                     │
                                                     ▼
                                           Runtime Service  ──┐
                                                              │
                                                              ▼
                                                       Data Source  ──┐
                                                                      │
                                                                      ▼
                                                                 Audit Log
                                                                      │
                                                                      ▼
                                                                 Worker Queue
                                                                      │
                                                                      ▼
                                                     External Action only if allowed
```

### Stage contracts

| Stage             | Owner              | Responsibility                                                                         |
|-------------------|--------------------|----------------------------------------------------------------------------------------|
| Founder Console   | Frontend           | Render state, present decisions, never decide on behalf of the founder.                |
| Internal API      | Backend (`api/`)   | Validate input, attach actor, route to the runtime service.                            |
| Auth Gate         | `api/security`     | Enforce founder-only access; reject anonymous / unauthenticated calls.                 |
| Trust Gate        | `dealix/trust`     | Evaluate policy: class, suppression, reversibility, evidence. Block if not allowed.    |
| Runtime Service   | `dealix/*`         | Perform the actual business logic (score a lead, render a proposal, mark a payment).   |
| Data Source       | `db/` / private ops| Persist state in Postgres / CSV / event log.                                           |
| Audit Log         | `audit_events`     | Append immutable record: actor, action, payload digest, decision, timestamp.           |
| Worker Queue      | `dealix/runtime`   | Hand the work to a background worker for async execution.                              |
| External Action   | `integrations/`    | The only place that touches the outside world (email, WhatsApp, Stripe, etc.).         |

### Invariants

1. **Trust before runtime.** No runtime service is called before the trust gate returns `ALLOWED`.
2. **Audit before external.** No external action is dispatched before the audit record is written.
3. **One actor.** Every step records the same `actor_id` (founder, worker, agent).
4. **One trace ID.** Every step shares a `trace_id` for end-to-end debugging.

---

## 2. Data Flow (how a lead becomes cash)

```
Lead Sources
   │
   ▼
Market Accounts
   │
   ▼
Lead Intelligence
   │
   ▼
Outreach Queue
   │
   ▼
Approval Queue
   │
   ▼
Send Queue
   │
   ▼
Conversation Log
   │
   ▼
Sample Queue
   │
   ▼
Proposal Queue
   │
   ▼
Payment Capture
   │
   ▼
Delivery Queue
   │
   ▼
Retention Queue
   │
   ▼
Proof Library
```

### Stage contracts

| Stage              | Source                        | Owner             | Exit criterion                                                  |
|--------------------|-------------------------------|-------------------|-----------------------------------------------------------------|
| Lead Sources       | Public registries, partners   | Lead Intelligence | Raw record stored with provenance.                              |
| Market Accounts    | Filtered + deduped sources    | Lead Intelligence | Account passes sector + ICP filter.                             |
| Lead Intelligence  | Enrichment workers            | Lead Intelligence | Account has firmographics, signals, contacts.                   |
| Outreach Queue     | Scoring + drafting workers    | Revenue Factory   | Draft outreach is attached and scored.                          |
| Approval Queue     | Trust evaluator               | Founder           | Founder approves / rejects / edits.                             |
| Send Queue         | Send worker                   | Revenue Factory   | Send attempt is recorded (success or failure).                  |
| Conversation Log   | Reply ingestion               | Revenue Factory   | Reply is classified (positive / neutral / negative / OOO).      |
| Sample Queue       | Sample factory                | Revenue Factory   | Sample is generated, QA'd, delivered to founder for approval.   |
| Proposal Queue     | Proposal factory              | Revenue Factory   | Proposal sent and tracked.                                      |
| Payment Capture    | Payment follow-up worker      | Finance           | Payment received / payment plan agreed / proposal closed lost.  |
| Delivery Queue     | Delivery intake               | Delivery          | Workspace created, plan written, QA scheduled.                  |
| Retention Queue    | Health-score worker           | Delivery          | Renewal / referral / retainer decision is queued for founder.   |
| Proof Library      | Proof approval worker         | Marketing         | Approved proof is published as a sales / content asset.         |

### Invariants

1. **No skipping stages.** A record cannot enter `Proposal Queue` without a `Conversation Log` entry.
2. **Forward-only.** Records move forward through the funnel; rejections / closed-lost are recorded, not deleted.
3. **One record, one ID.** A lead keeps the same primary key from `Market Accounts` to `Proof Library`.
4. **Every stage emits an event** to the event log (see `docs/data/ULTIMATE_DATA_PLATFORM.md` §3).

---

## 3. AI Flow (how a model call becomes a safe action)

```
Prompt
   │
   ▼
Tool Scope
   │
   ▼
Context Policy
   │
   ▼
Model Call
   │
   ▼
Output Contract
   │
   ▼
Eval Check
   │
   ▼
Approval Class
   │
   ▼
Audit
   │
   ▼
Human Approval if needed
   │
   ▼
Action
```

### Stage contracts

| Stage                | Owner             | Responsibility                                                                            |
|----------------------|-------------------|-------------------------------------------------------------------------------------------|
| Prompt               | Caller            | Built from a versioned template in `dealix/prompts/` (no inline strings in workers).      |
| Tool Scope           | `dealix/governance` | Declare which tools the model may call (none, by default).                              |
| Context Policy       | `dealix/governance` | Strip PII, mask secrets, redact suppression-list entries.                                |
| Model Call           | `dealix/intelligence` | Call the model with the declared scope; record token + cost.                          |
| Output Contract      | Caller            | Validate output against a schema before any downstream use.                               |
| Eval Check           | `evals/`          | Run prompt-injection, refusal, overclaim, and regression checks.                          |
| Approval Class       | `dealix/trust`    | Map output to A0/A1/A2/A3 based on the action it would trigger.                           |
| Audit                | `audit_events`    | Record prompt hash, output hash, eval results, approval class.                            |
| Human Approval       | Founder           | Required for A2/A3 actions before they leave the building.                                |
| Action               | `integrations/`   | The actual side effect.                                                                   |

### Invariants

1. **No untrusted tool use.** A model never calls a tool it has not been explicitly granted in `Tool Scope`.
2. **No raw output → action.** Every model output passes the `Output Contract` and `Eval Check` before any downstream use.
3. **Prompt injection is a known risk.** Every prompt template has at least one prompt-injection regression test (`evals/`).
4. **AI cost is tracked.** Every model call writes a row to `finance_events` with provider, model, tokens, cost.

This flow implements the principles in the NIST AI Risk Management Framework: govern, map, measure, manage. See `docs/trust/ULTIMATE_TRUST_PLANE.md` §6 for the policy details.

---

## 4. Production Flow (how a code change becomes a safe deploy)

```
PR
 │
 ▼
CI
 │
 ▼
Security Scan
 │
 ▼
Eval Gate
 │
 ▼
Frontend Build
 │
 ▼
Backend Tests
 │
 ▼
Migration Check
 │
 ▼
Deploy
 │
 ▼
Smoke Test
 │
 ▼
Observability
 │
 ▼
Rollback Ready
```

### Stage contracts

| Stage              | Tool                                  | Pass criterion                                                          |
|--------------------|---------------------------------------|-------------------------------------------------------------------------|
| PR                 | GitHub                                | Title, description, linked issue, ≥1 reviewer.                          |
| CI                 | `.github/workflows/ci.yml`            | Lint, type-check, unit tests green.                                     |
| Security Scan      | `.github/workflows/codeql.yml`        | No high/critical findings. Secrets not present (gitleaks).              |
| Eval Gate          | `.github/workflows/dealix-ultimate-level.yml` | Ultimate blueprint intact; AI evals (where present) pass.       |
| Frontend Build     | `frontend/` build                     | `npm run build` succeeds.                                               |
| Backend Tests      | `pytest`                              | All unit + integration tests green.                                     |
| Migration Check    | Alembic                               | New migrations apply cleanly to a fresh DB and to a copy of prod.       |
| Deploy             | Railway / Docker                      | Deployment succeeds; `/healthz` returns 200 within 60s.                 |
| Smoke Test         | `scripts/v5-verify`                   | 22-point production verifier passes against the new deploy.             |
| Observability      | Worker Health page + logs             | No new error spike in the first 15 minutes.                             |
| Rollback Ready     | Previous container retained           | A `make rollback` (or equivalent) restores the previous version.        |

### Invariants

1. **No merge without required checks.** `main` is protected and required status checks are configured (see `docs/security/ULTIMATE_SECURITY_GOVERNANCE.md`).
2. **No deploy without smoke test.** A green deploy that fails smoke is treated as a failed deploy.
3. **No undocumented migration.** Every migration has a description and a tested down-path.
4. **DORA tracked.** Change lead time, deployment frequency, change-fail rate, recovery time, rework rate are recorded for every deploy (`docs/engineering/ULTIMATE_OBSERVABILITY_DORA.md`).

---

## 5. How the four flows relate

- **Request Flow** is the **runtime** dimension (a human action).
- **Data Flow** is the **business** dimension (a lead becoming cash).
- **AI Flow** is the **intelligence** dimension (a model output becoming a safe action).
- **Production Flow** is the **engineering** dimension (a commit becoming a safe deploy).

A healthy company has all four flows working at once. The Ultimate Architecture Map exists so that any new component can declare which flow(s) it belongs to and what stage it implements.

---

## 6. Quick reference for contributors

When you add a new module, answer these four questions before writing code:

1. Which **Request Flow** stage does it implement (or which stage does it call)?
2. Which **Data Flow** stage does it advance?
3. Does it touch an AI model? If yes, walk the **AI Flow** stages.
4. What's the **Production Flow** gate it adds or relies on?

If you cannot answer all four, you are not yet ready to write the code.
