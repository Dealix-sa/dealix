# Eval / Red-Team System

Source of truth: [`evals/gates/dealix_agent_eval_gate.yaml`](../../evals/gates/dealix_agent_eval_gate.yaml).

## How a suite runs

1. Suite definition has `must_reject_examples` (and optionally `must_accept_examples`).
2. Eval Guardian invokes the agent with each example.
3. Pass = agent rejects every `must_reject_examples` entry.
4. Fail = the suite blocks the agent until fixed.

## Red-team additions

Coding agents (Claude Code etc.) MUST add a new red-team example any
time a safety regression is discovered. The new example becomes a
permanent part of the gate.

## Coverage

The 15 mandatory suites are listed in
[`docs/evals/EVAL_GATE_V1.md`](../evals/EVAL_GATE_V1.md). Every suite
maps to at least one entry in the prompt/output eval matrix.
