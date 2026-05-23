# Prompt / Output Eval Matrix

`scripts/verify_prompt_output_quality.py` scans the markdown and YAML
under `docs/`, `prompts/`, `policies/`, `registries/`, and `evals/` for:

- forbidden marketing claims (e.g. "guaranteed revenue")
- secret-looking literals
- accidental real-domain email addresses (informational only)

Files that *define* the forbidden phrases (policy and eval YAML, the
verifier itself, and `CLAUDE.md`) are allow-listed so they can name the
phrases without triggering a failure.

This script is intentionally simple — its job is to catch obvious
regressions, not replace a full red-team eval.
