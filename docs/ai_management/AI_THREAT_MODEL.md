# AI Threat Model — نموذج التهديدات للذكاء الاصطناعي

## Purpose
Identify the categories of threat against Dealix's AI surface and the defenses against each. The threat model feeds the risk register and the release gate.

## Owner
Founder.

## Inputs
- Agent inventory.
- External threat-research notes.
- Incident history.

## Outputs
- Threat catalogue (below).
- Defense map per threat.

## Rules (numbered)
1. Every threat category has a documented defense.
2. New agents are evaluated against this threat model at the release gate.
3. Threats are reviewed quarterly alongside the risk register.
4. New threat categories require A3 approval to add to the model.
5. Defenses must be testable; an untested defense is not counted.

## Metrics
- Threats with documented defense (target 100).
- Defenses with a test reference (target 100).
- New threat categories added per year.

## Cadence
Quarterly review.

## Evidence (paths)
- `docs/ai_management/AI_THREAT_MODEL.md` (this file).
- `docs/ai_management/AI_RISK_REGISTER.md` for scored versions.

## Verifier
Founder.

## Runtime Command
`make ai.threat.review` opens this file with the latest risk register for cross-check.

## Threat catalogue

**T1 Prompt injection.** Hostile content in a source URL, document, or input that attempts to override agent instructions. Defense: source content is never concatenated raw into agent prompts; only structured metadata (URL, title, date, sector code) is passed. Test: red-team prompt set run quarterly.

**T2 Data leakage.** Agent reveals client-confidential data to a third party (another client, a public artifact, a log). Defense: per-client data isolation; no cross-sprint context sharing; PII never enters agent context. Test: log audit and isolation check monthly.

**T3 Hallucination.** Agent fabricates facts (a company that does not exist, a tender that was not posted, a source URL that does not resolve). Defense: source URL required per claim; URL resolution check; QA spot-check on random rows. Test: weekly URL resolution scan.

**T4 Runaway autonomy.** Agent takes actions beyond its assigned class. Defense: tool layer enforces autonomy at call time; A2 calls require review token; A3 calls require named approval ID. Test: monthly enforcement audit.

**T5 Output overclaim.** Agent produces content that triggers the no-overclaim policy. Defense: banned-phrase scanner runs before any output reaches a human; safe-language library lookup; final human review at G3. Test: scanner hit-rate trend in the trust dashboard.

**T6 Bias in scoring.** Agent's scoring rubric application varies systematically by sector, region, or company size in ways the rubric does not justify. Defense: dual-scoring calibration at sprint start; quarterly bias review on aggregated scores. Test: dual-rater agreement metric tracked.

**T7 Model availability.** Third-party model is unavailable, rate-limited, or changes behavior without notice. Defense: manual fallback documented per agent; sprint workflow can complete without agent assistance at degraded throughput. Test: monthly manual-fallback drill.

**T8 Prompt regression.** Prompt change degrades output quality without triggering an obvious incident. Defense: prompt versioning; offline evals required on prompt change; rollback path documented. Test: pre/post-change eval run.

**T9 Cross-tenant contamination.** Agent's context window includes data from a different sprint or client. Defense: agents run with single-sprint scope; no agent has standing access to multiple sprint folders. Test: scope assertion in tool layer.

**T10 Shadow agent.** An agent runs that is not in the inventory. Defense: every model API call must reference an inventory agent ID; calls without ID are blocked. Test: monthly inventory completeness check.

## Operating substance
The threat model is deliberately concrete. Each threat names a specific attack or failure mode, a specific defense, and a specific test. Generic threats produce generic defenses, which is how AI governance becomes theatre.

The defenses are layered because no single defense holds. Hallucination defense is "URL required + URL resolution check + QA spot-check". Overclaim defense is "scanner + library + human review". Layering is the only credible posture against AI failure modes that are statistical rather than deterministic.

The tests matter. A defense that has not been exercised in the last quarter is not a defense; it is a hope. The quarterly review re-runs the test list and marks each one as exercised or not.

The model is finite. Ten threat categories is enough to cover the current Dealix AI surface. Future agents may add categories; the addition follows A3 approval.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
