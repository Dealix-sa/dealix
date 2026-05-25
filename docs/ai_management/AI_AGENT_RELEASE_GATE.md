# AI Agent Release Gate — بوابة إطلاق الوكلاء

## Purpose
Define the gates an agent must pass before it can run at A1 (against any client artifact) or A2 (autonomous on client-facing surface under review). The gate is how Dealix prevents quietly-promoted agents.

## Owner
Founder.

## Inputs
- Agent proposal.
- Prompt asset and prompt version.
- Offline evaluation results.
- Sandbox run results.

## Outputs
- Release decision (approved / blocked).
- Inventory row added.
- Sandbox-to-production transition log.

## Rules (numbered)
1. No agent reaches A1 without passing the documentation, eval, and sandbox gates.
2. No agent reaches A2 without passing the additional review-queue and rollback gates.
3. Gate decisions are written and signed by the founder.
4. Failed gates produce a documented gap; the agent stays in sandbox.
5. Promotion to a higher class requires re-running the relevant gates.
6. Rollback path is mandatory; an agent with no rollback path cannot reach A1.

## Metrics
- Agents passing all gates on first attempt.
- Mean time from proposal to A1.
- Promotion ratification rate (A1 to A2).

## Cadence
Per agent. Reviewed quarterly across all active agents.

## Evidence (paths)
- `docs/ai_management/release_logs/AG-<id>.md`
- `docs/ai_management/AI_SYSTEM_INVENTORY.md`

## Verifier
Founder.

## Runtime Command
`make ai.release.gate AGENT=<id>` opens the gate checklist for the proposed agent.

## Gates to reach A1

**G1 Documentation.** Agent has: a purpose statement, an owner, a prompt at a versioned path, a list of tools it can call, a stated risk class, a stated autonomy ceiling, and an inventory row prepared.

**G2 Offline evaluation.** A set of representative inputs has been run through the agent and the outputs have been reviewed by a human. Evaluation criteria are documented in `AI_EVALUATION_POLICY.md`. Pass threshold is documented per agent.

**G3 Sandbox run.** Agent has run for at least 5 sprint-equivalent workloads in a sandbox folder. Outputs reviewed. Defects fixed. No A1-level promotion until sandbox is clean.

**G4 Rollback path.** A documented sequence of steps to remove the agent from production within 1 hour of an incident. Includes who is paged, what tool calls are disabled, how human-only fallback works.

**G5 Inventory row.** Row added to `AI_SYSTEM_INVENTORY.md` with all required fields.

## Additional gates to reach A2

**G6 Review queue.** A2 outputs land in a review queue, not directly in client artifacts. Queue has a named reviewer and an SLA.

**G7 Risk register update.** The risk register has been updated with any new risks introduced by A2 promotion. Mitigations are in place.

**G8 Dashboard appearance.** Promotion appears on the AI Command Center dashboard for ratification. Ratification window is 14 days; unratified promotions auto-rollback to A1.

**G9 Founder sign-off.** Written, dated, signed.

## Gates to reach A3

A3 is per-action, not a permanent autonomy class for an agent. The Approval Matrix governs A3 routing. An agent does not "reach" A3; an action is escalated to A3 every time it is invoked.

## Operating substance
The gate exists because the cost of a bad agent in production is asymmetric. A good agent saves operator time; a bad agent leaks client data, generates overclaim, or takes an action no one approved. The gate is the asymmetry-correction.

Sandbox runs are the most useful gate. Five sprint-equivalent workloads in sandbox catch most of the failure modes that documentation alone misses. The cost of running in sandbox is small; the cost of skipping it is incident exposure.

Rollback paths are mandatory because every agent will eventually misbehave. The question is not whether but when, and how fast we can take it out of production. A documented rollback path is the difference between a 1-hour incident and a 1-day incident.

Promotion to A2 is the highest-friction step on purpose. Most agents stay at A1 forever. A2 is reserved for agents that have demonstrated stability across many sprints and where the operator-time savings justify the additional risk and review overhead.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
