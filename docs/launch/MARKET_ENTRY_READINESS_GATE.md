# Market Entry Readiness Gate — Dealix

## الدور — Role

بوابة القرار الوحيدة قبل أن تخرج Dealix إلى السوق. لا إطلاق بدون شهادة `PASS` من هذه البوابة.

The single gating contract that must turn green before any market-facing motion (paid outreach, campaign, partner activation) is allowed.

## شهادات الجاهزية المطلوبة — Required certifications

كل شهادة لها مصدر تحقق آلي:

| Certification | Verifier |
| --- | --- |
| Company OS | `scripts/verify_company_os.py` |
| Brand OS | `scripts/verify_company_os.py` |
| Growth OS | `scripts/verify_company_os.py` |
| Trust OS | `scripts/verify_company_os.py` |
| Agent OS | `scripts/verify_company_os.py` |
| Eval Gate | `scripts/verify_prompt_output_quality.py` |
| Founder Console | `scripts/verify_company_os.py` |
| Control Plane | `scripts/verify_company_os.py` |
| Launch Command Center | `scripts/verify_execution_launch_layer.py` |
| CEO Daily Brief | `scripts/verify_execution_launch_layer.py` |
| Weekly Growth War Room | `scripts/verify_execution_launch_layer.py` |
| Machine Registry | `scripts/verify_machine_registry.py` |
| Risk Register | `scripts/verify_execution_launch_layer.py` |
| Revenue Forecast | `scripts/verify_execution_launch_layer.py` |
| Acquisition Playbooks | `scripts/verify_execution_launch_layer.py` |
| Launch Readiness | `scripts/verify_launch_readiness.py` |
| Learning Memory | `scripts/verify_execution_launch_layer.py` |
| Frontend Build | `npm --prefix apps/web run build` |
| CI Workflows | `.github/workflows/dealix-execution-launch-layer.yml` |

## قواعد القرار — Decision rules

- `PASS` فقط إذا كل الشهادات أعلاه خضراء في نفس اليوم.
- `HOLD` إذا كانت `Trust OS` أو `Eval Gate` أو `Risk Register` غير خضراء.
- `BLOCK` إذا كان أي blocker مفتوح في `<private_ops>/launch/blockers.csv` بدرجة `critical`.

## ما لا يُسمح به — Hard rules

- لا تجاوز يدوي للبوابة.
- لا اعتبار "شبه أخضر" مكافئًا لـ `PASS`.
- لا حفظ شهادات قديمة كدليل — التحقق يجب أن يُعاد يوميًا قبل أي حملة جديدة.
- لا تجاوز لأي شهادة بسبب "ضغط وقت" أو "فرصة سوق".

## المخرج المطلوب — Output

كل تشغيل لـ `make execution-launch-layer` ينتج تقرير قرار:

```
Readiness Decision: PASS | HOLD | BLOCK
Failing certifications: [...]
Open blockers: [...]
Next CEO action: ...
```

## الملكية — Ownership

- Owner: Founder.
- Approver: Founder + Trust gate.
- Review cadence: قبل كل بدء حملة + كل يوم اثنين صباحًا.
