# Market Production OS — نظام إنتاج السوق — دستور السوق

> Dealix = نظام تشغيل شركة إنتاج سوق. AI ينتج ويقترح ويصنّف ويرتّب ويقيس؛ والإرسال
> والالتزامات الخارجية تبقى محكومة بموافقة المؤسس. هذا ليس تحفظًا — هذا النموذج الصحيح.
>
> Dealix is a Market Production Company OS. AI produces, suggests, classifies,
> ranks, and measures; sending and external commitments stay governed by founder
> approval. Not caution — the correct institutional model.

هذا الملف هو **المرجع المركزي (الدستور)** لطبقة إنتاج السوق. لا يكرّر الوحدات الموجودة
— بل **يربطها** ويقنّن العقيدة ويحدّد ما هو موجود وما أضافته هذه الموجة وما هو قادم.

This file is the **central reference (constitution)** for the market-production
layer. It does not duplicate existing modules — it **links** them, codifies the
doctrine, and states what exists, what this wave added, and what is next.

---

## 1) العقيدة — الـ11 محظورًا (غير قابلة للتفاوض) — Doctrine: the 11 non-negotiables

هذه القواعد مُنفَّذة في الكود عبر اختبارات تمر إجباريًا. كل ميزة في طبقة السوق تحترمها.
These are enforced in code by passing tests. Every market-layer feature honors them.

1. لا أنظمة scraping — No scraping systems.
2. لا أتمتة واتساب باردة — No cold WhatsApp automation.
3. لا أتمتة LinkedIn — No LinkedIn automation.
4. لا ادعاءات مزيّفة/بلا مصدر — No fake / un-sourced claims.
5. لا ضمان نتائج مبيعات — No guaranteed sales outcomes.
6. لا PII في السجلات — No PII in logs.
7. لا إجابات معرفية بلا مصدر — No source-less knowledge answers.
8. لا إجراء خارجي بلا موافقة — No external action without approval.
9. لا وكيل بلا هوية — No agent without identity.
10. لا مشروع بلا Proof Pack — No project without a Proof Pack.
11. لا مشروع بلا Capital Asset — No project without a Capital Asset.

الإنفاذ التنفيذي لطبقة السوق: `auto_client_acquisition/gtm_os/draft_quality_gate.py`
و`sending_ramp.py` + بوابات الحوكمة `auto_client_acquisition/governance_os/` + بوابة
الإرسال الآمن `auto_client_acquisition/safe_send_gateway/`.

---

## 2) الأنظمة الإثنا عشر ← الوحدات الموجودة — The 12 Operating Systems → existing modules

| النظام / OS | الدور / Role | أين يعيش اليوم / Where it lives |
| --- | --- | --- |
| Brand OS | هوية، نبرة، claims | `docs/BRAND_PRESS_KIT.md` · `docs/brand/` |
| Offer OS | عروض وتسعير | `docs/OFFER_LADDER_AND_PRICING.md` · `auto_client_acquisition/operating_finance_os/` |
| Sector OS | playbooks للقطاعات | `docs/SECTOR_PLAYBOOKS.md` · `auto_client_acquisition/vertical_playbooks/`, `vertical_os/` |
| Signal OS | إشارات شراء (إدخال مؤسس/عام) | `auto_client_acquisition/radar_events/` · `docs/MARKET_RADAR_SIGNALS.md` · **[docs/gtm/signals/SIGNAL_OS_AR.md](signals/SIGNAL_OS_AR.md)** |
| Prospect OS | جمع وتصنيف الشركات | `auto_client_acquisition/crm_v10/`, `agents/icp_matcher.py`, `agents/lead_scoring.py` · **[docs/gtm/prospects/PROSPECT_OS_AR.md](prospects/PROSPECT_OS_AR.md)** |
| Draft Factory | 250 مسودة/يوم | `auto_client_acquisition/gtm_os/outreach_draft.py` · `email/` · **[docs/gtm/outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md](outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md)** |
| Compliance Gate | منع المخاطر | `auto_client_acquisition/gtm_os/draft_quality_gate.py` · `compliance_os/` · `governance_os/` |
| Deliverability OS | حماية الدومين + Ramp | `auto_client_acquisition/gtm_os/sending_ramp.py` · `safe_send_gateway/` · **[docs/gtm/outreach/SENDING_RAMP_OS_AR.md](outreach/SENDING_RAMP_OS_AR.md)** |
| Reply OS | تصنيف الردود | `auto_client_acquisition/email/reply_classifier.py` · `gtm_os/records.py` · **[docs/gtm/outreach/REPLY_HANDLING_OS_AR.md](outreach/REPLY_HANDLING_OS_AR.md)** |
| WhatsApp Conversion OS | تحويل المهتمين (بعد موافقة) | `auto_client_acquisition/whatsapp_decision_bot/` · **[docs/gtm/whatsapp/WHATSAPP_POST_REPLY_FLOW_AR.md](whatsapp/WHATSAPP_POST_REPLY_FLOW_AR.md)** |
| Content/Press/Partner OS | توزيع غير مباشر | `dealix/marketing_factory/` · `auto_client_acquisition/partnership_os/` · `docs/MARKETING_AND_CONTENT_SYSTEM.md` |
| Founder GTM Cockpit | قرار يومي واحد | `scripts/gtm_daily_command.py` → `reports/gtm/GTM_DAILY_COMMAND.md` · **[docs/gtm/GTM_CONTROL_ROOM_SPEC_AR.md](GTM_CONTROL_ROOM_SPEC_AR.md)** |

