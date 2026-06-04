# Dealix — Commercial Metrics Dashboard — لوحة المؤشرات التجارية

> **Golden rule / القاعدة الذهبية:**
> AI recommends and drafts. Deterministic workflows verify. Founder approves. Nothing is sent automatically.
> الذكاء يقترح ويصيغ، مسارات حتمية تتحقق، المؤسس يعتمد، لا شيء يُرسل تلقائيًا.

Related: [08_FOUNDER_DAILY_REVIEW_PLAYBOOK.md](08_FOUNDER_DAILY_REVIEW_PLAYBOOK.md) · [09_DAILY_EXECUTION_RHYTHM.md](09_DAILY_EXECUTION_RHYTHM.md) · [18_HANDOVER_AND_SUCCESS_REPORT.md](18_HANDOVER_AND_SUCCESS_REPORT.md)

**EN —** This dashboard tracks the commercial pipeline honestly. Generation and gating are measured by the system. Sends, replies, sales, and revenue are **manual, example inputs** logged by the founder — never assumed, never auto-generated. Revenue is never inferred; if it was not logged, it did not happen.

**AR —** تتابع هذه اللوحة المسار التجاري بصدق. التوليد والفلترة يقيسهما النظام. الإرسال والردود والمبيعات والإيراد **مدخلات يدوية للمثال** يسجّلها المؤسس — لا تُفترض ولا تُولَّد تلقائيًا. الإيراد لا يُستنتج أبدًا؛ ما لم يُسجَّل لم يحدث.

---

## Metrics / المؤشرات

| Metric / المؤشر | Source / المصدر | Meaning / المعنى |
|---|---|---|
| `drafts_generated` | System / النظام | Drafts produced. / المسودات المُنتَجة. |
| `founder_review_count` | System / النظام | Drafts placed in the review queue. / الموضوعة في طابور المراجعة. |
| `rejected_quality` | Founder / المؤسس | Discarded as weak/off-target. / المستبعَدة لضعف/خروج عن الهدف. |
| `rejected_compliance` | Founder / المؤسس | Discarded for breaking a non-negotiable. / المستبعَدة لمخالفة بند غير قابل للتفاوض. |
| `needs_research` | Founder / المؤسس | Held pending a fact to verify. / المعلّقة لانتظار التحقق من معلومة. |
| `approved_manual` | Founder / المؤسس | Approved for personal manual send. / المعتمَدة للإرسال اليدوي. |
| `manual_sent` | Founder (manual) / المؤسس (يدوي) | Actually sent by the founder, logged manually. / المُرسلة فعلًا، مسجّلة يدويًا. |
| `replies_positive` | Founder (manual) / المؤسس (يدوي) | Positive replies received. / ردود إيجابية. |
| `replies_negative` | Founder (manual) / المؤسس (يدوي) | Negative replies / opt-outs. / ردود سلبية / إلغاء. |
| `reply_rate` | Derived / مشتق | replies / manual_sent. / الردود ÷ المُرسل. |
| `qualified_calls` | Founder (manual) / المؤسس (يدوي) | Discovery calls that qualified. / مكالمات اكتشاف مؤهلة. |
| `diagnostics_sold` | Founder (manual) / المؤسس (يدوي) | Diagnostics sold. / تشخيصات مباعة. |
| `pilots_sold` | Founder (manual) / المؤسس (يدوي) | Pilots sold. / تجارب مباعة. |
| `retainers_started` | Founder (manual) / المؤسس (يدوي) | Retainers started. / اشتراكات بدأت. |
| `revenue_pipeline_sar` | Founder (manual) / المؤسس (يدوي) | Value of open opportunities (SAR), example input. / قيمة الفرص المفتوحة (ريال)، مدخل مثال. |
| `realized_revenue_sar` | Founder (manual) / المؤسس (يدوي) | Collected revenue (SAR), example input. / إيراد محصّل (ريال)، مدخل مثال. |

---

## Derived rates / المعدلات المشتقة

**EN —**
- `reply_rate` = (replies_positive + replies_negative) / manual_sent.
- Treat all derived rates as estimates over small samples; do not present them as benchmarks.

**AR —**
- `reply_rate` = (الردود الإيجابية + السلبية) ÷ المُرسل.
- عامل كل المعدلات المشتقة كتقديرات على عينات صغيرة؛ لا تقدّمها كمعايير.

---

## Reading discipline / انضباط القراءة

**EN —**
- System metrics show activity, not value. High `drafts_generated` is not success.
- Quality is `approved_manual` and `replies_positive`, not raw volume.
- `rejected_compliance` rising is healthy — the gate is working.
- Revenue figures are manual example inputs; never assume, infer, or auto-fill them.

**AR —**
- مؤشرات النظام تُظهر النشاط لا القيمة. كثرة `drafts_generated` ليست نجاحًا.
- الجودة هي `approved_manual` و`replies_positive`، لا الكمية الخام.
- ارتفاع `rejected_compliance` صحي — البوابة تعمل.
- أرقام الإيراد مدخلات يدوية للمثال؛ لا تُفترض ولا تُستنتج ولا تُملأ تلقائيًا.

---

## What the dashboard never does / ما لا تفعله اللوحة أبدًا

**EN —** It never sends, never books, never invoices, and never generates revenue figures on its own. It is a logbook the founder maintains by hand.

**AR —** لا ترسل، ولا تحجز، ولا تفوتر، ولا تولّد أرقام إيراد من تلقاء نفسها. هي سجل يدوي يحفظه المؤسس بيده.

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
