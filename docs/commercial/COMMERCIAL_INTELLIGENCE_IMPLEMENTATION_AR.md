# Commercial Intelligence — دليل التنفيذ

## الغرض

هذه الطبقة تكمل Commercial Universe الموجود ولا تستبدله:

- `dealix/commercial_universe.py` يعرّف الحساب والعلاقة والهدف والموافقة.
- `dealix/company_os/company_directory.py` يحلل دليل الشركات دون تخزين القيم الخام للاتصال.
- `dealix/commercial_intelligence.py` يقيّم المصدر والإشارة والفرصة مع Evidence Caps.
- `db/models_commercial_intelligence.py` يحفظ الرسم التجاري متعدد المستأجرين.
- `api/routers/commercial_intelligence.py` يوفّر قراءة وكتابة داخلية محمية بالمستخدم والمستأجر.
- Approval Center الحالي يبقى المسار الوحيد لأي قرار خارجي.

## نموذج البيانات

| الجدول | المعنى | القاعدة |
|---|---|---|
| `commercial_intelligence_sources` | مصدر وسياساته وصلاحيته | المصدر المحظور لا ينتج إشارة |
| `commercial_intelligence_signals` | claim + evidence ref + freshness | لا إشارة بلا مصدر وحساب وتاريخ |
| `commercial_department_objectives` | هدف قسم ومقياس ومالك | لا فرصة بلا هدف |
| `commercial_strategic_relationships` | نوع العلاقة والقيمة المتبادلة والإذن | البيانات العامة لا تعني consent |
| `commercial_intelligence_opportunities` | العقدة التجارية المربوطة بكل ما سبق | `external_action_allowed=false` دائمًا |
| `commercial_opportunity_signals` | حواف Evidence فعلية بين الإشارة والفرصة | لا Opportunity Graph قائم على JSON فقط |

Alembic:

```text
20260715_016_company_targeting
→ 20260715_017_commercial_intelligence
```

## Evidence Caps

| المستوى | الحد الأعلى لترتيب الفرصة | الاستخدام |
|---|---:|---|
| L0 unknown | 20 | لا توجد إشارة |
| L1 hypothesis | 40 | فرضية داخلية |
| L2 public signal | 60 | بحث عام؛ يحتاج تحققًا من العميل |
| L3 first-party | 75 | بيانات/تصريح من العميل |
| L4 verified | 90 | تحقق مستقل أو تشغيلي |
| L5 measured outcome | 100 | baseline/after وattribution |

الدرجة ليست احتمال إغلاق ولا ضمان إيراد. هي أولوية بحث/تشغيل مقيدة بقوة الدليل.

## API

Prefix: `/api/v1/commercial-intelligence`

قراءة:

- `GET /status`
- `GET /snapshot`
- `GET /sources`
- `GET /source-scorecards`
- `GET /objectives`
- `GET /relationships`
- `GET /opportunities`
- `GET /graph`

كتابة داخلية، tenant-scoped:

- `POST /sources`
- `POST /signals`
- `POST /objectives`
- `POST /relationships`
- `POST /opportunities`

لا يوجد endpoint باسم send، publish، charge، deploy، أو mutate CRM.

## تشغيل المؤسس

```bash
python scripts/commercial/run_commercial_intelligence_founder_cycle.py
python scripts/commercial/verify_commercial_intelligence.py
python scripts/check_alembic_single_head.py
```

أول تشغيل لا يخترع شركات أو فرصًا. ينتج Source Scorecards وأهداف الأقسام ويصرح بأن عدد الإشارات والفرص الحقيقية صفر حتى تحميل Evidence مصرح به.

## ربط Command Center

تعرض لوحة المؤسس:

- عدد المصادر والإشارات والأهداف والعلاقات والفرص.
- الفرص عالية الأولوية.
- جودة المصادر وstaleness.
- أعلى فرص مرتبة مع مستوى الدليل والبلوكيرات.

لا تعرض قيم اتصال خام ولا تسمح بإرسال من اللوحة.

## Definition of Done

- single Alembic head.
- tenant scope في كل query وunique constraint.
- canonical service catalog validation لكل فرصة.
- evidence/source/objective required.
- public signals capped at L2.
- blocked sources rejected.
- no external side effect path.
- domain, migration, router, runner, and dashboard contract tests pass.
