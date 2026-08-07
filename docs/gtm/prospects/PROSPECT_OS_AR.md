# Prospect OS — سجل العميل المحتمل ونظام التقييم — Prospect record and scoring

> طبقة الاستحواذ (Market Production OS) تبني المسودات لا الإرسال. هذه الوثيقة تصف **سجل العميل المحتمل الخالي من البيانات الشخصية**، وجدول الأوزان في `score_prospect`، ودورة حالة العميل، وكيف تصل العملاء المحتملون من **إدخال المؤسس أو الإشارات العامة** (لا scraping) إلى مصنع المسودات. هذه وثيقة **رابطة** — لا تكرّر منطق CRM القائم بل تربطه.

---

## 1) المبدأ — Principle

العميل المحتمل في هذه الطبقة هو **شركة مؤهَّلة**، لا شخص. كل سجل يخزّن وسوم شركة (`company_label`)، ونطاق موقع عام (`website_domain`)، و**دور** صانع القرار (`decision_maker_role`) — لا اسم، لا بريد، لا هاتف، لا هوية وطنية. هذا يبقي العينات والسجلّات خالية من PII (راجع `data_os.pii_flags_for_row`).

مصدر البيانات **حصرًا**: إدخال المؤسس أو بيانات عامة. لا scraping في أي مكان من هذه الطبقة (محرّم بنص العقيدة). للبحث اليدوي عن شركة نستخدم **manual LinkedIn company search (founder-approved per call)** — بحثًا يدويًا بموافقة المؤسس لكل حالة، وليس أتمتة.

The prospect here is a **qualified company, never a person**. Records store company labels, a public website domain, and a decision-maker **role** — never a name, email, phone, or national ID. Prospect data is **founder-input or public only — no scraping**. Manual company lookups use **manual LinkedIn company search (founder-approved per call)**, never automation.

المصدر البرمجي: [`auto_client_acquisition/gtm_os/records.py`](../../../auto_client_acquisition/gtm_os/records.py).

---

## 2) سجل العميل المحتمل (Prospect) — الحقول الخالية من PII — The PII-free Prospect record

```json
{
  "prospect_ref": "opaque-id",
  "company_label": "Riyadh marketing agency (mid)",
  "website_domain": "example.com",
  "sector": "agency",
  "region": "Saudi Arabia",
  "source": "founder_input",
  "signal_ref": "signal-id",
  "decision_maker_role": "Marketing Director",
  "pain_hypothesis": "...",
  "offer_match": "revenue_proof_sprint_499",
  "personalization_note": "...",
  "risk_level": "low",
  "evidence_level": "L1",
  "status": "new",
  "score": 0.0,
  "score_tier": "C",
  "governance_decision": "approval_required"
}
```

`decision_maker_role` **دور وليس اسمًا**. `recipient_ref` (في المسودة) مرجع مبهم لا بريدًا ولا هاتفًا. كل سجل يولد بـ `governance_decision = "approval_required"`.

`decision_maker_role` is **a role, not a name**. Every record is born `approval_required`; nothing is auto-allowed.

---

## 3) الإشارات (CompanySignal) — founder-input / public only

كل عميل محتمل يُسند إلى **إشارة توقيت شراء** لاحظها المؤسس أو من بيانات عامة. أنواع الإشارات تشمل: توظيف مبيعات/CRM/تسويق/دعم، فرع جديد، تحديث موقع، رابط حجز، إنفاق إعلاني جديد، تمويل، حضور فعالية، شراكة، إطلاق منتج، مناقصة، تغيّر تقييمات، نمو عدد الموظفين، بطء رد.

مصادر الإشارة المسموحة: `founder_input`، `public_post`، `public_job_board`، `customer_referral`، `event`، `inbound`. **لا توجد قيمة باسم scraping**؛ هذا مفروض في الكود لا في النص فقط.

Every prospect ties to a **buying-timing signal** the founder observed or sourced from public data (hiring, new branch, website update, booking link, ad spend, funding, event, partnership, launch, tender, review change, headcount growth, slow reply). Allowed sources are listed above — **scraping is not a value**, enforced in code.

```json
{
  "signal_id": "...",
  "company_label": "...",
  "signal_type": "hiring_sales_ops",
  "source": "founder_input",
  "strength": "high",
  "suggested_offer": "growth_ops_monthly_2999",
  "governance_decision": "approval_required"
}
```

---

## 4) جدول الأوزان — `score_prospect` weighting table

النتيجة من 0 إلى 100. كل مكوّن ثقة 0..1 يُضرب في وزنه. مصدر الحقيقة للأوزان هو الثابت `PROSPECT_SCORE_WEIGHTS` في [`records.py`](../../../auto_client_acquisition/gtm_os/records.py) — **لا تُعدَّل الأوزان في الوثيقة**.

The score is 0–100. Each component is a 0..1 confidence multiplied by its weight. The weights live in `PROSPECT_SCORE_WEIGHTS`; this table mirrors code and is not the source of truth.

