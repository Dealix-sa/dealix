# Customer Folder Template — قالب مجلد العميل

**Status: BETA**

> Purpose — الغرض: the standard folder structure and contents for every Command Sprint engagement. One folder per customer, grounded in the canonical backend modules under `auto_client_acquisition/` — `data_os`, `proof_os`, `value_os`, `governance_os`. Cross-link: [COMMAND_SPRINT_DELIVERY_OS.md](./COMMAND_SPRINT_DELIVERY_OS.md), [PROOF_PACK_TEMPLATE.md](./PROOF_PACK_TEMPLATE.md), [../03_governance/HUMAN_APPROVAL_POLICY.md](../03_governance/HUMAN_APPROVAL_POLICY.md).

بنية مجلد قياسية وموحَّدة لكل تكليف سبرنت قيادة. مجلد واحد لكل عميل، مُؤسَّس على الوحدات البرمجية المعتمدة في الخلفية. ما يخرج للعميل ينتهي بسطر الإفصاح، ولا بيانات شخصية في أي مادة عامة.

---

## Folder layout — بنية المجلد

```
engagements/<engagement_id>/
  00_passport/
  01_data_quality/
  02_scoring/
  03_drafts/
  04_proof_pack/
  05_approvals/
  06_value_ledger/
  07_handover/
```

Each subfolder maps to a backend module and a delivery stage. Nothing is stored that the source passport does not permit.

كل مجلد فرعي يقابل وحدة برمجية ومرحلة تسليم. لا يُخزَّن ما لا يسمح به جواز المصدر.

---

## 00_passport — جواز المصدر

Backed by `data_os.source_passport`. The sovereignty gate before any AI use.

- `source_id`, `source_type` (`client_upload` / `crm_export` / `manual_entry` — never `scraped`).
- `owner`, `allowed_use`, `contains_pii`, `sensitivity`, `retention_policy`.
- `ai_access_allowed`, `external_use_allowed`.

If the passport does not allow AI use, the data is not processed. PII flagged for external use requires an approval workflow.

إذا لم يسمح الجواز باستخدام الذكاء، لا تُعالَج البيانات. البيانات الشخصية للاستخدام الخارجي تتطلب مسار اعتماد.

## 01_data_quality — جودة البيانات (DQ)

Backed by `data_os.data_quality_score`, `data_os.import_preview`, `data_os.pii_detection`.

- DQ baseline across the standard dimensions.
- Import preview (non-destructive sample read).
- PII classification result and redaction notes.

## 02_scoring — التقييم

Backed by `data_os.validation_rules`, `data_os.dedupe`, `data_os.normalization`.

- Validation results, deduplication report, normalization notes.
- Opportunity scoring inputs for the Revenue Map.

## 03_drafts — المسودات

- Approval-ready drafts only. Never sent automatically.
- Each draft pre-checked for forbidden patterns (no cold WhatsApp automation, no bulk outreach, no scraped data) and safe claim wording before it enters this folder.
- A draft moves to "sent" only after a recorded approval in `05_approvals/`.

المسودات جاهزة للاعتماد فقط ولا تُرسَل تلقائياً، ومفحوصة مسبقاً من الأنماط المحظورة.

## 04_proof_pack — حزمة الإثبات

Backed by `proof_os.proof_pack` (14 canonical sections) and `proof_os.proof_score`.

- The full Proof Pack per [PROOF_PACK_TEMPLATE.md](./PROOF_PACK_TEMPLATE.md).
- Proof score and evidence tiers per item.
- Ends with the disclosure line.

## 05_approvals — الاعتمادات

Backed by `governance_os` (approval matrix, claim safety, draft gate).

- One entry per approval: item, class (external action / claim / send / data use), evidence tier, decision, timestamp, actor.
- Audit trail: every external action maps to a prior approval. No exception is silent.

سجل اعتماد لكل عنصر: العنصر وفئته ودرجة الدليل والقرار والوقت والفاعل. كل إجراء خارجي يقابله اعتماد سابق.

## 06_value_ledger — سجل القيمة

Backed by `value_os.value_ledger`.

- One event per value item: `kind`, `amount`, `tier` (estimated / observed / verified / client_confirmed), `source_ref`, `confirmation_ref`.
- A value item rises from `estimated` only with a `source_ref`, and to `client_confirmed` only with a `confirmation_ref`. Tier discipline is enforced, not optional.

## 07_handover — التسليم

- Final Proof Pack, Executive Command Brief, Next Action Board, Upsell Recommendation.
- Customer approval record for any public reference. No public case study without customer approval.
- Closing note with the disclosure line.

---

## Rules across the folder — قواعد عابرة للمجلد

- No PII in any artifact intended to leave the engagement folder. — لا بيانات شخصية في أي مادة تغادر المجلد.
- No claim without evidence or safe wording. — لا ادعاء بلا دليل أو صياغة آمنة.
- No external action without a logged approval. — لا إجراء خارجي بلا اعتماد مُسجَّل.
- Retention follows the passport's `retention_policy`. — الاحتفاظ يتبع سياسة الجواز.

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