النتيجة: Dealix لا يعتمد على قناة واحدة — آلة سوق متعددة القنوات محكومة.
Result: Dealix is a governed, multi-channel market machine — not a single channel.

---

## 3) العمود الفقري: مسودة ← بوابة ← موافقة ← تدرّج ← إرسال — The spine

```
Signal (founder/public)  →  Prospect (scored)  →  OutreachDraft (250/day)
        →  draft_quality_gate.validate_outreach_draft()      [Compliance Gate]
        →  approval_required  →  Founder approval queue        [No auto-send]
        →  sending_ramp.plan_sending_batches()                [Reputation-safe]
        →  send (founder-approved only)  →  Reply (classified) →  WhatsApp (consent)
```

- **المسودة لا تساوي الإرسال.** كل `OutreachDraft` تولد بـ `governance_decision = "approval_required"`
  و`send_status = "draft"`. لا حقل يخزّن PII خام — المستلم بـ `recipient_ref` معتم فقط.
- **البوابة** ترفض أي مسودة تخالف: `governance:*` (scraping / cold whatsapp / linkedin
  automation / ادعاء مضمون)، `missing_unsubscribe`، `missing_evidence_level`،
  `suppression_hit`، `fake_reply_prefix`، `misleading_subject`، `personalization_below_p1`،
  `offer_not_matched`، `risk_high`، `empty_body`.
- **التدرّج** يمنع 250 إرسالًا/يوم من دومين غير مهيّأ، ويحجب الإرسال كليًا عند سوء صحة الدومين.

The draft is not the send. The gate blocks any violation. The ramp protects the
domain. Nothing here sends, charges, or scrapes.

---

## 4) التسعير — Pricing (المصدر الرسمي)

سلّم العروض الخماسي **هو المصدر الرسمي** ولا يُخترع في الكود:
The five-rung ladder is the source of truth and is never invented in code:

| Rung | Offer | Price |
| --- | --- | --- |
| 0 | Free AI Ops Diagnostic | 0 |
| 1 | 7-Day Revenue Intelligence Sprint | 499 SAR |
| 2 | Data-to-Revenue Pack | 1,500 SAR |
| 3 | Managed Revenue Ops | 2,999–4,999 SAR/mo |
| 4 | Custom AI Service Setup | 5,000–25,000 SAR (+1,000/mo) |
| Enterprise (slow) | AI Governance Review | 25,000–50,000 SAR |

