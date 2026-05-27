# Tooling Adoption Matrix

## Purpose
Evaluate helpful libraries and tools without creating dependency sprawl or production risk.

## Optional extras added

The PR adds optional dependency groups in `pyproject.toml`:

| Extra | Purpose | Install command |
|---|---|---|
| observability | tracing, monitoring, error tracking | `pip install -e '.[observability]'` |
| evaluation | AI/RAG output evaluation | `pip install -e '.[evaluation]'` |
| data_quality | data checks and drift review | `pip install -e '.[data_quality]'` |
| analytics | local analysis and lightweight data work | `pip install -e '.[analytics]'` |
| security_advanced | extra static/security auditing tools | `pip install -e '.[security_advanced]'` |
| automation | workflow orchestration experiments | `pip install -e '.[automation]'` |
| founder_stack | all strategic extras | `pip install -e '.[founder_stack]'` |

## Candidate tool categories

| Category | Candidate tools | Use case | Risk |
|---|---|---|---|
| Observability | OpenTelemetry, Sentry | API and workflow visibility | Data and cost review needed |
| AI evaluation | Ragas, DeepEval | Score AI output quality | Requires curated test sets |
| Data quality | Great Expectations, Evidently | Data validation and drift checks | Setup and owner needed |
| Analytics | pandas, Polars, DuckDB | Founder analysis and dashboards | Low if local/internal |
| Security | Semgrep, pip-audit | Additional code and dependency review | False positives need triage |
| Automation | Prefect | Scheduled workflows and jobs | Operational overhead |

## Adoption checklist

Before activating a tool:

- [ ] Owner assigned.
- [ ] Business use case written.
- [ ] Data sent or stored is documented.
- [ ] Cost driver is known.
- [ ] Security review completed.
- [ ] Test environment used first.
- [ ] Exit plan exists.
- [ ] Tool is added to AI Tool Registry or Tool Register.

## Founder rule

Install only what increases speed, trust, quality, revenue, retention, or strategic leverage.
