# Saudi Real Estate Offices — Governed AI Operations Sector Report 2026

## تقرير قطاعي — مكاتب العقار في السعودية: عمليات الذكاء الاصطناعي المُحوكَمة 2026

> **SYNTHETIC + AGGREGATED.** This report models Saudi commercial and residential real estate offices (brokerage, leasing, and property management firms selling to businesses and developers). All numbers are synthetic, drawn from sector-typical operating patterns and disclosed public sources, and aggregated with K-anonymity ≥ 5. No real client data is referenced. No organization is named or identifiable. This report does not measure compliance with the Saudi Personal Data Protection Law (PDPL) or sectoral regulation.
>
> **اصطناعي ومُجمَّع.** يصف هذا التقرير مكاتب العقار التجاري والسكني في السعودية. كل الأرقام اصطناعية، مبنية على أنماط تشغيل نمطية ومصادر عامة مُعلَنة، ومُجمَّعة بعتبة إخفاء هوية K ≥ 5. لا يستند إلى بيانات عملاء حقيقيين، ولا يُسمّي أي جهة.
>
> Cross-link: [b2b_services_sample.md](./b2b_services_sample.md), [SAUDI_AI_OPERATIONS_READINESS_REPORT_v1.md](../41_benchmarks/SAUDI_AI_OPERATIONS_READINESS_REPORT_v1.md), [DEALIX_GOVERNED_AI_OPERATIONS_STANDARD.md](../23_standards/DEALIX_GOVERNED_AI_OPERATIONS_STANDARD.md).

---

## 1. Why this sector — لماذا هذا القطاع

Saudi real estate offices sit at a structural pressure point in 2026. Vision 2030 housing programs, the maturing of off-plan sales regulation, and rising institutional demand for commercial space have all increased the volume of inbound business inquiries reaching a typical office. At the same time, the office's operating model has not changed: a small team of brokers, a shared inbox, a spreadsheet of leads, and an owner who personally decides which inquiries get a same-day response.

The result is a volume-versus-method gap. The number of inquiries has grown; the method for triaging them has not. This report describes that gap with synthetic, aggregated data, and sets out what a governed operating layer changes — without claiming a revenue outcome for any office.

في 2026، يقف مكتب العقار السعودي عند نقطة ضغط: حجم الاستفسارات الواردة ارتفع بفعل برامج الإسكان وتنظيم البيع على الخارطة والطلب المؤسسي، بينما بقي أسلوب الفرز كما هو — صندوق وارد مشترك، وجدول بيانات، وقرار فردي من المالك. هذا التقرير يصف تلك الفجوة بأرقام اصطناعية مُجمَّعة.

---

## 2. The synthetic sector profile — الملف الاصطناعي للقطاع

In the synthetic model, the Saudi real estate office band shows the following structural features (300 synthetic organizations sampled):

- Median headcount: 9 employees (synthetic).
- Median active mandates (listings + leasing + management contracts): 34 (synthetic).
- Median monthly inbound inquiries across all channels: 210 (synthetic).
- Share of inquiries arriving via WhatsApp: 61% (synthetic).
- Share of inquiries arriving via web form or portal: 24% (synthetic).
- Share arriving via phone or walk-in: 15% (synthetic).
- Median time-to-first-response during business hours: 4.5 hours (synthetic).
- Share of organizations where inbound is triaged by a **documented rule**: 12% (synthetic).
- Share where triage is **a single person's judgment, undocumented**: 88% (synthetic).

The 88% figure is the structurally important one. Where triage is undocumented, the office cannot answer three questions that a governed operation answers by default: *which inquiry was prioritized and why*, *which inquiry was dropped and why*, and *what happens to inbound on the day the triage person is unavailable*.

في النموذج الاصطناعي، 88% من المكاتب تعتمد على حُكم شخص واحد غير موثَّق لفرز الوارد. هذه هي الفجوة البنيوية: المكتب لا يستطيع أن يُجيب لماذا رُتِّب استفسار، ولماذا أُسقِط آخر، وماذا يحدث للوارد يوم غياب الشخص المسؤول.

---

## 3. Readiness score distribution — توزيع درجة الجاهزية

Across the synthetic real estate office subpopulation, the readiness score (mean of five dimensions, each 0–100) is right-skewed and clusters lower than the broader B2B services band.

| Score band | Maturity equivalent | Share of synthetic real estate offices |
|------------|---------------------|------------------------------------------|
| 0 – 29 | Siloed | 22% |
| 30 – 49 | Structured | 44% |
| 50 – 69 | AI-Assisted | 27% |
| 70 – 84 | Governed | 6% |
| 85 – 100 | Orchestrated | 1% |

