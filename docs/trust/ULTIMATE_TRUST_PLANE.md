# Ultimate Trust Plane

> Every AI call, worker action, frontend interaction, and external-impact decision passes through this plane.
> The plane is implemented by `dealix/trust/` and called by every internal API endpoint defined in `docs/api/ULTIMATE_INTERNAL_API.md`.

---

## 1. Purpose

Make every AI, worker, frontend, and external-impact action **safe, auditable, and controllable**.

The trust plane is not a feature. It is the company's permission layer. If it is bypassed, the company has no permission system — only a deploy.

---

## 2. Where the plane runs

| Trigger                                                                  | Trust plane is called by                                  |
|---------------------------------------------------------------------------|-----------------------------------------------------------|
| Founder clicks "Approve" in the Approval Center.                          | `POST /api/v1/internal/approvals/{id}/approve`            |
| Worker prepares an outreach draft and asks for approval.                  | `dealix/runtime/outreach.py` → `trust.evaluate(...)`      |
| Worker is about to call an external service (email, WhatsApp, payment).   | `integrations/<provider>/client.py` (last gate before send) |
| Agent wants to call a tool.                                               | `dealix/intelligence/tools.py` → `trust.allow_tool(...)`  |
| Founder publishes a proof asset.                                          | `POST /api/v1/internal/proof/{id}/publish` (Phase 2)      |

If a path that produces external impact is not in this table, the path is **not yet** allowed to run.

---

## 3. Policy checks (every action runs every check that applies)

Each check returns `pass`, `fail`, or `needs_approval`. The action's overall decision is the **strictest** of all check results.

| Check                  | What it asks                                                                  |
|------------------------|-------------------------------------------------------------------------------|
| `approval_class`       | Is the action A0, A1, A2, or A3? (See §4.)                                    |
| `reversibility`        | Can the action be undone without external impact within 1 hour?               |
| `sensitivity`          | Does the action touch PII, financials, contracts, or legal text?              |
| `external_impact`      | Does the action send something to a non-Dealix entity?                        |
| `financial_impact`     | Does the action commit Dealix to a payment or pricing decision?               |
| `legal_impact`         | Does the action create a legal obligation (NDA, MSA, SOW)?                    |
| `suppression`          | Is the subject on the suppression list?                                       |
| `evidence`             | Is the evidence pack present and valid?                                       |
| `no_overclaim`         | Does the message claim a capability, certification, or KPI we cannot prove?   |
| `prompt_injection_risk`| Did the upstream model output trigger our prompt-injection regression set?    |
| `tool_permission`      | Is the tool the agent wants to call in its declared scope?                    |
| `data_boundary`        | Does the data leave the KSA region or cross a tenant boundary?                |
| `customer_proof_approval` | If publishing a customer asset, is the customer's written approval on file? |

Each check is a small, testable function in `dealix/trust/checks/`. New checks may be added; **none** may be removed.

---

## 4. Approval classes

Every action is assigned exactly one class **before** it is dispatched. The class is computed from the policy checks above.

| Class | Definition                                              | Example                                            | Default routing            |
|-------|---------------------------------------------------------|----------------------------------------------------|----------------------------|
| **A0** | Fully internal, safe, reversible.                       | Re-render a draft, compute a score, update a metric.| Auto-approved.            |
| **A1** | Internal draft or low-risk preparation.                 | Generate an outreach draft (not yet sent).         | Auto-approved + logged.   |
| **A2** | External impact, reversible only with effort.           | Send outreach, deliver sample, send proposal.      | **Founder approval required.** |
| **A3** | High-risk: financial / legal / contract / public claim. | Sign MSA, change pricing, publish case study.      | **Never automatic. Founder approval + evidence pack.** |

Rules:
- A3 may never be executed without **both** an approval record and an evidence pack.
- A2 may not be downgraded to A1 by any worker. Reclassification requires a founder action recorded in `audit_events`.
- A0 actions still write to `audit_events` for traceability (lightweight schema).

---

## 5. Required artifacts (per action)

Every action that passes the trust plane produces these artifacts:

