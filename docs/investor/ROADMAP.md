# Investor-View Roadmap — خارطة طريق المستثمر

## Purpose
Public-safe roadmap for investor conversations. Mirrors `docs/product/ROADMAP.md` but redacted of client names and sensitive commercial detail. Built around proof gates, not feature wishes.

## Owner
Founder.

## Inputs
- `docs/product/ROADMAP.md`.
- Proof-gate status from `docs/founder/CEO_90_DAY_STRATEGIC_PLAN.md`.
- Productization candidates from `docs/product/PRODUCTIZATION_COMMAND_CENTER.md`.

## Outputs
- This document.
- PDF export quarterly into the data room.

## Roadmap Frame

### Where We Are (Today)
- Proof gate passed: [list].
- Proof gate active: [name + kill criterion].
- Productization candidates by stage: Manual [count] / Template [count] / Automation [count] / SaaS Candidate [count].

### Next 90 Days
- Active proof gate completion.
- Targeted candidate promotions (named only after gate passed).
- Operating-system maturation (`docs/founder/CEO_OPERATING_MODEL.md`).

### Next 6-12 Months
- First SaaS candidate Build/Defer/Kill decision (if any).
- First sector report published quarterly (after T-0 baseline).
- Partner portfolio growth (only after Proof of Delivery passed).

### 12-24 Months (Directional Only)
- Theme: deepening sector authority.
- Theme: productizing the most repeatable workflows.
- Theme: hiring against documented bottlenecks (`docs/people/HIRING_TRIGGERS.md`).

## Rules
1. No client names. No partner names without consent.
2. No specific revenue projections without the disclosure "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة".
3. Themes for 12-24 months are directional, not commitments.
4. Aligned with `docs/product/NO_OVERBUILD_POLICY.md`; no items contradicting it.
5. Updated quarterly; never older than 90 days when shared with an investor.
6. Watermarked when shared externally.

## Metrics
- Public-safe items vs internal-only items (parity tracked).
- Update freshness.
- Items achieved as planned vs revised vs killed (transparent reporting).

## Cadence
- Quarterly refresh.
- Updated on every proof-gate pass.

## Evidence
- `evidence/investor/roadmap/<YYYY-Qn>.md`.

## Verifier
Founder.

## Runtime Command
`make investor-roadmap` — redacts internal roadmap into the public-safe version; refuses publication if any client name remains.

## Arabic Summary — ملخص عربي
خارطة طريق آمنة للمستثمرين، مبنية حول بوابات الإثبات. بدون أسماء عملاء أو شركاء بلا موافقة. الموضوعات 12-24 شهرًا اتجاهات، لا التزامات. القيم التقديرية ليست مُتحقَّقة.
