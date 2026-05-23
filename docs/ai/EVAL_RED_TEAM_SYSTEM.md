# Eval / Red-Team System

The eval gate (`evals/gates/dealix_agent_eval_gate.yaml`) defines the
suites that block a release. Each suite has a `severity` and either a
list of `forbidden_phrases`, a list of `forbidden_patterns`, or a named
`rule` that the platform implements (e.g. `arabic_lint_pass`).

Suites must include prompt-injection, sensitive-data leakage, approval
bypass, and pricing/proof safety. The verifier enforces the required
suite set.
