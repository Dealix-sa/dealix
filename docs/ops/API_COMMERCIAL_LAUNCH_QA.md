# API Commercial Launch QA — Dealix — فحص جودة واجهة الإطلاق التجاري

The QA standard for the commercial API surface at launch. Only read-only commercial endpoints are allowed. No endpoint may send email, WhatsApp, or LinkedIn messages, push-and-send to a CRM, or auto-submit a form. This is enforced by a static check.

## Governing rule — القاعدة الحاكمة

**EN:** AI drafts, ranks, and recommends. Founder reviews, approves, and sends manually. The system never sends externally.

**AR:** الذكاء الاصطناعي يصيغ ويرتّب ويوصي. المؤسس يراجع ويعتمد ويرسل يدويًا. النظام لا يرسل خارجيًا إطلاقًا.

## Allowed endpoints (read-only) — نقاط النهاية المسموحة (للقراءة فقط)

All GET. No request body causes an external send. These are the only commercial endpoints permitted at launch.

| Method | Endpoint | Purpose — الغرض |
|---|---|---|
| GET | `/api/v1/commercial/verticals` | List the five priority verticals |
| GET | `/api/v1/commercial/offers` | Return the offer ladder (SAR ranges) |
| GET | `/api/v1/commercial/readiness` | Return launch readiness status |
| GET | `/api/v1/commercial/channel-policy` | Return the channel policy (draft-only posture) |
| GET | `/api/v1/commercial/metrics-schema` | Return the analytics/metrics schema |
| GET | `/api/v1/media-social/calendar-schema` | Return the media/social calendar schema |
| GET | `/health` | Service health probe |

```
GET /api/v1/commercial/verticals          -> 200, read-only
GET /api/v1/commercial/offers             -> 200, read-only
GET /api/v1/commercial/readiness          -> 200, read-only
GET /api/v1/commercial/channel-policy     -> 200, read-only
GET /api/v1/commercial/metrics-schema     -> 200, read-only
GET /api/v1/media-social/calendar-schema  -> 200, read-only
GET /health                               -> 200
```

## Forbidden endpoints — نقاط النهاية المحظورة

None of these may exist on the launch surface.

- Any email send endpoint (e.g. `POST /.../email/send`).
- Any WhatsApp send endpoint.
- Any LinkedIn send or automation endpoint.
- Any CRM push-and-send endpoint that triggers external delivery.
- Any website form auto-submit endpoint.
- Any bulk send endpoint.

If any forbidden endpoint is present, launch is **No-Go** (`docs/launch-control/02_GO_NO_GO_MATRIX.md`).

## Static check — الفحص الساكن

A static check runs against the API source before launch and writes its result to `outputs/final_launch_control/api_commercial_qa.json`. It must verify:

1. **`/health` exists.** A health probe is registered and reachable.
2. **No send endpoints.** No route path or handler implements email/WhatsApp/LinkedIn/CRM external send, form auto-submit, or bulk send.
3. **No outbound send imports.** The commercial API modules import no client or SDK whose purpose is external sending.
4. **Endpoints are read-only.** Every commercial endpoint listed above is GET and performs no external side effect.

### Check criteria — معايير الفحص

| Check | Pass condition | Fail action |
|---|---|---|
| health_present | `/health` route found | No-Go |
| no_send_endpoints | Zero send routes found | No-Go |
| no_outbound_imports | Zero outbound send imports found | No-Go |
| endpoints_read_only | All commercial endpoints are GET, no side effect | No-Go |

### Result shape — شكل النتيجة

```json
{
  "check": "api_commercial_launch_qa",
  "health_present": true,
  "allowed_endpoints": [
    "GET /api/v1/commercial/verticals",
    "GET /api/v1/commercial/offers",
    "GET /api/v1/commercial/readiness",
    "GET /api/v1/commercial/channel-policy",
    "GET /api/v1/commercial/metrics-schema",
    "GET /api/v1/media-social/calendar-schema"
  ],
  "send_endpoints_found": [],
  "outbound_send_imports": [],
  "non_readonly_commercial_endpoints": [],
  "result": "pass"
}
```

`result` is `pass` only when `health_present` is true and the three "found/imports/non-readonly" lists are all empty. Any non-empty list sets `result` to `fail` and lists the offending paths for the founder.

## How to run before launch — كيفية التشغيل قبل الإطلاق

- [ ] Run the static check; confirm `api_commercial_qa.json` result is `pass`.
- [ ] Confirm `/health` returns healthy in the live environment.
- [ ] Cross-check the result against `safety_audit.json` (`docs/launch-control/03_EVIDENCE_PACK.md`).
- [ ] Attach the result to the Go/No-Go decision.

## Arabic summary — ملخص عربي

تسمح واجهة الإطلاق بنقاط نهاية تجارية للقراءة فقط: verticals وoffers وreadiness وchannel-policy وmetrics-schema وcalendar-schema، إضافةً إلى `/health`. يُحظر أي نقطة إرسال بريد أو واتساب أو لينكدإن، أو دفع وإرسال إلى CRM، أو إرسال آلي للنموذج، أو إرسال جماعي. يتحقق فحص ساكن من وجود `/health`، وعدم وجود نقاط إرسال، وعدم وجود استيرادات إرسال خارجي، وأن جميع نقاط النهاية للقراءة فقط، ويكتب النتيجة إلى `outputs/final_launch_control/api_commercial_qa.json`. أي إخفاق يعني «لا انطلاق».

## Related — روابط

- `docs/launch-control/02_GO_NO_GO_MATRIX.md`
- `docs/launch-control/03_EVIDENCE_PACK.md`
- `docs/05_governance_os/CHANNEL_POLICY.md`

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
