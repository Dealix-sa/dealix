# Risk Model + L0–L6 Permission Model

> المرجع: §39 (Risk levels + Critical triggers) و §38 (L0–L6 permissions).

---

## القسم الأول — مستويات المخاطر

كل خطر معروف أو مُكتشَف في Dealix يُصنَّف في أحد 4 مستويات. التصنيف يحدّد سرعة الاستجابة، الجهة المسؤولة، والأثر على الـ Kill Switch.

| المستوى | الوصف | زمن الاستجابة | الجهة المسؤولة |
|---|---|---|---|
| **Low** | تنبيه شكلي، لا أثر فوري على القيمة أو الثقة | ضمن دورة المراجعة اليومية | Internal — تُسجَّل وتُغلَق |
| **Medium** | احتمال تأثير على عميل واحد أو تشغيل واحد | ضمن 24 ساعة | Internal مع إخطار Trust |
| **High** | تأثير محتمل على عدة عملاء / شركاء / قنوات | ضمن 4 ساعات | Trust + Sovereign (إخطار، انتظار قرار) |
| **Critical** | تهديد فوري على السيادة، البيانات، أو الاستمرار | فورًا (دقائق) | Sovereign — إيقاف تلقائي حيث يلزم |

---

## الـ 7 محفِّزات لتصنيف Critical

أي خطر يستوفي أحد هذه السبعة يُصنَّف Critical تلقائيًا:

1. **اختراق محتمل لـ PII** (حتى لو لم يُؤكَّد بعد).
2. **خرق إقامة بيانات** — بيانات حساسة عبرت حدودًا غير معتمدة.
3. **اختراق Tool Registry** — أداة سُجِّلت أو عُدِّلت دون مرور Trust.
4. **Agent يتجاوز صلاحياته L0–L6** — تنفيذ خرج عن المستوى المُصرَّح به.
5. **خرق PDPL مُحقَّق** — حدث فعلي (لا مجرد احتمال).
6. **رسالة خارجية خرجت بدون Quality Gate** (راجع [QUALITY_GATES_AR.md](QUALITY_GATES_AR.md)).
7. **انتهاك Sovereign Boundary** — workspace آخر حاول قراءة/تعديل Sovereign.

عند Critical:
- Hermes ينشر `governance.alert` بمستوى critical.
- Kill Switch ذو الصلة يُفعَّل تلقائيًا (إن مرتبطًا).
- Sovereign يُخطَر فورًا.
- Audit Trail يُجمَّد للحدث (لا تعديل بعد الكشف).
- يُسجَّل في Decision Journal مع توصية وإجراء.

---

## القسم الثاني — L0 إلى L6 Permission Model

كل فعل في Dealix له **مستوى صلاحية** مطلوب. كل **منفِّذ** (وكيل، نظام، إنسان) له مستوى أقصى يستطيع تشغيله. Hermes يطابق الاثنين قبل أي dispatch.

| المستوى | الوصف الموجز | أمثلة على الأفعال المسموحة | من يملكه افتراضيًا |
|---|---|---|---|
| **L0** | قراءة عامة فقط | فتح صفحة عامة، قراءة وثيقة مفتوحة | أي مكوّن مُسجَّل |
| **L1** | قراءة بيانات داخلية غير حسّاسة | تصفّح Inbox مُجمَّع، قراءة سياسات | فريق Internal |
| **L2** | كتابة بيانات تشغيلية محدودة | تصنيف إشارة، تحديث حالة opportunity | وكلاء التشغيل اليومي |
| **L3** | استدعاء أدوات داخلية مُسموح بها | تشغيل classifier، استخراج source passport | وكلاء + Internal leads |
| **L4** | تنفيذ تأثيرات خارجية محدودة (مسوَّدات لا تُرسَل) | بناء مسوَّدة رسالة/مقترح، توليد تقرير | وكلاء بإشراف بشري |
| **L5** | إرسال خارجي / تأثير على عميل/شريك بعد بوابة جودة | إرسال رسالة، تسليم مقترح، نشر تقرير | بشر معتمدون فقط — لا وكلاء بشكل مباشر |
| **L6** | قرارات سيادية + تعديل سياسات + Scale/Kill + Kill Switch | اعتماد شراكة، إنهاء قطاع، تعديل Tool Registry | Sovereign فقط |

