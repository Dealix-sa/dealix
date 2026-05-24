# Proof Pack Template — Delivery

**المرجع الاستراتيجي:** [`../strategy/DEALIX_FULL_OPS_MASTER_PLAN_AR.md`](../strategy/DEALIX_FULL_OPS_MASTER_PLAN_AR.md)
**عقد البرنامج (schema):** `auto_client_acquisition/proof_architecture_os/proof_pack_v2.py` — 14 قسم canonical
**سلسلة التسليم:** Free Diagnostic → **499 SAR Revenue Intelligence Sprint** → 2,999–4,999 SAR/mo Managed Ops

> هذا القالب هو **العقد** الذي يثبت على المؤسس قبل إرساء أي proof pack
> لعميل. كل قسم إلزامي. كل رقم يحتاج مصدراً أو يُسمَّى صراحة `is_estimate=true`.
> لا إصدار خارجي بدون توقيع المؤسس في **Cover Page**.

---

## Cover Page (إلزامي قبل أي إرسال)

```yaml
client_name: "<Legal name كما في الفاتورة>"
client_handle: "<short handle للـ ledger>"
engagement_id: "eng_<YYYYMMDD>_<slug>"
customer_id: "cus_<short>"
sprint_offer: "Revenue Intelligence Sprint — 499 SAR"   # أو Free Diagnostic
week_iso: "<YYYY-Www>"                                   # مثال: 2026-W21
delivery_started: "<YYYY-MM-DD>"
delivery_completed: "<YYYY-MM-DD>"
proof_pack_version: "v2.14"
proof_score: <0-100>                                      # حسب proof_os.score
tier: "<draft|internal|client_review|client_approved|public_safe>"
language: "ar+en"                                         # AR primary, EN gloss

founder_review:
  reviewed_by: "Bassam M. Assiri"
  reviewed_at: "<ISO timestamp>"
  signature_line: "________________________________________"   # توقيع يدوي PDF
  decision: "<approved|revise|blocked>"
  notes_internal: "<≤120 char — sanitized via redact_text>"
```

---

## الهيكل (14 قسم — Canonical V2)

| # | Section Key (schema) | عنوان عربي | محتوى مطلوب أدنى |
|---|---------------------|------------|------------------|
| 1 | `executive_summary` | الملخص التنفيذي | 5–7 أسطر · القيمة المثبتة · top finding واحد |
| 2 | `problem` | المشكلة الموثَّقة | السؤال الذي وقّع العميل عليه + كيف نُقيس النجاح |
| 3 | `inputs` | المدخلات | قوائم الـ CSVs · صفّات · مقابلات · لقطات CRM (asset refs فقط — لا PII) |
| 4 | `source_passports` | بطاقات المصدر | لكل مدخل: `source_id`, `owner`, `allowed_use`, `pii?`, `validate()=ok` |
| 5 | `work_completed` | العمل المنفَّذ | جدول الـ 7 أيام: تاريخ · خطوة · مالك · مخرَج |
| 6 | `outputs` | المخرجات | روابط للملفات داخل engagement (drafts AR+EN · scoring CSV · etc.) |
| 7 | `quality_scores` | درجات الجودة | جدول DQ + Proof Score (راجع §"DQ Summary" أدناه) |
| 8 | `governance_decisions` | قرارات الحوكمة | كل `governance_os.decide` event مع `action`, `decision`, `reason_code` |
| 9 | `blocked_risks` | المخاطر الموقوفة | كل `BLOCK` / `REDACT` event + سبب + إجراء بديل |
| 10 | `value_metrics` | مقاييس القيمة | من `value_os` ledger — tier فقط (estimated/observed/verified) |
| 11 | `limitations` | الحدود والشكوك | ما لم نُقِسه · افتراضات · نطاق غير مشمول |
| 12 | `recommended_next_step` | الخطوة التالية | 1 من: stop · sprint extension · managed ops · custom |
| 13 | `retainer_expansion_path` | مسار التوسعة | شرط الأهلية + العرض المقترَح (راجع `RETAINER_ELIGIBILITY_CHECKLIST_AR.md`) |
| 14 | `capital_assets_created` | الأصول المنتَجة | راجع §"Capital Asset Registration Block" أدناه — ≥ 1 إلزامي |

---

## §A — DQ Summary Table (يدخل في §7 `quality_scores`)

