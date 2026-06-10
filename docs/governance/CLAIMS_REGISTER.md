# Claims Register — سجل الادعاءات

> Canonical list of forbidden claims and their safe replacements.
> القائمة المرجعية للادعاءات الممنوعة وبدائلها الآمنة.
>
> **This file is allowed to quote forbidden phrases — documenting them is its purpose.**
> هذا الملف مسموح له باقتباس العبارات الممنوعة لأن غرضه توثيقها.
>
> Enforcement sources / مصادر الإنفاذ:
> `auto_client_acquisition/governance_os/draft_gate.py`,
> `auto_client_acquisition/saudi_layer/forbidden_claims.py`,
> `scripts/verify_dealix_positioning.py`.
>
> Aligned with `docs/00_platform_truth/PLATFORM_TRUTH.md` §4 (Claims discipline).

---

## القاعدة — The rule

أي ادعاء عن نتائج مضمونة أو إرسال تلقائي أو استبدال البشر **ممنوع** في كل أصل (موقع، عرض، إيميل، محتوى).
البديل الآمن دائماً يصف ما نفعله فعلاً: توضيح الخطوات التالية، ترتيب الفرص والمتابعة والإثبات، تجهيز مسودات قابلة للمراجعة البشرية، وتسليم Proof Pack خلال Command Sprint.

Any claim of guaranteed results, automatic sending, or replacing humans is **forbidden** in every asset (site, deck, email, content).
The safe replacement always describes what we actually do: clarify next actions, organize opportunities, follow-up and proof, prepare human-review-ready drafts, and deliver a Proof Pack within a Command Sprint.

---

## السبب العام — Why these are forbidden

- **نتائج مضمونة:** لا يمكن ضمان مبيعات أو ROI؛ يعتمد على عوامل خارج سيطرتنا — وهذا تضليل.
- **إرسال تلقائي / واتساب بارد:** يخالف الموافقة البشرية الإلزامية و PDPL ويعرّض العميل للمخاطر.
- **AI بدون بشر:** يخالف نموذج Human-in-the-Loop؛ كل إجراء خارجي يتطلب موافقة.

- **Guaranteed results:** sales/ROI depend on factors outside our control — claiming them is misrepresentation.
- **Auto-send / cold WhatsApp:** violates mandatory human approval and PDPL, and exposes the customer to risk.
- **AI with no human:** violates the Human-in-the-Loop model; every external action requires approval.

---

## Forbidden claims — العبارات الممنوعة (Arabic)

| Forbidden phrase / العبارة الممنوعة | Why forbidden / السبب | Safe replacement / البديل الآمن |
|---|---|---|
| `نضمن زيادة المبيعات` | ضمان نتائج لا نتحكم بها — تضليل | `نساعدك توضح الـ next actions ونرتب فرصك` |
| `نجيب لك عملاء مضمونين` | ضمان نتائج + يوحي بـ scraping/قوائم مشتراة | `نرتب فرصك ومتابعتك وإثباتك` |
| `نرسل واتساب تلقائي` | إرسال خارجي بلا موافقة بشرية — يخالف PDPL والحوكمة | `نجهز مسودات قابلة للمراجعة البشرية` |
| `نغلق لك الصفقات` | يوحي بإجراء خارجي نيابة عن العميل بلا موافقة | `نرتب فرصك ومتابعتك حتى القرار التنفيذي التالي` |
| `AI يشتغل بدون تدخل منك` | يخالف Human-in-the-Loop — كل إجراء خارجي يتطلب موافقة | `نسلم Proof Pack خلال Command Sprint بموافقتك على كل خطوة` |

---

## Forbidden claims — Forbidden phrases (English)

| Forbidden phrase | Why forbidden | Safe replacement |
|---|---|---|
| `guaranteed sales` | Guarantees a result outside our control — misrepresentation | We help you clarify your next actions and organize your opportunities |
| `guaranteed results` | Same — no result can be guaranteed | We deliver a clear, human-review-ready operating picture |
| `guaranteed ROI` | Financial guarantee we cannot make | We surface evidenced opportunities and the next executive decision |
| `auto-send` / `send automatically without approval` | External send without human approval — violates governance + PDPL | We prepare human-review-ready drafts for your approval |
| `cold whatsapp` | Cold/unconsented messaging — forbidden channel behavior | We organize your follow-up; you approve every external message |
| `we close deals for you` | Implies external action on the customer's behalf without approval | We organize your opportunities and follow-up to the next decision |
| `AI runs with no human` | Violates Human-in-the-Loop; every external action needs approval | We deliver a Proof Pack within the Command Sprint, you approve each step |

---

## The safe language set — مجموعة اللغة الآمنة

استخدم هذه العبارات دائماً بدل الممنوعة:

- "نساعدك توضح الـ next actions." / "We help you clarify your next actions."
- "نرتب فرصك ومتابعتك وإثباتك." / "We organize your opportunities, follow-up, and proof."
- "نجهز مسودات قابلة للمراجعة البشرية." / "We prepare human-review-ready drafts."
- "نسلم Proof Pack خلال Command Sprint." / "We deliver a Proof Pack within the Command Sprint."

For opportunity language, say **evidenced opportunities / فرص مُثبتة بأدلة**, never "guaranteed."

---

## Cross-references — مراجع

- `docs/governance/FORBIDDEN_ACTIONS.md`
- `docs/governance/APPROVAL_MATRIX.md`
- `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md`
- `docs/00_platform_truth/PLATFORM_TRUTH.md`
- `docs/00_platform_truth/CTA_MAP.md`

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
