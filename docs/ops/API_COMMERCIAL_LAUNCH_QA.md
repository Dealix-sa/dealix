# API Commercial Launch QA — فحص إطلاق الواجهة البرمجية التجارية

> QA for the commercial launch API surface. The automated check is `scripts/api_commercial_static_check.py`, which scans the `api/` source (it is a static scan, not a live server test). The API must expose no send endpoints of any kind.
>
> فحص لسطح الواجهة البرمجية للإطلاق التجاري. الفحص الآلي هو `scripts/api_commercial_static_check.py`، الذي يمسح مصدر `api/` (فحص ثابت، وليس اختبار خادم حي). يجب ألا تكشف الواجهة أي نقاط إرسال من أي نوع.

---

## EN — Checklist

| # | Check | Pass criteria | How |
|---|---|---|---|
| 1 | `/health` endpoint | Exists and returns a healthy status | Live check, separate from static scan |
| 2 | Commercial read-only endpoints | If present, they are read-only (GET), no mutation of external state | Static scan + review |
| 3 | No send endpoints | No endpoint that sends email, SMS, WhatsApp, or any external message | `scripts/api_commercial_static_check.py` |
| 4 | No WhatsApp send | No WhatsApp send path or client in source | static scan |
| 5 | No LinkedIn send | No LinkedIn send/connect/scrape path in source | static scan |
| 6 | No SMTP | No SMTP client, no mail transport configured for sending | static scan |
| 7 | No unsafe POST | No POST that triggers external dispatch without a human gate | static scan + review |
| 8 | No secrets in source | No API keys, tokens, or credentials committed | `scripts/final_secret_and_risk_scan.py` |

### Acceptance
- The static check must pass with no send-capable paths found.
- `/health` is verified against a running instance separately; the static scan does not prove a live server.
- Any read endpoint must not return forbidden PII.

---

## AR — القائمة

| # | الفحص | معيار النجاح | الطريقة |
|---|---|---|---|
| 1 | نقطة `/health` | موجودة وتُرجع حالة سليمة | فحص حي، منفصل عن الفحص الثابت |
| 2 | نقاط تجارية للقراءة فقط | إن وُجدت، فهي للقراءة فقط (GET)، دون تعديل حالة خارجية | فحص ثابت + مراجعة |
| 3 | لا نقاط إرسال | لا نقطة ترسل بريدًا أو رسالة نصية أو واتساب أو أي رسالة خارجية | `scripts/api_commercial_static_check.py` |
| 4 | لا إرسال واتساب | لا مسار أو عميل إرسال واتساب في المصدر | فحص ثابت |
| 5 | لا إرسال لينكدإن | لا مسار إرسال/إضافة/كشط لينكدإن في المصدر | فحص ثابت |
| 6 | لا SMTP | لا عميل SMTP، ولا نقل بريد مُهيأ للإرسال | فحص ثابت |
| 7 | لا POST غير آمن | لا POST يُطلق إرسالًا خارجيًا دون بوابة بشرية | فحص ثابت + مراجعة |
| 8 | لا أسرار في المصدر | لا مفاتيح API أو رموز أو بيانات اعتماد مودَعة | `scripts/final_secret_and_risk_scan.py` |

### القبول
- يجب أن ينجح الفحص الثابت دون العثور على أي مسار قادر على الإرسال.
- يُتحقق من `/health` مقابل نسخة قيد التشغيل بشكل منفصل؛ الفحص الثابت لا يُثبت خادمًا حيًا.
- يجب ألا تُرجع أي نقطة قراءة PII ممنوعًا.

---

Related: [Site Manual QA Checklist](../site-launch/100_SITE_MANUAL_QA_CHECKLIST.md) · [Final Launch Control Tower](../launch-control/00_FINAL_LAUNCH_CONTROL_TOWER.md) · [Evidence Pack](../launch-control/03_EVIDENCE_PACK.md)

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
