# AI Incident Response — استجابة حوادث الذكاء الاصطناعي

## Purpose
Define the AI-specific incident playbook: hallucination, data leakage, biased output, prompt injection, runaway autonomy. Sits inside the broader `docs/trust/INCIDENT_RESPONSE.md` framework but adds AI-specific containment steps.

## Owner
Founder (Sev-1, Sev-2). Head of Delivery (Sev-3).

## Inputs
- AI incident detection signals (eval failures, sampling defects, client reports).
- Threat model categories.
- Agent inventory and recent change log.

## Outputs
- Incident log entry in `docs/trust/registers/incident_log.md` with AI-specific fields.
- Containment actions logged.
- Post-incident learning entry and policy or prompt update.

## Rules (numbered)
1. AI incidents follow the broader incident response cadence, plus AI-specific containment.
2. First containment action for any AI incident is to pause the agent at its tool layer.
3. Prompt rollback is the second action when a prompt change is suspected.
4. Sev-1 AI incidents: agent is rolled back to last known good prompt; sandbox-only until cleared.
5. Every AI incident updates either the eval set, the threat model, or the risk register.
6. Pattern of 3 similar incidents within a quarter triggers a structural review of the agent.

## Metrics
- AI incident count by category and severity.
- Mean time from detection to agent pause.
- Mean time from pause to root cause documented.
- Repeat-category incidents per quarter.

## Cadence
Continuous. Monthly aggregate review.

## Evidence (paths)
- `docs/trust/registers/incident_log.md`
- `docs/ai_management/incidents/AG-<id>/<date>.md` for AI-specific detail.

## Verifier
Founder.

## Runtime Command
`make ai.incident.pause AGENT=<id> REASON=<r>` pauses an agent and writes the incident skeleton.

## AI incident categories

**Hallucination.** Agent produced a claim that does not match a verifiable source. Containment: pause agent; pull the offending artifact from any pipeline; review last 10 outputs of the same agent for similar defects. Root cause analysis: prompt issue, source mishandling, model regression. Update: eval set; possibly prompt.

**Data leakage.** Agent included data from outside its scope (different sprint, different client, PII). Containment: pause agent; review tool layer scope enforcement; identify all affected artifacts; notify affected clients within 24h. This is at least Sev-2. Update: tool layer; threat model T9.

**Biased output.** Agent's scoring or drafting varies systematically along an unjustified axis. Containment: re-score affected sprints with a different operator; review rubric application. Root cause: rubric interpretation, training data drift, prompt phrasing. Update: scoring rules, prompt.

**Prompt injection.** Hostile content from a source caused the agent to deviate from its instructions. Containment: pause agent; quarantine the source; review what data was passed into the agent context. This is at least Sev-2. Update: threat model T1; tool layer to sanitize inputs.

**Runaway autonomy.** Agent took an action beyond its assigned class. Containment: pause agent; review tool layer enforcement (this should not have happened); revoke any consequences if reversible; notify if not. This is Sev-1. Update: tool layer; risk register AIR-005.

**Output overclaim.** Agent produced content with banned phrases that reached past the scanner. Containment: pull the artifact; rerun the scanner with the new pattern. This is Sev-2 if published, Sev-3 if caught at QA. Update: scanner rules; safe language library; possibly prompt.

## Containment-first principle

Across all categories, the first action is containment, not investigation. Pause the agent. Pull the artifact. Then investigate. Order matters because the cost of an agent producing more bad output during investigation is asymmetric.

## Operating substance
AI incidents have a different shape from traditional software incidents. The failure is often probabilistic (the agent does the wrong thing 1 in 200 times) rather than deterministic. This makes detection harder and containment more important.

Pause-first is the discipline that compensates. We do not wait for certainty before pausing; uncertainty itself is enough. A paused agent that turns out to be fine costs an hour of operator time. An unpaused agent that turns out to be wrong costs trust.

Every AI incident produces a structural update — to the eval set, the threat model, the risk register, the tool layer, or the prompt. An incident that does not produce an update is an incident that will recur. The closing artifact of every AI incident is the diff: what changed in the system.

Pattern detection across incidents is the meta-discipline. Three hallucinations in a quarter on the same agent is a different problem from one hallucination. The agent needs structural review, not just a prompt tweak.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
