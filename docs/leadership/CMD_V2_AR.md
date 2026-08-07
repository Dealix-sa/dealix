# Dealix Command v2

## الهدف

توسيع Dealix من نظام تجاري إلى نظام قيادة يومية يغطي ثمانية مسارات:

1. CEO Command Lane v2
2. Growth Director Lane v2
3. Sales + Negotiation Lane v2
4. Partnerships Lane v2
5. Marketing Command Lane v2
6. Trust + Pricing Gate v2
7. WhatsApp Decision Routing v2
8. Executive Command Room UI

## طريقة التشغيل

```bash
python scripts/leadership/run_cmd_v2.py
python scripts/leadership/generate_cmd_v2_snapshot.py
python -m pytest -q tests/test_cmd_v2.py
```

## المخرجات

```text
reports/leadership/cmd_v2/latest.json
reports/leadership/cmd_v2/latest.md
apps/web/lib/cmd-v2-snapshot.ts
apps/web/app/cmd-v2/page.tsx
```

## القاعدة التشغيلية

النظام يحضر القرارات والكروت والتوصيات، لكنه يبقى review-first. لا يرسل خارجيًا ولا يعتمد التزامات نهائية تلقائيًا.

## تجربة المدير

كل مسار يحصل على كرت قرار يحتوي:

- المالك.
- الهدف.
- القناة.
- الهدف التجاري.
- التوصية.
- الخطوة التالية.
- مؤشر القياس.
- مستوى المخاطر.
- أزرار اعتماد وتعديل وتخطي.

## معيار القبول

- كل المسارات الثمانية موجودة.
- كل مسار يخرج actions.
- كل card له ثلاثة أزرار أو أقل.
- كل action يحتاج approval.
- external_sends يساوي صفر.
- final_commitments يساوي صفر.
