# Hermes Agent OS

Hermes is the Dealix internal agent reporting layer. It starts as a safe dry-run system that reads repository configuration and writes reviewable reports.

## Files

| Purpose | File |
|---|---|
| Agent registry | `dealix/hermes/agents.yaml` |
| Governance policy | `dealix/hermes/policy.yaml` |
| Local report generator | `scripts/hermes_report.py` |
| Generated reports | `docs/generated/hermes/` |

## Agents

| Agent | Purpose |
|---|---|
| Founder Chief of Staff | Daily priorities and founder brief. |
| Revenue Operator | Revenue readiness and proof-pack focus. |
| Trust Guardian | Claims, approvals, and evidence discipline. |
| Platform SRE | CI, smoke, domain, deployment, and rollback awareness. |
| Security Auditor | Security workflows and dependency evidence. |
| Product Strategist | Roadmap and feature-to-revenue mapping. |
| AI Quality Evaluator | Eval rubrics and structured-output quality. |

## Run locally

```bash
python scripts/hermes_report.py
```

## Operating rule

Hermes reports are review-only by default. Keep the system in dry-run until production gates, approval paths, and generated outputs are reviewed.

## Review checklist

- [ ] Agent mission is clear.
- [ ] Output is useful.
- [ ] Stop rules are understood.
- [ ] Human approval expectations are clear.
- [ ] Generated report is reviewed before operational use.

## Arabic summary

Hermes طبقة وكلاء داخلية تبدأ كتقارير فقط. تقرأ إعدادات الريبو وتكتب تقارير قابلة للمراجعة، ولا يجب رفع صلاحياتها إلا بعد مراجعة بشرية واضحة.
