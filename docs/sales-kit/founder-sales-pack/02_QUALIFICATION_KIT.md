# 02 — Qualification Kit — حقيبة التأهيل

> Discovery-call script, qualifying questions, offer-recommendation logic, and an
> objection-handling sheet. Everything maps to the code in
> `auto_client_acquisition/sales_os/qualification.py`.

---

## 1. Discovery call script — سكربت مكالمة الاكتشاف (≤ 30 minutes)

The call has five sections. Stay in low-claim language: ask, do not pitch. The founder
fills the scorecard (Section 3) inline as the call runs.

### Section 1 — Open & frame (3 min)

> "Thanks for the time. This is a short call to understand your revenue motion and see
> whether Dealix fits. If it does, the next step is a free diagnostic; if it does not,
> I will say so honestly. No deck today — just questions."

### Section 2 — The situation (8 min)

Ask, listen, do not solve:
- Walk me through how a new revenue opportunity reaches your team today.
- Who owns the follow-up — one named person, or is it shared?
- Where do your contacts and account data live — CRM, spreadsheet, WhatsApp, memory?
- When you last lost a deal, what was the reason you would put on it?

### Section 3 — The eight qualifying questions (10 min)

Map each answer to a flag. These are the exact inputs to `qualify(...)`.

| # | Question to ask | Flag | Counts when... |
|---|-----------------|------|----------------|
| 1 | "What is the single revenue problem costing you most right now?" | `pain_clear` | They name one concrete, owned problem. |
| 2 | "Who on your side would own this workflow day-to-day?" | `owner_present` | A named person with authority is identified. |
| 3 | "Do you have an account/contact list you own and can share?" | `data_available` | Yes — a CSV, CRM export, or owned list exists. |
| 4 | "Are you comfortable that every message is drafted for your approval before it sends?" | `accepts_governance` | They accept the approval gate. |
| 5 | "Is there budget for a 499 SAR sprint if the diagnostic shows it is worth it?" | `has_budget` | Budget exists or is reachable. |
| 6 | "Just to be clear — are you looking for safe, consent-based outreach, not scraping or mass blasts?" | `wants_safe_methods` | They want safe methods. **If they want scraping/spam/guarantees → REJECT.** |
| 7 | "If we ranked your accounts and drafted outreach, could you see a measurable proof point in 7 days?" | `proof_path_visible` | A realistic proof path exists. |
| 8 | "If the sprint works, would a monthly retainer to keep it running make sense later?" | `retainer_path_visible` | A retainer path is plausible. |

### Section 4 — Recap & decide (5 min)

Recap what you heard in two sentences. Then tell them the next step honestly (diagnostic,
reframe, or referral). Do not promise outcomes.

### Section 5 — Close & next action (4 min)

If ACCEPT or DIAGNOSTIC_ONLY: agree the diagnostic intake will reach them within 24h, and
the diagnostic itself within 24h of submission. If REJECT/REFER_OUT: be direct and kind.

---

## 2. Qualification scorecard — بطاقة التأهيل (fill inline)

| Flag | Yes? | Weight |
|------|------|--------|
| pain_clear | ☐ | 15 |
| owner_present | ☐ | 15 |
| data_available | ☐ | 15 |
| accepts_governance | ☐ | 10 |
| has_budget | ☐ | 10 |
| wants_safe_methods | ☐ | 10 |
| proof_path_visible | ☐ | 15 |
| retainer_path_visible | ☐ | 10 |
| **Total** | | **/ 100** |

Then run the code to get the deterministic decision:

```python
from auto_client_acquisition.sales_os.qualification import qualify

result = qualify(
    pain_clear=True, owner_present=True, data_available=True,
    accepts_governance=True, has_budget=True, wants_safe_methods=True,
    proof_path_visible=True, retainer_path_visible=False,
    raw_request_text="<verbatim what the prospect asked for>",
    sector="real_estate", city="Riyadh",
)
print(result.decision, result.score, result.recommended_offer)
```

---

