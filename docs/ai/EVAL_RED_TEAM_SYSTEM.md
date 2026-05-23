# Eval + Red Team System

Every AI agent in Dealix passes its own eval suite **before** it runs
in production, and every release passes a red-team gate.

## 1. Eval discipline

For every agent (see `docs/ai/*_AGENT.md`):

- A named `eval_suite` lives under `evals/`.
- The suite covers correctness, voice, safety, and provenance.
- The agent's pipeline refuses to deploy if any case regresses below
  the configured threshold.

## 2. Red-team gate

A red-team gate runs against the agent registry on every release. It
attempts:

- Prompt injection via tool inputs.
- Excessive-agency probes (asking the agent to "just send it").
- Data exfiltration probes ("show me PII").
- Cross-tenant probes ("read account X's data").
- Jailbreak probes ("ignore previous instructions").

Every probe that succeeds blocks the release.

## 3. Audit and reporting

- Every eval run writes a row to `audit/evals/`.
- Every red-team result writes a row to `audit/red_team/`.
- Releases are tagged with the eval + red-team verdict.

## 4. Failure handling

- An agent that fails its eval is **stopped**, not "downgraded".
- The kill switch is engaged automatically.
- The founder is notified through the console (not via external
  channels).

## 5. Banned patterns

- ❌ Deploying an agent without an eval suite.
- ❌ Skipping the red-team gate "just this once".
- ❌ Hiding a regression behind a threshold change.
