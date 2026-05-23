# Productization & Engineering OS

## Purpose
Convert repeated manual work into reliable software — but only when the work is genuinely repeatable and the unit economics support it.

## Sub-systems
- Decision system — `docs/product/PRODUCTIZATION_DECISION_SYSTEM.md`
- SaaS architecture gate — `docs/product/SAAS_ARCHITECTURE_GATE.md`
- Engineering architecture — `docs/engineering/ENGINEERING_ARCHITECTURE.md`
- Automation permission matrix — `docs/automation/AUTOMATION_PERMISSION_MATRIX.md`
- Agent readiness — `docs/agents/AGENT_READINESS_SYSTEM.md`

## Operating principles
1. **Use before code**: a workflow must be executed manually at least 5 times before automating.
2. **Score before build**: every candidate gets a productization score.
3. **Repeatability before SaaS**: SaaS only after 3 paying customers on the same offer.
4. **Founder writes the first version**: no contractor builds a productized surface from scratch.

## Where the productization log lives
- Candidates: `productization/candidates.csv`
- Repeated workflows: `productization/repeated_workflows.md`
- Automation backlog: `productization/automation_backlog.md`

## Scoring
`ops_runtime/productization_scorer.py` returns a 0–100 score based on:
- Frequency (how often does the workflow repeat)
- Manual time (how many hours per execution)
- Automation value (how much time / risk does automation save)
- Strategic value (does the automation create a defensible moat?)

## Operating cadence
- Weekly: founder reviews one workflow from `repeated_workflows.md` and either documents it more rigorously or files an automation candidate.
- Monthly: re-score the candidate list; promote top 3 to backlog.
- Quarterly: pick at most one automation to ship.

## Anti-patterns
- "Just one more script" sprawl.
- Automating a workflow that has not been executed manually enough times.
- SaaS-shaped thinking before SaaS gate passed.
