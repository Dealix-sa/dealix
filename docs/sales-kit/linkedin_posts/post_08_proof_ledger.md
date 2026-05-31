# Post 08 — What a proof ledger is and why we built one · ما هو proof ledger ولماذا بنيناه

**Cluster:** Technical Proof
**Best day:** Tuesday 09:00 KSA
**Expected length:** AR 700 words · EN 500 words

---

## Arabic

"كيف نعرف أن النتائج التي تذكرونها في الـ case studies حقيقية؟"

هذا أكثر سؤال يطرحه عليّ مدراء المالية والقانون في عملاء B2B
سعوديين، وهو سؤال عقلاني تمامًا. السوق مليء بـ case studies تذكر
"ارتفاع ٣٠٠٪ في الإيراد" بدون أي إثبات قابل للتحقق.

في Dealix بنينا حلًا تقنيًا لهذا اسمه **proof_ledger** — جدول
append-only في Postgres يسجل كل event يحدث في رحلة عميل:

```
event_id        UUID
customer_handle TEXT
event_type      TEXT  -- lead_intake, draft_approved, message_sent,
                       -- payment_confirmed, demo_booked, deal_won, etc.
level           TEXT  -- L0-L5 (confidence/evidence strength)
source          TEXT  -- which agent / which system / human approval
created_at      TIMESTAMPTZ
payload_jsonb   JSONB -- raw data of the event
```

**ماذا يعني هذا عمليًا؟**

- لا case study تنشر بدون citation لـ event IDs.
- كل رقم في تقرير عميل يستطيع الـ auditor تتبعه إلى event محدد في
  الـ ledger.
- إن لم يكن هناك event، الرقم لا يُنشر — حتى لو "نعرف أنه صحيح".

**الـ Levels (L0-L5) — منظومة الإثبات:**

- **L0:** ادعاء بدون شواهد (لا يُنشر أبدًا).
- **L1:** ادعاء داخلي (لا يُنشر علنًا).
- **L2:** Founder observation (لا يُنشر).
- **L3:** Customer self-report (يُنشر مع disclaimer).
- **L4:** Internal system event (يُنشر مع source).
- **L5:** Confirmed transaction + customer signature (يُنشر بدون
  تحفظ).

في الـ Proof Pack النهائية، نسمح فقط بـ L3 وما فوق. لو رقم لا
يستوفي، يبقى في خانة "Under observation" — صريح وصادق.

**لماذا هذا مهم لكم كعملاء أو شركاء؟**

١. لما نقول "ارتفع conversion rate من ١.٢٪ إلى ٢.٧٪"، نستطيع
   إعطاءكم 47 event_id الذي يثبت كل خطوة.

٢. لو SDAIA أو ZATCA طلبت audit، نستطيع تقديم evidence chain خلال
   ساعة.

٣. لو fraud في الـ proof دعينا في المستقبل، الـ ledger يُظهر متى
   حدث الـ tampering — والتأمين القانوني محفوظ.

**في المقابل، شركات الـ AI التي لا تملك proof ledger:**

- تعرض case studies بدون verifiability.
- تستخدم "بناءً على المتوسطات في القطاع" كقاع.
- لا تستطيع الرد على audit بدون chaos.

**القاعدة الذهبية:** قبل توقيع أي عقد AI في B2B، اسأل: "أرونا
كيف نتتبع رقم محدد في الـ case study إلى evidence أصلي." لو
الإجابة مرتبكة، لا توقع.

في Dealix هذه الأرقام مفتوحة. اسأل وأنا أُري.

---

## English

"How do we know the numbers in your case studies are real?"

The most frequent question from finance and legal managers at
Saudi B2B customers — and a completely rational one. The market
is full of case studies citing "300% revenue lift" with no
verifiable proof.

At Dealix we built a technical answer to this called the
**proof_ledger** — an append-only Postgres table that records
every event in a customer's journey:

```
event_id        UUID
customer_handle TEXT
event_type      TEXT  -- lead_intake, draft_approved, message_sent,
                       -- payment_confirmed, demo_booked, deal_won
level           TEXT  -- L0-L5 (confidence/evidence strength)
source          TEXT  -- which agent / which system / human approver
created_at      TIMESTAMPTZ
payload_jsonb   JSONB -- raw event data
```

**What this means in practice:**

- No case study published without citation to event IDs.
- Every number in a customer report can be traced by an auditor to
  a specific ledger event.
- If there's no event, the number doesn't publish — even if "we
  know it's true."

**The Levels (L0-L5) — the evidence framework:**

- **L0:** Claim without evidence (never published).
- **L1:** Internal claim (not published).
- **L2:** Founder observation (not published).
- **L3:** Customer self-report (publishable with disclaimer).
- **L4:** Internal system event (publishable with source).
- **L5:** Confirmed transaction + customer signature (publishable
  without caveat).

In a final Proof Pack we only allow L3+. If a number doesn't qualify
it stays in "Under observation" — explicit and honest.

**Why this matters for customers and partners:**

1. When we say "conversion rate moved from 1.2% to 2.7%," we can
   hand you 47 event_ids proving each step.
2. If SDAIA or ZATCA requests an audit, we produce the evidence
   chain in under an hour.
3. If proof fraud is alleged in the future, the ledger shows when
   tampering happened — legal protection preserved.

**In contrast, AI companies without a proof ledger:**

- Show case studies with no verifiability.
- Use "industry-average benchmarks" as floor.
- Can't respond to audit without chaos.

**The golden rule:** before signing any AI contract in B2B, ask:
"show me how to trace one specific number in a case study back to
original evidence." If the answer is muddled, don't sign.

At Dealix these numbers are open. Ask, I'll show.

---

## CTA

- AR: "نموذج proof_ledger مفتوح للنقاش الفني. DM."
- EN: "The proof_ledger architecture is open for technical
  discussion. DM."
