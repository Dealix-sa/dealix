# H1 — Signal OS — نظام إشارات توقيت الشراء

> طبقة **Market Production OS**. هذه وثيقة **رابطة**: تشرح كيف نلتقط إشارات توقيت الشراء (مُدخَلة من المؤسس أو عامة فقط)، وكيف تغذّي العملاء المحتملين والمسودات. تربط الوحدات القائمة ولا تكرّرها. المصدر البرمجي الموثوق هو الكود لا هذه الوثيقة.

## 1. المبدأ الحاكم — لا scraping إطلاقًا (AR)

كل إشارة في `auto_client_acquisition/gtm_os/records.py` (`CompanySignal`, ثابتا `SIGNAL_TYPES` و`SIGNAL_SOURCES`) هي **ملاحظة مُدخَلة من المؤسس أو من مصدر عام فقط**. لا scraping، ولا جمع ويب غير مصرّح، ولا قوائم مشتراة — بند غير قابل للتفاوض. أي بحث عن شركة على LinkedIn يكون **manual LinkedIn company search (founder-approved per call)** فقط. كل سجل خالٍ من PII: الشركة `company_label` (لا اسم شخص)، والدور دور لا اسم، ويولد بـ `governance_decision = "approval_required"`.

## 1. Governing Principle — No Scraping, Ever (EN)

