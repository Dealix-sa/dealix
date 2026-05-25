---
title: Productization Command Center
owner: Founder (Bassam)
status: active
last_review: 2026-05-23
---

# Productization Command Center — مركز قيادة المُنتجة

## Purpose
Single index for how Dealix turns repeated manual delivery into templates, automation, and eventually SaaS. No feature ships without evidence of repeat demand and proven manual success.

## Rules
- No feature is built on opinion. Each requires three signals: paying customer demand, repeated manual delivery, measurable post-build outcome.
- Every decision logged in [`BUILD_DEFER_KILL.md`](BUILD_DEFER_KILL.md).
- Productization ladder is enforced — see [`PRODUCTIZATION_ENGINE.md`](PRODUCTIZATION_ENGINE.md).
- Banned scope listed in [`NO_OVERBUILD_POLICY.md`](NO_OVERBUILD_POLICY.md). No exceptions before first SAR is collected.

## Evidence required to build
| Item | Source |
|---|---|
| Paying-customer demand | Sales ledger; ≥1 signed proposal referencing the feature |
| Manual success count | Delivery log; minimum thresholds in `PRODUCTIZATION_ENGINE.md` |
| Estimated build cost | Engineering estimate (hours, infra) |
| Reversibility plan | Rollback path documented |
| Approval level | Per `docs/governance/APPROVAL_MATRIX.md` |

## Operations
- Weekly: founder reviews feature intake (see [`FEATURE_INTAKE.md`](FEATURE_INTAKE.md)).
- Monthly: engineering health review ([`ENGINEERING_HEALTH_REVIEW.md`](ENGINEERING_HEALTH_REVIEW.md)).
- Quarterly: build/defer/kill review for backlog.
- Release gate per [`RELEASE_POLICY.md`](RELEASE_POLICY.md).

## Owner & cadence
- Owner: Founder until Engineering Lead is hired (trigger in `docs/people/HIRING_TRIGGERS.md`).
- Cadence: weekly intake triage, monthly health, quarterly portfolio review.

## Cross-links
- [`PRODUCTIZATION_ENGINE.md`](PRODUCTIZATION_ENGINE.md)
- [`DORA_METRICS_POLICY.md`](DORA_METRICS_POLICY.md)
- [`ENGINEERING_METRICS.md`](ENGINEERING_METRICS.md)
- [`BUG_TRIAGE.md`](BUG_TRIAGE.md)

---

## القسم العربي

**الغرض:** فهرس واحد يحكم كيف يتحول العمل اليدوي المتكرر إلى قوالب ثم أتمتة ثم منتج SaaS. لا تُبنى أي ميزة بدون دليل طلب متكرر ونجاح يدوي مُثبت.

**القواعد:**
- لا تُبنى ميزة بناءً على رأي. ثلاث إشارات مطلوبة: طلب من عميل دافع، تنفيذ يدوي ناجح متكرر، نتيجة قابلة للقياس بعد البناء.
- كل قرار يُسجّل في `BUILD_DEFER_KILL.md`.
- سُلّم المُنتجة مُلزم — راجع `PRODUCTIZATION_ENGINE.md`.
- القائمة الممنوعة في `NO_OVERBUILD_POLICY.md`. لا استثناءات قبل أول ريال محصّل.

**التشغيل:** مراجعة أسبوعية للطلبات، شهرية لصحة الهندسة، ربعية لمحفظة المنتج.

**المالك:** المؤسس حتى تعيين قائد هندسي.