```text
| Source ID       | Rows | Null %  | Dup %  | Schema Errors | DQ Score | Tier         |
|-----------------|------|---------|--------|---------------|----------|--------------|
| crm_leads.csv   | 1247 |   8.2%  |  3.1%  |       2       |    78    | observed     |
| hubspot_export  |  430 |  11.5%  |  6.0%  |       0       |    71    | observed     |
| <add row>       | ...  |   ...   |  ...   |      ...      |   ...    | ...          |

Overall DQ Score: <0-100>   (founder review required if < 70)
Computed via: data_os.compute_dq(...)  · evidence_ref: <path/to/dq_run.json>
```

---

## §B — Top-3 Revenue-Leak Findings (يدخل في §1 + §6)

> كل finding يحتاج: مصدر صريح · رقم بـ tier · إجراء قابل للقياس.
> ممنوع: "نعتقد أن..." بدون مصدر. ممنوع: تقدير revenue بدون `is_estimate=true`.

```text
Finding #1: <عنوان قصير >
  Evidence: <source_id + line/row refs>
  Tier: <estimated|observed|verified|client_confirmed>
  Quantified leak (range): <SAR/mo أو # of leads أو % churn>
  Root cause (one sentence): <...>
  Fix horizon: <0-30 / 30-60 / 60-90 days>

Finding #2: <...>
Finding #3: <...>
```

---

## §C — 90-Day Plan (يدخل في §12 + §13)

> ثلاث إجراءات ملموسة فقط — لا قائمة 12 بنداً. كل إجراء له **مالك** + **مقياس
> نجاح بسيط** + **مصدر القياس**.

```text
Action 1 (0-30 days): <مثال: إعادة تأهيل 247 lead نائم — قائمة A>
  Owner (client side): <اسم/دور>
  Owner (Dealix side): <اسم — founder/agent>
  Success metric: <مثال: ≥ 18 lead عاد إلى Stage 2>
  Measurement source: <CRM export weekly · أو dashboard ref>
  Estimated value tier: estimated  → upgrades to observed after 30d

Action 2 (30-60 days): <مثال: AR follow-up template لـ top 3 segments>
  Owner client / Dealix · Success metric · Measurement source

Action 3 (60-90 days): <مثال: governance rule لمنع تجاوز SLA>
  Owner client / Dealix · Success metric · Measurement source
```

---

## §D — Evidence Appendix (L0–L5 levels)

> كل ادّعاء في proof pack يجب أن يُربط بمستوى دليل. لا claim بدون evidence_ref.

| Level | اسم | تعريف | يُسمح به في |
|-------|-----|------|-------------|
| **L0** | None | لا دليل | لا يُستخدم خارج الملاحظات الداخلية |
| **L1** | Founder assertion | إفادة المؤسس بدون مصدر مكتوب | `tier=estimated` فقط · لا case study |
| **L2** | Client verbal | تصريح شفهي من العميل (محضر اجتماع) | internal فقط |
| **L3** | Client artifact | CRM export · screenshot · email | `tier=observed` |
| **L4** | Cross-source verified | رقم مطابق من ≥ مصدرين مستقلين | `tier=verified` · يحتاج `source_ref` |
| **L5** | Client-signed confirmation | بريد/توقيع رسمي يؤكّد الرقم | `tier=client_confirmed` · case-study eligible |

### Evidence index (table)

```text
| Claim ID | Section | Evidence Level | Source Ref                        | Notes |
|----------|---------|----------------|-----------------------------------|-------|
| C-01     | §1 exec | L4             | dq_run_2026-05-22.json + CRM csv  | --    |
| C-02     | §B #1   | L3             | hubspot_export_stage2.csv         | --    |
| <...>    | <...>   | <...>          | <...>                             | <...> |
```

> **قاعدة الجودة:** أي claim بمستوى L2 أو أدنى لا يُنشر خارجياً. founder يراجع
> ويرفع التصنيف فقط بعد الحصول على مصدر أعلى — **لا auto-promote**.

---

## §E — Consent Letter Section (إلزامي لأي publication خارج العميل)

> لا case study · لا LinkedIn post · لا proof_example مسجَّل كـ `public_safe`
> بدون consent مكتوب من العميل. النموذج التالي يُرفَق كملف PDF منفصل وموقَّع.

