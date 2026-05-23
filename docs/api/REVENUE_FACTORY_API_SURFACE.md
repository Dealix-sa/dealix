# Revenue Factory API Surface / سطح API مصنع الإيرادات

## Purpose / الغرض

Define API endpoints required to operate the revenue factory.

تعريف نقاط نهاية API المطلوبة لتشغيل مصنع الإيرادات.

## Endpoints / نقاط النهاية

### Accounts / الحسابات
```http
GET  /api/v1/accounts
POST /api/v1/accounts/import
POST /api/v1/accounts/enrich
POST /api/v1/accounts/score
```

### Outreach / التواصل
```http
GET  /api/v1/outreach/pending
POST /api/v1/outreach/:id/approve
POST /api/v1/outreach/:id/reject
POST /api/v1/outreach/:id/draft
POST /api/v1/outreach/:id/mark-sent
```

### Conversations / المحادثات
```http
POST /api/v1/conversations/log
POST /api/v1/conversations/route
```

### Samples / العينات
```http
GET  /api/v1/samples/queue
POST /api/v1/samples/generate
POST /api/v1/samples/approve
```

### Proposals / العروض
```http
GET  /api/v1/proposals/queue
POST /api/v1/proposals/generate
POST /api/v1/proposals/approve
```

### Payments / المدفوعات
```http
GET  /api/v1/payments/capture-queue
POST /api/v1/payments/follow-up
POST /api/v1/payments/mark-paid
```

### Delivery / التسليم
```http
POST /api/v1/delivery/start
GET  /api/v1/delivery/queue
```

### Retention / الاحتفاظ
```http
GET  /api/v1/retention/queue
POST /api/v1/retention/ask-retainer
```

### Trust / الثقة
```http
GET  /api/v1/trust/flags
POST /api/v1/trust/evaluate
POST /api/v1/trust/approval
```

## Rule / القاعدة

Every external-impacting endpoint checks trust policy and approval class.

كل نقطة نهاية ذات تأثير خارجي تفحص سياسة الثقة وفئة الموافقة.

## See Also / مراجع

- [`../data/UNIFIED_OPERATING_DATABASE.md`](../data/UNIFIED_OPERATING_DATABASE.md)
- [`../agents/AGENT_GOVERNANCE_V3.md`](../agents/AGENT_GOVERNANCE_V3.md)
- [`../product/CEO_COMMAND_CENTER_V1.md`](../product/CEO_COMMAND_CENTER_V1.md)

## Owner / المسؤول

Sami / سامي (CEO)

## Version / الإصدار

v3.0 — 2026-05-23
