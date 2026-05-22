# What Dealix Actually Does

> الحقيقة التشغيلية لـ Dealix. اقرأ هذا قبل أي محادثة عميل، أو قبل تكليف أي جلسة AI ببناء "ميزات جديدة" — لأن أغلب الجلسات السابقة بالغت وادّعت أنظمة لا توجد في الكود.

**آخر تحديث:** 2026-05-22 · **مكتوب على فرع** `claude/great-faraday-Prwsz`

---

## 1. الجملة الواحدة

Dealix هو **Post-Lead Revenue Operations OS** للسوق السعودي B2B. يُثبت ما يحدث **بعد** وصول الـ lead: مَن المالك (Owner)، ما الموافقة (Approval)، ما الدليل (Evidence)، ما الخطوة التالية (Next Action) — اختصار **SOAEN**. Dealix لا يستبدل الـ CRM؛ يُثبت قرار الإيراد الموثّق فوقه.

---

## 2. الـ 5 منتجات الحقيقية (Ladder)

| الرقم | الاسم | السعر | متى | الـ SKU في الباك إند |
|---|---|---|---|---|
| 0 | Risk Score | مجاناً | كل تواصل أول | `risk_score_free` (واجهة فقط) |
| 1 | Managed Diagnostic (7 أيام) | 499 ر.س | الـ pain واضح + جاهز يصدّر CSV | `pilot_managed` |
| 2 | Data-to-Revenue Proof Pack | 1,500 ر.س | لديه 20-50 lead جاهز للفحص | (يدوي حالياً) |
| 3 | Managed Revenue Ops (شهري) | 999 - 7,999 ر.س | Proof ≥ 80 + adoption ≥ 70% | `starter`, `growth`, `scale` |
| 4 | Custom AI Service Setup | 5,000 - 25,000 ر.س + 1,000/شهر | خارج نطاق الـ ladder | يدوي |

> الـ SKUs الموجودة فعلاً في `api/routers/pricing.py:PLANS`. أي اسم باقة ثانٍ ادّعته جلسة سابقة (Sovereign Holding, Investor Tier, إلخ) — **غير موجود في الكود**.

---

## 3. ما يعمل فعلاً اليوم (Hard Truth Inventory)

### Backend (يعمل)
| النظام | المسار | الحالة |
|---|---|---|
| Moyasar payments | `dealix/payments/moyasar.py` + `api/routers/pricing.py` | ✅ HMAC webhook + idempotency + DB persistence |
| PDPL DSAR | `api/routers/pdpl_dsar.py` | ✅ POST /request, GET /policy, two-step verify |
| Proof Pack CLI | `scripts/dealix_proof_pack.py` | ✅ Bilingual MD output, `approval_status=approval_required` دائماً |
| Risk Score | `auto_client_acquisition/risk_resilience_os/` | ✅ Multiple scorers (client_risk, agent_risk) |
| Content drafter | `auto_client_acquisition/growth_beast/content_engine.py` | ✅ Draft-only |
| Objection library | `auto_client_acquisition/revenue_graph/objection_library.py` + `dealix/commercial_ops/objections.py` | ✅ Matrix exists |
| Referral program | `api/routers/referral_program.py` + `auto_client_acquisition/partnership_os/` | ✅ With DB migration 010 |
| Onboarding wizard | `scripts/dealix_customer_onboarding_wizard.py` | ✅ Manual wizard |
| WhatsApp safe-send | `auto_client_acquisition/whatsapp_safe_send.py` (205 lines) | ✅ Approval-gated only |
| Channel policy gate | `api/routers/autonomous.py:channel_policy` | ✅ Blocks LinkedIn + cold WhatsApp at runtime |
| Doctrine guard | `scripts/check_doctrine.py` + `tests/test_doctrine_enforcement.py` | ✅ Added in this branch |
| Daily founder ops | `scripts/run_founder_commercial_day.sh` + 30+ companion scripts | ✅ Heavy real implementation |

### Frontend (يعمل)
- `/[locale]` — landing (CommercialLaunchHome)
- `/[locale]/services`, `/[locale]/risk-score`, `/[locale]/proof-pack`, `/[locale]/dealix-diagnostic`
- `/[locale]/learn` + `/[locale]/learn/[slug]`
- `/[locale]/partners` — partner application form (real)
- `/[locale]/legal/{privacy,terms,dsar}` — **added in this branch**
- `/[locale]/brand` — interactive brand guide — **added in this branch**
- `/[locale]/billing` — Moyasar checkout panel — **added in this branch**
- `/[locale]/tools/roi` — ROI calculator — **added in this branch**
- `/[locale]/ops/founder` + `/ops/war-room` + `/ops/marketing` + `/ops/sales` + `/ops/partners` + `/ops/evidence` + `/ops/approvals` + `/ops/support` + `/ops/targeting` — gated by `NEXT_PUBLIC_DEALIX_ADMIN_API_KEY`
- Brand assets at `frontend/public/brand/` (logo, wordmark, favicon, tokens.json) — **added in this branch**
- Edge-rendered OG image at `frontend/src/app/opengraph-image.tsx` — **added in this branch**

