# Prompt Versioning Policy

## Versioning
- Prompts are versioned: v1, v2, ... in the file name or as a header.
- A prompt change that changes the output meaningfully bumps the version.
- The old version is kept for audit reproducibility.

## Promoting a prompt
1. Author proposes a new version in a PR.
2. Author runs `scripts/run_ai_evals.py --mode demo` showing the new version passes all evals.
3. Author updates `PROMPT_REGISTRY.md`.
4. Reviewer signs off.

## Deprecating
- A prompt is deprecated when no current task class references it.
- Deprecated prompts move to `business/ai/prompts/_archived/`.

## Audit
- Every AI call records `prompt_version`.
- If a customer asks "which prompt produced this?", we answer by reading `ai_audit_log.json`.
