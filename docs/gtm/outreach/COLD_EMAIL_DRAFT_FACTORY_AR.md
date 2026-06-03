# H1 — Cold Email Draft Factory — مصنع مسودات البريد (250/يوم)

> طبقة **Market Production OS**. هذه وثيقة **رابطة**: تشرح كيف يُنتَج 250 مسودة يوميًا وتربط الوحدات القائمة، ولا تكرّرها. المصدر البرمجي الموثوق هو الكود لا هذه الوثيقة.

## 1. المبدأ الحاكم — المسودة ليست إرسالًا (AR)

المصنع يُنتج **مسودات فقط**. كل `OutreachDraft` يولد بـ `governance_decision = "approval_required"` و`send_status = "draft"`، ولا يغادر النظام إلا عبر قائمة موافقة المؤسس في `auto_client_acquisition/approval_center/`. لا scraping، ولا واتساب بارد، ولا أتمتة LinkedIn، ولا قوائم مشتراة — هذه بنود غير قابلة للتفاوض. أي بحث عن شركة على LinkedIn يكون عبر **manual LinkedIn company search (founder-approved per call)** فقط.

- **250 مسودة/يوم مقبول. 250 إرسال/يوم ممنوع** حتى تجتاز صحة التسليم (انظر [SENDING_RAMP_OS_AR.md](SENDING_RAMP_OS_AR.md)).
- لا حقل يخزّن PII: المستلم يُعرَّف بـ `recipient_ref` معتم (هاش/معرّف CRM)، لا بريد ولا هاتف.
- مصدر البيانات **مُدخَل من المؤسس أو عام فقط** (انظر [../signals/SIGNAL_OS_AR.md](../signals/SIGNAL_OS_AR.md)).

## 1. Governing Principle — A Draft Is Not a Send (EN)

The factory produces **drafts only**. Every `OutreachDraft` is born with `governance_decision = "approval_required"` and `send_status = "draft"`, and leaves only through the founder approval queue in `auto_client_acquisition/approval_center/`. No scraping, no cold WhatsApp, no LinkedIn automation, no purchased lists — non-negotiable. Any LinkedIn lookup is **manual LinkedIn company search (founder-approved per call)** only.

- **250 drafts/day is fine. 250 sends/day is forbidden** until deliverability health passes (see [SENDING_RAMP_OS_AR.md](SENDING_RAMP_OS_AR.md)).
- No field stores PII: the recipient is an opaque `recipient_ref` (hash / CRM id), never an email or phone.
- Input data is **founder-input or public only** (see [../signals/SIGNAL_OS_AR.md](../signals/SIGNAL_OS_AR.md)).

## 2. المزيج اليومي — DAILY_DRAFT_MIX (AR)

المزيج معرّف في `auto_client_acquisition/gtm_os/outreach_draft.py` ثابتًا `DAILY_DRAFT_MIX`. مجموعه 250 مسودة عبر خمس خطوات تسلسل.

| خطوة التسلسل (`sequence_step`) | المسودات/يوم | الغرض |
|---|---|---|
| `first_touch` | 100 | لمسة أولى بأطروحة ألم + إشارة |
| `follow_up_1` | 75 | متابعة بزاوية قيمة جديدة |
| `follow_up_2` | 50 | متابعة أخيرة قبل الإغلاق المؤدب |
| `proposal_intro` | 15 | تمهيد عرض لمتفاعل مؤهَّل |
| `close_loop` | 10 | إغلاق حلقة محترم |
| **المجموع** | **250** | — |

## 2. The Daily Mix — DAILY_DRAFT_MIX (EN)

The mix is the `DAILY_DRAFT_MIX` constant in `auto_client_acquisition/gtm_os/outreach_draft.py`. It totals 250 drafts across five sequence steps.

| Sequence step (`sequence_step`) | Drafts/day | Purpose |
|---|---|---|
| `first_touch` | 100 | First touch with a pain hypothesis + signal |
| `follow_up_1` | 75 | Follow-up on a fresh value angle |
| `follow_up_2` | 50 | Final follow-up before a polite close |
| `proposal_intro` | 15 | Proposal intro for a qualified engaged contact |
| `close_loop` | 10 | Respectful loop close |
| **Total** | **250** | — |

## 3. مكوّنات كل OutreachDraft (AR)

