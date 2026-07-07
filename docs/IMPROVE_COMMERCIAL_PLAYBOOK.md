# improve — Commercial Playbook

How Dealix turns the `improve` skill into recurring revenue. This is the
commercial companion to `docs/IMPROVE_SKILL_INTEGRATION.md` (technical) and
`sales/IMPROVE_DIAGNOSTIC_DELIVERY_SOP_AR.md` (delivery runbook).

> Doctrine: hypothesis language only ("we expect / the goal is / we will
> measure"), no guaranteed outcomes, no fabricated numbers, human-review gate
> before anything reaches a customer, draft-only, no auto-execution.

## ملخص تنفيذي (AR)

`improve` ليس مجرد أداة داخلية — هو **محرّك تسليم** يحوّل عروض التشخيص الموجودة
إلى منتج قابل للتكرار بهامش عالٍ: مستشار غالٍ (Opus) ينتج خطط، منفّذ رخيص ينفّذ،
والمؤسس يراجع ويسلّم. القمع: تشخيص مجاني (طُعم) → Sprint (7,500–25,000) → Managed
Ops شهري. الملاءمة: الشركات ذات الأنظمة الرقمية (SaaS، أدوات داخلية، تدفّقات بيانات).

---

## 1. The product, precisely

`improve` produces, from real evidence: a **prioritized findings table**
(impact ÷ effort, weighted by confidence) and **self-contained executable plans**.
That is exactly the shape of the deliverable Dealix already promises in its
diagnostic funnel — `customers/_template/02_diagnostic_summary.md` (findings +
confidence + evidence) and the "Command Sprint scope" next step. `improve`
populates that funnel instead of it being hand-authored each time.

**Where it fits the funnel that already exists in the repo:**
- `api/routers/diagnostic.py`, `frontend/.../DealixDiagnosticLanding.tsx`,
  `landing/diagnostic.html` — the intake surfaces.
- `customers/<name>/02_diagnostic_summary.md` — filled from an `improve` run.
- Proof Pack (`proof_os`) — the paid deliverable.

## 2. Segment fit (be honest)

`improve` audits **codebases and digital systems**. It is the right engine when
the customer has software to look at:
- SaaS / product companies, tech-enabled B2B, teams with internal tooling,
  data pipelines, or integrations.

It is **not** a generic business consult. If a prospect has no digital system,
route them to the operational Command Room offer instead — do not stretch
`improve` to fit. Honest scoping protects the Proof Pack's credibility.

## 3. The funnel

```
Free Diagnostic (/improve quick)   → findings table = the hook
        │  upsell: "turn these into executed plans + proof"
        ▼
Diagnostic Sprint (/improve deep)  → plans + Proof Pack   (7,500–25,000 SAR)
        │  upsell: "keep the improvement backlog alive"
        ▼
Managed Ops (/improve reconcile)   → recurring backlog    (2,999–4,999 SAR/mo)
        │
        ▼
Custom Enterprise                  → improve + supervised execution (25,000+ SAR)
```

Prices per the official ladder (`CLAUDE.md`). Final scope/price set after the
free diagnostic. Ignore any archived pricing file that conflicts.

## 4. Margin economics

| Cost line | Who | Cost profile |
|-----------|-----|--------------|
| Recon + audit + vet + spec | Opus advisor | high $/token, but hours not days |
| Execution of accepted plans | free-tier executor via provider radar | ~$0/token, non-confidential repo code only |
| Review + merge decision | founder | fixed human time, the value gate |

The billed value is judgment (what's worth doing, written so it's shippable).
The variable cost is near-zero execution. That gap is the Sprint's gross margin,
and `reconcile` converts a one-off sale into a retainer.

## 5. Trust & compliance as a selling point

The same properties that satisfy Dealix doctrine are also what enterprise buyers
ask for: every finding cites evidence (no hand-waving), rejected findings are
recorded (transparency), nothing auto-executes (human control), secrets are never
reproduced (only location + type, rotation recommended), and merging stays the
customer's decision. Lead with this in regulated/PDPL-sensitive Saudi accounts.

## 6. What NOT to sell

- No "guaranteed" savings/ROI — estimates are hypotheses to be measured.
- No auto-remediation pitch — execution is supervised and customer-approved.
- No claim that `improve` fixes non-digital business problems.
- No routing of customer PII/secrets to free-tier executor models.

## 7. Related assets

- Delivery runbook: `sales/IMPROVE_DIAGNOSTIC_DELIVERY_SOP_AR.md`
- Customer deliverable template: `sales/DIAGNOSTIC_REPORT_TEMPLATE_AR.md`
- Technical integration: `docs/IMPROVE_SKILL_INTEGRATION.md`
- Provider economics: `scripts/ops/free_llm_provider_radar.py` +
  `scripts/ops/check_provider_registry_freshness.py`
