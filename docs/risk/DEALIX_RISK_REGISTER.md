# Dealix Risk Register — System

## الدور — Role

سجل المخاطر الموحَّد. يعتمد إطار NIST AI RMF: **Govern, Map, Measure, Manage**.

## مصدر الحقيقة — Source of truth

```
<private_ops>/risk/risk_register.csv
```

ويُولَّد منه bootstrap في:

```
docs/risk/templates/risk_register_bootstrap.csv  (مثال)
```

## الحقول — Fields

`risk_id,category,description,severity,likelihood,owner,mitigation,status,next_review`

- **category** — `market | ai_agent | revenue | operating | trust | legal | data | security`.
- **severity** — `low | medium | high | critical`.
- **likelihood** — `low | medium | high`.
- **status** — `open | mitigating | accepted | closed`.

## فئات المخاطر — Risk categories

- [MARKET_ENTRY_RISK_MODEL.md](./MARKET_ENTRY_RISK_MODEL.md)
- [AI_AGENT_RISK_MODEL.md](./AI_AGENT_RISK_MODEL.md)
- [REVENUE_RISK_MODEL.md](./REVENUE_RISK_MODEL.md)
- [OPERATING_RISK_MODEL.md](./OPERATING_RISK_MODEL.md)

## واجهة API الداخلية

- `GET /api/v1/internal/risks/register` — admin-key gated.
- Frontend: `/risk` يقرأ من نفس المصدر.

## القواعد — Rules

- لا حذف row من السجل — `status: closed` فقط.
- `critical` يحتاج mitigation خلال 48 ساعة.
- مراجعة كاملة في اليوم 15 من كل شهر.
- لا تشغيل ماكينة جديدة بدون تسجيل مخاطرها هنا.

## الملكية — Ownership

- Owner: Founder.
- Auditor: Trust gate.
