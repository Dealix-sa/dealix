# Machine Health Standard — Dealix

## الدور — Role

تعريف موحَّد لما يعنيه "ماكينة بصحة جيدة". يستخدمه `verify_machine_registry.py` وكذلك `MACHINE_FAILURE_PLAYBOOK.md`.

## الحالات — States

| State | تعريف |
| --- | --- |
| `healthy` | تشغّلت في آخر 24 ساعة + KPI ضمن الحد + لا errors |
| `degraded` | تشغّلت لكن KPI تحت الحد أو errors >0 لكن <5% |
| `down` | لم تتشغّل ≥ 48 ساعة أو errors ≥5% |
| `archived` | معطلة بنية — لا تشغيل ولا قياس |

## مصدر الحالة — Health source

```
<private_ops>/ops/machine_health.csv
```

أعمدة: `machine_id, last_run_at, state, kpi_value, errors_24h, notes`.

## DORA metrics — Build/operate posture

كمعيار جانبي للماكينات الـ code-deployed:

- Deployment frequency
- Lead time for changes
- Change failure rate
- MTTR

تُسجَّل في `<private_ops>/ops/dora_metrics.csv` (اختياري).

## القواعد — Rules

- `down` لأكثر من 48 ساعة → escalate إلى Founder.
- `degraded` لمدة أسبوع → فتح Fix decision.
- `archived` يحتاج تحديث `disable_switch` فعّال.

## الملكية — Ownership

- Owner: Founder (مؤقتاً).
- Cadence: يومي عبر `make machine-registry`.
