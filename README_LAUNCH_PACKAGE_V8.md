# Dealix Launch Package V8 — Investor / Enterprise Proof & Trust Readiness

V8 يبني فوق V1–V7 ويضيف طبقة إثبات، ثقة، وقياس تناسب البيع المؤسسي، الشراكات، والمحادثات الاستثمارية المبكرة.

## الهدف
تحويل Dealix من نظام تشغيل إيرادي داخلي إلى شركة تستطيع إثبات:
- ماذا تم بناؤه.
- ماذا تم بيعه أو اختباره.
- ما الدليل على القيمة.
- ما المخاطر وكيف تُدار.
- ما القابلية للتوسع.
- ما المقاييس التي يراها العميل/الشريك/المستثمر.

## التشغيل السريع
```bash
python scripts/dealix_v8_readiness_check.py
python scripts/dealix_traction_ledger.py --event-type pilot --account "شركة تدريب الرياض" --value-sar 499 --note "Pilot qualified"
python scripts/dealix_proof_vault_indexer.py
python scripts/dealix_board_metrics.py
python scripts/dealix_investor_memo_builder.py
python scripts/dealix_trust_center_manifest.py
python scripts/dealix_enterprise_proof_packet.py --account "شركة تدريب الرياض"
```

## القاعدة
لا تُعرض أرقام أو نتائج كضمان. كل proof يجب أن يكون موثق المصدر، قابل للمراجعة، ومفصولًا عن بيانات العميل الحساسة.
