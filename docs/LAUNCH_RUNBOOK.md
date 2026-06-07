# Dealix — دليل الإطلاق التشغيلي / Launch Runbook

> كيف تُشغّل Dealix كشركة حيّة **اليوم**، بصفر أسرار، باحترام الـ 11 مبدأ غير القابل للتفاوض.
> How to run Dealix as a live company **today**, with zero secrets, honoring the 11 non-negotiables.

---

## 0) تحقّق الجاهزية / Readiness check
```bash
python scripts/verify_launch_ready.py
```
يجب أن تظهر `RESULT: READY ✅` (6 فحوص: الإطار، المنسّق، الطابور، مسارات الموافقة، مستويات الخدمة، إخلاء المسؤولية).

---

## 1) تسلسل اليوم الأول / Day-1 sequence (degraded-but-real, no secrets)

**أ) حمّل العملاء الحقيقيين / Load real prospects**
```bash
python scripts/ingest_saudi_prospects.py --top 15           # رتّب الإطار حسب ICP
python scripts/ingest_saudi_prospects.py --seed-inbox       # (اختياري) يظهرون في /api/v1/founder/leads
```
المصدر: `data/leads/saudi_b2b_prospects.csv` (45 حساباً، 22 قطاعاً، مصادر عامة). الإسناد: `data/leads/SOURCES.md`.

**ب) ولّد الدرافتات اليومية / Generate the daily drafts**
```bash
python scripts/dealix_daily_draft_loop.py --print
```
يكتب موجزاً للمؤسس في `data/founder_briefs/daily_drafts_<date>.md` + `.json`، ويصفّ كل مسوّدة في طابور الموافقة الدائم (`var/draft-queue.jsonl`). **لا يُرسَل شيء.**

> تلقائياً: GitHub Action **Dealix Daily Drafts** يشغّل هذا ~07:00 KSA ويرفع الموجز كـ artifact (وبريد اختياري عند `RESEND_API_KEY`).

**ج) راجع واعتمد / Review & approve** (شغّل الـ API: `uvicorn api.main:app`)
```bash
curl localhost:8000/api/v1/founder/approvals                       # القائمة + الإحصاء
curl -X POST localhost:8000/api/v1/founder/approvals/<id>/approve  -d '{"who":"founder"}'
curl -X POST localhost:8000/api/v1/founder/approvals/<id>/reject   -d '{"reason":"..."}'
```
أو من الواجهة: صفحة الموافقات في `frontend/` (`/[locale]/approvals`).

**د) الموقع / The website**
- الموقع الرئيسي: `frontend/` — القمع: الرئيسية → `dealix-diagnostic` → `risk-score` → `proof-pack` → `pricing` → **`build` (الذكاء المخصص)**.
- محلياً: `cd frontend && npm run dev` → `http://localhost:3000/ar`.
- SEO/تسويق ثابت: `landing/` على GitHub Pages.

---

## 2) العقيدة في التشغيل / Doctrine in operation (لا تُكسَر)
- **لا إرسال خارجي تلقائي.** كل مسوّدة على مستوى الشركة، `approval_required=true`، و`consent_status=required_before_contact` حتى تؤكّد جهة التواصل وتعتمد.
- **لا scraping، لا PII** في القاعدة أو السجلات. مصادر عامة فقط.
- **لا ضمان ROI** — كل مسوّدة تحمل "تقديري ≠ مضمون".
- الاعتماد يخوّل إرسالاً بشرياً مؤكَّداً لاحقاً؛ مسارات الإرسال (WhatsApp/بريد) تبقى مُسيَّجة (opt-out, quiet-hours, نافذة 72h).

---

## 3) من حقيقي-مُخفَّض إلى Live كامل / Degraded-but-real → full live
الشركة تعمل الآن بلا أسرار. لتحويل قدرة إلى Live، أضِف السرّ المقابل:

| القدرة | السرّ | ماذا يتغيّر |
|---|---|---|
| بريد الموجز | `RESEND_API_KEY` + `DEALIX_FOUNDER_EMAIL` | يُرسَل الموجز بريدياً (بدلاً من artifact) |
| إرسال WhatsApp | `whatsapp_allow_live_send=true` + موافقة Meta | يُسمح بالإرسال **بعد اعتماد المؤسس** فقط |
| الدفع الحقيقي | `MOYASAR_API_KEY` + `MOYASAR_LIVE_MODE=1` | روابط دفع حيّة (الافتراضي sandbox) |
| التحليلات | `POSTHOG_KEY` / `GA4_ID` | تفعيل أحداث الموقع |
| النشر | `RAILWAY_TOKEN` + DNS لـ `dealix.me`/`api.dealix.me` | نشر `frontend/` + `api/` على Railway |
| مصادقة الإنتاج | `APP_SECRET_KEY`,`JWT_SECRET_KEY`,`API_KEYS`,`ADMIN_API_KEYS` | تشغيل `APP_ENV=production` |

**لا شيء من هذه يعيق الإطلاق** — كلها ترقيات تدريجية.

---

## 4) أين كل شيء / Where things live
| المكوّن | المسار |
|---|---|
| إطار العملاء | `data/leads/saudi_b2b_prospects.csv` · `data/leads/SOURCES.md` |
| منسّق الحلقة | `auto_client_acquisition/commercial_orchestrator/` |
| الحلقة اليومية | `scripts/dealix_daily_draft_loop.py` · `.github/workflows/dealix_daily_drafts.yml` |
| طابور الموافقة | `var/draft-queue.jsonl` (gitignored) |
| API الموافقة | `api/routers/founder.py` → `/api/v1/founder/approvals*` |
| الموقع (custom-AI) | `frontend/src/app/[locale]/build/` |
| تحقّق الإطلاق | `scripts/verify_launch_ready.py` |
| الخطة الكاملة | `docs/...` (هذا الملف) + وصف PR |
