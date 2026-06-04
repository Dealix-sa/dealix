# Evidence Pack — حزمة الأدلة

> Readiness is proven by command outputs and artifact files, not by claims. Every item below names the exact command and the exact output path. Nothing here sends anything externally.
>
> تُثبَت الجاهزية بمخرجات الأوامر وملفات الأدلة، لا بالادعاءات. كل بند أدناه يذكر الأمر الدقيق ومسار المخرج الدقيق. لا شيء هنا يُرسل خارجيًا.

---

## EN — Required evidence

| # | What it proves | Command to run | Output file / location |
|---|---|---|---|
| 1 | Master launch readiness | `python scripts/final_launch_control_verify.py` | `outputs/final_launch_control/` |
| 2 | 400+ review-only drafts generated | `python scripts/commercial_generate_400_drafts.py` | `outputs/commercial_launch/latest/draft_queue.jsonl` |
| 3 | Draft count >= 400 | inspect line count of draft queue | `outputs/commercial_launch/latest/daily_metrics.json` |
| 4 | Safety audit passes (zero violations) | `python scripts/commercial_safety_audit.py` | `outputs/commercial_launch/latest/safety_audit.json` |
| 5 | Commercial launch readiness | `python scripts/commercial_launch_readiness.py` | `outputs/commercial_launch/latest/` |
| 6 | Founder review queue + top 50 | produced by readiness/draft run | `outputs/commercial_launch/latest/founder_review.md`, `top_50_priority.md` |
| 7 | Website static build/check | `python scripts/site_launch_static_check.py` | console result + `outputs/final_launch_control/` |
| 8 | API source static check (no send endpoints) | `python scripts/api_commercial_static_check.py` | console result |
| 9 | CRM schema valid (no forbidden PII fields) | `python scripts/commercial_crm_schema_verify.py` | console result, reads `config/crm_pipeline_schema.json` |
| 10 | Media/social calendar generated | `python scripts/media_social_calendar_generate.py` | `outputs/media_social/` |
| 11 | Media/social verifier passes | `python scripts/media_social_verify.py` | console result |
| 12 | Secret + risk scan clean | `python scripts/final_secret_and_risk_scan.py` | console result |
| 13 | Daily workflow result (artifact-only) | GitHub Actions → `final-launch-control.yml` | workflow run artifacts |
| 14 | Test suite result | `pytest -q` (or repo test runner) | console result |
| 15 | README / docs status | review `docs/launch-control/*` and root `README` | repository |

### Evidence acceptance rules
- Each command must exit successfully and produce its named output file.
- Safety audit must report **zero** violations before any manual outreach begins.
- Draft queue must contain at least **400** entries, each with `send_allowed=false`, `external_send_blocked=true`, `no_auto_send=true`, `requires_founder_approval=true`.
- The secret + risk scan must report **no** secrets and **no** send-capable paths.
- The GitHub Actions run must show `permissions: contents: read`, no secrets, artifacts only.

---

## AR — الأدلة المطلوبة

| # | ما يُثبته | الأمر للتشغيل | ملف / موقع المخرج |
|---|---|---|---|
| 1 | جاهزية الإطلاق الرئيسية | `python scripts/final_launch_control_verify.py` | `outputs/final_launch_control/` |
| 2 | توليد 400+ مسودة للمراجعة | `python scripts/commercial_generate_400_drafts.py` | `outputs/commercial_launch/latest/draft_queue.jsonl` |
| 3 | عدد المسودات >= 400 | فحص عدد أسطر طابور المسودات | `outputs/commercial_launch/latest/daily_metrics.json` |
| 4 | نجاح تدقيق الأمان (صفر مخالفات) | `python scripts/commercial_safety_audit.py` | `outputs/commercial_launch/latest/safety_audit.json` |
| 5 | جاهزية الإطلاق التجاري | `python scripts/commercial_launch_readiness.py` | `outputs/commercial_launch/latest/` |
| 6 | طابور مراجعة المؤسس + أعلى 50 | يُنتَج من تشغيل الجاهزية/المسودات | `outputs/commercial_launch/latest/founder_review.md`، `top_50_priority.md` |
| 7 | فحص بناء الموقع الثابت | `python scripts/site_launch_static_check.py` | نتيجة الطرفية + `outputs/final_launch_control/` |
| 8 | فحص مصدر الواجهة البرمجية (لا نقاط إرسال) | `python scripts/api_commercial_static_check.py` | نتيجة الطرفية |
| 9 | صحة مخطط CRM (لا حقول PII ممنوعة) | `python scripts/commercial_crm_schema_verify.py` | نتيجة الطرفية، يقرأ `config/crm_pipeline_schema.json` |
| 10 | توليد تقويم الإعلام والتواصل | `python scripts/media_social_calendar_generate.py` | `outputs/media_social/` |
| 11 | نجاح مدقق الإعلام والتواصل | `python scripts/media_social_verify.py` | نتيجة الطرفية |
| 12 | نظافة فحص الأسرار والمخاطر | `python scripts/final_secret_and_risk_scan.py` | نتيجة الطرفية |
| 13 | نتيجة التشغيل اليومي (مخرجات فقط) | GitHub Actions ← `final-launch-control.yml` | مخرجات تشغيل سير العمل |
| 14 | نتيجة مجموعة الاختبارات | `pytest -q` (أو مشغّل اختبارات المستودع) | نتيجة الطرفية |
| 15 | حالة README / المستندات | مراجعة `docs/launch-control/*` و`README` الجذر | المستودع |

### قواعد قبول الأدلة
- يجب أن ينتهي كل أمر بنجاح وأن يُنتج ملف المخرج المسمّى.
- يجب أن يُبلّغ تدقيق الأمان عن **صفر** مخالفات قبل بدء أي تواصل يدوي.
- يجب أن يحتوي طابور المسودات على **400** مدخل على الأقل، كل منها بـ `send_allowed=false` و`external_send_blocked=true` و`no_auto_send=true` و`requires_founder_approval=true`.
- يجب أن يُبلّغ فحص الأسرار والمخاطر عن **عدم** وجود أسرار و**عدم** وجود مسارات قادرة على الإرسال.
- يجب أن يُظهر تشغيل GitHub Actions صلاحية `permissions: contents: read`، بدون أسرار، مخرجات فقط.

---

Related: [Launch Scorecard](01_LAUNCH_SCORECARD.md) · [Daily Command Center](05_DAILY_COMMAND_CENTER.md) · [Failure Response Playbook](06_FAILURE_RESPONSE_PLAYBOOK.md)

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
