---
title: No-Overbuild Policy
owner: Founder (Bassam)
status: active
last_review: 2026-05-23
---

# No-Overbuild Policy — سياسة عدم الإفراط في البناء

## Purpose
Explicit, named list of features that Dealix will not build before clear preconditions are met. The list exists because the founder is the bottleneck; engineering effort before paid traction kills the company.

## Rules
- Every item below is auto-killed in [`BUILD_DEFER_KILL.md`](BUILD_DEFER_KILL.md) until its unlocking precondition is satisfied.
- Preconditions are non-negotiable; founder cannot self-override.
- An item moved off the list requires written rationale and evidence in `docs/product/kill_log/`.

## Banned-before-first-payment list

| # | Feature | Unlocking precondition |
|---|---|---|
| 1 | Multi-tenant SaaS platform | ≥SAR 100k MRR sustained 3 months; ≥3 unsolicited SaaS asks |
| 2 | Advanced autonomous agents (level ≥4 per AI Action Levels) | All level-3 agents pass eval; governance approval logged |
| 3 | Investor data room | Term sheet signed or fundraising decision made by founder |
| 4 | Native mobile app | Web product has ≥1k weekly active sessions for 60 days |
| 5 | White-label / reseller surface | ≥5 active retainers; partner program signed off per `docs/partners/WHITE_LABEL_RULES.md` |
| 6 | Enterprise admin console (SSO, audit UI, RBAC editor) | ≥1 enterprise contract signed with these as written requirements |
| 7 | Complex billing automation (dunning, proration, multi-currency) | ≥20 active paying customers; manual billing fails to scale |
| 8 | Public API / developer portal | ≥3 partners with signed integration contracts |
| 9 | In-app analytics dashboards beyond MVP | Clients explicitly pay for analytics, not by-product |
| 10 | Custom workflow builder | Three sectors have stabilized templates |

## Operations
- Quarterly review: does any precondition now hold? If yes, item moves to [`BUILD_DEFER_KILL.md`](BUILD_DEFER_KILL.md) for scoring (still not auto-build).
- Any pitch deck, proposal, or content claiming these capabilities must be blocked at QA per `docs/content/CONTENT_STRATEGY.md`.

## Evidence
- This list is the evidence. Citing it in a Build/Defer/Kill decision is sufficient grounds to kill.

## Owner & cadence
- Owner: Founder.
- Cadence: quarterly precondition check.

## Cross-links
- [`BUILD_DEFER_KILL.md`](BUILD_DEFER_KILL.md)
- [`PRODUCTIZATION_ENGINE.md`](PRODUCTIZATION_ENGINE.md)
- `docs/governance/AI_ACTION_LEVELS.md`

---

## القسم العربي

**الغرض:** قائمة صريحة بميزات لن تُبنى قبل تحقق شروط الفك.

**الممنوع قبل أول دفعة:**
1. منصة SaaS متعددة المستأجرين — حتى 100 ألف ريال MRR لـ 3 أشهر و3 طلبات SaaS تلقائية.
2. وكلاء ذاتيون متقدمون مستوى ≥4 — حتى اجتياز التقييم وموافقة الحوكمة.
3. غرفة بيانات للمستثمرين — حتى توقيع term sheet أو قرار جمع تمويل.
4. تطبيق جوال أصلي — حتى 1000 جلسة أسبوعية لمدة 60 يومًا.
5. White-label — حتى 5 retainers نشطة وبرنامج شركاء معتمد.
6. لوحة إدارة مؤسسية (SSO/RBAC) — حتى عقد مؤسسي يطلبها كتابيًا.
7. أتمتة فوترة معقدة — حتى 20 عميلًا دافعًا.
8. واجهة API عامة — حتى 3 عقود تكامل موقّعة.
9. لوحات تحليلات داخل المنتج تتجاوز MVP — حتى يدفع العملاء صراحة مقابلها.
10. منشئ سير عمل مخصص — حتى استقرار قوالب ثلاثة قطاعات.

**المالك:** المؤسس. **الإيقاع:** فحص ربعي للشروط.