> **قاعدة الذهب**: لا وكيل يمتلك L5 أو L6 بشكل دائم. الوكلاء يُولِّدون مسوَّدات (L4)، البشر يُرسلون (L5)، Sovereign يُقرّر (L6).

---

## مصفوفة الأفعال ⇄ المستويات

| الفعل | المستوى المطلوب | البوابات الإضافية |
|---|---|---|
| قراءة وثيقة عامة | L0 | — |
| تصنيف إشارة واردة | L2 | — |
| تشغيل classifier agent | L3 | بوابة الوكيل |
| تشغيل crawler / parser | L3 | بوابة الأداة + Trust check |
| بناء مسوَّدة مقترح | L4 | بوابة المقترح (لاحقًا قبل الإرسال) |
| إرسال إيميل لعميل | L5 | بوابة الرسالة الخارجية |
| إرسال WhatsApp ضمن السياسة | L5 | بوابة الرسالة + channel policy |
| إصدار حزمة دليل مختومة | L5 (بناء L4 + ختم L5) | بوابة الإثبات |
| اعتماد شريك جديد | L6 | Strategic Decision + Decision Journal |
| إنهاء قطاع (Kill vertical) | L6 | Scale/Kill Playbook + Decision Journal |
| تعديل سياسة Trust | L6 | Trust review + Decision Journal |
| Kill Switch لأداة/وكيل | L6 | فوري بلا تأكيد ثانٍ |

---

## التطابق مع نموذج المخاطر

| مستوى الخطر | يُتعامَل عبر | المستوى المطلوب لإغلاق الحدث |
|---|---|---|
| Low | تسجيل في Trust | L1–L2 |
| Medium | فحص بشري + قرار | L4 |
| High | قرار Trust + إخطار Sovereign | L5 |
| Critical | Sovereign — قرار + توثيق | L6 |

---

## كيف يفرض Hermes هذه المصفوفة؟

في الخطوة 6 من قرار Hermes (راجع [HERMES_ORCHESTRATOR_AR.md](HERMES_ORCHESTRATOR_AR.md)):

1. يحدد المستوى المطلوب للفعل.
2. يقرأ مستوى المُنفِّذ من Agent/Tool Registry.
3. إن كان المُنفِّذ أدنى: يرفع `decision.requested` لرفع المستوى أو يرفض.
4. إن كان أعلى أو مساويًا: يُمرّر إلى البوابة الإضافية إن وُجدت.
5. إن مرّت البوابة: dispatch.

---

## ما لا يُقاس بـ L0–L6

- **قرارات الـ Personal Wealth** — هذه حصرية Sovereign، خارج نموذج الصلاحيات التشغيلي.
- **قرارات Trust حول السياسات نفسها** — يدخل المستوى L6 لكن المنطق يختلف (راجع [TRUST_WORKSPACE_AR.md](TRUST_WORKSPACE_AR.md)).

---

## English Summary

- Risk is classified into Low, Medium, High, and Critical, with explicit response-time targets and owners; Critical fires the kill switch and freezes the audit trail.
- Seven triggers auto-classify a risk as Critical: PII breach, data-residency violation, tool registry tampering, agent permission overrun, confirmed PDPL violation, external message bypassing quality gates, Sovereign boundary violation.
- Actions are gated by an L0–L6 permission model; the gold rule is that no agent permanently holds L5 or L6 — agents draft (L4), humans send (L5), Sovereign decides (L6).
- An action-to-level mapping table specifies which level each common action requires and which additional gate applies.
- Hermes enforces the model at step 6 of its decision flow, rejecting or escalating any mismatch.
