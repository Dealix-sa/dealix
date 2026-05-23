# Conversion Diagnostics

Conversion Diagnostics is the discipline of asking "why did this rate move?" at every node of the Revenue KPI Tree. It produces explanations, not just numbers.

**Source of truth:** `$PRIVATE_OPS/conversion_diagnostics_log.csv`
**Owner:** Performance Analyst (`docs/ai/PERFORMANCE_ANALYST_AGENT.md`) + Marketing Lead
**Trust gate:** A1 — diagnostic conclusions are reviewed before they feed experiment proposals.

## When a diagnostic is triggered

| Trigger | Threshold |
|---------|-----------|
| Week-over-week drop | > 15% at any node |
| Conversion rate drop | > 10 percentage points |
| Outlier client/segment | Single source explains > 50% of movement |
| Anomalous experiment | Experiment result inconsistent with prior runs |

## Diagnostic method

1. State the headline: "Node X moved from A to B (Δ%)."
2. Decompose: rank child nodes by contribution to the movement.
3. Slice: by sector, channel, package, owner, agent involvement.
4. Hypothesise: list 2-3 hypotheses with the evidence each requires.
5. Test design: name the experiment that would distinguish hypotheses.
6. Risk note: what could be wrong with this diagnostic.

Diagnostics never assert causation without an experiment.

## Output

Each diagnostic is a one-page document:

```
diagnostic_id, triggered_at, headline_node,
movement, decomposition[], slicing[],
hypotheses[], test_design, risk_note,
linked_experiment_id, conclusion_status
```

`conclusion_status` is one of `open`, `experiment_running`, `concluded_supported`, `concluded_refuted`, `dropped`.

## Language discipline

| Allowed | Banned |
|---------|--------|
| "Associated with" | "Caused by" without experiment |
| "Explained by" (in regression sense) | "Because of" without evidence |
| "Likely contributor" | "Definitely due to" |
| "Estimated impact" | "Will deliver X" |

## OWASP / NIST posture

Diagnostics are produced by the Performance Analyst agent. The agent's eval suite checks for banned framings and for citation density.

## Failure modes

- **Premature conclusion:** a diagnostic concludes without experiment. Detection: weekly review. Recovery: reopen; design experiment.
- **Slicing fishing:** the diagnostic slices until something significant appears. Detection: pre-registered slice list. Recovery: discard, redesign.
- **Stale diagnostic:** an open diagnostic > 30 days. Detection: nightly job. Recovery: re-prioritise or drop.

## Recovery path

If diagnostics consistently fail to predict experiment outcomes, the agent is paused (or killed) and diagnostics revert to human-only authorship.

## Metrics

- Diagnostics opened per week.
- Median time-to-conclusion.
- Supported / refuted ratio.
- Diagnostic-to-experiment conversion (estimated).

## Disclaimer

Diagnostics propose explanations. Experiments test them. Neither guarantees outcomes. Estimated value is not Verified value.
