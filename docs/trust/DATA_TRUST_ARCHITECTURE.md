# Dealix Data Trust Architecture

## Source Passport (مفهوم)

كل مصدر بيانات له **«جواز»** يحدد المالك، الاستخدام المسموح، الحساسية، والاحتفاظ.

```json
{
  "source_id": "SRC-001",
  "source_type": "client_upload",
  "owner": "client",
  "allowed_use": ["internal_analysis", "draft_only"],
  "contains_pii": true,
  "sensitivity": "medium",
  "relationship_status": "existing_relationship",
  "retention_policy": "project_duration",
  "ai_access_allowed": true,
  "external_use_allowed": false
}
```

## Why it matters (السعودية)

منظومة البيانات والذكاء الاصطناعي في المملكة تتطور بسرعة؛ تعزيز **حوكمة البيانات والخصوصية** أولوية وطنية — مرجعان للسياق المؤسسي: [SDAIA](https://www.sdaia.gov.sa/en) · [المركز الوطني لإدارة البيانات NDMO](https://ndmo.gov.sa). تصميم **data trust architecture** يقلل مخاطر الامتثال ويزيد جاهزية الصفقات الكبيرة.

**الكود:** `auto_client_acquisition/trust_os/source_passport.py`

**صعود:** [`ENTERPRISE_TRUST_PACK.md`](ENTERPRISE_TRUST_PACK.md)

---

## Document Standard Compliance

## Purpose
Defines this operating document's role inside Dealix Company OS.

## Owner
Sami (Founder). Reassign to the responsible operator when one is named.

## Review Cadence
Weekly until stable, then monthly.

## Inputs
- Relevant company data and signals.
- Founder decisions and customer evidence.

## Outputs
- Operating guidance, decisions, or templates produced by this document.
- Evidence captured for verification.

## Rules
- Must support revenue, delivery, trust, learning, or founder leverage.
- Must not introduce unsupported claims.
- Must preserve public/private boundaries.

## Metrics
- Completion status of the actions this document drives.
- Impact on revenue, delivery, trust, or founder leverage.

## Evidence
- Linked workflow, file, test output, customer interaction, or decision log.

## Last Reviewed
2026-05-23
