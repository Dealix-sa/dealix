# Deal Desk System — نظام مكتب الصفقات

**Purpose / الغرض**
Approval flow for non-standard deals — anything outside the published scope, price, or payment terms. Captures who decides, by when, and with what evidence.
مسار اعتماد للصفقات غير القياسية — أي شيء خارج النطاق أو السعر أو شروط الدفع المنشورة. يحدّد من يقرر، متى، وبأي أدلة.

**Owner placeholder:** Deal Desk lead = `<founder>` until volume justifies a dedicated owner.
**Cadence:** Async by default; sync escalation if SLA breached. / غير متزامن افتراضيًا؛ تصعيد متزامن عند خرق الـ SLA.
**KPIs:** (1) median time from request to decision, (2) % of non-standard deals approved without scope expansion, (3) count of post-signature scope creep events.
**Risk if missing / مخاطر الغياب:** Discounts get given to the loudest buyer. Scope creeps without revenue. Pricing integrity erodes. / الخصومات تذهب لأعلى صوت. النطاق يتسرّب بلا إيراد. سلامة التسعير تتآكل.

---

## EN summary

The Deal Desk is the single channel for any deal element that deviates from the published norm. It approves or declines four categories of deviation: discount, custom scope, payment terms, and enterprise terms. Each category has a threshold, a role-based approver, and a service level. No exception ships without a written rationale stored alongside the proposal.

## ملخص بالعربية

مكتب الصفقات هو القناة الوحيدة لأي عنصر صفقة يخرج عن المنشور. يعتمد أو يرفض أربع فئات انحراف: الخصم، النطاق المخصص، شروط الدفع، شروط المؤسسات. لكل فئة عتبة، معتمِد، ومستوى خدمة. لا استثناء يمرّ دون مبرر مكتوب يُحفظ مع المقترح.

---

## الفئات الأربعة / Four categories

| # | Deviation type | Examples | Default approver |
|---|---|---|---|
| 1 | Discount | أي خصم على السعر المنشور. Any discount off list. | Founder if > 10%; Sales lead if ≤ 10%. |
| 2 | Custom scope | بند خارج Scope الموحَّد. Item outside standard scope. | Founder + Delivery Coordinator (joint). |
| 3 | Payment terms | شروط أبطأ من Net-15 أو مخالفة لـ`docs/revenue/INVOICE_FLOW.md`. Slower than Net-15 or off-policy. | Founder + finance advisor (review). |
| 4 | Enterprise terms | بنود MSA، شروط أمان مخصصة، حصرية، شروط إنهاء. MSA, custom security, exclusivity, termination clauses. | Founder (mandatory). |

---

## عتبات وحدود / Thresholds

> الأرقام أدناه placeholders. تُملأ مع `docs/company/PRICING_DECISION.md` و `docs/company/PRICE_INCREASE_RULES.md`. / Placeholders. To be populated jointly with PRICING_DECISION.md and PRICE_INCREASE_RULES.md.

| Discount band | Approver | SLA |
|---|---|---|
| 0% | None (standard) | n/a |
| 1–10% | Sales lead (or founder if no dedicated sales lead) | < 24 hours |
| 11–20% | Founder | < 48 hours |
| > 20% | Founder + written narrative + linked decision | < 72 hours |
| > 30% | Default: decline. Reopen only with board-level rationale. | n/a |

| Payment term | Approver | Conditions |
|---|---|---|
| Net-15 (standard) | None | Default per `docs/revenue/INVOICE_FLOW.md`. |
| Net-30 | Founder | Only if customer is a verified entity with prior delivery. |
| Net-45+ | Founder + finance advisor | Requires written cash-flow note. |
| Milestone-based | Founder + Delivery Coordinator | Requires acceptance criteria per milestone. |

| Custom scope | Approver | Required artifact |
|---|---|---|
| Inside published service ±10% effort | Sales lead | Proposal addendum. |
| ±10–25% effort | Founder + Delivery Coordinator | Re-priced proposal + scope diff. |
| > 25% effort | Founder | New SOW, not an addendum. |

---

## السلسلة الافتراضية للأدوار / Default role chain