| المكوّن — Component | الوزن — Weight | المعنى — Meaning |
|---|---|---|
| `sector_fit` | 20 | ملاءمة القطاع لـ ICP — sector fit to ICP |
| `buying_signal` | 20 | قوة إشارة التوقيت — strength of buying-timing signal |
| `lead_flow_likelihood` | 15 | احتمال تدفّق العملاء — likelihood of lead flow |
| `decision_maker_clarity` | 15 | وضوح دور صانع القرار — clarity of the decision-maker role |
| `payment_ability` | 15 | القدرة على الدفع — ability to pay |
| `personalization_signal` | 10 | إشارة تخصيص متاحة — personalization signal available |
| `risk_low` | 5 | انخفاض المخاطرة — low risk posture |
| **المجموع — Total** | **100** | |

### الطبقات — Tiers

| النتيجة — Score | الطبقة — Tier | التوصية — Recommendation |
|---|---|---|
| ≥ 70 | **A** | أولوية للمسودة والموافقة — prioritize for draft + approval |
| 50–69 | **B** | يدخل المصنع بترتيب أدنى — enters factory, lower priority |
| < 50 | **C** | تنشئة أو إعادة تأهيل — nurture or re-qualify |

التوقيع — Signature:

```python
score_prospect(*, sector_fit, buying_signal, lead_flow_likelihood,
               decision_maker_clarity, payment_ability,
               personalization_signal, risk_low) -> {"total", "tier", "breakdown"}
```

النتيجة **تقدير داخلي للترتيب**، ليست وعدًا بنتيجة بيع. The score is an **internal prioritization estimate**, never a promise of a sale.

---

## 5) دورة الحالة — Status lifecycle

| الحالة — Status | المعنى — Meaning |
|---|---|
| `new` | سجل جديد لم يُبحث — new, not yet researched |
| `researching` | بحث عام/إدخال مؤسس جارٍ — public research / founder input in progress |
| `drafted` | تم توليد مسودة (لم تُرسل) — a draft was produced (not sent) |
| `queued` | في طابور الموافقة — in the approval queue |
| `contacted` | تواصُل بعد موافقة المؤسس — contacted after founder approval |
| `replied` | ورد رد (يُوجَّه عبر `route_reply`) — replied (routed) |
| `nurture` | تنشئة لاحقة — later nurture |
| `do_not_contact` | لا يُتواصَل معه إطلاقًا — never contact |

`do_not_contact` نهائي ويُكافئ قائمة الكبح (`SuppressionEntry`). الانتقال من `drafted` إلى `contacted` لا يحدث إلا بعد بوابة الموافقة. `do_not_contact` is terminal and mirrors suppression; `drafted → contacted` only happens through the approval gate.

---

## 6) من الإشارة إلى مصنع المسودات — From signal to the draft factory

1. المؤسس أو إشارة عامة تنتج `CompanySignal`.
2. يُبنى `Prospect` ويُقيَّم عبر `score_prospect` (الطبقة A/B/C).
3. الطبقات الأعلى تُغذّي مصنع المسودات اليومي (250 مسودة، مزيج `DAILY_DRAFT_MIX`) → `OutreachDraft` في [`outreach_draft.py`](../../../auto_client_acquisition/gtm_os/outreach_draft.py).
4. كل مسودة تمر ببوابة الجودة [`draft_quality_gate.py`](../../../auto_client_acquisition/gtm_os/draft_quality_gate.py)؛ الناجحة تُوسَم `approval_required` وتدخل [طابور موافقة المؤسس](../FOUNDER_APPROVAL_QUEUE_AR.md).
5. الردود الإيجابية تُوجَّه إلى [مسار واتساب بعد الرد](../whatsapp/WHATSAPP_POST_REPLY_FLOW_AR.md) — بعد الموافقة فقط.

Signal → scored Prospect → daily draft factory → quality gate → founder approval queue → consent-gated reply flow. No step sends; every external send needs founder approval.

---

## 7) إعادة الاستخدام — لا تكرار — Reuse, not duplication

هذه الطبقة **لا تستبدل** بنية CRM القائمة؛ تربطها:

- **CRM والعملاء:** [`auto_client_acquisition/crm_v10/`](../../../auto_client_acquisition/crm_v10/) — نموذج الكائنات وآلة المراحل ودرجات الصفقة وصحة العميل بعد التأهيل.
- **مطابقة ICP:** [`auto_client_acquisition/agents/icp_matcher.py`](../../../auto_client_acquisition/agents/icp_matcher.py) — مدخل لمكوّن `sector_fit`.
- **تقييم العملاء (حتمي):** [`auto_client_acquisition/crm_v10/lead_scoring.py`](../../../auto_client_acquisition/crm_v10/lead_scoring.py) — ملاءمة + إلحاح؛ مدخل مرجعي لـ `lead_flow_likelihood`.
- **التخصيب:** [`auto_client_acquisition/enrichment_provider.py`](../../../auto_client_acquisition/enrichment_provider.py) — بيانات عامة فقط، بلا scraping.
- **العروض/الأسعار (مصدر الحقيقة):** [`auto_client_acquisition/service_catalog/registry.py`](../../../auto_client_acquisition/service_catalog/registry.py) وسلّم الأدوار في [`docs/strategic/DEALIX_ROLE_SERVICE_LADDER_AR.md`](../../strategic/DEALIX_ROLE_SERVICE_LADDER_AR.md). لا تُخترع أسعار في هذه الوثيقة.

This layer **does not replace** the existing CRM; it links to it. Prices come only from the service catalog and the role/service ladder — never invented here.

---

> القيمة التقديرية ليست قيمة مُتحقَّقة. لا تواصُل خارجي بلا موافقة المؤسس.
> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
