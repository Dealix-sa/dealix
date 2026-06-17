# H1 — Deliverability & Compliance — التسليم والامتثال للبريد الخارجي

> طبقة **Market Production OS**. هذه وثيقة **رابطة**: تجمع قواعد التسليم والامتثال للبريد الخارجي وتربط الوحدات القائمة ولا تكرّرها. المصدر البرمجي والقانوني الموثوق هو الكود والمستشار القانوني، لا هذه الوثيقة.

## 1. المبدأ الحاكم — البريد امتياز لا حق (AR)

التسليم إلى صندوق الوارد امتياز يُكتسب بالسمعة والامتثال. كل إرسال خارجي يتطلّب: موافقة المؤسس عبر `auto_client_acquisition/approval_center/`، رابط إلغاء اشتراك حاضرًا، ومرورًا عبر `auto_client_acquisition/safe_send_gateway/`. **المصدر مُدخَل من المؤسس أو عام فقط — لا scraping ولا قوائم مشتراة.** أي بحث عن شركة على LinkedIn يكون **manual LinkedIn company search (founder-approved per call)** فقط. الحجم محكوم بالمنحنى في [SENDING_RAMP_OS_AR.md](SENDING_RAMP_OS_AR.md).

## 1. Governing Principle — Inbox Is a Privilege, Not a Right (EN)

Inbox delivery is a privilege earned through reputation and compliance. Every external send requires: founder approval via `auto_client_acquisition/approval_center/`, a present unsubscribe link, and passage through `auto_client_acquisition/safe_send_gateway/`. **Data is founder-input or public only — no scraping, no purchased lists.** Any LinkedIn lookup is **manual LinkedIn company search (founder-approved per call)** only. Volume is governed by the curve in [SENDING_RAMP_OS_AR.md](SENDING_RAMP_OS_AR.md).

## 2. مصادقة الدومين — SPF / DKIM / DMARC (AR)

السمعة تبدأ من المصادقة. سجلات DNS الكاملة والقيم في [../../ops/EMAIL_DELIVERABILITY.md](../../ops/EMAIL_DELIVERABILITY.md)؛ لا نكرّرها هنا بل نلخّص الغرض:

| السجل | الغرض |
|---|---|
| **SPF** | يعلن من يحق له الإرسال نيابة عن الدومين (`v=spf1 … -all`) |
| **DKIM** | توقيع تشفيري يثبت عدم العبث بالرسالة |
| **DMARC** | سياسة المحاذاة والتقارير؛ ابدأ بـ `p=quarantine` ثم `p=reject` بعد 30 يومًا نظيفًا |

## 2. Domain Authentication — SPF / DKIM / DMARC (EN)

Reputation starts with authentication. Full DNS records and values are in [../../ops/EMAIL_DELIVERABILITY.md](../../ops/EMAIL_DELIVERABILITY.md); we do not duplicate them — we summarize purpose:

| Record | Purpose |
|---|---|
| **SPF** | Declares who may send for the domain (`v=spf1 … -all`) |
| **DKIM** | Cryptographic signature proving the message was not altered |
| **DMARC** | Alignment + reporting policy; start at `p=quarantine`, move to `p=reject` after 30 clean days |

## 3. دومين إرسال منفصل (AR)

ابدأ على Gmail الشخصي بحدود منخفضة، ثم انقل الإرسال إلى **دومين منفصل تتحكّم به** بعد أول pilots مدفوعة (انظر المرحلتين في [../../ops/EMAIL_DELIVERABILITY.md](../../ops/EMAIL_DELIVERABILITY.md)). الفصل يحمي الدومين الأساسي للشركة من أي ضرر سمعة، ويُبقي إشارات الإرسال البارد معزولة عن البريد المعاملاتي. الإحماء يتبع منحنى الترقّي، لا قفزة مفاجئة.

## 3. Separate Sending Domain (EN)

Start on personal Gmail at low limits, then move sending to a **separate domain you control** after the first paid pilots (see the two phases in [../../ops/EMAIL_DELIVERABILITY.md](../../ops/EMAIL_DELIVERABILITY.md)). Separation protects the company's primary domain from any reputation damage and keeps cold-send signals isolated from transactional mail. Warm-up follows the ramp curve, never a sudden jump.

## 4. متطلبات مرسِلي Google (AR)

قواعد مرسِلي Google السائبة (تنطبق عند الحجوم الأعلى إلى صناديق المستهلكين): **List-Unsubscribe بنقرة واحدة (RFC 8058)** في كل إرسال، **معدل شكاوى سبام < 0.3%** (استهدف < 0.1%)، ومصادقة دومين قائمة (SPF/DKIM/DMARC). الدالة `auto_client_acquisition/email/deliverability_check.py` تفحص الجاهزية التشغيلية. أي حالة `unhealthy/bounce_spike/spam_warning` تحجب كل الإرسال في المخطِّط.

## 4. Google Sender Requirements (EN)

Google's bulk sender rules (apply at higher volumes to consumer inboxes): **one-click List-Unsubscribe (RFC 8058)** on every send, **spam-complaint rate < 0.3%** (target < 0.1%), and standing domain authentication (SPF/DKIM/DMARC). `auto_client_acquisition/email/deliverability_check.py` checks operational readiness. Any `unhealthy/bounce_spike/spam_warning` state blocks all sending in the planner.

## 5. CAN-SPAM — القواعد الأربع (AR)