---

## 4. ما لا يعمل (والسبب)

| ما ادّعته جلسة سابقة | الواقع | ماذا نفعل |
|---|---|---|
| "100 Sovereign Engine" | لم تُكتب — فقط 4 ملفات في `auto_client_acquisition/meta_os/` بمجموع 95 سطر | لن نبني 100 — البساطة تربح |
| "Master Orchestrator يعمل في الخلفية 24/7 داخل FastAPI lifespan" | غير موجود — كان سيتسبب في تسريب موارد | نوصي بـ cron خارجي يستدعي السكربتات الموجودة |
| "M&A Radar مع تقييم EBITDA آلي" | غير موجود | سابق لأوانه — pre-launch solo founder لا يحتاج |
| "Investor Room تعرض ARR حي" | غير موجود | بعد أول 5 عملاء فقط |
| "Meta-OS Dashboard مع 100 محرك" | غير موجود | بُني `/brand` بدلاً منه |
| "Auto-send عبر LinkedIn / WhatsApp" | **محظور بالـ doctrine** | الـ doctrine guard يفشل البناء لو حد كسرها |
| "نظام تطوير ذاتي (Autonomous Developer Agent)" | غير موجود — خطير لو وُجد | لا نبنيه |

---

## 5. الـ 11 Non-Negotiables (لا تُكسر)

من `AGENTS.md`:

1. لا scraping
2. لا cold WhatsApp automation
3. لا LinkedIn automation
4. لا ادعاءات بلا مصدر
5. لا ضمانات نتائج مبيعات
6. لا PII في الـ logs
7. لا إجابات بلا Source Passport
8. لا إجراء خارجي بدون موافقة
9. لا وكيل بلا هوية مسجّلة
10. لا مشروع بدون Proof Pack
11. لا مشروع بدون Capital Asset مسجّل

**كل مخالفة لهذه الـ 11 يلتقطها `scripts/check_doctrine.py`** (Track C في خطة `cozy-painting-corbato.md`).

---

## 6. الإيقاع اليومي الواقعي

| الوقت | السكربت | الناتج |
|---|---|---|
| 08:00 AST | `bash scripts/run_founder_commercial_day.sh` | War Room + content drafts + targeting refresh |
| خلال اليوم | يدوي عبر الـ Approvals UI | اعتماد + إرسال يدوي على LinkedIn/WhatsApp/email |
| 18:00 AST | `python3 scripts/founder_evening_evidence.py` | تسجيل أدلة اليوم في `evidence_events_tracker.csv` |
| جمعة 15:00 AST | `bash scripts/founder_weekly_loop.sh` | Scorecard + retro |

---

## 7. كيف تبيع — السكربت الواقعي (لا تخترعه)

1. ابحث عن وكالة سعودية أو شركة عقارات/SaaS صغيرة عبر LinkedIn يدوياً.
2. أرسل DM مكتوب يدوياً يبدأ بسؤال واحد عن "متابعة الـ leads بعد الحملات".
3. لو ردّ، اطلب منه CSV لـ 10 leads (قدامى أو غير مغلقين).
4. شغّل `python3 scripts/dealix_proof_pack.py --customer-handle <slug>` على بياناته.
5. قدّم التقرير في اجتماع 15 دقيقة — اعرض الفجوة الإيرادية والـ SOAEN.
6. وقّع على Diagnostic 499 ر.س — رابط Moyasar عبر `/[locale]/billing`.
7. عند نجاح الـ webhook، يسجل النظام `payment_received` تلقائياً.

> **هذا هو المسار الوحيد.** كل ما يحاول الـ AI أن يبيعه نيابة عنك — رفضه. أنت الواجهة البشرية.

---

## 8. مَن يقرأ هذا الملف

- **الفاوندر** — قبل أي محادثة عميل، تأكد من حدود الوعد.
- **جلسات AI القادمة** — لا تبني ما هو موجود بالفعل، ولا تدّعي ما هو غير موجود.
- **المستثمر / الشريك** — هذا ما اشتريته/شاركت فيه. لا "إمبراطورية ذاتية التشغيل".
- **مراجع PDPL/SDAIA** — كل شيء أعلاه قابل للتدقيق في الـ Git history.

---

## 9. التحديث

هذا الملف يُحدّث **يدوياً** كلما:
- أُضيف نظام حقيقي (commit feat:)
- اتضح أن ادعاءاً سابقاً غير صحيح (commit chore(docs): correction)
- تغيّرت الـ ladder الأسعار

لا تترك جلسة AI تعدّل هذا الملف بدون مراجعتك. هذا هو **مصدر الحقيقة**.
