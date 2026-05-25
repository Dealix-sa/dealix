# Autonomy Policy — سياسة الاستقلالية

## Purpose
Define the boundary of agent autonomy: what agents may do alone, what requires human review, and what is forbidden under any condition.

## Owner
Founder.

## Inputs
- Agent inventory from `docs/ai_management/AI_SYSTEM_INVENTORY.md`.
- Approval Matrix `docs/trust/APPROVAL_MATRIX.md`.
- Threat model `docs/ai_management/AI_THREAT_MODEL.md`.

## Outputs
- Per-agent autonomy level recorded in the inventory.
- Forbidden-action list maintained here.

## Rules (numbered)
1. No agent operates above its assigned autonomy level. Ever.
2. Default for any new agent is A1. Promotion follows `docs/ai_management/AI_AGENT_RELEASE_GATE.md`.
3. No agent sends external messages on a client's behalf without A3 approval per request.
4. No agent publishes to Dealix's public channels without A3 approval.
5. No agent claims outcomes, revenue, or conversion rates in any artifact it produces.
6. No agent stores PII it was not explicitly authorized to receive.
7. No agent calls a tool that performs irreversible action (delete, send, pay) without a human in the loop.
8. Forbidden actions cannot be unlocked by autonomy promotion. They are out of scope for any agent.

## Metrics
- Agents operating at assigned level (target 100%).
- Autonomy violations per quarter (target 0).
- Forbidden-action attempts blocked.

## Cadence
Policy reviewed quarterly. Per-agent level reviewed monthly.

## Evidence (paths)
- `docs/ai_management/AI_SYSTEM_INVENTORY.md`
- `docs/trust/registers/autonomy_violations.md`

## Verifier
Founder.

## Runtime Command
`make trust.autonomy.audit` produces a per-agent level table and recent violations.

## What agents can do alone (A0–A1)

- Read public sources.
- Draft markdown files for internal review.
- Validate CSVs against published schemas.
- Score rows using published rubrics.
- Search internal docs and surface relevant paths.
- Summarize sprint folders for the operator.

## What requires human review (A2)

- Sending a draft to a client (any client-facing artifact).
- Publishing to docs/ areas that the public-private boundary classifies as public.
- Calling third-party APIs that have a cost or rate limit per call.
- Updating templates or schemas that downstream sprints depend on.
- Producing a case-study draft.

## What requires explicit human approval (A3)

- Sending any external message on behalf of a client or Dealix.
- Posting to public social channels.
- Publishing a named case study.
- Modifying the approval matrix, no-overclaim policy, or autonomy policy.
- Promoting an agent's autonomy level.
- Storing or processing any PII outside the agreed minimal set.

## Forbidden under any condition

- Cold scraping of gated social platforms.
- Bulk WhatsApp automation.
- LinkedIn automation that simulates a human.
- Buying or using unverifiable lead lists.
- Generating fake testimonials, case studies, or reviews.
- Claiming outcomes that are not evidenced.
- Storing national IDs.
- Operating on a sprint that has not closed G1.

## Operating substance
Autonomy is not a perk we extend to capable agents. It is a risk concession we make grudgingly, reviewed often, and reversible at any time. An agent that has been at A2 for six months is still subject to roll-back if its outputs drift.

The forbidden list is the safety floor. It is not negotiable across autonomy levels. The reason something is forbidden is independent of how reliable the agent is; it is forbidden because the action itself is incompatible with Dealix's trust posture.

The policy is short on purpose. Long policies invite reinterpretation in edge cases. When a new edge case appears, the answer is to bring it to the founder, decide, and add a one-sentence rule. We do not let agents resolve their own ambiguities.

This policy is read alongside `docs/ai_management/AI_HUMAN_OVERSIGHT.md`, which describes the operational pattern (queues, reviewers, SLAs) that implements these rules.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
