# Delegation Rules — قواعد التفويض

## Purpose
The explicit, named list of decisions and actions the founder must not delegate. Pre-Series A, the founder is the company's brain on certain matters; delegating these erodes the company's signal. Visible at the top of `docs/people/DELEGATION_COMMAND_CENTER.md`.

## Owner
Founder. List modified only by founder.

## Inputs
- Stage of company.
- Lessons from prior delegation incidents.
- Investor and regulator expectations.

## Outputs
- This list.
- Daily visibility on delegation dashboard.

## The Non-Delegable List
1. **Strategic direction** — what Dealix is and is not, choosing proof gates, killing or pursuing a market.
2. **Product Build/Defer/Kill decisions** — the final call on `docs/product/BUILD_DEFER_KILL.md`.
3. **Hiring decisions** — final yes / no on every hire, including contractors.
4. **Pricing and commercial terms** — list pricing changes, discounts, custom terms.
5. **A3 root-cause actions** — naming the cause and committing to the countermeasure.
6. **Client retention conversations (At-Risk)** — `docs/client_success/RETENTION_PLAYBOOK.md`.
7. **Renewal conversations for Strategic-tier clients**.
8. **Public statements representing Dealix** — content the founder doesn't sign cannot be published in Dealix's name.
9. **Founder voice on owned channels** — drafts allowed, voice not.
10. **Investor and board communications** — once those exist.
11. **Regulator-facing positions** — PDPL, SDAIA, tax authority correspondence.
12. **Legal positions** — what we will sign, what we will refuse.
13. **Case study approvals and consent** — Dealix's signature on client publication.
14. **Productization stage promotions** — the formal gate decision.
15. **Banned-practice exceptions** — there are no exceptions; this is named to prevent drift.

## Rules
1. The list is read aloud (literally) by the founder at quarterly review; no item drops silently.
2. Adding an item requires written rationale.
3. Removing an item requires the founder to write a one-page rationale and date.
4. Any delegate who is asked to make a non-delegable decision escalates immediately; no implicit re-delegation.
5. The disclosure "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة" applies to any estimated time-cost of non-delegation.
6. Non-delegation does not mean non-listening; founder consults broadly, decides personally.

## Metrics
- Delegate escalations on non-delegable items (target: small but non-zero; signals discipline).
- Founder hours on non-delegable decisions (tracked; not optimized down).
- Delegation incidents (target 0).

## Cadence
- Daily visible.
- Quarterly read-aloud review.

## Evidence
- `evidence/delegation/non-delegable/<YYYY-Qn>_review.md` per quarter.

## Verifier
Founder.

## Runtime Command
`make delegation-rules` — prints this list at the top of every delegation review.

## Arabic Summary — ملخص عربي
قائمة صريحة لما لا يُفوَّض: الاتجاه الاستراتيجي، قرارات بناء الميزات، التوظيف، التسعير، أسباب الجذور، احتفاظ العملاء في خطر، صوت المؤسس، تواصل المستثمرين، الحكومة، القانون. لا استثناءات. القيم التقديرية ليست مُتحقَّقة.