```
Account owner → Deal Desk intake → Approver(s) → Decision logged → Proposal updated
        (any team)        (founder by default)   (per category)   (written)        (template re-saved)
```

- **Account owner** ينشئ طلب Deal Desk.
- **Deal Desk intake** يتحقق من اكتمال الحقول قبل العرض على المعتمد.
- **Approver(s)** يعتمد أو يرفض ضمن الـ SLA.
- **Decision logged** يُكتب القرار + المبرر في سجل قابل للتدقيق.
- **Proposal updated** يُحدَّث المقترح وفق `docs/29_sales_os/PROPOSAL_OS.md`.

---

## نموذج طلب Deal Desk / Deal Desk request schema

```yaml
request_id: DD-YYYYMMDD-NN
opened_by: <role>
account_label: <opaque account label>          # no PII
deal_size_sar: <number>
deviation_category: discount | scope | payment | enterprise
deviation_size:
  discount_pct: <number or null>
  scope_delta_pct: <number or null>
  payment_term: <Net-XX or milestone>
  enterprise_clauses: [<short tag>, ...]
rationale: |
  <one paragraph; must reference a customer-side reality, not just "to close the deal">
risk_if_approved: |
  <one paragraph; capacity, margin, precedent, governance>
risk_if_declined: |
  <one paragraph; revenue, relationship, sector signal>
proposed_compensating_control: |
  <e.g., shorter payment term in exchange for the scope add>
attachments:
  - proposal_path
  - any prior comparable deal id
sla_target_hours: <derived from category>
approver_chain: [<role>, ...]
status: open | approved | declined | conditional
decision_rationale: <filled by approver>
closed_at: <date>
```

---

## قواعد لا تُكسر / Non-negotiables

### AR

- لا اعتماد على خصم > 30% بدون مبرر مستوى مجلس مكتوب.
- لا قبول بنود حصرية تمنع البيع في القطاع لمدة > 12 شهرًا.
- لا قبول شرط ضمان إيرادات أو نتائج مبيعات بأي صياغة.
- لا تعديل خلفي بعد التوقيع. أي تغيير يصبح Deal Desk جديد.
- لا تجاوز SLA دون تصعيد مكتوب وسبب.

### EN

- No > 30% discount without a written board-level rationale.
- No exclusivity that blocks sector sales for more than 12 months.
- No revenue or sales-outcome guarantee in any wording.
- No silent post-signature edits. Any change becomes a new Deal Desk request.
- No SLA breach without a written escalation and reason.

---

## التصعيد / Escalation

- **SLA breach by 24h** → الباحث في الصفقة يفتح صفحة قرار في `docs/founder/FOUNDER_LEVERAGE_DASHBOARD.md`.
- **SLA breach by 72h** → يُسجَّل تلقائيًا كإشارة عنق زجاجة في `docs/people/FOUNDER_BOTTLENECK_REMOVAL.md`.
- **انحراف غير مغطّى بأي فئة** → القرار افتراضيًا «لا» حتى يُكتب القرار من المؤسس.

---

## ربط مع الأنظمة الأخرى / Ties

- التسعير القياسي: `docs/company/PRICING_DECISION.md`
- مقترحات: `docs/29_sales_os/PROPOSAL_OS.md`
- شروط دفع: `docs/revenue/INVOICE_FLOW.md`
- استثناءات حوكمة: `docs/governance/APPROVAL_MATRIX.md`
- ملخص يومي: `docs/ops/FOUNDER_DAILY_ANCHOR_AR.md`

---

## Disclosure / إفصاح

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
Any number in this doc — discount band, SLA, threshold — is a placeholder until set by the founder in `docs/company/PRICING_DECISION.md`.

## Related canonical docs

- `docs/29_sales_os/PROPOSAL_OS.md`
- `docs/company/PRICING_DECISION.md`
- `docs/company/PRICE_INCREASE_RULES.md`
- `docs/revenue/INVOICE_FLOW.md`
- `docs/governance/APPROVAL_MATRIX.md`
- `docs/29_sales_os/PROPOSAL_EXCLUSIONS.md`