Every signal in `auto_client_acquisition/gtm_os/records.py` (`CompanySignal`, the `SIGNAL_TYPES` and `SIGNAL_SOURCES` constants) is a **founder-input or public observation only**. No scraping, no unauthorized web collection, no purchased lists — non-negotiable. Any LinkedIn lookup is **manual LinkedIn company search (founder-approved per call)** only. Every record is PII-free: the company is a `company_label` (never a person's name), the role is a role not a name, and it is born with `governance_decision = "approval_required"`.

## 2. مصادر الإشارات (AR)

`SIGNAL_SOURCES` ست مصادر مسموحة — **لا «scraping» بينها**:

| المصدر (`source`) | المعنى |
|---|---|
| `founder_input` | ملاحظة مباشرة من المؤسس |
| `public_post` | منشور عام (موقع/مدونة/إعلان عام) |
| `public_job_board` | إعلان وظيفة على لوحة عامة |
| `customer_referral` | تحويل من عميل قائم |
| `event` | لقاء/فعالية حضرها المؤسس |
| `inbound` | اهتمام وارد بادر به الطرف الآخر |

## 2. Signal Sources (EN)

`SIGNAL_SOURCES` is six allowed sources — **none of them is "scraping"**:

| Source (`source`) | Meaning |
|---|---|
| `founder_input` | A direct observation by the founder |
| `public_post` | A public post (site / blog / public ad) |
| `public_job_board` | A job posting on a public board |
| `customer_referral` | A referral from an existing customer |
| `event` | A meeting / event the founder attended |
| `inbound` | Inbound interest initiated by the other party |

## 3. أنواع الإشارات والزاوية المقترحة (AR)

`SIGNAL_TYPES` تغطّي إشارات توقيت الشراء. كل إشارة تحمل `strength` (low/medium/high) و`suggested_offer` وزاوية ثنائية اللغة (`suggested_angle_ar/en`):

| النوع (`signal_type`) | لماذا يهم | زاوية مقترحة |
|---|---|---|
| `hiring_sales_ops` | ضغط أنابيب / توسع مبيعات | تنظيم عمليات الإيراد |
| `hiring_crm_manager` | نضج عمليات CRM | بيانات إلى إيراد |
| `hiring_marketing` | استثمار في الطلب | جودة الليدز وتأهيلها |
| `hiring_support` | نمو حجم العملاء | تشغيل ردود مُحوكَم |
| `new_branch` | توسع جغرافي | أنبوب للفرع الجديد |
| `new_ad_spend` | استثمار بالطلب | تحويل الإنفاق إلى ليدز مؤهَّلة |
| `funding` | نافذة شراء | تهيئة ذكاء مخصّص |
| `tender` | B2B رسمي | حزمة إثبات للمناقصة |
| `product_launch` | تفعيل سوق | تشخيص فجوات النمو |
| `partnership` | قنوات جديدة | تشغيل إيرادات مُدار |
| `headcount_growth` | نمو تنظيمي | جاهزية بيانات |
| `review_change` | ضغط تجربة | معالجة ردود مُحوكَمة |
| `slow_reply` | تسريب فرص | سرعة استجابة |

بقية الأنواع (`website_update`, `booking_link`, `event_attendance`) في الثابت نفسه. قائمة الإشارات الأوسع وزواياها في [../../MARKET_RADAR_SIGNALS.md](../../MARKET_RADAR_SIGNALS.md)؛ لا نكرّرها هنا.

## 3. Signal Types and Suggested Angle (EN)

`SIGNAL_TYPES` covers buying-timing signals. Each signal carries `strength` (low/medium/high), a `suggested_offer`, and a bilingual angle (`suggested_angle_ar/en`):

| Type (`signal_type`) | Why it matters | Suggested angle |
|---|---|---|
| `hiring_sales_ops` | Pipeline pressure / sales expansion | Organize revenue operations |
| `hiring_crm_manager` | CRM operations maturing | Data to revenue |
| `hiring_marketing` | Investing in demand | Lead quality and qualification |
| `hiring_support` | Growing customer volume | Governed reply operations |
| `new_branch` | Geographic expansion | Pipeline for the new branch |
| `new_ad_spend` | Investing in demand | Turn spend into qualified leads |
| `funding` | Buying window | Custom AI setup |
| `tender` | Formal B2B | Proof pack for the tender |
| `product_launch` | Market activation | Growth-gap diagnostic |
| `partnership` | New channels | Managed revenue ops |
| `headcount_growth` | Organizational growth | Data readiness |
| `review_change` | Experience pressure | Governed reply handling |
| `slow_reply` | Opportunity leakage | Response speed |

The remaining types (`website_update`, `booking_link`, `event_attendance`) are in the same constant. The wider signal catalog and angles live in [../../MARKET_RADAR_SIGNALS.md](../../MARKET_RADAR_SIGNALS.md); we do not duplicate them here.

## 4. قوة الإشارة (AR)

`strength` ثلاث درجات: `low`, `medium`, `high` (الافتراضي `medium`). القوة تعكس وضوح التوقيت لا حجم الصفقة. إشارة `high` حديثة (مثل `funding` أو `tender`) ترفع وزن `buying_signal` في ترتيب العميل المحتمل. كل إشارة تتطلّب `evidence_note` — مصدرًا يمكن مراجعته — تماشيًا مع انضباط الأدلة في طبقة المصنع.

## 4. Signal Strength (EN)

`strength` has three levels: `low`, `medium`, `high` (default `medium`). Strength reflects timing clarity, not deal size. A fresh `high` signal (e.g. `funding` or `tender`) raises the `buying_signal` weight in prospect scoring. Every signal requires an `evidence_note` — a reviewable source — consistent with the evidence discipline in the factory layer.

## 5. كيف تغذّي الإشارات العملاء والمسودات (AR)

الإشارة تربط بالعميل المحتمل عبر `signal_ref`، والمسودة تربط بالإشارة عبر `signal_ref` أيضًا (انظر [../outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md](../outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md)). دالة `score_prospect()` ترتّب العميل 0–100 بأوزان:

| المكوّن | الوزن |
|---|---|
| `sector_fit` | 20 |
| `buying_signal` | 20 |
| `lead_flow_likelihood` | 15 |
| `decision_maker_clarity` | 15 |
| `payment_ability` | 15 |
| `personalization_signal` | 10 |
| `risk_low` | 5 |

الدرجات: A ≥ 70، B ≥ 50، وإلا C. الإشارة القوية ترفع `buying_signal` و`personalization_signal`، فتنتقل إلى تخصيص أعلى (P2/P3) في المصنع. مطابقة العميل والترتيب تُكمَّل بـ `agents/icp_matcher.py` و`agents/lead_scoring.py` و`auto_client_acquisition/crm_v10/`.

## 5. How Signals Feed Prospects and Drafts (EN)

A signal links to a prospect via `signal_ref`, and a draft links to the signal via `signal_ref` too (see [../outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md](../outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md)). `score_prospect()` ranks a prospect 0–100 with weights:

| Component | Weight |
|---|---|
| `sector_fit` | 20 |
| `buying_signal` | 20 |
| `lead_flow_likelihood` | 15 |
| `decision_maker_clarity` | 15 |
| `payment_ability` | 15 |
| `personalization_signal` | 10 |
| `risk_low` | 5 |

Tiers: A ≥ 70, B ≥ 50, else C. A strong signal raises `buying_signal` and `personalization_signal`, lifting the prospect to a higher personalization tier (P2/P3) in the factory. Prospect matching and scoring are complemented by `agents/icp_matcher.py`, `agents/lead_scoring.py`, and `auto_client_acquisition/crm_v10/`.

## 6. العقود والعينات (AR)

مخطط `company_signal.schema.json` و`prospect.schema.json` في `dealix/contracts/schemas/`، والعينات في `data/gtm/signals/*.sample.jsonl` و`data/gtm/prospects/*.sample.jsonl`. تُولَّد بـ `scripts/gtm_seed_samples.py`. مصدر إشارات الرادار التشغيلي في `auto_client_acquisition/radar_events/` و`market_intelligence/`.

## 6. Contracts and Samples (EN)

The `company_signal.schema.json` and `prospect.schema.json` schemas live in `dealix/contracts/schemas/`, with samples in `data/gtm/signals/*.sample.jsonl` and `data/gtm/prospects/*.sample.jsonl`. They are generated by `scripts/gtm_seed_samples.py`. The operational radar signal source lives in `auto_client_acquisition/radar_events/` and `market_intelligence/`.

## روابط مرجعية / Related

- [../outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md](../outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md) — مصنع المسودات / the draft factory.
- [../outreach/REPLY_HANDLING_OS_AR.md](../outreach/REPLY_HANDLING_OS_AR.md) — معالجة الردود / reply handling.
- [../../MARKET_RADAR_SIGNALS.md](../../MARKET_RADAR_SIGNALS.md) — قائمة إشارات الرادار / market radar signal catalog.
- [../../OFFER_LADDER_AND_PRICING.md](../../OFFER_LADDER_AND_PRICING.md) — سلّم الدرجات الخمس / the five-rung ladder.

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
