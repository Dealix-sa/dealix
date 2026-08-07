# 09 — تكامل المستودع / Repo Integration — خريطة (spec فقط، لا كود)

هذا القسم **خريطة تكامل ومواصفات فقط**. وكيل المحتوى لا يكتب كوداً. الغرض: ربط حزمة Acquisition OS v2 بما هو موجود فعلاً في كود المستودع، دون تكرار أو ادّعاء قدرات غير موجودة.

> المرجع للوكلاء: [AGENTS.md](../../../AGENTS.md) (قسم مكينة الليدز السعودية + endpoints). راوتر تجاري: [api/routers/commercial.py](../../../api/routers/commercial.py).

## كيف تُسقَط أقسام الحزمة على أنظمة المستودع

| قسم الحزمة | نظام/كود المستودع | نقطة الربط |
|------------|---------------------|------------|
| 02 محرّك الليدز | `data_os` + leads pipeline | `POST /api/v1/leads` · `POST /api/v1/leads/batch` · `POST /api/v1/leads/discover/local` |
| 02 السورسينج المحكوم | `revenue_os` source registry | `GET /api/v1/revenue-os/catalog` (مصادر مسموحة/محظورة) |
| 03 التواصل (مسودات) | `sales_os` + action catalog + بوابات الموافقة | `POST /api/v1/commercial/warm-intro/draft` (مسودة، تتطلب موافقة) |
| 04 العروض/التسعير | commercial diagnostic/payment | `POST /api/v1/commercial/diagnostic/generate` · `GET /api/v1/commercial/payment/tiers` |
| 07 التسليم + Proof | `proof_os` + `value_os` | `POST /api/v1/commercial/proof/build` · `GET /api/v1/commercial/pilot/{id}/report` |
| 08 الامتثال | `governance_os` + suppression list | بوابات الموافقة + `data_suppression_list` |
| 04 القيمة التقديرية/المُتحقَّقة | `value_os` | Estimated/Observed/Verified ledger |
| 04/13 رأس المال/الإنتاج | `capital_os` | productization ledger (لاحقاً) |

## الحدود المعمارية (تُفرض في الكود الموجود)

- لا قناة خارجية تُرسِل بلا اجتياز بوابة الموافقة (`governance_os`).
- المصادر الحمراء مرفوضة قبل التشغيل عبر `source_registry` / `forbidden_sources`.
- `value_os` يفصل القيمة التقديرية عن المُتحقَّقة — تُفرض في كل تقرير.

## ما هو خارج نطاق هذا القسم

- **لا** يُكتب أو يُعدَّل أي كود هنا.
- **لا** تُخترع endpoints غير موجودة؛ ما ورد أعلاه مُتحقَّق من [api/routers/commercial.py](../../../api/routers/commercial.py) و[AGENTS.md](../../../AGENTS.md).
- أي تطوير لاحق يُفتح كـ issue ([13_AUTOMATION_BACKLOG](../13_AUTOMATION_BACKLOG/GITHUB_ISSUES_BACKLOG.md)) — بلا أي بند scraping/أتمتة.

## تحقّق للمطوّرين

`bash scripts/revenue_os_master_verify.sh` (يطبع `DEALIX_REVENUE_OS_VERDICT`) — انظر [AGENTS.md](../../../AGENTS.md).

---
**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
