# Growth Metrics — مقاييس النمو

**Status: INTERNAL** — metrics dashboard spec for the growth funnel. Dashboard build is FUTURE; this defines what it must measure.

> Purpose — الغرض: specify the growth metrics dashboard for Dealix, the Saudi-first AI Business Operating System. Funnel metrics, activation, proof reuse, CAC/payback framing, leading vs lagging indicators, and a weekly review cadence. No vanity-only metrics. Cross-link: [SELF_GROWTH_OS.md](./SELF_GROWTH_OS.md), [WEBSITE_FUNNEL_MAP.md](./WEBSITE_FUNNEL_MAP.md), [GROWTH_EXPERIMENTS.md](./GROWTH_EXPERIMENTS.md), [../08_value_os/VALUE_DASHBOARD.md](../08_value_os/VALUE_DASHBOARD.md).

مقاييس النمو تحدد لوحة قياس قمع النمو في Dealix: مقاييس القمع، التفعيل، إعادة استخدام الإثبات، تأطير CAC والاسترداد، المؤشرات القائدة مقابل المتأخرة، وإيقاع المراجعة الأسبوعي. لا مقاييس استعراضية فقط.

---

## Funnel metrics — مقاييس القمع

The core funnel: Traffic → Tool → Diagnostic → Sprint → Retainer. Track the conversion between each pair, not just the totals.

| Stage transition | Metric | Type |
|---|---|---|
| Traffic → Tool | Tool-start rate | Leading |
| Tool → Tool complete | Completion rate | Leading |
| Tool → Diagnostic | Score/tool-to-Diagnostic rate | Leading |
| Diagnostic → Sprint | Diagnostic-to-Sprint rate | Lagging |
| Sprint → Retainer | Retainer conversion rate | Lagging |

Each transition aligns with a page and one CTA in [WEBSITE_FUNNEL_MAP.md](./WEBSITE_FUNNEL_MAP.md).

---

## Activation — التفعيل

Activation is the point a lead receives real value, not just signs up.

- **Tool activation:** lead completes a free tool and views their estimated result.
- **Diagnostic activation:** lead completes the Diagnostic and receives a scoped finding.
- **Sprint activation:** client receives the Proof Pack.

Activation rate is reported per stage; a high capture with low activation flags a value or friction problem.

التفعيل لحظة وصول العميل لقيمة حقيقية، ويُقاس لكل مرحلة.

---

## Proof reuse — إعادة استخدام الإثبات

The compounding loop (L3) deserves its own measurement.

- **Proof Packs delivered** (count, by sector).
- **Case-safe summaries published** (founder-approved).
- **Inbound attributed to proof reuse** (leads citing a case-safe asset).
- **Proof-to-demand ratio:** demand generated per delivered Proof Pack.

This ties growth to [../07_proof_os/PROOF_OS.md](../07_proof_os/PROOF_OS.md) and the value tiers in [../08_value_os/ESTIMATED_OBSERVED_VERIFIED_VALUE.md](../08_value_os/ESTIMATED_OBSERVED_VERIFIED_VALUE.md).

---

## CAC / payback framing — تأطير CAC والاسترداد

- **CAC** = founder time + tool/content cost + partner share, per acquired Sprint client. Framed as estimated until a stable cohort exists.
- **Payback period** = months for a client's revenue (Sprint + retainer) to cover CAC.
- **LTV direction:** retainer continuity, not a single Sprint, drives long-term value.
- All figures are **estimated** early; labeled as such, never presented as verified. No guaranteed-ROI claim.

CAC وقت المؤسس وتكلفة المحتوى وحصة الشريك لكل عميل سبرنت. الاسترداد عدد الأشهر لتغطية CAC. كل الأرقام تقديرية في البداية.

---

## Leading vs lagging — القائدة مقابل المتأخرة

| Leading (act on weekly) | Lagging (review monthly) |
|---|---|
| Posts published, tool starts | Sprints delivered |
| Tool completion rate | Retainer conversions |
| Diagnostic bookings | Revenue (estimated) |
| Nurture draft approvals | CAC / payback |

Leading indicators are controllable now; lagging indicators confirm whether the loops compound.

المؤشرات القائدة قابلة للتحكم الآن، والمتأخرة تؤكد تركيب الحلقات.

---

## What we do NOT track as success — ما لا نعدّه نجاحاً

- Raw impressions, follower counts, or likes in isolation (vanity-only).
- "Leads" without consent or activation.
- Any metric inflated by automation, scraping, or purchased lists.

A vanity number may inform reach but never defines growth health.

لا انطباعات أو متابعون أو إعجابات منفصلة، ولا عملاء بلا موافقة أو تفعيل.

---

## Weekly review cadence — إيقاع المراجعة الأسبوعي

```
1. Read the funnel: each transition rate vs last week.
2. Read activation per stage (capture without activation = fix friction).
3. Read proof reuse (Packs delivered, demand attributed).
4. Score live experiments vs their single metric ([GROWTH_EXPERIMENTS.md]).
5. Decide: promote, iterate, or kill. Record the decision.
```

Monthly: review CAC/payback and lagging indicators. Quarterly: review loop health against [SELF_GROWTH_OS.md](./SELF_GROWTH_OS.md).

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
