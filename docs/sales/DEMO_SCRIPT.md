# Demo Script · سكريبت العرض (30 min)

> Bilingual structure. Customer speaks 60%, you speak 40%. Doctrine
> stays visible the entire call. No screen share until minute 10.

**Pre-call checklist (the morning of):**
- [ ] Pull customer's HubSpot profile (or `pipeline_leads` row)
- [ ] Open `/founder-leads.html` filtered to their company
- [ ] Have `data/demos/sample_saudi_b2b.csv` ready (offline fallback)
- [ ] WhatsApp Decision Bot accessible (in case of urgent draft)
- [ ] Doctrine page open: `docs/architecture/AGENTS.md` (for reference)

---

## Minute 0-3 · Rapport (3 min) · بناء العلاقة

**Goal:** establish trust, confirm the call is the right time.

**Founder opening (AR):** "السلام عليكم {{lead_name}}، شكرًا على وقتك. قبل
ما نبدأ — هل ما زال الـ ٣٠ دقيقة مناسبة لك؟ ولو احتجت توقف في أي
لحظة لرد سؤال، فقط افعل."

**Founder opening (EN):** "Hello {{lead_name}}, thank you for the time.
Before we start — is the 30-minute window still good? And if you
need to stop at any point to ask a question, just do."

**Listen for:** energy level, who else is on the call, any context
shifts (PO change, leadership update).

---

## Minute 3-10 · Discovery (7 min) · الاكتشاف

**Goal:** understand THEIR situation in their words. NEVER lead the
witness.

**Open question (AR):** "في كلمتك، ما هي أكبر فجوة في
{{their_revenue_function}} الآن؟"

**Open question (EN):** "In your own words, what is the biggest gap
in {{their_revenue_function}} right now?"

**Listen for (and record in HubSpot during the call):**
- Specific friction points (named)
- Tools they're already using
- Who suffers when the gap is unresolved
- Budget signal (don't ask directly — listen)
- Authority signal (who decides)

**Bridge to demo (only when 1+ pain is clearly named):**
"دعني أُريك ما لاحظنا في شركات قطاع {{sector}} بهذا الوضع تحديدًا."

---

## Minute 10-20 · Demo on their scenario (10 min) · العرض على وضعهم

**Goal:** show the proof loop using their language. NEVER pitch
features.

**Live workflow on screen:**
1. Open `frontend/src/app/[locale]/ops/cockpit` — show the 7 panels.
2. Open `/api/v1/founder/dashboard/cockpit` JSON view briefly.
3. Show one Sprint checklist (`/api/v1/sprint/{run_id}/checklist`).
4. Show one approval queue item — emphasize "this never sends without
   me clicking approve."
5. Show one Proof Pack section — point to is_estimate flags.

**Key phrases to repeat (intentionally):**
- AR: "لا شيء يخرج بدون موافقتي."
- EN: "Nothing goes out without my approval."
- AR: "كل رقم ترونه له مصدر مسجّل."
- EN: "Every number you see has a recorded source."

**Avoid:**
- Long product tours
- Feature lists
- Comparisons to competitors by name

---

## Minute 20-25 · ROI + pricing (5 min) · العائد والسعر

**Goal:** tie deliverables to their specific scenario. Honest math
only.

**Frame (AR):** "بناءً على ما شاركته، الـ Sprint بـ ٤٩٩ ر.س يجاوب على
السؤال: 'كم من leads حاليًا قابل للتحويل لو طبقنا ICP-fit ranking
عليها؟' السعر يساوي ساعة عمل مدير مبيعات واحد."

**Frame (EN):** "Based on what you shared, the 499 SAR Sprint answers
the question: 'how many current leads are convertible if we apply
ICP-fit ranking?' The price equals one sales manager hour."

**Show the 5-rung ladder briefly (15 sec each):**
1. Free Diagnostic — 24h, no commitment
2. 1 SAR — verify the loop
3. 499 Sprint — 7 days
4. 2,999 Growth — monthly retainer
5. Custom AI — scoped engagement

**Never:**
- Quote a revenue uplift figure
- Compare your pricing to competitors
- Discount on the first call

---

## Minute 25-28 · Pilot offer (3 min) · العرض

**Goal:** propose the next concrete step. Give 3 options always.

**Three paths (AR):**
1. "نبدأ Free Diagnostic الآن — ٦ أسئلة، رد خلال ٢٤ ساعة."
2. "نوقّع Sprint اليوم، نبدأ غدًا بعد توقيع الـ DPA."
3. "أرسل لك ١-pager للمراجعة الداخلية، نتحدث بعد ٤٨ ساعة."

**Three paths (EN):**
1. "Start the Free Diagnostic right now — 6 questions, 24h reply."
2. "Sign the Sprint today, start tomorrow after DPA signature."
3. "I send you a 1-pager for internal review, we talk in 48h."

**Listen for which option energizes them.** Don't push.

---

## Minute 28-30 · Next steps (2 min) · الخطوات التالية

**Confirm in writing (within 1 hour of call ending):**
- Option chosen (or "none, will revisit")
- Specific next action (with date)
- Who else needs to be in the loop
- DPA link if applicable

**Founder closing (AR):** "شكرًا {{lead_name}}، تجربتك تساعدنا. سأرسل
ملخصًا خلال ساعة، وأي سؤال — WhatsApp مفتوح."

**Founder closing (EN):** "Thank you {{lead_name}}, your input helps
us. I'll send a summary within an hour — any questions, WhatsApp is
open."

---

## Post-call ritual (within 30 min)

1. Log call notes in HubSpot
2. Update `pipeline_leads.last_status_change`
3. Queue follow-up email draft in `approval_center`
4. If proposal needed: render `docs/sales/PROPOSAL_TEMPLATE.md`
   with their merge fields → approval queue
5. Record any objections raised in `docs/sales/OBJECTION_HANDLING.md`
   if they're new

---

## Doctrine reminders (visible to founder, never to customer)

- Customer speaks 60%, you 40% — if reversed, slow down
- No autonomous send promises — restate it whenever asked
- Never compare to a named competitor
- "I don't know" is a valid answer — never invent
- Every revenue claim cites a public benchmark or "is_estimate=True"
- If a pain falls outside the doctrine (wants LinkedIn automation,
  wants cold WhatsApp, wants guaranteed close rate) — politely
  decline; the doctrine IS the product

---

## Failure modes (what NOT to do)

- ❌ Open with "Dealix is the leading..." (chest-beating; lose trust)
- ❌ "We've helped X customers..." without naming the proof_ledger
- ❌ "Don't worry, we handle everything" (false; you approve everything)
- ❌ Discount when asked (signals weakness; deflect to scope reduction)
- ❌ Promise a specific result number (Doctrine #6)
- ❌ Take over the screen for >5 min straight (customer disengages)
- ❌ Skip the "what's the biggest gap" question (you'll be selling
  blindly)