1. **Policy result** — JSON: list of checks, results, overall decision, class.
2. **Evidence pack** — JSON: the inputs the action relied on (draft id, payload digest, model id, prompt hash, eval pass record).
3. **Audit record** — Row in `audit_events`.
4. **Actor** — The human / worker / agent that initiated the action.
5. **Timestamp** — `occurred_at` in UTC.
6. **Decision** — `ALLOWED`, `ALLOWED_WITH_APPROVAL`, or `DENIED`.
7. **Rollback path** — A documented procedure to undo the action (per action type, stored in `docs/trust/rollback/`).

Missing any of the seven → the action **does not run**.

---

## 6. Connection to NIST AI RMF

The trust plane operationalizes the four NIST AI RMF functions:

| NIST function | How the trust plane implements it                                                                 |
|---------------|---------------------------------------------------------------------------------------------------|
| **Govern**    | Approval classes A0–A3, founder-only authority on A3, suppression policy, written rollback paths. |
| **Map**       | Every action declares actor, subject, evidence, tools — recorded in the policy result.            |
| **Measure**   | `ai_eval_results`, `audit_events`, and trust-metric dashboards (`/trust`, `/evals`).              |
| **Manage**    | Incident response procedure (§9), feature-flag disable per worker/tool, suppression-list edits.   |

---

## 7. Connection to OWASP LLM Top 10

Prompt injection (LLM01) is treated as a **first-class** risk. Every prompt template in `dealix/prompts/` has at least one regression test in `evals/`. The trust plane refuses any action whose upstream model output triggered the regression set within the last `N=10` runs without a reset.

Other relevant LLM risks (sensitive information disclosure, insecure output handling, excessive agency) are enforced by:
- `data_boundary` and `sensitivity` checks (disclosure),
- `tool_permission` check (excessive agency),
- output schemas in the runtime services (insecure output handling).

---

## 8. Approval routing rules

- A0 → no routing. Worker proceeds.
- A1 → no routing. Worker proceeds; entry visible in `/audit`.
- A2 → routed to **Approval Center** (`/approvals`). The founder approves, rejects, requests edit, or escalates.
- A3 → routed to **Approval Center with `class=A3` tag**. Always requires the founder. Always requires the evidence pack to be opened and reviewed (UI enforces a 5-second minimum on the evidence view before the Approve button enables).

The founder may **always** demote an A0/A1/A2 action to require approval. The founder may **never** promote an A3 to auto-approve.

---

## 9. Incident response procedure

Triggered by any of:
- Sev1: external action sent that should have been blocked.
- Sev1: data crossed a tenant or region boundary.
- Sev2: eval pass rate drops below 95% for any suite.
- Sev2: suppression-list violation attempted.
- Sev3: A3 attempted without an evidence pack.

For every incident:
1. **Contain** — disable the relevant worker / tool via the disable switch (no deploy).
2. **Triage** — capture the trace_id and the audit chain.
3. **Notify** — founder, plus customer if the incident touched their data.
4. **Correct** — fix the immediate cause; ship a regression test.
5. **Postmortem** — written within 7 days; linked from `/trust` → Incidents.

Postmortems are stored under `docs/trust/postmortems/YYYY-MM-DD-<slug>.md`.

---

## 10. Suppression list

- File: `dealix/trust/suppression.yaml` (Phase 1) → `suppression` table (Phase 2).
- Sources: customer request, manual flag, regulator request, internal review.
- Granularity: by domain, by email, by phone, by account handle, by company.
- Enforcement: every outbound action consults the list **at send time**, not at draft time. A draft is allowed; a send is not.
- Auditability: every suppression change writes to `audit_events` with the actor and reason.

---

## 11. AI eval gates (link to `/evals`)

| Suite                | What it tests                                                | Required pass rate |
|----------------------|--------------------------------------------------------------|--------------------|
| `prompt_injection`   | Adversarial inputs designed to override the prompt.          | 100%               |
| `refusal`            | Out-of-scope or harmful requests are refused.                | 100%               |
| `no_overclaim`       | Outputs do not claim capabilities / KPIs we cannot prove.    | 100%               |
| `regression`         | Curated set of canonical inputs produces canonical outputs.  | ≥ 98%              |
| `red_team`           | Quarterly adversarial run.                                   | Reviewed.          |

A failed prompt-injection or refusal test on the latest run **blocks** any A2/A3 action that uses the affected prompt template until a green run is recorded.

---

## 12. Rule

> **No trust record, no action.**

If you cannot point to a `policy_result`, an `evidence` pack, and an `audit_events` row for an action — that action is forbidden, regardless of who initiated it.
