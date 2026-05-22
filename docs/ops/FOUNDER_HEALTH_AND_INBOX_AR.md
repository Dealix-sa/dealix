# Founder Health Score + Action Inbox — Dealix

**الغرض:** رقم واحد + قائمة واحدة يلخصان حالة الشركة اليوم — للمؤسس وحده.

**العقيدة:** اقرأ فقط (Article 4). الأعداد تقديرات تشغيلية (Article 8). تجميع بدون منطق جديد (Article 11).

---

## 1) Founder Health Score — رقم 0-100

نتيجة موحّدة من خمسة إشارات حقيقية في المستودع:

| الإشارة | الوزن | المصدر |
|---|---:|---|
| تدفق الأدلة (Evidence flow) | 25% | `evidence_events_tracker.csv` (آخر 7 أيام) |
| أول مدفوع (Paid traction) | 25% | `first_paid_tracker.analyze_first_paid_diagnostic` |
| امتثال PDPL (Compliance) | 20% | `founder_pdpl_compliance_pass.yaml` |
| ربط أقوى خطة (Plan wiring) | 15% | `founder_strongest_plan_status.py` |
| صندوق الـ Leads (Inbox freshness) | 15% | `auto_client_acquisition.lead_inbox` |

**الحكم:**
- `80-100` → **HEALTHY** — استمر بالإيقاع
- `50-79` → **CAUTION** — أغلق البوابات المتبقية
- `0-49` → **ACTION_NEEDED** — أوقف التوسع، افتح يوم أدلة

### الاستخدام

```bash
# طباعة في الترمنال (Arabic + English):
py -3 scripts/founder_health_brief.py

# JSON (للأنظمة الأخرى):
py -3 scripts/founder_health_brief.py --format json

# كتابة الملف:
py -3 scripts/founder_health_brief.py --out data/founder_briefs/health_today.md

# CI gate (exit 0=HEALTHY, 1=CAUTION, 2=ACTION_NEEDED):
py -3 scripts/founder_health_brief.py --exit-code-by-verdict
```

### API

```
GET /api/v1/founder/health-score              · JSON (مع تفاصيل sub-scores)
GET /api/v1/founder/health-score.md           · Markdown brief
GET /api/v1/founder/health-score?stale_hours=12   · ضبط عتبة الـ leads
```

كلها admin-key gated (`X-Admin-API-Key`).

---

## 2) Founder Action Inbox — قائمة P0 → P3

قائمة موحّدة لكل عنصر يحتاج لمسة المؤسس، مرتّبة بالأولوية:

| المصدر | المنتج |
|---|---|
| Approval Center | موافقات معلّقة (P0 high · P1 med · P2 low) |
| Lead Inbox | leads متروكة > N ساعة (P0 ≥ 48h · P1 < 48h) |
| Evidence CSV | لم تسجّل أي حدث اليوم (P1) أو إيقاع أسبوع منخفض (P2) |
| PDPL Compliance | بنود مفتوحة (P0 — مع مراجعة قانونية) |
| First Paid Tracker | Article 13 غير مغلق (P0) |
| Strongest Plan | مسارات ناقصة (P1) أو نقص مهام (P2) |

**الحكم العام:**
- `BLOCKED` — يوجد P0 — أغلقه قبل أي شيء
- `ACTIVE_DAY` — P1 لليوم — افتح الـ Cockpit وابدأ
- `MAINTENANCE` — لا عناصر عاجلة — حافظ على الإيقاع
- `CLEAR` — صندوق نظيف — يوم تعلّم

### الاستخدام

```bash
# Markdown (Arabic + English):
py -3 scripts/founder_action_inbox.py

# JSON:
py -3 scripts/founder_action_inbox.py --format json

# ضبط حدود:
py -3 scripts/founder_action_inbox.py --stale-hours 12 --limit 20

# CI gate (exit 0=clear/maint, 1=active, 2=blocked):
py -3 scripts/founder_action_inbox.py --exit-code-by-verdict
```

### API

```
GET /api/v1/founder/action-inbox              · JSON (مع items وtotal_items)
GET /api/v1/founder/action-inbox.md           · Markdown brief
GET /api/v1/founder/action-inbox?limit=10     · حدّ القائمة
```

---

## 3) Daily flow — كيف يستخدمها المؤسس

**الصباح (دقيقتين):**
1. `py -3 scripts/founder_health_brief.py` → اقرأ الرقم + الـ verdict
2. `py -3 scripts/founder_action_inbox.py` → افتح القائمة وابدأ من P0
3. كلا الأمرين قابلان للأتمتة عبر Task Scheduler / cron

**المساء (دقيقة):**
- إذا انجزت لمسات: سجّلها في `evidence_events_tracker.csv`
- إذا أُغلقت موافقات: تظهر تلقائياً خارج الـ inbox غداً

**الأسبوع:**
- اربط `--exit-code-by-verdict` في CI لمراقبة الانحدار

---

## 4) ضمانات العقيدة (Hard Rules)

| القاعدة | كيف نلتزم بها |
|---|---|
| Article 4 — لا إرسال آلي خارجي | كل النقاط للقراءة فقط، لا webhooks، لا outbound calls |
| Article 8 — الأعداد تقديرات | `is_estimate=True` في كل payload؛ توضيح في الـ markdown |
| Article 11 — تجميع فقط | الموديولان لا يضيفان منطق أعمال؛ يستدعيان وحدات قائمة |
| PDPL | لا تخزين بيانات شخصية حساسة جديدة؛ نقرأ من ملفات تعريف موجودة |

---

## 5) الملفات والاختبارات

| نوع | المسار |
|---|---|
| Core module — score | [`dealix/commercial_ops/founder_health_score.py`](../../dealix/commercial_ops/founder_health_score.py) |
| Core module — inbox | [`dealix/commercial_ops/founder_action_inbox.py`](../../dealix/commercial_ops/founder_action_inbox.py) |
| API router | [`api/routers/founder_health.py`](../../api/routers/founder_health.py) |
| CLI — health | [`scripts/founder_health_brief.py`](../../scripts/founder_health_brief.py) |
| CLI — inbox | [`scripts/founder_action_inbox.py`](../../scripts/founder_action_inbox.py) |
| Unit tests — score | [`tests/test_founder_health_score.py`](../../tests/test_founder_health_score.py) |
| API tests — score | [`tests/test_founder_health_api.py`](../../tests/test_founder_health_api.py) |
| Unit tests — inbox | [`tests/test_founder_action_inbox.py`](../../tests/test_founder_action_inbox.py) |
| API tests — inbox | [`tests/test_founder_action_inbox_api.py`](../../tests/test_founder_action_inbox_api.py) |

**اجمالي:** 44 اختبار pytest حقيقي مرّ بنجاح (20 + 4 + 12 + 4 + 4).
