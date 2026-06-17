# API and Integration Intake Checklist — قائمة استقبال الـ API والتكاملات

**Version:** 1.0 | **Owner:** Founder | **Last Updated:** 2026-06-01

Cross-links: [MVP_SCOPE_TEMPLATE.md](MVP_SCOPE_TEMPLATE.md) | [DATA_PROCESSING_CHECKLIST.md](DATA_PROCESSING_CHECKLIST.md) | [CLIENT_ACCESS_MATRIX.md](CLIENT_ACCESS_MATRIX.md) | [RISK_REGISTER_TEMPLATE.md](RISK_REGISTER_TEMPLATE.md)

---

## Rule — القاعدة

Complete this checklist for every external system or API that the Dealix solution will connect to. An untested or undocumented integration is a project risk. No integration goes to production without completing this checklist.

أكمل هذه القائمة لكل نظام خارجي أو API ستتصل به حلول ديليكس. التكامل غير المختبر أو غير الموثق هو خطر على المشروع. لا يذهب أي تكامل إلى الإنتاج قبل إكمال هذه القائمة.

---

## Integration Header — رأس التكامل

| Field — الحقل | Value — القيمة |
|---|---|
| Project name | [PROJECT_NAME] |
| Integration name | [e.g., Client ERP API, Maintenance System Export, etc.] |
| System type | [ ] ERP [ ] CRM [ ] CMMS [ ] Custom API [ ] Database [ ] File export [ ] Other: [___] |
| System vendor | [Vendor name if commercial product] |
| Integration owner (client side) | [Client IT contact — role/title] |
| Checklist completed by | [Dealix role] |
| Date | [YYYY-MM-DD] |

---

## Section 1 — Documentation | الوثائق

| Item — البند | Status — الحالة | Notes — ملاحظات |
|---|---|---|
| [ ] API documentation received | [ ] Complete [ ] Partial [ ] Pending | Version: [vX.X] |
| [ ] Data schema or ERD (for database integrations) received | [ ] Complete [ ] Not applicable | |
| [ ] File format specification received (for export integrations) | [ ] Complete [ ] Not applicable | Format: [CSV / Excel / JSON / XML] |
| [ ] Changelog or version history reviewed | [ ] Complete [ ] Not available | Last API version change: [date] |

---

## Section 2 — Test Environment | بيئة الاختبار

**(STOP if no sandbox/test environment is available — do not test against production.)**

| Item — البند | Status — الحالة | Notes — ملاحظات |
|---|---|---|
| [ ] Sandbox or test environment available | [ ] Yes [ ] No — STOP | URL/endpoint: [___] |
| [ ] Test credentials provided by client | [ ] Yes [ ] Pending | Stored: [credentials manager — not plaintext] |
| [ ] Test data loaded in sandbox environment | [ ] Yes [ ] Pending | |
| [ ] Dealix has confirmed connectivity to sandbox | [ ] Confirmed | Date tested: [YYYY-MM-DD] |
| [ ] Test environment mirrors production API version | [ ] Confirmed [ ] Difference noted: [___] | |

---

## Section 3 — Authentication | التحقق من الهوية

| Item — البند | Detail — التفصيل | Confirmed |
|---|---|---|
| Authentication method | [ ] API Key [ ] OAuth 2.0 [ ] Basic Auth [ ] JWT [ ] Other: [___] | [ ] |
| [ ] Authentication documented | Method and implementation steps recorded | [ ] |
| [ ] Credentials stored securely | Storage location: [secrets manager name] — NOT in code | [ ] |
| [ ] Token/key rotation process defined | Rotation interval: [X days] — who rotates: [role] | [ ] |
| [ ] What happens if credentials expire? | Fallback behavior: [describe] | [ ] |

---

## Section 4 — Rate Limits | حدود معدل الطلبات

| Item — البند | Value — القيمة | Notes — ملاحظات |
|---|---|---|
| Requests per minute limit | [N] or "not specified" | |
| Requests per day limit | [N] or "not specified" | |
| Concurrent connection limit | [N] or "not specified" | |
| [ ] Rate limits confirmed in documentation or from vendor | | |
| [ ] Dealix solution designed to stay within limits | Buffer: [% below limit] | [ ] |
| [ ] Retry logic implemented for rate-limit errors | Back-off strategy: [describe] | [ ] |

---

## Section 5 — SLA and Uptime | مستوى الخدمة وزمن التشغيل

| Item — البند | Value — القيمة | Confirmed |
|---|---|---|
| Vendor-stated uptime SLA | [%] or "not documented" | [ ] |
| Planned maintenance window | [Day/time or "not defined"] | [ ] |
| [ ] Dealix solution behavior during API downtime defined | Fallback: [queue and retry / alert admin / fail gracefully] | [ ] |
| Client IT contact for API issues | [Role — not personal name] | [ ] |
| Escalation path for extended outage (> 4 hours) | [Contact role + method] | [ ] |

---

## Section 6 — Error Handling | معالجة الأخطاء

| Error Type — نوع الخطأ | Expected Behavior — السلوك المتوقع | Confirmed |
|---|---|---|
| Authentication failure (401) | Alert admin, halt processing, log error | [ ] |
| Rate limit exceeded (429) | Wait and retry with exponential back-off | [ ] |
| Server error (5xx) | Retry up to 3 times, then alert admin and pause | [ ] |
| Invalid data returned (unexpected format) | Log malformed response, skip record, alert admin | [ ] |
| Connection timeout | Retry after [X] seconds, alert after [N] retries | [ ] |
| Partial data (incomplete response) | Log, flag for manual review, do not process partial records as complete | [ ] |

- [ ] All error types handled in build. No silent failures permitted.

---

## Section 7 — Cost and Billing | التكلفة والفواترة

| Item — البند | Value — القيمة | Confirmed |
|---|---|---|
| Cost per API call | [SAR / USD / per 1000 calls / free tier] | [ ] |
| Estimated monthly call volume | [N calls/month] | [ ] |
| Estimated monthly API cost | [SAR] — factored into project margin | [ ] |
| [ ] API cost included in project unit economics | Reference: [../finance/UNIT_ECONOMICS_TEMPLATE.md] | [ ] |
| Who pays for API costs | [ ] Dealix (included in project price) [ ] Client (direct billing) [ ] Split: [describe] | [ ] |

---

## Section 8 — Go-Live Readiness | جاهزية الإطلاق

Complete immediately before switching from test to production:

| Item — البند | Confirmed |
|---|---|
| [ ] All tests passed in sandbox environment | [ ] |
| [ ] Production credentials obtained and stored securely | [ ] |
| [ ] Production endpoint tested with one real data pull (read-only) | [ ] |
| [ ] Error monitoring enabled in production | [ ] |
| [ ] Client IT contact notified of go-live date | [ ] |
| [ ] Rollback plan documented if production integration fails | [ ] |

---

> **Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة**