Dimension averages for real estate offices in the synthetic model:

| Dimension | Average score | Reading |
|-----------|---------------|---------|
| Leadership alignment | 58 | The office owner is usually engaged — decisions are centralized. |
| Workflow clarity | 44 | The inbound triage workflow exists in practice but rarely on paper. |
| Data readiness | 39 | Lead records are scattered across WhatsApp, spreadsheets, and portals. |
| Human capability | 47 | Brokers can operate an output, but no one owns the data layer. |
| Governance maturity | 33 | Few offices have an approval workflow, audit trail, or retention policy. |

The pattern matches the v1 benchmark: governance is the weakest link, data is the second weakest. The notable sector-specific signal is **data readiness at 39** — lower than the B2B services average — because real estate lead data is spread across more channels than most sectors.

النمط مطابق للقياس العام: الحوكمة هي الأضعف، والبيانات الثانية. الإشارة الخاصة بالقطاع أن جاهزية البيانات منخفضة (39) لأن بيانات العملاء موزَّعة على قنوات أكثر من غيرها.

---

## 4. Five friction patterns — أنماط الاحتكاك الخمسة

Each pattern below is recurring in the synthetic dataset. None describes a real organization. Each is paired with the governed standard that addresses it.

### 4.1 Multi-channel lead fragmentation — تشتّت العميل عبر القنوات

The same prospective tenant appears as a WhatsApp contact, a portal lead, and a spreadsheet row — three records, no link between them. A broker calls back an inquiry the office already answered yesterday on another channel.

- **Frequency in synthetic data:** 73% of real estate offices show this pattern at least weekly.
- **Standard activated:** [SOURCE_PASSPORT_STANDARD.md](../23_standards/SOURCE_PASSPORT_STANDARD.md) — every lead source declared, deduplication applied at intake.

### 4.2 Undocumented triage — فرز غير موثَّق

Inbound inquiries are prioritized by one person's instinct. When that person is on leave, inquiries queue without triage, and high-intent inquiries are answered after low-intent ones. There is no record of why one inquiry led.

- **Frequency in synthetic data:** 88% of offices.
- **Standard activated:** [DEALIX_GOVERNED_AI_OPERATIONS_STANDARD.md](../23_standards/DEALIX_GOVERNED_AI_OPERATIONS_STANDARD.md) — Stage 2 Workflow Owner artifact; explainable scoring replaces instinct.

### 4.3 Cold outreach on scraped numbers — تواصل بارد على أرقام مكشوطة

A growth-minded office sends WhatsApp messages to phone numbers collected from public listing portals or scraped directories. No consent record exists; no opt-in path was offered. This pattern is a direct PDPL exposure and a hard-blocked behavior in a governed operation.

- **Frequency in synthetic data:** 51% of offices.
- **Standard activated:** [RUNTIME_GOVERNANCE_STANDARD.md](../23_standards/RUNTIME_GOVERNANCE_STANDARD.md) — `BLOCK` on the channel. A governed operation refuses scraping and cold messaging entirely; it works only first-party, consented data.

### 4.4 Guarantee language in proposals — لغة الضمان في العروض

Listing pitches and leasing proposals contain phrases like "we will lease this unit within thirty days" or "guaranteed sale price". These claims would be refused by a claim-safety check, but most offices have no such check.

- **Frequency in synthetic data:** 41% of proposals reviewed in the synthetic dataset.
- **Standard activated:** [RUNTIME_GOVERNANCE_STANDARD.md](../23_standards/RUNTIME_GOVERNANCE_STANDARD.md) — `BLOCK` on guarantee language; replaced with evidenced, estimate-marked statements.

### 4.5 PII in shared logs — بيانات شخصية في سجلات مشتركة

Client names, phone numbers, and budget figures are pasted into shared WhatsApp groups, broker spreadsheets, and unmanaged chat tools. No retention policy applies; the data outlives the mandate.

- **Frequency in synthetic data:** 66% of offices.
- **Standard activated:** [SOURCE_PASSPORT_STANDARD.md](../23_standards/SOURCE_PASSPORT_STANDARD.md) — retention window enforcement; `REDACT` on over-exposed previews.

---

## 5. What a governed operating layer changes — ما الذي تغيّره طبقة التشغيل المُحوكَمة

A governed layer does not promise more deals. It changes four things, each measurable inside the operation itself (Tier 1 and Tier 2 value, in the Value Ledger):