المرجع: [`docs/OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md). معرّفات العروض
التشغيلية في `auto_client_acquisition/gtm_os/offer_catalog.py` (تستخدمها البوابة للتحقق
من `offer_matched`). أي أرقام موسّعة أعلى تبقى **مقترحة وتحتاج مراجعة المؤسس قبل التفعيل**.

---

## 5) لا scraping — كل الإشارات إدخال مؤسس أو عام — No scraping

Signal OS وProspect OS يعتمدان حصرًا على **إدخال المؤسس أو بيانات عامة** (إعلان وظيفة
عام، منشور عام، إحالة عميل، حدث، inbound). مصادر الإشارة المسموحة محصورة في
`SIGNAL_SOURCES` ولا تتضمن scraping إطلاقًا. البحث اليدوي العام عن شركة على LinkedIn
يكون **بموافقة المؤسس لكل حالة** ولا يُؤتمت.

---

## 6) الإيقاع اليومي والتعلّم الأسبوعي — Daily rhythm + weekly loop

التفصيل في [`docs/gtm/DAILY_OPERATING_RHYTHM_AR.md`](DAILY_OPERATING_RHYTHM_AR.md). المختصر:
07:30 إشارات · 08:30 توليد 250 مسودة · 09:00 بوابات · 10:00 موافقة 30–50 · 11:00 إرسال
محدود معتمد · 13:00 ردود · 15:00 قنوات أخرى · 18:00 محتوى · 21:00 أمر اليوم
(`scripts/gtm_daily_command.py`).

---

## 7) صلاحيات الوكلاء — Agent permissions

التفصيل في [`docs/gtm/MARKET_AGENT_REGISTRY_AR.md`](MARKET_AGENT_REGISTRY_AR.md). القاعدة:
> الوكلاء **يجوز** لهم: المسودة، التصنيف، الترتيب، التقرير.
> الوكلاء **لا يجوز** لهم: الإرسال، تثبيت السعر، الالتزام، تجاوز opt-out.
> Agents may draft, classify, rank, report. Agents may not send, price-finalize,
> commit, or bypass opt-out.

---

## 8) أوامر سريعة — Quick commands

```bash
# توليد بيانات عيّنة (تركيبية، بلا PII) / seed synthetic samples
python3 scripts/gtm_seed_samples.py

# تشغيل بوابة الجودة على المسودات / run the quality gate
python3 scripts/gtm_quality_gate.py --report reports/gtm/DRAFT_QUALITY_REPORT.md
#   أضف --require-all-pass على ملف إنتاج فعلي قبل الإدراج في قائمة الموافقة

# أمر اليوم التجاري / the founder's single daily command
python3 scripts/gtm_daily_command.py --domain-age-days 10 --domain-health healthy

# مزامنة السكيمات مع النماذج / keep JSON schemas in sync with models
python3 scripts/gen_gtm_schemas.py

# اختبارات العقيدة / doctrine contract tests
pytest tests/test_gtm_draft_quality_gate.py tests/test_gtm_sending_ramp.py \
       tests/test_gtm_records.py tests/test_gtm_schema_consistency.py \
       tests/test_gtm_scripts.py -q --no-cov
```

بوابة CI: `.github/workflows/gtm-quality-gate.yml`.

---

## 9) ما الموجود · ما أضافته هذه الموجة · القادم — Status

**موجود مسبقًا (يُعاد استخدامه):** approval_center، compliance_os (consent/ROPA/PDPL)،
safe_send_gateway، email/reply_classifier، crm_v10/icp_matcher، radar_events،
partnership_os، operating_finance_os، delivery_factory، marketing_factory،
whatsapp_decision_bot، BRAND_PRESS_KIT، OFFER_LADDER، SECTOR_PLAYBOOKS.

**أضافته موجة Market Production OS v1 (هذه):**
- كود طبقة السوق: `auto_client_acquisition/gtm_os/` →
  `outreach_draft.py`، `offer_catalog.py`، `draft_quality_gate.py`، `sending_ramp.py`، `records.py`.
- سكيمات JSON معتمدة: `dealix/contracts/schemas/{outreach_draft,sending_plan,prospect,company_signal,reply,suppression_entry}.schema.json`.
- سكربتات: `gtm_seed_samples.py`، `gtm_quality_gate.py`، `gtm_daily_command.py`، `gen_gtm_schemas.py`.
- بيانات عيّنة تركيبية: `data/gtm/{outreach,signals,prospects,replies,suppression}/`.
- بوابة CI: `gtm-quality-gate.yml`. اختبارات: `tests/test_gtm_*.py`.
- وثائق ربط: هذا الدستور + [signals](signals/SIGNAL_OS_AR.md) · [prospects](prospects/PROSPECT_OS_AR.md) ·
  [draft factory](outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md) · [sending ramp](outreach/SENDING_RAMP_OS_AR.md) ·
  [deliverability+compliance](outreach/DELIVERABILITY_AND_COMPLIANCE_AR.md) · [replies](outreach/REPLY_HANDLING_OS_AR.md) ·
  [whatsapp](whatsapp/WHATSAPP_POST_REPLY_FLOW_AR.md) · [approval queue](FOUNDER_APPROVAL_QUEUE_AR.md) ·
  [control room spec](GTM_CONTROL_ROOM_SPEC_AR.md) · [rhythm](DAILY_OPERATING_RHYTHM_AR.md) ·
  [agent registry](MARKET_AGENT_REGISTRY_AR.md).

**القادم (موجات تالية):** ربط API routers، صفحة `/[locale]/ops/gtm-control`، سجل ردود دائم،
حلقة أداء المحتوى، بوابة شركاء، لوحة مالية حيّة. هذه الموجة تتعمّد إبقاء الكود مكتبة دوال
نقية (بلا إرسال/شبكة/DB) لتقليل المخاطرة وإبقاء CI أخضر.

---

> هذا أمر تشغيلي — لا إرسال خارجي إلا بموافقة المؤسس.
> No external send happens without founder approval.
>
> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
