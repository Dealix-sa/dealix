# Free Tools Strategy — أدوات مجّانية تلتقط العملاء

> Loop 1 of the Self-Growth OS. Every tool is a **lead-capture surface** that routes to exactly
> one CTA. Tools give a genuinely useful result first; capture is value-for-value, never bait.
> Status labels reflect `docs/00_platform_truth/MODULE_STATUS_MAP.md`.

## المبدأ (Principle)

A free tool must deliver a standalone-useful result in under 60 seconds, Arabic-first,
PDPL-disciplined, no forced signup to *see* the result — capture comes at the "go deeper" step.
The result is engineered to make the **single** CTA the obvious next move.

## كتالوج الأدوات (Tool catalog)

| Tool | Surface | What it returns | Primary CTA | Status |
|------|---------|-----------------|-------------|--------|
| Business OS Score | `frontend/[locale]/risk-score` | Operating-rhythm score across the 14 OS areas | **Get Business OS Score** → Diagnostic | `BETA` |
| AI Ops Diagnostic (Lite) | `landing/diagnostic.html` | Readiness snapshot + top 3 gaps | **Book Diagnostic** | `BETA` |
| Lead Score Calculator | `landing/free-tools/lead-score-calculator.html` | Single-lead strength score (KSA B2B benchmarks) | **Book Diagnostic** | `LIVE` |
| ROI Estimator | `landing/roi.html` | Rough revenue-leak estimate | **Book Diagnostic** | `LIVE` |
| LTV Calculator | `landing/ltv-calculator.html` | Customer LTV + payback hypothesis | **Book Diagnostic** | `LIVE` |
| Market Radar (Lite) | `landing/market-radar.html` | Sector signal sample | **Get Business OS Score** | `BETA` |
| Sector Report Sample | `landing/sector-report-b2b-services.html` | Anonymized sector pattern preview | **Book Diagnostic** | `DOCS_ONLY` |

> Any tool labeled `BETA`/`DOCS_ONLY` must be presented as such on-page. Never present a
> `FUTURE`/`DOCS_ONLY` tool as live.

## قاعدة التوجيه (Routing rule)

- Lowest-intent / top-of-funnel tools → **Business OS Score**.
- Calculators and readiness tools (named pain) → **Book Diagnostic**.
- Never route a free tool directly to the 499 Sprint — earn it through Diagnostic first.

## التقاط القيمة مقابل القيمة (Value-for-value capture)

1. Show the result immediately, no wall.
2. Offer "email me the full breakdown / benchmark context" → optional email field.
3. The result page's single CTA is the routed next step (Score or Diagnostic).
4. Captured email enters the **free-tool-lead** nurture (drafts only — see `NURTURE_SEQUENCES.md`).

No dark patterns, no fake "X people scored today" counters, no fake scarcity. PDPL consent line
on every capture field.

## حلقة الأداة → المحتوى (Tool → content loop)

Aggregated, anonymized tool inputs become benchmark content (e.g. "median lead score in KSA
B2B services"), feeding the Content Factory — but only as **hypothesis-framed** insight until a
Proof Pack backs the number. Never publish a specific client's inputs.

## خطة 30 يوم (30-day plan)

1. Audit the live calculators (`roi`, `ltv`, `lead-score-calculator`) — confirm each has exactly
   one CTA and a PDPL consent line; fix any with competing CTAs.
2. Ship the Business OS Score `BETA` result page with the email-capture step.
3. Add an honest status label badge to every `BETA`/`DOCS_ONLY` tool.
4. Connect captured emails to the queued free-tool-lead sequence (no auto-send).
5. Define one aggregate benchmark metric per tool to feed the Content Factory.