كل مسودة يجب أن تحمل، كحد أدنى: `subject`، `body_ar`، `body_en`، `evidence_level` (واحد من L0–L5)، `risk_level`، `personalization_tier` (P0–P3)، `sequence_step`، `unsubscribe_included`، `offer`، و`offer_matched`. الاستهداف بعلامات غير شخصية: `company_label` (مثل «وكالة تسويق بالرياض — متوسطة»)، `sector`، `recipient_role` (دور لا اسم)، و`recipient_ref` المعتم. الربط بالإشارة عبر `signal_ref` (انظر [../signals/SIGNAL_OS_AR.md](../signals/SIGNAL_OS_AR.md)).

- **مستويات الأدلة L0–L5:** كل ادعاء يحتاج مصدرًا. القيمة فارغة = مفقودة = تُحجب.
- **العرض (`offer`)** يجب أن يطابق كتالوج العروض المعتمد (`offer_matched = true`)؛ التسعير محكوم في وثائق التجارة عبر سلّم الدرجات الخمس، ولا يُخترَع سعر هنا.

## 3. What Each OutreachDraft Must Contain (EN)

Every draft must carry, at minimum: `subject`, `body_ar`, `body_en`, `evidence_level` (one of L0–L5), `risk_level`, `personalization_tier` (P0–P3), `sequence_step`, `unsubscribe_included`, `offer`, and `offer_matched`. Targeting uses non-personal labels: `company_label` (e.g. "Riyadh marketing agency (mid)"), `sector`, `recipient_role` (a role, not a name), and the opaque `recipient_ref`. Signal linkage is via `signal_ref` (see [../signals/SIGNAL_OS_AR.md](../signals/SIGNAL_OS_AR.md)).

- **Evidence levels L0–L5:** every claim needs provenance. Empty value = missing = blocked.
- **The `offer`** must match the approved offer catalog (`offer_matched = true`); pricing is governed in the commercial docs via the canonical five-rung ladder, and no price is invented here.

## 4. درجات التخصيص P0–P3 (AR)

| الدرجة | المعنى | يدخل قائمة الموافقة؟ |
|---|---|---|
| **P0** | عام، لا إشارة خاصة | لا — يُحجب بـ `personalization_below_p1` |
| **P1** | إشارة قطاعية + ألم محدد | نعم (الحد الأدنى) |
| **P2** | إشارة شركة محددة + زاوية مطابِقة | نعم |
| **P3** | إشارة دور/توقيت دقيقة + عرض مطابق | نعم (الأعلى) |

P0 لا يدخل قائمة الموافقة إطلاقًا. ابدأ من P1 فما فوق.

## 4. Personalization Tiers P0–P3 (EN)

| Tier | Meaning | Enters approval queue? |
|---|---|---|
| **P0** | Generic, no specific signal | No — blocked by `personalization_below_p1` |
| **P1** | Sector signal + specific pain | Yes (the floor) |
| **P2** | Company-specific signal + matched angle | Yes |
| **P3** | Precise role/timing signal + matched offer | Yes (the ceiling) |

P0 never enters the approval queue. Start at P1 and above.

## 5. متى تدخل المسودة قائمة الموافقة فقط (AR)

المسودة تصبح **«approval_required» (جاهزة لإنسان، لا مُرسَلة تلقائيًا)** فقط حين تجتاز **كل** سطر في `auto_client_acquisition/gtm_os/draft_quality_gate.py` عبر `validate_outreach_draft()`. أي إخفاق يُرجِع `BLOCK` (أعد الصياغة قبل إعادة الإدراج). الأكواد:

| الكود | الفئة | السبب |
|---|---|---|
| `governance:*` | عقيدة | مخالفة في النص (يعيد استخدام `governance_os.policy_check_draft`) |
| `missing_unsubscribe` | امتثال | لا رابط إلغاء اشتراك (CAN-SPAM) |
| `missing_evidence_level` | امتثال | مستوى الأدلة L0–L5 غير محدد |
| `suppression_hit` | امتثال | المستلم في قائمة الكبح |
| `fake_reply_prefix` | تسليم | عنوان يبدأ بـ Re:/Fwd: في رسالة باردة |
| `misleading_subject` | تسليم | نمط سبام أو إفراط أحرف كبيرة |
| `personalization_below_p1` | جودة | التخصيص P0 |
| `offer_not_matched` | جودة | العرض غير مطابق للكتالوج |
| `risk_high` | جودة | المخاطرة مرتفعة |
| `empty_body` | جودة | النص فارغ |
| `send_without_approval` | عقيدة | حالة إرسال بلا موافقة |

