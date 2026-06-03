# ملكية الأدوار والمسؤوليات
# Role Ownership and Responsibilities

---

## المبدأ — Principle

كل وثيقة، كل تقرير، كل قرار له مالك واحد. لا مهمة "لأحد ما" — كل شيء له مسؤول محدد.

Every document, every report, every decision has one owner. No task belongs to "someone" — everything has a defined owner.

---

## جدول ملكية الأدوار — Role Ownership Table

| الدور | المسؤولية الأساسية | التقرير الرئيسي | تردد المراجعة | المالك |
|-------|------------------|----------------|--------------|--------|
| **المؤسس — Founder** | القرار الاستراتيجي اليومي، موافقة كل إجراء خارجي، الحوكمة الكاملة | DAILY_SUPER_COMMAND | يومي | المؤسس |
| **Revenue Lead** | إدارة قائمة الحسابات، متابعة الفرص، إغلاق الصفقات | DAILY_REVENUE_OPPORTUNITY_REPORT | يومي | المؤسس (يُفوَّض لاحقاً) |
| **Delivery Lead** | إدارة خط التسليم، معالجة الاختناقات، جودة المخرجات | DELIVERY_PIPELINE_STATUS | يومي | المؤسس (يُفوَّض لاحقاً) |
| **Agent Governance Lead** | مراجعة أنشطة الوكلاء، تطبيق سياسة الصلاحيات، التدقيق الأمني | AGENT_DAILY_ACTIVITY_REVIEW | يومي | المؤسس |
| **Finance Lead** | تتبع الهوامش، التدفق النقدي، Cash Priority Score | DAILY_REVENUE_OPPORTUNITY_REPORT | أسبوعي | المؤسس (يُفوَّض لاحقاً) |

---

## ملكية التقارير — Report Ownership

| التقرير | المالك | من يُعبئه | تردد التحديث |
|---------|--------|-----------|-------------|
| DAILY_SUPER_COMMAND | المؤسس | المؤسس | يومي |
| FOUNDER_WAR_ROOM_DAILY | المؤسس | المؤسس | يومي |
| FOUNDER_WAR_ROOM_WEEKLY | المؤسس | المؤسس | أسبوعي (الأحد) |
| TOP_100_ACCOUNT_QUEUE | Revenue Lead | dealix-sales (مسودة) + المؤسس | يومي |
| SYSTEM_EMAIL_DRAFTS_REVIEW | Revenue Lead | dealix-sales (مسودة) + المؤسس | عند الحاجة |
| CALL_FOLLOWUP_QUEUE | Revenue Lead | dealix-sales (مسودة) + المؤسس | بعد كل مكالمة |
| MINI_PROPOSAL_QUEUE | Revenue Lead | dealix-sales (مسودة) + المؤسس | عند الحاجة |
| DELIVERY_PIPELINE_STATUS | Delivery Lead | dealix-delivery | يومي |
| DELIVERY_BLOCKERS | Delivery Lead | dealix-delivery | فوري عند الحدوث |
| CLIENT_SIGN_OFF_QUEUE | Delivery Lead | dealix-delivery | عند الحاجة |
| DELIVERY_HEALTH_SCORECARD | Delivery Lead | المؤسس | أسبوعي |
| WEEKLY_VALUE_REPORT_QUEUE | Delivery Lead | dealix-delivery (مسودة) + المؤسس | أسبوعي |
| AGENT_DAILY_ACTIVITY_REVIEW | Agent Governance Lead | كل وكيل | يومي |
| AGENT_PERMISSION_AUDIT | Agent Governance Lead | Security Audit Agent + المؤسس | أسبوعي |
| AGENT_AUDIT_LOG_REVIEW | Agent Governance Lead | Security Audit Agent | يومي |
| DAILY_AGENT_SECURITY_REVIEW | Agent Governance Lead | Security Audit Agent | يومي |
| DAILY_REVENUE_OPPORTUNITY_REPORT | Finance Lead | dealix-sales (مسودة) + المؤسس | يومي |
| LAUNCH_SCORECARD | المؤسس | المؤسس | أسبوعي |
| ULTIMATE_SCALE_SCORECARD | المؤسس | المؤسس | أسبوعي |
| WEEKLY_SCALE_REVIEW | المؤسس | المؤسس | أسبوعي (الأحد) |
| DOMAIN_HEALTH_REVIEW | Agent Governance Lead | Security Audit Agent | أسبوعي |

---

## مبدأ التفويض — Delegation Principle

في مرحلة الإطلاق (Solo Founder)، المؤسس يملك كل الأدوار. مع النمو:

| مرحلة النمو | الأدوار التي تُفوَّض أولاً | الشرط |
|------------|--------------------------|-------|
| 3 عملاء نشطين | Delivery Lead | Delivery Health Score ≥ 80 باستمرار |
| 5 عملاء نشطين | Revenue Lead | Scale Score ≥ 80 |
| 8+ عملاء | Finance Lead | نموذج هامش موثق |

**قاعدة التفويض:** لا تُفوِّض دوراً قبل توثيق كل إجراءاته في SOPs مكتوبة.

---

## الوثائق المرتبطة — Related Documents

- [`docs/operating_factory/DAILY_LOOP_AR.md`](./DAILY_LOOP_AR.md)
- [`docs/operating_factory/WEEKLY_LOOP_AR.md`](./WEEKLY_LOOP_AR.md)
- [`docs/agents/AGENT_REGISTRY_AR.md`](../agents/AGENT_REGISTRY_AR.md)
- [`docs/scale/DELIVERY_CAPACITY_PLANNING_AR.md`](../scale/DELIVERY_CAPACITY_PLANNING_AR.md)

---

*القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value*