## 3. Offer-recommendation logic — منطق التوصية بالعرض

This mirrors `qualify(...)` exactly. **Doctrine violation always wins** — if
`raw_request_text` mentions cold WhatsApp, LinkedIn automation, scraping, or guaranteed
sales, the result is REJECT regardless of score.

| Decision | Trigger | Recommended next step |
|----------|---------|----------------------|
| **REJECT** | Doctrine violation, or `wants_safe_methods` is false | Decline politely, cite the constitution, offer the safe alternative. No follow-up. |
| **REFER_OUT** | `accepts_governance` false, or score < 45 | Refusal of the approval gate / insufficient fit. Make a partner intro if a real need exists. |
| **DIAGNOSTIC_ONLY** | Score 45–69, or score 70–84 without `data_available` | Free **Tier 0 Diagnostic**. Decide on the sprint at delivery. |
| **REFRAME** | Score 70–84 with `data_available` | The need fits, but the frame is off. Send a 3-line reframe, re-qualify. Often lands on the **Data-to-Revenue Pack**. |
| **ACCEPT** | Score ≥ 85 | Recommend the **499 SAR Revenue Intelligence Sprint** directly (after the free diagnostic). |

### Profile → ladder rung map

| Prospect profile | Likely rung |
|------------------|-------------|
| Curious, unclear pain, no data ready | Tier 0 — Free Diagnostic |
| Clear pain, named owner, owned contact list, 499 budget | Tier 1 — 499 Sprint |
| Has a messy CRM/CSV export, PII handling needed, wants accounts mined | Tier 2 — 1,500 Data Pack |
| Completed a successful pilot, wants it to keep running monthly | Tier 3 — Managed Ops 2,999–4,999/mo |
| Asking for scraping / cold WhatsApp / LinkedIn automation / guaranteed deals | **REJECT** — no rung |

---

## 4. Objection-handling sheet — ورقة معالجة الاعتراضات

Use the prospect's language. Never overpromise. Cross-link:
[`docs/29_sales_os/OBJECTION_HANDLING.md`](../../29_sales_os/OBJECTION_HANDLING.md).

### 4.1 "499 / the retainer is too expensive" — السعر مرتفع

**EN:** "Fair question. The diagnostic is free, so you decide on the 499 sprint only
after you have seen real findings on your own data. 499 SAR is a one-time, fixed price —
roughly a fraction of one closed B2B deal. If the diagnostic does not show a clear proof
path, I will tell you not to buy the sprint."

**AR:** "سؤال وجيه. التشخيص مجاني، فتقرّر بشأن سبرنت الـ499 فقط بعد أن ترى نتائج حقيقية
على بياناتك. الـ499 ريال سعر ثابت لمرة واحدة — جزء بسيط من قيمة صفقة B2B واحدة. وإن لم
يُظهر التشخيص مساراً واضحاً للإثبات، سأنصحك بعدم شراء السبرنت."

### 4.2 "Is my data safe?" — هل بياناتي آمنة؟

**EN:** "Your data stays under your ownership the whole time. We work from a list you
share, on a signed Source Passport that declares ownership, allowed use, and retention.
No PII goes into logs or telemetry — that is a hard rule enforced in code. We do not sell,
share, or scrape data. You can ask us to delete your data at any point."

**AR:** "بياناتك تبقى تحت ملكيتك طوال الوقت. نعمل من قائمة تشاركها، وبموجب جواز مصدر
موقّع يُحدّد الملكية والاستخدام المسموح ومدة الاحتفاظ. لا تدخل أي بيانات شخصية في
السجلات — قاعدة صارمة مفروضة في الكود. لا نبيع ولا نشارك ولا نستخرج البيانات. ويمكنك طلب
حذف بياناتك في أي وقت."

### 4.3 "Why not just hire a salesperson?" — لماذا لا نوظّف مندوب مبيعات؟

