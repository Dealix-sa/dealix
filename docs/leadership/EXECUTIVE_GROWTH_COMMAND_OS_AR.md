# Dealix Executive Growth Command OS

هذه الطبقة تجعل Dealix يعطي قرارات يومية لكل إدارة في الشركة.

## المسارات

- CEO
- Growth
- Sales
- Partnerships
- Marketing
- Customer Success
- Delivery
- Trust
- Pricing

## التشغيل

```bash
python scripts/leadership/run_executive_growth_command_day.py
```

## الاختبار

```bash
python -m pytest -q tests/test_executive_growth_command_os.py
```

## المخرجات

```text
reports/executive_growth/latest.json
reports/executive_growth/latest.md
```

## القاعدة

كل دور يحصل على كرت قرار. كل كرت يحتوي أزرار اعتماد وتعديل وتخطي. كل قرار يحتاج مراجعة بشرية قبل أي إجراء خارجي حساس.