1. **One lead record per person.** Multi-channel fragmentation collapses into a single deduplicated record with a Source Passport. The broker stops calling back an inquiry already answered.
2. **Triage becomes a rule, not an instinct.** Inquiries are ranked by explainable features — channel, recency, mandate fit, declared budget band. The ranking survives the triage person's absence.
3. **Every external message passes a decision gate.** Drafts are produced bilingually and held `DRAFT_ONLY` until a named human approves. Guarantee language is blocked. Dealix does not send any message on the office's behalf — the broker approves and sends.
4. **The operation becomes auditable.** A decisions log records what was prioritized, what was refused, and why. When a developer-partner, a regulator, or an owner asks, the answer is a file, not a memory.

طبقة التشغيل المُحوكَمة لا تَعِد بصفقات أكثر. تُغيّر أربعة أشياء قابلة للقياس داخل العملية: سجل عميل واحد، فرز بقاعدة لا بحدس، بوابة قرار على كل رسالة خارجية، وعملية قابلة للتدقيق.

---

## 6. Recommended next steps — الخطوات التالية الموصى بها

For a real estate office assessing itself against this report, the recommended sequence — none of it requiring a Dealix engagement:

1. **List every channel inbound arrives on** (WhatsApp, portals, web form, phone) and assign each a Source Passport. Budget: half a day.
2. **Name one Workflow Owner for inbound triage** in writing. Budget: one hour.
3. **Write your triage rule down** — even a four-line rule beats instinct, because it survives an absence. Budget: one team conversation.
4. **Adopt the seven-decision vocabulary on paper** before any tooling: every external-bound message gets a one-line decision tag (ALLOW / DRAFT_ONLY / REQUIRE_APPROVAL / REDACT / BLOCK / RATE_LIMIT / REROUTE). Budget: one workshop.
5. **Apply a retention window** to your lead data and remove records past it. Budget: half a day.

After sixty days of consistent execution on these five items, an organization typically moves one maturity level in the framework, in the synthetic model.

بعد ستين يوماً من الالتزام بالخطوات الخمس، تنتقل المنشأة عادةً مستوى نضج واحداً وفق النموذج الاصطناعي.

---

## 7. How to read your own score — كيف تقرأ درجتك أنت

This report describes a synthetic population. Your office is not in it. To know where you actually stand, the honest path is a first-party assessment of your own operating context.

Dealix offers a Free Diagnostic delivered within 24 hours: a score per readiness dimension and a plain-language read on where your office stands, before you spend a riyal on any tool. The diagnostic carries no commitment. If a paid engagement follows, it is fixed-price and fixed-scope — a 499 SAR Revenue Intelligence Sprint, not an open-ended retainer pitch.

تشخيص ديليكس المجاني يُسلَّم خلال 24 ساعة: درجة لكل بُعد، ورأي صريح عن موقع مكتبك، بلا التزام بعده.

---

## 8. Methodology — المنهجية

- **Synthetic and aggregated data only.** No real client data contributed to the numbers in this report.
- **Subpopulation:** 300 synthetic real estate office organizations sampled from the v1 benchmark dataset, with parameters disclosed in [SAUDI_AI_OPERATIONS_READINESS_REPORT_v1.md](../41_benchmarks/SAUDI_AI_OPERATIONS_READINESS_REPORT_v1.md).
- **Public sources:** disclosed government statistical releases (Saudi GASTAT, Real Estate General Authority publications, Vision 2030 housing program progress reports). No scraping. No customer data.
- **K-anonymity ≥ 5** on every cell. Any slice that would represent fewer than five underlying records is suppressed.
- **No naming.** No organization is named, characterized, or identifiable.
- **No claims.** Numbers illustrate the framework. They are not measurements of any real population, and they are not forecasts.

---

## 9. Limitations — حدود التقرير

- The synthetic model encodes qualitative priors. Real-world distributions may differ in magnitude.
- "Real estate offices" is a broad band. A high-end commercial brokerage differs materially from a residential leasing office; v2 will model subsegments where the synthetic sample supports it.
- The five friction patterns are recurring patterns in the synthetic model, not the only patterns. Regulation-specific friction (off-plan sales rules, escrow handling) is not fully modeled in v1.
- This report does not measure PDPL compliance or any sectoral regulatory standing. It is an operating-readiness model, not a legal assessment.

---

## 10. Disclaimer — إخلاء مسؤولية

This is a synthetic, aggregated sector report. The numbers illustrate the Dealix governed-operations framework; they do not measure any real organization or market. Any decision made on the basis of this report should be paired with a first-party assessment of the operating context.

هذا تقرير قطاعي اصطناعي ومُجمَّع. الأرقام توضّح إطار العمل ولا تقيس أي جهة أو سوق حقيقي. أي قرار يُبنى عليه يجب أن يُسنَد بتقييم ذاتي مباشر.

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