**EN:** "You should, when the volume justifies it — Dealix is not a replacement for a
closer. What Dealix does is the part a salesperson is worst at: consistently scoring the
whole list, drafting bilingual outreach with the evidence attached, and keeping a
governance trail. A salesperson then spends their time on calls and closing, not on
deciding who to chase. Many clients use Dealix to make a future hire more productive."

**AR:** "ينبغي ذلك حين يبرّر الحجم التوظيف — Dealix ليس بديلاً عن مُغلِق صفقات. ما يفعله
Dealix هو الجزء الأضعف لدى المندوب: ترتيب القائمة كاملةً باستمرار، وصياغة تواصل ثنائي
اللغة مع الدليل، والاحتفاظ بسجل حوكمة. عندها يقضي المندوب وقته في المكالمات والإغلاق، لا
في تحديد من يُتابع. كثير من العملاء يستخدمون Dealix لرفع إنتاجية موظف مستقبلي."

### 4.4 "What about PDPL / compliance?" — ماذا عن نظام حماية البيانات والامتثال؟

**EN:** "Dealix is built around Saudi PDPL. Three things matter: (1) we only work data you
own and have a lawful basis to use — declared in the Source Passport; (2) no outreach
sends without your explicit approval, so consent and channel choice stay with you; (3) no
PII in logs, no scraping, no third-party data harvesting — these are enforced
non-negotiables, not promises. Compliance review is documented in the Proof Pack."

**AR:** "Dealix مبني حول نظام حماية البيانات الشخصية السعودي. ثلاثة أمور: (1) نعمل فقط
على بيانات تملكها ولديك أساس نظامي لاستخدامها — مُوثَّق في جواز المصدر؛ (2) لا تُرسَل أي
رسالة دون موافقتك الصريحة، فيبقى القرار والقناة لديك؛ (3) لا بيانات شخصية في السجلات، ولا
استخراج، ولا جمع بيانات من أطراف ثالثة — ثوابت مفروضة لا وعود. وتُوثَّق مراجعة الامتثال
في حزمة الإثبات."

### 4.5 "Can you guarantee X deals / a revenue lift?" — هل تضمنون صفقات؟

**EN:** "No, and I would not trust anyone who does. Dealix promises **methodology and
audit-trail metrics**: a data-quality baseline, ranked accounts with explainable scores,
approved bilingual drafts, a 14-section Proof Pack, and at least one reusable asset.
Closed deals depend on your offer, your pricing, and your follow-through. Estimated
outcomes are not guaranteed outcomes."

**AR:** "لا، ولا تثق بمن يفعل. Dealix يَعِد بمقاييس المنهجية وسجل التدقيق: خط أساس لجودة
البيانات، حسابات مُرتّبة بدرجات قابلة للتفسير، مسودات ثنائية اللغة معتمدة، حزمة إثبات من
14 قسماً، وأصل واحد قابل لإعادة الاستخدام على الأقل. إغلاق الصفقات يعتمد على عرضك وتسعيرك
ومتابعتك. النتائج التقديرية ليست نتائج مضمونة."

### 4.6 "Can you just scrape leads / send cold WhatsApp for us?" — استخراج وإرسال بارد

**Refuse cleanly:**

**EN:** "Dealix doesn't offer scraping, cold WhatsApp, or LinkedIn automation. The safe
alternative is working the contacts you already own with consent-based, draft-only
outreach that you approve and send yourself. Want me to draft that alternative pitch?"

**AR:** "Dealix لا يقدّم استخراج البيانات ولا الواتساب البارد ولا أتمتة LinkedIn. البديل
الآمن هو العمل على جهات الاتصال التي تملكها أصلاً، بتواصل قائم على الموافقة، مسودات فقط
تعتمدها وترسلها بنفسك. هل أُجهّز لك العرض البديل؟"

---

## 5. The five decisions are the complete set

ACCEPT / DIAGNOSTIC_ONLY / REFRAME / REJECT / REFER_OUT. The founder does not invent a
sixth. Log every decision in `proof_ledger` as `event=qualify_decision`.

---

**Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.**
