# AI Human Oversight — الرقابة البشرية على الذكاء الاصطناعي

## Purpose
Define the operational pattern that implements the autonomy policy: queues, reviewers, SLAs, and the human-in-the-loop checkpoints by autonomy level.

## Owner
Founder.

## Inputs
- Autonomy levels per agent from the inventory.
- Approval matrix.
- Sprint workflow.

## Outputs
- Review queues per agent class.
- Logged human decisions on every A2 and A3 output.

## Rules (numbered)
1. A0 outputs: no per-output review; sampled at 5 percent weekly.
2. A1 outputs: reviewed at sprint G3 before reaching QA.
3. A2 outputs: reviewed individually before reaching client artifacts; named reviewer; SLA documented.
4. A3 actions: not executed until written approval is logged.
5. Reviewers are documented per agent class.
6. Review queues have an SLA; queue items older than the SLA are escalated.

## Metrics
- A2 review SLA compliance (target greater than or equal to 95 percent).
- A3 approval median time.
- Outputs sampled at A0 rate (target at least 5 percent weekly).
- Escalations from queue (target near zero).

## Cadence
Continuous. Reviewed monthly.

## Evidence (paths)
- `docs/ai_management/review_queues/`
- `docs/trust/registers/a3_log.md`

## Verifier
Founder.

## Runtime Command
`make ai.oversight.queue STATUS=open` lists open review items.

## Oversight pattern by class

**A0 — sampled oversight.** No per-output gate. 5 percent of weekly outputs pulled into a sampling queue. Reviewer is the agent's owner. Findings feed the agent's evaluation set update.

**A1 — sprint-gate oversight.** Every A1 output that lands in a sprint artifact is reviewed at G3 by a human (typically the builder of the pack). Defects route back; the agent does not produce again until the defect class is addressed.

**A2 — per-output oversight.** Every A2 output lands in a named queue before reaching a client artifact. Queue has a named reviewer with a documented SLA (typically 4 business hours). Reviewer can approve, reject, or send back with notes. Rejected outputs do not silently disappear; they are logged for pattern analysis.

**A3 — explicit human approval.** A3 actions are not autonomy of the agent; they are actions of the human who approved them. The agent prepares the action; the human approves; the agent (or human) executes. The approval log is the audit trail.

## Reviewer assignments

| agent_id | autonomy | reviewer | sla |
|---|---|---|---|
| AG-001 | A1 | sprint builder | sprint G3 |
| AG-002 | A0 | data lead | sampled weekly |
| AG-003 | A1 | sprint builder | sprint G3 |
| AG-004 | A1 | sprint builder | sprint G3 |
| AG-005 | A0 | head of delivery | sampled weekly |
| AG-006 | A1 | sprint builder | sprint G3 |
| AG-007 | A1 | sprint builder | sprint G3 |

## Queue mechanics

A review queue is a folder under `docs/ai_management/review_queues/<agent_id>/` with one file per pending item. Each file contains: input summary, agent output, reviewer name, status (open, approved, rejected), decision timestamp, notes.

When an item is approved, the file is moved to `approved/`. When rejected, it goes to `rejected/` with the reason. The two folders are the audit trail.

## Operating substance
Human oversight is not a brake on agent productivity; it is the structure that makes agent productivity safe to deploy. Without oversight, agent outputs that are 95 percent right contaminate the 5 percent that need intervention. With oversight, the 5 percent is caught and the 95 percent flows through.

The SLA per reviewer matters. An oversight pattern with no SLA becomes a bottleneck and then an excuse to skip oversight. Realistic SLAs (4 business hours for A2) are what make the pattern sustainable.

A3 approvals are short, frequent, and per-action. They are not batched. Batching loses the auditability that A3 exists to provide. A founder approving five A3 actions in a day is exercising the system correctly; a founder approving one batch of 50 once a month is not.

Sampling at A0 is the safety net. Even outputs that do not need per-output review benefit from sampled review; the sampling discovers drift before it accumulates.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
