# بوابة BU4 — تفعيل خط Trust (BU4_TRUST_ACTIVATION_GATE_AR)

> سياسة بيع: لا تُباع حزم Trust موحّدة قبل إثبات الأهلية التشغيلية على N عميل.
> Partner-safe. مرجعية للبيع والامتثال، ليست عقد عميل.

## القاعدة الأساسية

**لا تُقدّم خط Trust (Enterprise Trust Pack) كمنتج موحّد للبيع قبل تحقق جميع هذه
الشروط:**

1. **N ≥ 5 عملاء** على Revenue OS أو Command Center في الإنتاج، بمؤشرات L3 (workflow
   proven) أو أعلى.
2. **audit trail مكتمل** لكل عميل من الـ N — لا gaps أطول من 7 أيام.
3. **zero PDPL incidents** مفتوحة.
4. **incident log template** معتمد ومُختبَر على حادثة واحدة على الأقل (test drill).
5. **founder + 1 advisor** يوقّعان على جاهزية BU4.

## لماذا البوابة

خط Trust يبيع ضمانات: audit trails، evidence packs، compliance registers. إذا لم
نكن أثبتنا أنّ النظام يعمل بشكل موثوق على N عميل، فالضمان فارغ. البيع المبكر يعرّض
Dealix لمسؤولية قانونية ويكسر `no-overclaim register`.

## المعايير القابلة للقياس

| المعيار | الحد الأدنى | المصدر |
|---|---|---|
| عملاء إنتاج | 5 | `business/_data/clients.json` |
| L3 proven | 5/5 | proof packs |
| Audit gaps | 0 gaps > 7d | `observability/audit_health.py` |
| PDPL incidents open | 0 | `compliance/incidents.json` |
| Incident drill | 1 completed | `ops/INCIDENT_DRILL_LOG.md` |

## مسار التفعيل

1. Founder يفتح تذكرة `BU4 activation request` مع توثيق الـ 5 عملاء.
2. Compliance reviewer مستقل يتحقق من المعايير ويوقّع.
3. بعد التوقيع: يُفعّل `trust_pack` في service catalog.
4. قبل كل صفقة Trust جديدة: فحص المعايير ذاتها (تفتيش دوري).

## العلاقة مع DOCS_ARCHIVE_POLICY_AR.md

لا تُباع حزم Trust موحّدة قبل هذه البوابة — هذه سياسة بيع، لا مجرد أرشفة. توثيق
البوابة يُحمى من التعديل بـ `validate_docs_governance.py`.

## روابط مرجعية

- [DOCS_ARCHIVE_POLICY_AR.md](../strategic/DOCS_ARCHIVE_POLICY_AR.md)
- [DOCS_CANONICAL_REGISTRY_AR.md](../strategic/DOCS_CANONICAL_REGISTRY_AR.md)
- [ENTERPRISE_TRUST_DATA_ROOM.md](ENTERPRISE_TRUST_DATA_ROOM.md)
- [TRUST_PACK_INDEX.md](TRUST_PACK_INDEX.md)