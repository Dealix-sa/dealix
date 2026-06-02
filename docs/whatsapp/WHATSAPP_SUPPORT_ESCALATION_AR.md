# WhatsApp Support Triage & Escalation — تصنيف الدعم والتصعيد على واتساب

## التصنيف

رسالة الدعم تُصنَّف إلى إحدى ثماني فئات قانونية (`SupportCategory`) عبر `support_triage.triage`. التصنيف حتمي (مطابقة أنماط عربية/إنجليزية)، والافتراضي `general`. بعض الفئات يجب أن تصل إلى إنسان مباشرة ولا يحلّها الروبوت وحده.

## الفئات الثماني (`SupportCategory`)

| الفئة | أمثلة الإشارات | تصعيد لإنسان؟ |
|---|---|---|
| `billing` | فاتورة، دفع، سداد، اشتراك، استرجاع مبلغ، invoice، refund | **نعم** |
| `urgent_complaint` | شكوى، عاجل جدًا، مشكلة كبيرة، توقف كل شيء، urgent، complaint | **نعم** |
| `technical` | لا يعمل، خطأ، عطل، توقف، not working، error، crash، bug | لا |
| `data` | بيانات ناقصة، مفقود، غير صحيح، data missing، wrong data | لا |
| `report` | التقرير، الأرقام غلط، report، dashboard wrong | لا |
| `draft_quality` | عدّل المسودة، صيغة الرسالة، draft wrong، reword، rewrite | لا |
| `permission` | صلاحية، وصول، ربط، permission، access، connect | لا |
| `general` | الافتراضي عند عدم المطابقة | لا |

> ترتيب المطابقة مهم: الفوترة والشكوى العاجلة تُفحَصان أولًا، فالمشكلة المتعلقة بفاتورة أو تقرير تُوجَّه إلى الدعم لا إلى الفوترة أو العرض.

## الفئات التي يجب أن تصل إلى إنسان

`billing` و`urgent_complaint` فقط محدَّدتان في `_HUMAN_ONLY`. عند أيٍّ منهما تُبنى بطاقة التصعيد (`support_escalation_card`) بقرار `ESCALATE` ومخاطر `high`، ويُدخَل أحد الفريق للرد. بقية الفئات قرارها `ALLOW` ومخاطرها `medium`، وتُعالَج مع عودة بخطوة واضحة. خيارات البطاقة في كل الحالات: `wait_team` (انتظار الفريق)، `book_call` (احجز مكالمة)، `add_details` (أرسل التفاصيل).

روابط: [التحويل إلى إنسان](./WHATSAPP_HUMAN_HANDOFF_AR.md) · [بطاقات الإجراء](./WHATSAPP_APPROVAL_CARDS_AR.md) · [المقاييس](./WHATSAPP_METRICS_AR.md) · [خريطة التدفقات](./WHATSAPP_FLOW_MAP_AR.md).

---

## English

### Triage

A support message is classified into one of eight canonical categories (`SupportCategory`) via `support_triage.triage`. Triage is deterministic (AR/EN pattern matching), defaulting to `general`. Some categories must reach a human directly and are not resolved by the bot alone.

### The eight categories (`SupportCategory`)

| Category | Example cues | Escalate to human? |
|---|---|---|
| `billing` | فاتورة، دفع، سداد، اشتراك، استرجاع مبلغ، invoice, refund | **Yes** |
| `urgent_complaint` | شكوى، عاجل جدًا، مشكلة كبيرة، توقف كل شيء، urgent, complaint | **Yes** |
| `technical` | لا يعمل، خطأ، عطل، توقف، not working, error, crash, bug | No |
| `data` | بيانات ناقصة، مفقود، غير صحيح، data missing, wrong data | No |
| `report` | التقرير، الأرقام غلط، report, dashboard wrong | No |
| `draft_quality` | عدّل المسودة، صيغة الرسالة، draft wrong, reword, rewrite | No |
| `permission` | صلاحية، وصول، ربط، permission, access, connect | No |
| `general` | The default when nothing matches | No |

> Match order matters: billing and urgent complaint are checked first, so a problem about an invoice or a report routes to support rather than to billing or a proposal.

### Categories that must reach a human

Only `billing` and `urgent_complaint` are listed in `_HUMAN_ONLY`. For either, the escalation card (`support_escalation_card`) is built with decision `ESCALATE` and risk `high`, and a teammate is brought in to reply. The remaining categories carry decision `ALLOW` and risk `medium`, and are resolved with a clear next step. The card options in all cases: `wait_team` (Wait for team), `book_call` (Book a call), `add_details` (Add details).

Links: [Human handoff](./WHATSAPP_HUMAN_HANDOFF_AR.md) · [Action cards](./WHATSAPP_APPROVAL_CARDS_AR.md) · [Metrics](./WHATSAPP_METRICS_AR.md) · [Flow map](./WHATSAPP_FLOW_MAP_AR.md).

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
