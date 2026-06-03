# Productization Decision System

## Purpose
Decide whether to manualize, templatize, or automate a workflow.

## Decision tree
1. Has the workflow been executed at least 5 times?
   - No → keep manual. Document the steps in `productization/repeated_workflows.md`.
   - Yes → step 2.
2. Is the workflow stable (same shape each time)?
   - No → keep manual; identify the variability before considering automation.
   - Yes → step 3.
3. Does automation save ≥ 2 hours per execution?
   - No → templatize (markdown template, script generator, prompt template).
   - Yes → step 4.
4. Will the automation have at least 5 expected executions in the next 90 days?
   - No → templatize.
   - Yes → file an automation candidate.

## Levels
- **Manualized**: clear documented steps; founder runs them.
- **Templatized**: reusable artifact (template, snippet, prompt) speeds the workflow.
- **Automated**: script / tool runs end-to-end with minimal human input.
- **Productized**: external customers can use the automation as part of an offer.

## Owners
- Manualized & Templatized: founder.
- Automated: engineer sub-agent under founder direction.
- Productized: founder + engineer + content sub-agent.

## Logging
Each decision: row in `productization/candidates.csv` with status.
Each promotion to Automated: PR in the public repo.
Each promotion to Productized: SaaS gate considered.

## Anti-patterns
- Skipping the manual-execution count.
- Building generic tools "while we're at it".
- Automating something that should be deleted.