```text
─────────────────────────────────────────────────────────────────────
خطاب موافقة على نشر النتائج (Case-Safe Publication Consent)
─────────────────────────────────────────────────────────────────────

العميل (Client):       <Legal entity name>
الممثّل (Signatory):    <Name + role>
Engagement ID:         eng_<...>
تاريخ التسليم:          <YYYY-MM-DD>

أوافق بصفتي ممثّلاً عن <Client> على ما يلي:

[ ] السماح لـ Dealix باستخدام **اسم الشركة** في case study عام.
[ ] السماح باستخدام **أرقام نسبية فقط** (لا أرقام مطلقة).
[ ] السماح باستخدام اللقب الوظيفي (لا أسماء شخصية).
[ ] الموافقة محدودة بـ <جغرافية / لغة / مدة> التالية: ____________
[ ] حق السحب خلال 30 يوماً من النشر بإشعار خطي.

تم الاطّلاع على Proof Pack رقم <version> ومراجعة §B "Top Findings"
ومراجعة §D "Evidence Appendix". الأرقام المنشورة لن تتجاوز ما تم
الموافقة عليه أعلاه.

التوقيع (Signature):    ________________________________________
التاريخ (Date):          ____ / ____ / ________
─────────────────────────────────────────────────────────────────────

Capital ledger reference (للتوثيق الداخلي):
  consent_on_file: <true|false>
  consent_doc_ref: <path/to/consent.pdf>
  publication_status: <internal_only | client_approved | public_safe>
```

> ⚠️  بدون `consent_on_file=true` لا يُسمح برفع أي capital asset إلى مستوى
> `public_safe`. هذا gate إلزامي قبل النشر.

---

## §F — Capital Asset Registration Block (إلزامي — ≥ 1 لكل engagement)

> كل engagement يجب أن يُنتج **أصلاً واحداً قابلاً لإعادة الاستخدام** على الأقل.
> التسجيل يتم عبر `auto_client_acquisition.capital_os.add_asset(...)` ويُكتب
> إلى `var/capital-ledger.jsonl` (env: `DEALIX_CAPITAL_LEDGER_PATH`).

```yaml
# لكل asset، انسخ الكتلة وأكملها
- asset_id: "<يولَّد تلقائياً — cap_<uuid12>>"
  customer_id: "<من Cover Page>"
  engagement_id: "<من Cover Page>"
  asset_type: "<scoring_rule | draft_template | governance_rule | proof_example | sector_insight | productization_signal>"
  owner: "<افتراضياً = customer_id>"
  reusable: true
  asset_ref: "<مسار الملف داخل المستودع — مثل docs/capital/<type>/<slug>.md>"
  notes: "<≤120 char — sanitized>"
  consent_on_file: "<true|false>"               # gap اليوم: غير مفروض في الـ dataclass
  publication_status: "<internal_only | client_approved | public_safe>"
  created_at: "<ISO timestamp>"
```

### قائمة تحقّق التسجيل (founder)

- [ ] الـ asset جديد فعلاً (ليس تكراراً لما هو في `list_assets(...)`)
- [ ] `asset_type` ضمن الـ 6 المسموحة في `CapitalAssetType` enum
- [ ] `asset_ref` يشير إلى ملف موجود فعلاً في المستودع
- [ ] `notes` لا تحوي PII (الـ sanitizer يطبّق تلقائياً، لكن راجع)
- [ ] إن كان `publication_status=public_safe` → `consent_on_file=true` + ملف موقَّع مرفق
- [ ] friction event مُسجَّل إذا فشل أي شرط أعلاه (`friction_log.emit(...)`)

---

## قواعد الجودة (يقرأها المؤسس قبل التوقيع)

- كل **finding** له **مصدر** (file · interview · CRM snapshot · internal policy)
- كل رقم: مصدر صريح أو `is_estimate=true` — لا استثناء
- أي **بيان ناقص** يُسمَّى صراحة «مفقود» (لا silent gaps)
- لا ادّعاء أمني (security / privacy claim) بدون مصدر L4 أو أعلى
- لا إصدار **نهائي** بدون مراجعة بشرية (Founder/lead)
- لا case study بدون L5 + consent letter موقَّع
- لا auto-promote tiers — كل ترقية تحتاج founder action صريح
- لا cold WhatsApp / LinkedIn / scraping drafts — `governance_os.decide` سيحجبها

---

## محتوى يجب أن يثبت (positioning)

Source clarity · Approval boundaries · Evidence trail · Decision passport scaffolding ·
Value report — **بدون** KPI وهمية أو «proof» مزيّف.

## ارتباط بالمنتج

- عرض تفاعلي للمؤسس: مسار `/{locale}/business-now#strategy` في الواجهة
- Sales Kit / Ops pack: [`../commercial/ops_client_pack/`](../commercial/ops_client_pack/)
- DoD مرجعي: [`../commercial/operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md`](../commercial/operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md)
- Retainer eligibility: [`./RETAINER_ELIGIBILITY_CHECKLIST_AR.md`](./RETAINER_ELIGIBILITY_CHECKLIST_AR.md)
- Schema الـ 14 قسم: `auto_client_acquisition/proof_architecture_os/proof_pack_v2.py`
