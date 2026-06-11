# Deterministic Fallback Policy

## Why
- Service must work in a permission-denied / offline / quota-exhausted environment.
- Customer who hasn't opted into LLM-assist still gets a usable artifact.
- Auditable output that doesn't depend on a third party.

## What "deterministic" means
- Same input → same output every run.
- Output is a structured placeholder for the operator to edit.
- Output never claims a result.
- Output carries `deterministic: true` in metadata.

## When fallback triggers
- `--use-ai` flag not passed.
- `AI_PROVIDER_DEFAULT` not set.
- Provider call raised an exception.
- Provider response failed safety check.
- Provider response failed evals.

## How to detect in downstream code
- Inspect `AIResponse.deterministic`.
- If `True`, treat output as a hand-edit template.
- If `False`, output came from LLM and is logged with provider/model/prompt_version.
