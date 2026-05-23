# Operating Risk Model — Dealix

## الدور — Role

مخاطر تشغيلية يومية — outage، فقدان بيانات، secret leak، CI down.

## فهرس المخاطر — Indexed risks

| ID | Description | Severity | Likelihood | Mitigation |
| --- | --- | --- | --- | --- |
| OPS-001 | تسريب secret في git | critical | low | gitleaks + pre-commit + .secrets.baseline |
| OPS-002 | تعطّل Stripe/Moyasar | high | low | webhook retry + fallback manual |
| OPS-003 | فقدان بيانات في `<private_ops>` | critical | medium | backup يومي + verify_backup.py |
| OPS-004 | CI أحمر يستمر >24 ساعة | high | medium | rotating owner + Daily Brief blocker |
| OPS-005 | DB migration فاشل | high | low | single-head check + dry-run |
| OPS-006 | DLQ يكبر بدون معالجة | medium | high | check_dlq_size.py + Daily Brief |
| OPS-007 | تجاوز سعة LLM/API | medium | medium | rate limits + budget caps |
| OPS-008 | جلسة dev تكتب على prod | critical | low | env separation + .env.staging.example |
| OPS-009 | Frontend build فاشل | medium | medium | CI gate + nightly build |
| OPS-010 | فقدان gh token / cred | high | low | rotation policy + 2 owners |

## أدوات التحقق — Verifiers

- `scripts/verify_backup.py`
- `scripts/check_alembic_single_head.py`
- `scripts/check_dlq_size.py`
- `scripts/verify_machine_registry.py`

## الملكية — Ownership

- Owner: Founder.
- Backup: Sales lead.
