# Real Estate Sample Sector Report

## تقرير قطاعي توضيحي — العقارات (B2B / الوساطة والتطوير)

> **SYNTHETIC + AGGREGATED.** This is a sample sector report for the Saudi real-estate sector (brokerage, development sales, and property management). All numbers are synthetic and aggregated for illustration. No real client data is referenced. K-anonymity ≥ 5 is enforced on every slice.
>
> **اصطناعي ومُجمَّع.** تقرير قطاعي توضيحي لقطاع العقارات في المملكة العربية السعودية. كل الأرقام اصطناعية لأغراض التوضيح، ولا تستند إلى أي بيانات عملاء حقيقية.

---

## 1. Saudi real-estate landscape — مشهد قطاع العقارات

The Saudi real-estate sector spans brokerage offices, development sales teams, and property-management operators selling and managing assets for owners and institutional clients. Organizations in this band rely heavily on WhatsApp-led relationships, individual broker networks, and inbound enquiries from listings portals. Records are fragmented across brokers' personal phones, spreadsheets, and partial CRM use.

In the synthetic model, the real-estate band shows the following structural features:

- Median headcount: 22 employees (synthetic).
- Median count of active client/owner relationships per office: 35 (synthetic).
- Share of organizations where opportunity tracking is **declared and documented**: 18% (synthetic).
- Share where opportunity tracking is **informal** (brokers track enquiries individually with no shared record): 82% (synthetic).
- Median age of dormant enquiries that were never re-contacted: 9 months (synthetic).

The informal-tracking figure is the structurally important one. Where opportunity tracking is informal, no Source Passport exists for the enquiry data, no workflow owner is named, no governance decision is recorded before follow-up, and no Proof Pack closes the engagement. A genuine revenue opportunity — a buyer who enquired about a project nine months ago and is now ready — stays invisible.

في المعطيات الاصطناعية، تتابع 82% من المنظمات الفرص بصورة غير رسمية: تتبّع فردي بلا سجل مشترك. هذه هي الفجوة البنيوية الرئيسية — فرص إيراد حقيقية تبقى غير مرئية.

---

## 2. Readiness score distribution — توزيع درجة الجاهزية

Across the synthetic real-estate subpopulation (300 organizations), the readiness score distribution is right-skewed. Most organizations cluster between 30 and 55. A small tail sits above 65.

| Score band | Maturity equivalent | Share of synthetic real-estate |
|------------|---------------------|--------------------------------|
| 0 – 29 | Siloed | 19% |
| 30 – 49 | Structured | 44% |
| 50 – 69 | AI-Assisted | 28% |
| 70 – 84 | Governed | 8% |
| 85 – 100 | Orchestrated | 1% |

Dimension averages for real-estate in the synthetic model:

| Dimension | Average score |
|-----------|---------------|
| Leadership alignment | 53 |
| Workflow clarity | 44 |
| Data readiness | 37 |
| Human capability | 50 |
| Governance maturity | 34 |

The pattern matches the full v1 benchmark, with real-estate scoring slightly lower on data readiness and workflow clarity: enquiry data is dispersed across personal channels, and follow-up workflows are broker-specific rather than shared.

---

## 3. Top five friction patterns — أنماط الاحتكاك الخمسة

The synthetic dataset reveals five recurring friction patterns. Each is anonymized; none describes a real organization.

### 3.1 Enquiry data trapped on personal devices

A broker receives buyer enquiries on a personal WhatsApp number. When the broker is unavailable, travels, or leaves the office, the enquiry history is unreachable. No shared record exists; no source declaration is possible.

- **Frequency in synthetic data**: 73% of real-estate organizations show this pattern.
- **Standards activated by remediation**: [SOURCE_PASSPORT_STANDARD.md](../23_standards/SOURCE_PASSPORT_STANDARD.md) — declare enquiry data ownership and allowed use.

### 3.2 Cold outreach to scraped contact lists

A sales team obtains phone numbers from scraped listing portals or purchased lists, then sends WhatsApp messages referencing the recipient by name. No consent record exists; no opt-in path was offered.

- **Frequency in synthetic data**: 51% of organizations.
- **Standards activated**: [RUNTIME_GOVERNANCE_STANDARD.md](../23_standards/RUNTIME_GOVERNANCE_STANDARD.md) — hard-blocks the channel; scraping is refused at intake.

### 3.3 Guaranteed-return language in pitches

Pitch material to owners and investors contains phrases like "guaranteed occupancy within sixty days" or "assured resale uplift". Claim-safety checks would refuse such language, but no claim-safety check exists in most real-estate sales operations.

- **Frequency in synthetic data**: 42% of pitch material reviewed in the synthetic dataset.
- **Standards activated**: [RUNTIME_GOVERNANCE_STANDARD.md](../23_standards/RUNTIME_GOVERNANCE_STANDARD.md) — `BLOCK` on guarantee language. The governed alternative is "evidenced opportunities" framed against documented enquiry signals.

### 3.4 Buyer PII in shared logs and chat groups