الحوكمة تُورَّث من `auto_client_acquisition/governance_os/` (`policy_check_draft`, `draft_gate`)؛ لا نكرّر قواعدها هنا.

## 5. When a Draft Enters the Approval Queue Only (EN)

A draft becomes **"approval_required" (ready for a human, never auto-sent)** only when it passes **every** line of `auto_client_acquisition/gtm_os/draft_quality_gate.py` via `validate_outreach_draft()`. Any failure returns `BLOCK` (rewrite before re-queue). The codes:

| Code | Category | Reason |
|---|---|---|
| `governance:*` | doctrine | Copy violation (reuses `governance_os.policy_check_draft`) |
| `missing_unsubscribe` | compliance | No unsubscribe link (CAN-SPAM) |
| `missing_evidence_level` | compliance | Evidence level L0–L5 missing |
| `suppression_hit` | compliance | Recipient on the suppression list |
| `fake_reply_prefix` | deliverability | Subject starts with Re:/Fwd: on a cold message |
| `misleading_subject` | deliverability | Spam pattern or ALL-CAPS over-use |
| `personalization_below_p1` | quality | Personalization is P0 |
| `offer_not_matched` | quality | Offer not matched to the catalog |
| `risk_high` | quality | Risk level is high |
| `empty_body` | quality | Body is empty |
| `send_without_approval` | doctrine | Send/queued state without approval |

Governance is inherited from `auto_client_acquisition/governance_os/` (`policy_check_draft`, `draft_gate`); we do not duplicate those rules here.

## 6. تشغيل البوابة (AR)

شغّل البوابة على ملف مسودات JSONL عبر `scripts/gtm_quality_gate.py`. وضع التدقيق هو الافتراضي؛ استخدم `--require-all-pass` على ملف **إنتاجي** قبل الإدراج للموافقة. الأمر اليومي الكامل في `scripts/gtm_daily_command.py`، والعينات تُولَّد بـ `scripts/gtm_seed_samples.py`. مخطط `outreach_draft.schema.json` في `dealix/contracts/schemas/`، والعينات في `data/gtm/outreach/*.sample.jsonl`.

```text
python3 scripts/gtm_quality_gate.py \
  --input data/gtm/outreach/drafts.sample.jsonl \
  --suppression data/gtm/suppression/suppression.sample.jsonl \
  --report reports/gtm/DRAFT_QUALITY_REPORT.md
```

## 6. Running the Gate (EN)

Run the gate over a JSONL drafts file via `scripts/gtm_quality_gate.py`. Audit mode is the default; use `--require-all-pass` on a **production** file before queueing for approval. The full daily command is `scripts/gtm_daily_command.py`, and samples are generated by `scripts/gtm_seed_samples.py`. The `outreach_draft.schema.json` lives in `dealix/contracts/schemas/`, with samples in `data/gtm/outreach/*.sample.jsonl`.

```text
python3 scripts/gtm_quality_gate.py \
  --input data/gtm/outreach/drafts.sample.jsonl \
  --suppression data/gtm/suppression/suppression.sample.jsonl \
  --report reports/gtm/DRAFT_QUALITY_REPORT.md
```

## روابط مرجعية / Related

- [SENDING_RAMP_OS_AR.md](SENDING_RAMP_OS_AR.md) — خطة الإرسال الآمن / safe sending plan.
- [DELIVERABILITY_AND_COMPLIANCE_AR.md](DELIVERABILITY_AND_COMPLIANCE_AR.md) — التسليم والامتثال / deliverability + compliance.
- [REPLY_HANDLING_OS_AR.md](REPLY_HANDLING_OS_AR.md) — معالجة الردود / reply handling.
- [../signals/SIGNAL_OS_AR.md](../signals/SIGNAL_OS_AR.md) — الإشارات / signals.
- [../../05_governance_os/GOVERNANCE_OS.md](../../05_governance_os/GOVERNANCE_OS.md) — الحوكمة / governance.

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
