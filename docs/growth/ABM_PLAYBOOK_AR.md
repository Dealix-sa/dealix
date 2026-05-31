# ABM Playbook — كتاب لعب الحسابات المستهدفة

> Section 34. خط أنابيب 10 مراحل لـ Account-Based Motion داخل Dealix. كل المخرجات metadata + drafts. لا إرسال خارجي بدون موافقة بشرية.
> Module path: `dealix/growth_os/abm_engine/`

---

## مقدّمة — Introduction

ABM في Dealix ليس "إرسال جماعي مخصَّص". هو معرفة عميقة بحساب واحد، مدعومة بإشارة عامة، ومُتَوَّجة برسالة واحدة يوقّعها المؤسس. كل خطوة قابلة للتدقيق.

ABM at Dealix is not "personalized blast". It is deep, public-source-only enrichment of a single account, anchored to a signal, ending in a single message approved by a human.

---

## خط الأنابيب — The 10-Stage Pipeline

| المرحلة | Stage | المُخرَج | أداة |
|---|---|---|---|
| 1 | Account Discovery | قائمة 25–50 حساب مرشَّح | SignalRadar + ICPProfile |
| 2 | Public Enrichment | AccountCard مبدئي (website, sector, size, public news) | OSINT layer (public sources only) |
| 3 | Signal Match | ربط الحساب بـ SignalCard فعّال | signal_radar/match |
| 4 | Fit Score | درجة 0–100 على ICP fit | icp_intelligence/score |
| 5 | Stakeholder Map | أدوار عامة فقط (LinkedIn public titles) | metadata only — no scraping of contacts |
| 6 | Insight Brief | ملخّص 1 صفحة: لماذا هذا الحساب الآن؟ | content_to_revenue/brief |
| 7 | Message Draft | رسالة مسوّدة (LinkedIn DM أو إيميل) — لا تُرسَل | direct_outreach/draft |
| 8 | Founder Approval | المؤسس يراجع، يعدّل، يوقّع، يُرسل يدويّاً | governance/approval |
| 9 | Conversation Log | تسجيل الردّ، next step، disqualification | crm/conversation |
| 10 | Outcome & Attribution | RevenueRecord أو DisqualificationRecord مع AttributionRecord | attribution/record |

---

## AccountCard JSON example

```json
{
  "account_id": "ACC-2026-0042",
  "company_name_display": "Agency X",
  "company_name_internal": "<TBD: founder fill>",
  "sector": "marketing_agency",
  "country": "SA",
  "city": "Riyadh",
  "size_band": "11-50",
  "icp_match": "agencies",
  "fit_score": 78,
  "signal_link": {
    "signal_id": "SIG-2026-0117",
    "signal_type": "sdaia_framework_update",
    "source_url": "https://sdaia.gov.sa/<public-page>",
    "captured_at": "2026-05-20T09:00:00+03:00"
  },
  "public_stakeholders": [
    {"role_public": "Founder/CEO", "channel": "linkedin_public_profile"},
    {"role_public": "Head of AI", "channel": "linkedin_public_profile"}
  ],
  "insight_brief_id": "INS-2026-0042",
  "message_draft_id": "MSG-2026-0042",
  "approval_status": "pending_founder_review",
  "outreach_status": "not_sent",
  "disclosures": [
    "Enrichment uses public sources only.",
    "No automated external sends; founder approval required."
  ]
}
```

---

## ABM Agent Roles (metadata only)

| Agent | Responsibility | يُسمح بـ | يُرفض |
|---|---|---|---|
| `signal_radar_agent` | يلتقط ويصنّف SignalCards | RSS عامة، صفحات حكومية | scraping خاص، شراء قوائم |
| `account_enricher_agent` | يبني AccountCard من مصادر علنيّة | LinkedIn public, company website | كشط emails/phones |
| `fit_scorer_agent` | يحسب fit_score | ICPProfile + AccountCard | تخمين بيانات مالية |
| `insight_brief_agent` | يصيغ 1-pager لماذا الآن | SignalCard + AccountCard | ادعاءات بلا مصدر |
| `message_drafter_agent` | يصيغ رسالة مسوّدة واحدة | tone guide + AccountCard | إرسال خارجي |
| `governance_reviewer_agent` | يطبّق claim-safety + PDPL check | policy registry | bypass approval |
| `attribution_agent` | يربط الإيراد بـ Signal + Message | RevenueRecord | تضخيم النتائج |

> ملاحظة: كل الـ agents تكتب metadata. الإرسال الفعلي يتمّ يدويّاً من المؤسس عبر قناته الشخصية.

---

## Worked Example — "Agency X"

**Context.** وكالة تسويق في الرياض، 24 موظف، عملاء B2B.

1. **Discovery.** ظهرت ضمن 30 وكالة في قائمة Riyadh-agencies-2026.
2. **Enrichment.** AccountCard مبني من موقعهم العام + LinkedIn page.
3. **Signal Match.** SDAIA نشرت إطار حوكمة AI جديد قبل 5 أيام → SignalCard SIG-2026-0117.
4. **Fit Score.** 78/100 (ICP = agencies, size match, signal relevance high).
5. **Stakeholder Map.** Founder + Head of Strategy (روابط LinkedIn عامة فقط).
6. **Insight Brief.** "وكالات الرياض ستُسأل عن AI compliance خلال 60 يوم — جاهزيتكم؟"
7. **Message Draft.** رسالة LinkedIn DM واحدة، 90 كلمة، تنتهي بـ CTA لقاء 20 دقيقة.
8. **Approval.** المؤسس يعدّل الفقرة الأخيرة، يوافق، ويرسل من حسابه.
9. **Conversation Log.** ردّ بعد 3 أيام → اجتماع.
10. **Outcome.** اجتماع → مقترح Governance Snapshot بقيمة `<TBD: founder fill>` ر.س → AttributionRecord يربط الإيراد بـ SIG-2026-0117.

---

## Refusal triggers — متى يرفض المحرّك العمل

- لا signal عام مرتبط بالحساب → ارفض الرسالة.
- fit_score < 50 → ضع الحساب في nurture، لا تواصل.
- المؤسس لم يوافق خلال 72 ساعة → ألغِ المسودة.
- الحساب طلب "remove me" سابقاً → إضافة دائمة لـ do-not-contact.

---

## How to verify

```bash
bash scripts/growth_os_master_verify.sh
```

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
