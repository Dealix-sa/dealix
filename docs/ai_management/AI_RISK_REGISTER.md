# AI Risk Register

> Per-agent risks, scored and reviewed.

## Risk Schema

```
- id: R-AI-NN
  agent_id: AI-NN
  risk: "..."
  likelihood: low / med / high
  impact: low / med / high
  mitigation: "..."
  residual_likelihood: low / med / high
  residual_impact: low / med / high
  owner: Sami
  review_date: yyyy-mm-dd
  status: open / mitigated / accepted
```

## Risk Categories (OWASP LLM-aligned)

- **Prompt Injection** — external content manipulating agent behaviour
- **Sensitive Information Disclosure** — agent leaking PII or customer data
- **Insecure Output Handling** — agent output being executed downstream
- **Training Data Poisoning** — N/A (we do not train models)
- **Model Denial of Service** — abuse of paid inference
- **Supply Chain** — vendor / model availability and behaviour change
- **Excessive Agency** — agent acting beyond autonomy tier
- **Overreliance** — humans rubber-stamping agent output
- **Model Theft** — N/A
- **Hallucination** — confident output without basis

## Sample Entries

### R-AI-01 — Prompt Injection via fetched web content (AI-02 Outreach Draft)

- Likelihood: med (we fetch public content)
- Impact: high (outbound message could be hijacked)
- Mitigation: external text treated as data; T2 approval per send; doctrine verifier
- Residual: low / med
- Status: open
- Review: monthly

### R-AI-02 — Hallucinated company facts in outreach drafts

- Likelihood: med
- Impact: high
- Mitigation: every claim in draft must cite a source already in the lead row; QA Checker (AI-05) fails drafts with unsupported claims
- Residual: low / med
- Status: open

### R-AI-03 — Customer PII leakage into public surfaces

- Likelihood: low
- Impact: very high (PDPL exposure)
- Mitigation: public/private boundary; CI scan; T2 approval for any case study
- Residual: low / med
- Status: open

### R-AI-04 — Excessive Agency: agent reaches A3 without per-send approval

- Likelihood: low
- Impact: very high (trust incident)
- Mitigation: outbound channel requires per-send token issued by founder approval; channel rejects messages without token
- Residual: low / low
- Status: open

### R-AI-05 — Overreliance: founder rubber-stamps agent drafts

- Likelihood: med (especially when busy)
- Impact: high
- Mitigation: review checklist surfaces top 3 hallucination risks per draft; weekly audit of 5 sent drafts vs source data
- Residual: low / med
- Status: open

### R-AI-06 — Vendor model retirement / behaviour shift

- Likelihood: med
- Impact: med
- Mitigation: pin models; canary on minor version changes; evaluation suite re-runs on any model bump
- Residual: low / med
- Status: open

### R-AI-07 — Inference cost runaway

- Likelihood: low
- Impact: med
- Mitigation: per-pipeline cost caps; monthly review of spend; cap alerts
- Residual: low / low
- Status: open

## Quarterly Risk Review

- Re-score each open risk.
- Close mitigated risks with evidence.
- Promote any residual risk that moved to higher severity.
- Add risks raised by incidents in `INCIDENT_RESPONSE.md`.
