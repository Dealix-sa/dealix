# Sovereign Workspace — مساحة Sami السيادية

> المرجع: §30 من المواصفة الأصلية.

---

## ما هذه المساحة؟

Sovereign Workspace هي **أعلى مستوى وصول** في Dealix. لها مستخدم واحد محدد (المؤسس). ترى كل شيء، تتحكم بكل شيء، وتمتلك الـ Kill Switch لكل ما عداها. لا واجهة عميل تتجاوزها، ولا وكيل ينفّذ شيئًا حسّاسًا دون مرورها، ولا قرار رأسمالي يخرج من غيرها.

هذه ليست لوحة قيادة عادية — هي **سطح قرار سيادي** يدمج إدارة الشركة وإدارة الثروة الشخصية في موضع واحد، لأن المؤسس واحد، والقرار في النهاية واحد.

---

## الـ 10 صفحات السيادية

| # | الصفحة | الغرض الجوهري |
|---|---|---|
| 1 | **Command Page** | اللوحة الأم — كل شيء في نظرة واحدة |
| 2 | **Money Command** | تدفق نقدي، خط الأنابيب، صحة Money Engine (راجع [MONEY_FLOW_AR.md](MONEY_FLOW_AR.md)) |
| 3 | **Approvals** | كل القرارات المُنتظرة للموافقة |
| 4 | **Strategic Decisions** | تتبّع القرارات الاستراتيجية الكبرى (Open/Closed) |
| 5 | **Risk Register** | كل المخاطر المعروفة + مستواها + الإجراء (راجع [RISK_MODEL_AR.md](RISK_MODEL_AR.md)) |
| 6 | **Decision Journal** | سجل دائم لكل قرار سيادي + المبررات + النتائج |
| 7 | **Capital Allocation** | توزيع رأس المال على الأصول/القطاعات/الأشخاص |
| 8 | **Kill Switch** | إيقاف فوري لأي وكيل/منتج/قطاع/عملية |
| 9 | **Agent Control** | تسجيل/إيقاف/تعديل صلاحيات الوكلاء (L0–L6) |
| 10 | **Tool Control** | إدارة Tool Registry: السماح، التحقق الدلالي، الحجر |

---

## مكونات الـ Command Page (widgets)

الـ Command Page هي الواجهة التي يفتحها المؤسس أولًا كل صباح. تجمع ويدجتات من كل المصادر الأخرى:

- **Today's pending approvals** — قائمة بكل ما يحتاج قرار اليوم.
- **Money pulse** — تدفق، التزامات، نقد محقق، نقد متوقع.
- **Top 3 opportunities** — أعلى الفرص بحسب القيمة المُقدَّرة × الاحتمال.
- **Active agents** — كم وكيل يعمل الآن، كم تكلفته الجارية.
- **Risk alerts** — تنبيهات Critical/High غير المُعالَجة.
- **Asset reuse** — كم أصلًا أُعيد استخدامه هذا الأسبوع.
- **Scale/Kill candidates** — قائمة المرشحين للتقييم (راجع [SCALE_KILL_PLAYBOOK_AR.md](SCALE_KILL_PLAYBOOK_AR.md)).
- **Personal Wealth pulse** — صحة محفظة Sami الشخصية باختصار.
- **Decision streak** — كم قرار اتُّخذ هذا الأسبوع، كم بقي مُعلَّقًا.
- **Trust score** — مؤشر مُلخَّص لحالة الحوكمة (من [TRUST_WORKSPACE_AR.md](TRUST_WORKSPACE_AR.md)).

---

## مخطط Command Page (ASCII)

```
+----------------------------------------------------------------------+
| SOVEREIGN COMMAND — Sami                       2026-05-24  09:14 AST |
+----------------------------------------------------------------------+
|  PENDING APPROVALS (3)              |  MONEY PULSE                    |
|  - Partner admission: opp_8841      |  In:    [bar bar bar bar __ ]   |
|  - Spend > limit: agent.crawler     |  Out:   [bar bar __ __ __ __]   |
|  - Open vertical: clinics_riyadh    |  Net:   +TBD                    |
+----------------------------------------------------------------------+
|  TOP 3 OPPORTUNITIES                |  RISK ALERTS                    |
|  1. opp_8841  agency_whitelabel     |  [!] tool.crawler quota         |
|  2. opp_8855  clinic_pilot          |  [!] PDPL review overdue x1     |
|  3. opp_8901  retainer_renewal      |                                 |
+----------------------------------------------------------------------+
|  ACTIVE AGENTS (4)   COST: TBD/hr   |  ASSET REUSE (week): 7          |
|  qualifier.v3 | classifier.v2       |  SCALE candidates: 2            |
|  partner_onboarding | evidence      |  KILL candidates:  1            |
+----------------------------------------------------------------------+
|  PERSONAL WEALTH PULSE              |  TRUST SCORE                    |
|  Liquidity band: green              |  Gates pass:  98%               |
|  Concentration:  watch              |  Open alerts: 2                 |
+----------------------------------------------------------------------+
|  [ KILL SWITCH ]   [ APPROVE QUEUE ]   [ DECISION JOURNAL ]          |
+----------------------------------------------------------------------+
```

---

## Personal Wealth Command Angles

§30 يوضح أن Sovereign Workspace ليست لإدارة الشركة فقط — هي تدمج زوايا إدارة الثروة الشخصية للمؤسس لأن السيادة الواحدة تتطلب رؤية واحدة. الزوايا (مفصّلة في [MONEY_FLOW_AR.md](MONEY_FLOW_AR.md) § Sami Personal Wealth OS):

1. **Liquidity** — السيولة المتاحة فورًا.
2. **Concentration** — تركيز الأصول (هل خطر؟).
3. **Cash conversion** — كم يستغرق تحويل الأصول إلى نقد.
4. **Income mix** — مصادر الدخل ومدى تنوّعها.
5. **Burn vs runway personal** — تكلفة شخصية مقابل العائد.
6. **Asset productivity** — أي أصل ينتج، أيها خامل.
7. **Tax + zakat posture** — موقف زكاة وضريبة بشكل دوري.

كل زاوية تظهر كمؤشر مُلخَّص في الـ Command Page، وتفصيلها متاح في Money Command.

---

## قواعد لا تتغيّر

- **مستخدم واحد** — لا حسابات ثانوية، لا "Sovereign-lite".
- **MFA دائم** — أعلى مستوى تحقق.
- **لا API خارجي يصل** — Sovereign لا يُعرَض على Marketplace API بأي حال.
- **سجل دائم لكل دخول** — كل جلسة مُسجَّلة بـ trace كامل.
- **Kill Switch لا يحتاج تأكيدًا ثانيًا** — حين يصدر، ينفّذ، ثم يُسجَّل.

---

## English Summary

- The Sovereign Workspace is the highest-privilege surface in Dealix; one user, all access, full kill switch.
- It contains ten pages: Command, Money Command, Approvals, Strategic Decisions, Risk Register, Decision Journal, Capital Allocation, Kill Switch, Agent Control, and Tool Control.
- The Command Page aggregates widgets from every other workspace so the founder can see company state and personal wealth posture in one view.
- Personal Wealth angles (liquidity, concentration, cash conversion, income mix, personal runway, asset productivity, tax/zakat posture) are integrated by design.
- Hard rules: single user, mandatory MFA, no external API exposure, full session logging, kill switch fires without secondary confirmation.
