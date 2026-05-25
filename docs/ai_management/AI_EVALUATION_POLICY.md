# AI Evaluation Policy — سياسة تقييم الذكاء الاصطناعي

## Purpose
Define how Dealix evaluates AI outputs: offline evaluations before release, sampling during production, and human review checkpoints. Evaluations are how we know an agent is doing what its inventory row says it does.

## Owner
Founder. Per-agent owner runs evaluations.

## Inputs
- Agent under evaluation.
- Evaluation set per agent.
- Sampling cadence per agent.

## Outputs
- Offline evaluation reports at `docs/ai_management/evals/AG-<id>/<date>.md`.
- Sampling logs per agent.
- Pass/fail decisions at release and at quarterly review.

## Rules (numbered)
1. Every agent has an evaluation set before it reaches A1.
2. The evaluation set covers normal inputs, edge cases, and adversarial inputs.
3. Pass thresholds are documented per agent.
4. Production sampling rate is at least 5 percent of outputs per week, manually reviewed.
5. Human review is required at every sprint G3 for any agent-touched artifact.
6. Failed evaluations block promotion or trigger rollback.

## Metrics
- Evaluation pass rate per agent over time.
- Sampling review completion rate (target 100).
- Defects found in sampling vs at QA (sampling should catch more).

## Cadence
- Offline evals: at release, on prompt change, quarterly.
- Sampling: continuous.
- Human review at sprint G3: every sprint.

## Evidence (paths)
- `docs/ai_management/evals/AG-<id>/`
- `docs/audit/sprints/SPRINT_<ID>/agent_review.md`

## Verifier
Founder for release evals. Head of Delivery for quarterly evals.

## Runtime Command
`make ai.eval.run AGENT=<id>` runs the agent's evaluation set and writes the report.

## Evaluation set design

Each agent has an evaluation set with at least three categories:

**Normal.** 20 to 50 inputs that represent typical production usage. Pass threshold is documented per agent (typically high; these are the easy cases).

**Edge.** 10 to 20 inputs at the boundary of the agent's stated capability. Pass threshold is lower; goal is to know where the agent degrades.

**Adversarial.** 10 to 20 inputs designed to provoke the threat categories in `AI_THREAT_MODEL.md`. Prompt-injection attempts, ambiguous instructions, content with banned phrases, etc. Pass means the agent declines or escalates rather than complying.

## Sampling

In production, at least 5 percent of agent outputs are pulled into a review queue weekly. The reviewer is the agent's owner. The review uses the same rubric as the offline evaluation. Defects are logged; patterns inform the next eval set update.

## Human review at G3

Every sprint's G3 gate includes a human review of every agent-touched artifact in the pack. This is not the QA review (which is at G4 and broader); this is the per-agent review at G3. It is where most agent defects are caught and fixed before QA.

## Eval set update cadence

Evaluation sets are living documents. Sampling defects, sprint defects, and adversarial findings feed back into the set. The set is updated quarterly with at least one new edge case per agent and one new adversarial case per agent.

## Operating substance
Evaluations are how we replace "this agent feels right" with "this agent passes a documented set". The shift from intuition to evidence is the same shift Dealix makes for clients with the evidence pack. We apply it to our own tooling.

The adversarial portion of the evaluation set is the most useful and the most often skipped. Adversarial inputs are the ones the agent will see in production from a hostile or unusual source. An agent that has never been tested adversarially is an agent with unknown failure modes.

Sampling is more rigorous than QA because it inspects routine output, not exceptional output. QA looks at the pack that will ship; sampling looks at the agent that produced many packs. The two are complementary.

Eval sets that do not change are eval sets that decay. The quarterly update is the discipline that keeps them honest as agents, prompts, and sectors evolve.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
