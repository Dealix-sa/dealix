# AI Command Center — مركز قيادة الذكاء الاصطناعي

## Purpose
Single dashboard view of every AI system in production at Dealix: which agents are running, at what autonomy level, with what risk class, and which incidents are open.

## Owner
Founder. Backup: Head of Delivery.

## Inputs
- `docs/ai_management/AI_SYSTEM_INVENTORY.md`.
- `docs/ai_management/AI_RISK_REGISTER.md`.
- `docs/ai_management/AI_INCIDENT_RESPONSE.md` register.
- `docs/trust/APPROVAL_MATRIX.md` for current autonomy assignments.

## Outputs
- Daily AI posture snapshot.
- Weekly written summary into `docs/learning/WEEKLY_INTELLIGENCE_REVIEW.md`.

## Rules (numbered)
1. Every agent appears in the inventory before it runs against any client work.
2. Every agent has an owner, an autonomy level, a risk class, and a last-review date.
3. Autonomy promotions appear on the dashboard until they have been reviewed and ratified or rolled back.
4. Open AI incidents are listed with severity and owner.
5. No agent runs above its assigned autonomy level. Ever.
6. Forbidden actions from `docs/trust/AUTONOMY_POLICY.md` are unreachable to any agent regardless of class.

## Metrics
- Agents in inventory vs agents running (target equal).
- Open AI incidents by severity.
- Mean time since last review per agent.
- Autonomy promotions per quarter, ratification rate.

## Cadence
Daily glance. Weekly written summary. Monthly inventory completeness check.

## Evidence (paths)
- `docs/ai_management/AI_SYSTEM_INVENTORY.md`
- `docs/ai_management/AI_RISK_REGISTER.md`
- `docs/trust/registers/incident_log.md`

## Verifier
Founder.

## Runtime Command
`make ai.dashboard` prints the current AI posture with agent counts, levels, and incident summary.

## Dashboard sections

**Section A — Agent inventory.** Table of every agent in the inventory. Columns: agent ID, name, owner, autonomy level, risk class, last review date, last incident date.

**Section B — Open incidents.** AI-specific incidents. Columns: incident ID, severity, opened at, owner, status.

**Section C — Pending autonomy promotions.** Agents recently promoted, waiting for ratification. Columns: agent ID, from level, to level, requested by, requested at, ratifier, target ratify date.

**Section D — Risk register heat map.** High-likelihood, high-impact risks from `AI_RISK_REGISTER.md` flagged.

**Section E — Evaluation queue.** Agents due for offline evaluation per `AI_EVALUATION_POLICY.md`.

**Section F — Forbidden-action attempts.** Logged attempts by agents to take forbidden actions, blocked by guardrails. Pattern detection only; no agent should ever try.

## Operating substance
AI command exists because AI risk does not present as a single incident; it presents as drift. An agent at A1 today behaves slightly differently next month, and unless someone is watching the aggregate, the drift becomes the next incident. The dashboard is the watcher.

Every agent must be inventoried. There are no "small" agents that escape the inventory because they are convenient. If a script calls a model, it is an agent and it is in the inventory. The discipline is non-negotiable because the alternative is invisible AI surface area.

Autonomy promotions are the riskiest decisions in this system. They appear on the dashboard until ratified because the ratification step is the catch-net for promotions that were made for convenience rather than evidence. A promotion that cannot survive a written ratification should not have been made.

The dashboard mirrors state; it does not change state. Changes happen in the inventory, the risk register, and the incident log. This separation prevents the dashboard from becoming a fake source of truth.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
