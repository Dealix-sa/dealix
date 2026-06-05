# Proof Pack Template — قالب حزمة الإثبات

**Status: BETA**

> Purpose — الغرض: the fourteen-section Proof Pack the client receives at the close of a Command Sprint. Grounded in `auto_client_acquisition/proof_os/` (the canonical 14 sections) with safe wording, evidence tiers, and the disclosure. Cross-link: [COMMAND_SPRINT_DELIVERY_OS.md](./COMMAND_SPRINT_DELIVERY_OS.md), [CUSTOMER_FOLDER_TEMPLATE.md](./CUSTOMER_FOLDER_TEMPLATE.md), [../03_governance/CLAIMS_REGISTER.md](../03_governance/CLAIMS_REGISTER.md), [../07_proof_os/PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md).

حزمة الإثبات المكوَّنة من أربعة عشر قسماً يستلمها العميل عند ختام السبرنت. مُؤسَّسة على الوحدة البرمجية المعتمدة بصياغة آمنة ودرجات دليل والإفصاح. لا إثبات مزيّف، ولا ادعاء بلا دليل.

---

## Evidence tiers — درجات الدليل

Every value statement in the pack carries exactly one tier. The tier governs the wording.

كل عبارة قيمة في الحزمة تحمل درجة واحدة بالضبط، والدرجة تحكم الصياغة.

| Tier — الدرجة | Meaning — المعنى | Required reference — المرجع المطلوب |
|---|---|---|
| `estimated` — تقديرية | a model or analyst estimate, not measured — تقدير لم يُقَس | none, but labeled "estimated" |
| `observed` — مُلاحَظة | observed in the client's data — مُلاحَظة في بيانات العميل | `source_ref` |
| `verified` — مُتحقَّقة | verified against a source of record — مُتحقَّقة من مصدر مرجعي | `source_ref` |
| `client_confirmed` — مؤكَّدة من العميل | confirmed by the client — أكّدها العميل | `confirmation_ref` |

A value item rises from `estimated` only with a source reference, and to `client_confirmed` only with a client confirmation reference. Only `client_confirmed` may be described as realized. Estimated value is never reported as revenue.

ترتفع القيمة من "تقديرية" بمرجع مصدر فقط، وإلى "مؤكَّدة من العميل" بمرجع تأكيد فقط. وحدها المؤكَّدة تُوصَف كمُتحقَّقة، والقيمة التقديرية لا تُعرَض كإيراد.

---

## The fourteen sections — الأقسام الأربعة عشر

Order and names match the canonical backend sections. None may be left empty at handover.

الترتيب والأسماء مطابقة للأقسام المعتمدة. لا يُترَك أي قسم فارغاً عند التسليم.

1. **Executive summary — الموجز التنفيذي.** What was done and what it means, in plain executive language. Facts only.
2. **Problem — المشكلة.** The focus workflow and the business problem behind it.
3. **Inputs — المدخلات.** The data and context provided, each tied to its source passport.
4. **Source passports — جوازات المصادر.** `source_type`, `owner`, `allowed_use`, `contains_pii`. Never `scraped`.
5. **Work completed — العمل المُنجَز.** Each work item with its source reference.
6. **Outputs — المخرجات.** The Revenue Map, Executive Command Brief, Next Action Board, and drafts.
7. **Quality scores — درجات الجودة.** DQ baseline and proof score, with method named.
8. **Governance decisions — قرارات الحوكمة.** Approvals, claim checks, and any draft routed for review.
9. **Blocked / risks — المحجوب والمخاطر.** What was blocked and why — data gaps, missing lawful basis, unsafe claims caught.
10. **Value metrics — مقاييس القيمة.** Each value item with its tier and reference. Estimated stays labeled estimated.
11. **Limitations — القيود.** Honest scope limits, sample sizes, and what was *not* measured.
12. **Recommended next step — الخطوة التالية الموصى بها.** Framed as evidenced opportunities, not guarantees.
13. **Retainer / expansion path — مسار الاستمرار والتوسّع.** Where a retainer or deeper module would add value, with the evidence behind it.
14. **Capital assets created — الأصول المعرفية المُنشأة.** Reusable artifacts produced (maps, registers, templates) that remain with the engagement.

---

## Safe wording rules — قواعد الصياغة الآمنة

- No guaranteed revenue, no guaranteed ROI, no guaranteed sales. Use "evidenced opportunities." — لا ضمان إيراد أو عائد أو مبيعات؛ استخدم "فرص مُثبتة بأدلة".
- No fake proof, no invented testimonials, no fabricated figures. — لا إثبات مزيّف ولا شهادات مُختلقة ولا أرقام مُلفَّقة.
- No public case study without customer approval. — لا دراسة حالة عامة دون اعتماد العميل.
- No PII anywhere in the pack. — لا بيانات شخصية في أي موضع.
- Aggregated patterns and methodology only — no confidential third-party metrics. — أنماط مُجمَّعة ومنهجية فقط.

### Forbidden → safe rewrite — المحظور ← البديل الآمن

| Forbidden — محظور | Safe — آمن |
|---|---|
| "We guarantee X SAR in sales" / "نضمن لك مبيعات بقيمة كذا" | "Estimated opportunity of X SAR (tier: estimated)" / "فرصة تقديرية بقيمة كذا (درجة: تقديرية)" |
| "Proven ROI" / "عائد مُثبت" | "Observed value where evidenced" / "قيمة مُلاحَظة حيث توفّر الدليل" |
| "Verified results" (no source) | "Estimated, pending verification" / "تقديرية بانتظار التحقّق" |

---

## Handover check — فحص التسليم

Before handover: all 14 sections complete, every value item tier-tagged, every claim checked against [../03_governance/CLAIMS_REGISTER.md](../03_governance/CLAIMS_REGISTER.md), no PII present, disclosure line at the end.

قبل التسليم: اكتمال الأقسام الأربعة عشر، وسم كل قيمة بدرجتها، فحص كل ادعاء مقابل السجل، خلوّها من البيانات الشخصية، وحضور سطر الإفصاح.

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