Teams paste full names, national-ID fragments, phone numbers, and budget figures of buyers into office WhatsApp groups, shared spreadsheets, and ticketing tools. The data is retained indefinitely. No retention policy is applied.

- **Frequency in synthetic data**: 66% of organizations.
- **Standards activated**: [SOURCE_PASSPORT_STANDARD.md](../23_standards/SOURCE_PASSPORT_STANDARD.md) — retention policy enforcement; PII redaction in preview fields.

### 3.5 Dormant-enquiry blind spot

A buyer enquired about a project, was not ready, and was never re-contacted. The enquiry sits in a broker's old chat thread. There is no scoring layer to surface "enquired 9 months ago, sector-fit high, now re-engageable" as a prioritized opportunity.

- **Frequency in synthetic data**: 78% of organizations carry a measurable dormant-enquiry backlog.
- **Standards activated**: [DEALIX_GOVERNED_AI_OPERATIONS_STANDARD.md](../23_standards/DEALIX_GOVERNED_AI_OPERATIONS_STANDARD.md) — Stage 2 Workflow Owner artifact; opportunity scoring with evidence attribution.

---

## 4. Recommended next steps — الخطوات التالية الموصى بها

For a real-estate organization assessing itself against this report, the recommended sequence is:

1. **Consolidate your enquiry data into one reviewable export** and assign it a Source Passport. Budget: half a day.
2. **Name a Workflow Owner for the enquiry-to-follow-up workflow** in writing. Budget: one day.
3. **Adopt the seven-decision governance vocabulary on paper** before tooling. Every owner-bound or buyer-bound message gets a one-line decision tag, and outreach drafts stay `DRAFT_ONLY` until a person approves each send. Budget: one team workshop.
4. **Run a governed scan of dormant enquiries** — surface the prioritized re-engageable opportunities with the evidence behind each ranking. Budget: aligns with a 7-day Revenue Intelligence Sprint.
5. **Close your next engagement with a Proof Pack** conforming to the fourteen-section schema. Budget: half a day at engagement close.

After sixty days of consistent execution on these five items, an organization typically moves one maturity level in the framework, in the synthetic model.

بعد ستين يوماً من الالتزام بالخطوات الخمس، تنتقل المنظمة عادةً مستوى نضج واحداً في الإطار وفق النموذج الاصطناعي. لا يُرسل أي تواصل بدون موافقة صريحة من المنظمة.

---

## 5. Methodology — المنهجية

- **Synthetic and aggregated data only.** No real client data contributed to the numbers in this report.
- **Subpopulation**: 300 synthetic real-estate organizations sampled from the v1 benchmark dataset, with parameters disclosed in [SAUDI_AI_OPERATIONS_READINESS_REPORT_v1.md](../41_benchmarks/SAUDI_AI_OPERATIONS_READINESS_REPORT_v1.md) section 8.
- **K-anonymity ≥ 5** on every cell. No slice in this report falls below the threshold.
- **No naming.** No organization is named, characterized, or identifiable.
- **No claims.** Numbers are illustrative of the framework. They are not measurements of any real population, and they are not confidential client metrics.

---

## 6. Limitations — حدود التقرير

- The synthetic model encodes qualitative priors. Real-world distributions may differ in magnitude.
- The real-estate band is broad. Residential brokerage, commercial leasing, off-plan development sales, and property management differ materially; v2 will model subsectors where the synthetic sample supports it.
- The five friction patterns are recurring patterns in the synthetic model, not the only patterns. Sector-specific friction (regulatory exposure under REGA, escrow rules, off-plan sales regulation) is not fully modeled in v1.
- This report does not measure compliance with the Saudi Personal Data Protection Law or sectoral regulation.

---

## 7. Cross-references — مراجع متقاطعة

- [b2b_services_sample.md](./b2b_services_sample.md) — companion sector report.
- [SAUDI_AI_OPERATIONS_READINESS_REPORT_v1.md](../41_benchmarks/SAUDI_AI_OPERATIONS_READINESS_REPORT_v1.md).
- [DEALIX_GOVERNED_AI_OPERATIONS_STANDARD.md](../23_standards/DEALIX_GOVERNED_AI_OPERATIONS_STANDARD.md).
- [SOURCE_PASSPORT_STANDARD.md](../23_standards/SOURCE_PASSPORT_STANDARD.md).
- [RUNTIME_GOVERNANCE_STANDARD.md](../23_standards/RUNTIME_GOVERNANCE_STANDARD.md).
- [PROOF_PACK_STANDARD.md](../23_standards/PROOF_PACK_STANDARD.md).

---

## 8. Disclaimer — إخلاء مسؤولية

This is a sample sector report. The data is synthetic and aggregated; the numbers illustrate the framework rather than measure any real organization or population. Decisions made on the basis of this report should be paired with first-party assessment of the operating context.

هذا تقرير قطاعي توضيحي. البيانات اصطناعية ومُجمَّعة. الأرقام توضّح الإطار ولا تقيس أي جهة أو سوق حقيقي. أي قرار يُبنى عليه يجب أن يُسنَد بتقييم ذاتي مباشر.

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
