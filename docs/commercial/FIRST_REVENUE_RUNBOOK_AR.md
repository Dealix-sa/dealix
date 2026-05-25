# مسار أول إيراد — Diagnostic → دفع → تسليم → Proof

## 1. Diagnostic

```bash
python3 scripts/dealix_diagnostic.py --company "ACME" --sector b2b_services
```

## 2. تأهيل

```bash
curl -s -X POST http://localhost:8000/api/v1/service-setup/qualify \
  -H "Content-Type: application/json" \
  -d '{"pain_clear":true,"owner_present":true,"data_available":true,"accepts_governance":true,"has_budget":true,"wants_safe_methods":true,"proof_path_visible":true,"retainer_path_visible":false}'
```

## 3. فاتورة

```bash
python3 scripts/dealix_invoice.py --dry-run
# عند الجاهزية: docs/integrations/PAYMENT_MOYASAR_LIVE.md
```

## 4. Kickoff + سبرنت

```bash
python3 scripts/dealix_delivery_kickoff.py --engagement-id ENG-001 --service revenue_proof_sprint_499
```

```bash
curl -s -X POST http://localhost:8000/api/v1/commercial/engagements/lead-intelligence-sprint \
  -H "Content-Type: application/json" \
  -d '{"accounts":[{"company_name":"Acme","sector":"tech","city":"Riyadh"}],"top_n":50}'
```

## 5. Proof Pack + ProofEvent

```bash
python3 scripts/dealix_proof_pack.py --engagement-id ENG-001
```

سجّل حدثاً: انسخ [`docs/proof-events/SCHEMA.example.json`](../proof-events/SCHEMA.example.json) إلى `docs/proof-events/evt_001.json` بعد توقيع العميل.
