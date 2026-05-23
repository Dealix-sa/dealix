---
title: Release Policy
owner: Founder (Bassam)
status: active
last_review: 2026-05-23
---

# Release Policy — سياسة الإطلاق

## Purpose
Define what gates a release. A release is any change reaching production — code, prompt, model, template, or content that customers see. The same gates apply.

## Release gates (all must be green)
1. **Tests pass** — unit + integration suite on the critical paths the change touches.
2. **Evals pass** — golden suite ≥95% per [`ENGINEERING_METRICS.md`](ENGINEERING_METRICS.md). Required for any AI-touching change.
3. **No banned claims** — diff scanned against banned-claims list in `docs/content/CONTENT_STRATEGY.md` and `docs/governance/FORBIDDEN_ACTIONS.md`.
4. **PII review** — any change touching customer data passes redaction check per `docs/governance/PII_REDACTION_POLICY.md`.
5. **Approval log entry** — see Approval table below.
6. **Rollback plan** — written, one paragraph, attached to the release entry.

## Approval table

| Change class | Approval | Reference |
|---|---|---|
| Internal tool, no customer surface | Author self-approve | — |
| Customer-facing UI / content | Founder | `docs/governance/APPROVAL_MATRIX.md` |
| AI prompt or model change | Founder + eval pass | `docs/governance/AI_ACTION_CONTROL.md` |
| Pricing, billing, contracts code | Founder, written A2 | `docs/finance/BILLING_POLICY.md` |
| Public claim or case study | Founder + client consent if named | `docs/content/CASE_STUDY_SYSTEM.md` |

## Rules
- No release on Thursday after 4pm KSA without explicit founder override (weekend incident risk).
- Hotfix path exists but still requires gates 1, 3, 4, and a post-hoc gate 2 within 48h.
- Failed releases are recorded in the incident log and feed Change Failure Rate.

## Operations
- Each release gets a one-line entry in `docs/product/release_log.md` (created on first release). Fields: id, date, summary, gates passed, approver, rollback link.
- Failures roll back per the attached rollback plan; incident opened if customer-visible.

## Evidence
- Release log is the audit trail. Linked from `docs/governance/AUDIT_LOG_POLICY.md`.

## Owner & cadence
- Owner: Founder.
- Cadence: per release; weekly log review.

## Cross-links
- [`DORA_METRICS_POLICY.md`](DORA_METRICS_POLICY.md)
- [`ENGINEERING_METRICS.md`](ENGINEERING_METRICS.md)
- [`BUG_TRIAGE.md`](BUG_TRIAGE.md)
- `docs/governance/AUDIT_LOG_POLICY.md`

---

## القسم العربي

**الغرض:** بوابات إلزامية لأي تغيير يصل الإنتاج: كود، prompt، نموذج، قالب، محتوى.

**البوابات:** الاختبارات تمر، تقييمات الذكاء ≥95%، لا ادعاءات ممنوعة، مراجعة PII، تسجيل موافقة، خطة تراجع.

**جدول الموافقات:** أداة داخلية — الكاتب يوافق. واجهة عميل — المؤسس. تغيير prompt — المؤسس + اجتياز التقييم. تسعير/فوترة — موافقة A2 مكتوبة. ادعاء عام — المؤسس + موافقة العميل عند الذكر.

**القواعد:** لا إطلاق خميس بعد 4م بدون تجاوز مكتوب. الإصلاحات السريعة تمر بالبوابات 1-3-4 وتقييم خلال 48 ساعة.

**المالك:** المؤسس. **الإيقاع:** كل إطلاق، مراجعة سجل أسبوعيًا.