البوابة `auto_client_acquisition/gtm_os/draft_quality_gate.py` تُنفِّذ هذه القواعد كأكواد إخفاق:

| القاعدة | كيف تُنفَّذ |
|---|---|
| **لا عنوان مُضلِّل** | `misleading_subject` (أنماط سبام/أحرف كبيرة) + `fake_reply_prefix` (لا Re:/Fwd: في رسالة باردة) |
| **خيار إلغاء واضح يُحترَم بسرعة** | `missing_unsubscribe` يحجب أي مسودة بلا opt-out؛ الإلغاء → كبح فوري |
| **عنوان بريدي صحيح** | يُدرَج عنوان بريدي فعلي في تذييل الرسالة (سياسة المحتوى) |
| **لا خداع** | `governance:*` يعيد استخدام `governance_os.policy_check_draft` لحجب الادعاءات الكاذبة/المضمونة |

## 5. CAN-SPAM — The Four Rules (EN)

`auto_client_acquisition/gtm_os/draft_quality_gate.py` enforces these as fail codes:

| Rule | How it is enforced |
|---|---|
| **No misleading subject** | `misleading_subject` (spam patterns / ALL-CAPS) + `fake_reply_prefix` (no Re:/Fwd: on a cold message) |
| **Clear opt-out, honored promptly** | `missing_unsubscribe` blocks any draft without an opt-out; unsubscribe → immediate suppression |
| **Valid postal address** | A real postal address is included in the message footer (content policy) |
| **No deception** | `governance:*` reuses `governance_os.policy_check_draft` to block false / guaranteed claims |

## 6. الكبح ومعالجة الارتداد (AR)

قائمة الكبح قطعية. أسباب الكبح (`records.SUPPRESSION_REASONS`): `unsubscribe`, `complaint`, `bounce`, `angry`, `manual`. أي ارتداد (bounce) أو شكوى أو طلب إلغاء أو رد غاضب → `SuppressionEntry` فورًا و`permanent = true`. المخطِّط في [SENDING_RAMP_OS_AR.md](SENDING_RAMP_OS_AR.md) يستبعد أي `recipient_ref` مكبوح بـ `suppression_hit`، والبوابة تحجب المسودة بنفس الكود. منطق تصنيف الردود وتوليد الكبح في [REPLY_HANDLING_OS_AR.md](REPLY_HANDLING_OS_AR.md) و`auto_client_acquisition/email/reply_classifier.py`.

## 6. Suppression and Bounce Handling (EN)

The suppression list is absolute. Suppression reasons (`records.SUPPRESSION_REASONS`): `unsubscribe`, `complaint`, `bounce`, `angry`, `manual`. Any bounce, complaint, unsubscribe, or angry reply → a `SuppressionEntry` immediately, with `permanent = true`. The planner in [SENDING_RAMP_OS_AR.md](SENDING_RAMP_OS_AR.md) excludes any suppressed `recipient_ref` as `suppression_hit`, and the gate blocks the draft on the same code. Reply classification and suppression generation live in [REPLY_HANDLING_OS_AR.md](REPLY_HANDLING_OS_AR.md) and `auto_client_acquisition/email/reply_classifier.py`.

## 7. مؤشرات PDPL السعودي (AR)

للقرّاء السعوديين: حدّد في كل عرض/pilot من هو **المتحكّم** (عادة العميل) ومن هو **المعالج** (Dealix بتعليمات العميل)، والأساس القانوني، وقنوات حقوق الأفراد. التفاصيل الكاملة وسجل الموافقات وROPA وطلبات أصحاب البيانات في [../../PRIVACY_PDPL_READINESS.md](../../PRIVACY_PDPL_READINESS.md) و`auto_client_acquisition/compliance_os/` (`consent_ledger`, `contactability`, `ropa`, `data_subject_requests`). لا نكرّر السياسة هنا — هذه الطبقة تستهلكها فقط، وتبقي كل السجلات خالية من PII عبر `recipient_ref` المعتم.

## 7. Saudi PDPL Pointers (EN)

For Saudi readers: in every proposal/pilot, name the **controller** (usually the client) and the **processor** (Dealix under client instructions), the lawful basis, and the data-subject rights channels. Full detail, the consent ledger, ROPA, and data-subject requests live in [../../PRIVACY_PDPL_READINESS.md](../../PRIVACY_PDPL_READINESS.md) and `auto_client_acquisition/compliance_os/` (`consent_ledger`, `contactability`, `ropa`, `data_subject_requests`). We do not duplicate the policy — this layer only consumes it, and keeps every record PII-free via the opaque `recipient_ref`.

## روابط مرجعية / Related

- [COLD_EMAIL_DRAFT_FACTORY_AR.md](COLD_EMAIL_DRAFT_FACTORY_AR.md) — مصنع المسودات والبوابة / the draft factory + gate.
- [SENDING_RAMP_OS_AR.md](SENDING_RAMP_OS_AR.md) — المنحنى وصحة الدومين / ramp + domain health.
- [REPLY_HANDLING_OS_AR.md](REPLY_HANDLING_OS_AR.md) — الردود والكبح / replies + suppression.
- [../../ops/EMAIL_DELIVERABILITY.md](../../ops/EMAIL_DELIVERABILITY.md) — قائمة DNS والتسليم / DNS + deliverability checklist.
- [../../PRIVACY_PDPL_READINESS.md](../../PRIVACY_PDPL_READINESS.md) — جاهزية PDPL / PDPL readiness.

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
