# Commercial Launch API — QA & Contract (READ-ONLY)

## واجهة الإطلاق التجاري — ضمان الجودة والعقد (قراءة فقط)

> AI drafts, scores, ranks, analyzes, and recommends. The founder reviews, approves, and acts manually. The system never sends externally.

The commercial / media-social API surface is **read-only**. It exposes
configuration and schemas for the website and dashboards. It contains **no send
capability of any kind**.

### Allowed read-only endpoints / النقاط المسموحة (قراءة فقط)

- GET /api/v1/commercial/verticals
- GET /api/v1/commercial/offers
- GET /api/v1/commercial/readiness
- GET /api/v1/commercial/channel-policy
- GET /api/v1/commercial/metrics-schema
- GET /api/v1/media-social/calendar-schema

### Forbidden surfaces / النقاط المحظورة

The following are **forbidden** and must never be implemented:

- POST /api/v1/commercial/send (forbidden)
- any /send endpoint (forbidden)
- whatsapp send (forbidden)
- smtp / email send (forbidden)
- linkedin/post automation (forbidden)
- form auto-submit (forbidden)
- CRM push-send (forbidden)

### QA checklist / قائمة الفحص

- [ ] All documented endpoints are GET only.
- [ ] No mutating endpoint exists on the commercial namespace.
- [ ] No secrets are required to read configuration.
- [ ] Static check passes: `python scripts/api_commercial_static_check.py`.
