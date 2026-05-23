# Performance Improvement OS

The Performance Improvement OS is the operating layer that turns measurement into change. It is the loop that connects the Revenue KPI Tree to the Experiment Backlog to the Learning Loop.

**Source of truth:** `$PRIVATE_OPS/performance_state.csv`
**Owner:** Founder + Marketing Lead
**Trust gate:** A1 for internal experiments; A2 for any change that affects pricing, scope, or external surface.

## Components

| Component | Doc |
|-----------|-----|
| Revenue KPI Tree | `docs/performance/REVENUE_KPI_TREE.md` |
| Conversion Diagnostics | `docs/performance/CONVERSION_DIAGNOSTICS.md` |
| Experiment Backlog | `docs/performance/EXPERIMENT_BACKLOG.md` |
| Learning Loop | `docs/performance/LEARNING_LOOP.md` |
| Next Best Action Engine | `docs/performance/NEXT_BEST_ACTION_ENGINE.md` |

## Weekly cadence

1. **Monday.** Performance Analyst posts the weekly read (`docs/ai/PERFORMANCE_ANALYST_AGENT.md`).
2. **Tuesday.** Marketing Lead proposes the week's experiments using the read.
3. **Wednesday.** Founder approves at A1 / A2 as appropriate.
4. **Thursday-Sunday.** Experiments run.
5. **Following Monday.** Results land in the next read; learnings to the Learning Loop.

## Decision rules

| Movement | Action |
|----------|--------|
| KPI up, attributable to experiment | Promote experiment; keep change |
| KPI up, unattributable | Continue measurement; do not credit |
| KPI down, attributable to experiment | Revert experiment |
| KPI down, unattributable | Investigate; new diagnostic |
| KPI flat | Patience or new hypothesis |

## OWASP / NIST posture

The OS itself is a process, not an agent. The agents that feed it (Performance Analyst, Growth Strategist) follow the registered behaviour in `registries/agent_registry.yaml`.

## Failure modes

- **Read without action:** the read is produced but no experiments follow. Detection: weekly review. Recovery: founder re-engages the cycle.
- **Action without read:** experiments run without a prior read. Detection: backlog audit. Recovery: tie experiment to source KPI.
- **Credit creep:** unattributable wins claimed as experiment wins. Detection: audit. Recovery: re-classify; reduce confidence.

## Recovery path

If the OS produces inconsistent results (KPI vs experiment data conflict), the founder freezes new experiments and reconciles data sources.

## Metrics

- Weekly read produced (target: 100%).
- Experiments approved per week (target: 1-3).
- Experiments with attributable outcome (estimated).
- Learnings captured per quarter.

## Disclaimer

Performance Improvement is a method, not a guarantee. Dealix does not guarantee that experiments succeed. Estimated value is not Verified value.
