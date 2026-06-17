# Dealix — Full Company Launch Blueprint (v1, FROZEN)

> **النوع:** خطة إطلاق شركة كاملة (Strategy + Execution Architecture)
> **الحالة:** `FROZEN v1` — لا يتغيّر تسلسل الـ PRs إلا عند ظهور blocker، وبعد موافقة المؤسس.
> **آخر تحديث:** 2026-06-05
> **المالك:** المؤسس (Bassam) + Dealix Company OS (`os/`)
> **الوثائق الشقيقة:** [`DEALIX_EXECUTION_BOARD.md`](DEALIX_EXECUTION_BOARD.md) · [`DEALIX_LAUNCH_GO_NO_GO.md`](DEALIX_LAUNCH_GO_NO_GO.md)

---

## 0. القاعدة الذهبية (Operating Loop)

```
Plan → Review → Red Team → Score → Freeze → PR 1 only → Verify → Approve → PR 2 → …
```

هذه الوثيقة هي مخرج **Plan** بعد تجميده. ننفّذ **PR واحد في كل مرة**، نتحقق منه (`/dealix-verify`)، نأخذ موافقة المؤسس، ثم ننتقل للـ PR التالي.

### ماذا تخطط هذه الوثيقة؟
لا تخطط "موقعًا". تخطط **Dealix Launch Stack** كامل:

```
Brand → Website → Growth → Free Tools → Sales Funnel → Delivery → Proof → Governance → CI Gates → Launch Review
```

---

## 1. ما هو Dealix (التموضع المُجمّد)

**Dealix = نظام تشغيل أعمال بالذكاء الاصطناعي، سعودي الهوية، إنجليزي الجاهزية (Saudi-first AI Business Operating System).**

| ✅ Dealix هو | ❌ Dealix ليس |
|---|---|
| نظام تشغيل أعمال محكوم (governed) ينتج قدرة تشغيلية + إثبات قابل للتدقيق | ليس CRM |
| طبقة عمليات فوق بيانات الشركة وقراراتها | ليس chatbot |
| منصة بطبقات (Data → Governance → Proof → Value → Capital → Adoption) | ليس "Revenue only" |
| Approval-first: لا فعل خارجي بدون موافقة بشرية | ليست أداة تسويق آلي/spam |

**الإسفين الأول (first wedge):** **Command Sprint** = سبرنت تشخيص وتشغيل لمدة 7 أيام (يقابل في `os/` الـ *7-Day Revenue Intelligence Sprint*). السعر التأسيسي **499 ريال**.

> **Mapping للمسميات الجديدة ↔ الموجود في `os/`:**
> - *Command Sprint* ↔ 7-Day Revenue Intelligence Sprint (499 SAR)
> - *Business OS Score* ↔ Free AI Ops Diagnostic + Scoring (`os/05_SCORING.yml`)
> - *Managed OS* ↔ Managed Revenue Ops (2,999–4,999/mo)
> - سُلّم العروض الكامل في `os/03_OFFERS.yml` يبقى مرجعًا.

### سُلّم العروض (5 درجات — مُجمّد)
| Rung | Offer | Price (SAR) |
|---|---|---|
| 0 | Free Business OS Score / AI Ops Diagnostic | 0 |
| 1 | **Command Sprint** (7-day) | 499 (تأسيسي) |
| 2 | Data-to-Revenue Pack | 1,500 |
| 3 | Managed OS (Managed Revenue Ops) | 2,999–4,999 / mo |
| 4 | Custom AI Setup | 5,000–25,000 + 1,000/mo |
| Ent. | AI Governance Review (مسار بطيء) | 25,000–50,000 |

---

## 2. الـ 11 محرّمات (Non-Negotiables — مفروضة باختبارات)

1. لا أنظمة scraping.
2. لا أتمتة WhatsApp بارد.
3. لا أتمتة LinkedIn.
4. لا ادعاءات مزيّفة أو بلا مصدر.
5. لا ضمان نتائج بيع.
6. لا PII في الـ logs.
7. لا إجابات معرفية بلا مصدر.
8. لا فعل خارجي بدون موافقة.
9. لا agent بلا هوية.
10. لا مشروع بلا Proof Pack.
11. لا مشروع بلا Capital Asset.

أي طلب يخالف واحدة منها → **رفض + اقتراح بديل آمن**. لا التفاف.

---

## 3. تسلسل الـ PRs (Frozen Sequence)

> القاعدة: كل PR مستقل وقابل للشحن، ولا يعتمد على PR لاحق. كل PR يحتاج **موافقة مؤسس** قبل الدمج.

| PR | الاسم | الطبقة | المالك (agent) | يلمس كود مصدري؟ |
|----|------|--------|----------------|------------------|
| **PR 1** | Company OS Scaffolding | OS | dealix-pm | ❌ لا |
| **PR 2** | Brand & Visual Identity | Brand | dealix-content | ❌ لا (docs/tokens فقط) |
| **PR 3** | Core Website (4 صفحات بيعية) | Website | dealix-engineer | ✅ نعم (frontend) |
| **PR 4** | Free Tools (3 أدوات) | Growth/Product | dealix-engineer | ✅ نعم |
| **PR 5** | Growth OS + Answer Library | Growth | dealix-content + engineer | ✅ نعم (محتوى + صفحات) |
| **PR 6** | Delivery Factory + Proof + Governance docs | Delivery | dealix-delivery | ❌ لا (templates/docs) |
| **PR 7** | CI Gates + Launch Readiness | CI/Security | dealix-engineer | ✅ نعم (.github/workflows) |

كل PR موصوف بالتفصيل في القسم 4.

---

## 4. خريطة الـ PR (Scope · Files · Owner · Acceptance · Verify · Rollback)

### PR 1 — Company OS Scaffolding ✅ (هذا الـ PR)
- **Scope:** بنية تشغيل الشركة لـ Claude Code: `CLAUDE.md`, `.claude/commands/*`, تأكيد وجود subagents، والوثائق الثلاث المؤسِّسة (Blueprint/Board/Go-No-Go). **لا يُلمس أي كود مصدري.**
- **Files:**
  - `CLAUDE.md` (root) — قواعد + روابط (lean pointer إلى `AGENTS.md` و`os/`).
  - `.claude/commands/dealix-{audit,plan-review,red-team,brand,build-website,growth-os,delivery-proof,governance,verify,launch-review}.md`
  - `.claude/agents/*` (موجودة مسبقًا: pm, content, engineer, sales, delivery) — تأكيد.
  - `docs/05_founder/DEALIX_FULL_COMPANY_LAUNCH_BLUEPRINT.md` (هذا الملف)
  - `docs/05_founder/DEALIX_EXECUTION_BOARD.md`
  - `docs/05_founder/DEALIX_LAUNCH_GO_NO_GO.md`
- **Owner:** dealix-pm
- **Acceptance:** CLAUDE.md موجود · 10 commands موجودة · agents موجودة · الوثائق الثلاث موجودة · **لا تغيير في كود مصدري** (`git diff --stat` يُظهر فقط `.md`/`.claude`).
- **Verify:** `git diff --name-only main...HEAD` لا يحتوي `.py`/`.ts`/`.tsx` · `ls .claude/commands | wc -l` = 10.
- **Rollback:** `git revert` للـ commit — لا أثر على التطبيق (وثائق فقط).
- **Founder approval:** نعم (لتجميد الخطة).

### PR 2 — Brand & Visual Identity
- **Scope:** Messaging House + Visual Identity System + Product Family Map + Module Status Map. وثائق وtokens فقط.
- **Files:**
  - `docs/00_platform_truth/VISUAL_IDENTITY_SYSTEM.md`
  - `docs/00_platform_truth/MESSAGING_HOUSE.md`
  - `docs/00_platform_truth/PRODUCT_FAMILY_MAP.md`
  - `docs/00_platform_truth/MODULE_STATUS_MAP.md` (Live / Beta / Future لكل موديول)
- **Owner:** dealix-content (+ مراجعة المؤسس)
- **Acceptance:** هوية بصرية موجودة · messaging house موجود · product family موجود · module status موجود · **Dealix غير مختزل إلى CRM/Revenue**.
- **Verify:** positioning checker (PR 7) عند توفره؛ مبدئيًا مراجعة يدوية + `/dealix-brand`.
- **Rollback:** revert — وثائق فقط.
- **Founder approval:** نعم (الهوية قرار استراتيجي).

### PR 3 — Core Website (الإصدار القابل للبيع)
- **Scope:** 4 صفحات بيعية: Homepage, Command Sprint, Pricing, Start/Diagnostic. CTA واحد لكل صفحة + حدث analytics.
- **Files (frontend — مسار `frontend/src/app/[locale]/...`):**
  - `/` (Homepage) · `/command-sprint` · `/pricing` · `/start`
  - مكوّن مشترك لزر CTA + إطلاق حدث analytics.
- **Owner:** dealix-engineer
- **Acceptance:** الصفحات الأربع مُنفّذة · `npm run build` ينجح · لا ادعاءات مضمونة · CTA واحد لكل صفحة · CTA يوجّه إلى Score/Diagnostic/Command Sprint.
- **Verify:** `cd frontend && npm run build` · claims checker · positioning checker.
- **Rollback:** revert PR؛ الصفحات جديدة فلا تكسر مسارات قائمة.
- **Founder approval:** نعم (نسخ + سعر + CTA).

### PR 4 — Free Tools (3 أدوات)
- **Scope:** Business OS Score · Revenue Leakage Calculator · Proof Gap Audit. كل أداة تُخرج: **score + gaps + CTA**.
- **Files:** صفحات `/business-os-score`, `/revenue-leakage-calculator`, `/proof-gap-audit` + منطق التقييم (يستهلك `os/05_SCORING.yml` حيث ممكن) + أحداث analytics.
- **Owner:** dealix-engineer
- **Acceptance:** كل أداة مخطّطة أو منفّذة وتُخرج score + gaps + CTA · لا تخزين PII غير مبرّر · `npm run build` ينجح.
- **Verify:** build + اختبار وحدة لمنطق التقييم + claims checker.
- **Rollback:** revert PR.
- **Founder approval:** نعم (ترتيب أولوية الأداة الأولى — قرار مؤسس #5).

### PR 5 — Growth OS + Answer Library (SEO/GEO)
- **Scope:** Growth Loop Map منفّذ + Answer Library (8 صفحات) + content factory + nurture + partner/referral + metrics.
- **Files:**
  - `/ar/answers/*` (8 صفحات) + نسخ EN مع hreflang.
  - `docs/growth/GROWTH_LOOP_MAP.md` · `docs/growth/CONTENT_FACTORY.md` · `docs/growth/NURTURE.md` · `docs/growth/PARTNER_REFERRAL.md`
  - structured data حيث يناسب.
- **Owner:** dealix-content + dealix-engineer
- **Acceptance:** docs النمو موجودة · خطة SEO/GEO موجودة · content factory موجود · nurture موجود · partner/referral موجود · metrics موجودة · كل أصل يوجّه إلى Score/Diagnostic/Command Sprint.
- **Verify:** growth checker (PR 7) · build · فحص hreflang.
- **Rollback:** revert PR.
- **Founder approval:** نعم.

### PR 6 — Delivery Factory + Proof + Governance
- **Scope:** `customers/_template/` (12 ملفًا) + Proof Pack template + Claims Register + Human Approval Policy + No-Spam Policy.
- **Files:**
  - `customers/_template/00_intake.md … 11_upsell_recommendation.md`
  - `docs/14_proof/PROOF_PACK_TEMPLATE.md`
  - `docs/00_platform_truth/CLAIMS_REGISTER.md`
  - `docs/07_governance/HUMAN_APPROVAL_POLICY.md` · `docs/07_governance/NO_SPAM_POLICY.md`
- **Owner:** dealix-delivery
- **Acceptance:** template موجود · Proof Pack موجود · Claims Register موجود · Human Approval Policy موجودة · No-Spam Policy موجودة · لا مشروع بلا Proof Pack/Capital Asset.
- **Verify:** `/dealix-delivery-proof` dry-run على `_template` · فحص أن كل ملف يحوي الحقول التسعة (source…due_date).
- **Rollback:** revert PR — templates فقط.
- **Founder approval:** نعم.

### PR 7 — CI Gates + Launch Readiness
- **Scope:** GitHub Actions بأقل صلاحية + positioning checker + growth checker + claims/unsafe-claims checker + launch readiness checker.
- **Files:**
  - `.github/workflows/dealix-launch-gates.yml`
  - `scripts/check_positioning.py` · `scripts/check_unsafe_claims.py` · `scripts/check_growth_routing.py` · `scripts/check_launch_readiness.py`
  - `reports/launch/launch_readiness.md` (مخرج)
- **Owner:** dealix-engineer
- **Acceptance:** CI gate موجود · 4 checkers موجودة · GitHub Actions least-privilege.
- **Security (إلزامي):** `permissions:` على مستوى الـ workflow = `contents: read` افتراضيًا، رفع الصلاحية فقط للـ job المحتاج · لا طباعة أسرار في الـ logs · **عدم** حقن سياق GitHub غير الموثوق مباشرة في سكربتات shell (مرّره عبر `env:` ثم استخدمه مقتبسًا) · أقل صلاحية للـ `GITHUB_TOKEN`.
- **Verify:** تشغيل الـ workflow على PR تجريبي · `act` محليًا اختياري · مراجعة الصلاحيات.
- **Rollback:** revert PR — لا تأثير على التطبيق وقت التشغيل.
- **Founder approval:** نعم.

---

## 5. Launch Control System (نظام التحكم في الإطلاق)

يُتتبّع حيًّا في [`DEALIX_LAUNCH_GO_NO_GO.md`](DEALIX_LAUNCH_GO_NO_GO.md). الحقول:

| الحقل | القيمة الحالية (v1) |
|---|---|
| current launch status | PRE-LAUNCH (PR 1 only) |
| current ICP | TBD — قرار مؤسس #2 (افتراض: وكالات/تسويق B2B) |
| current offer | Command Sprint (7-day) |
| current price | 499 SAR (تأسيسي) — قرار مؤسس #3 |
| current pages ready | 0 / 4 core |
| current growth assets ready | 0 |
| current proof count | 0 |
| current paid sprint count | 0 |
| current blockers | قرارات المؤسس (#1–#5) غير محسومة |
| Go/No-Go decision | **NO-GO** حتى اكتمال PR 3 + أول Proof Pack |

---

## 6. Website Conversion Map

> القاعدة: **CTA واحد لكل صفحة**، يوجّه إلى Business OS Score أو Diagnostic أو Command Sprint. لا ادعاء مضمون. لا موديول مستقبلي كأنه live.

الصفحات الأساسية: `/` · `/ar` · `/platform` · `/command-sprint` · `/business-os` · `/pricing` · `/industries` · `/security` · `/start` · `/business-os-score` · `/revenue-leakage-calculator` · `/proof-gap-audit` · `/ai-governance-checklist`

| Page | Audience | Pain | Promise | Output shown | CTA | Status | Analytics event |
|---|---|---|---|---|---|---|---|
| `/` | مؤسس / GM / sales lead | عمليات مبعثرة، إثبات ضعيف، لا قرار تنفيذي | نظام تشغيل أعمال محكوم | لمحة Score + Proof | Get Business OS Score | LIVE (PR3) | `cta_click` |
| `/command-sprint` | مؤسس / GM / sales lead | متابعة مبعثرة، إثبات ضعيف، لا next action تنفيذي | 7-day Command Pack | Revenue Map + Proof Register + Executive Command Brief | Start Command Sprint | LIVE (PR3) | `command_sprint_clicked` |
| `/pricing` | مشترٍ | عدم وضوح القيمة/السعر | سُلّم واضح 5 درجات | جدول الدرجات | Start Command Sprint | LIVE (PR3) | `cta_click` |
| `/start` | lead جاهز | لا يعرف الخطوة الأولى | تشخيص مجاني الآن | نموذج تشخيص قصير | Book Diagnostic | LIVE (PR3) | `diagnostic_clicked` |
| `/business-os` | مؤسس مهتم بالعمق | يظن Dealix = أداة | منصة بطبقات | خريطة الطبقات | Get Business OS Score | BETA (PR4+) | `cta_click` |
| `/platform` | تقني/مشترٍ | "وش يفرقكم؟" | بنية approval-first | Module Status Map | Get Business OS Score | BETA | `cta_click` |
| `/business-os-score` | مؤسس | "وين أنا الآن؟" | درجة + فجوات | Score + Gaps + CTA | Start Command Sprint | LIVE (PR4) | `business_os_score_completed` |
| `/revenue-leakage-calculator` | مالي/مبيعات | تسرّب إيراد خفي | تقدير التسرّب | Estimate + Gaps + CTA | Book Diagnostic | LIVE (PR4) | `tool_completed` |
| `/proof-gap-audit` | مؤسس | لا إثبات للعملاء | فجوة الإثبات | Gap list + CTA | Start Command Sprint | LIVE (PR4) | `tool_completed` |
| `/industries` | قطاعات | "هل يناسب قطاعي؟" | تخصيص قطاعي | أمثلة قطاع | Get Business OS Score | FUTURE | `cta_click` |
| `/security` | enterprise | قلق حوكمة/PDPL | approval-first + سجلات | governance summary | Book Diagnostic | BETA | `cta_click` |
| `/ai-governance-checklist` | enterprise/GM | لا إطار حوكمة AI | checklist عملي | Checklist + CTA | Book Diagnostic | LIVE (PR5) | `tool_completed` |

> **SEO ملاحظة (Google):** SEO الجيد يساعد المحركات على فهم المحتوى واكتشاف الصفحات — وليس ضمان ترتيب. اجعل الصفحات مفيدة ومهيكلة، لا حِيَل سطحية.

---

## 7. Growth Loop Map

| Asset | Source of traffic | Lead capture | Nurture path | Conversion path | Proof loop | Metric |
|---|---|---|---|---|---|---|
| Business OS Score | عضوي/SEO + مشاركة المؤسس | email لإرسال النتيجة | تسلسل 3 رسائل | → Command Sprint | كل score → حالة مجهّلة في Proof Register | score_completed → checkout |
| Answer Library (GEO) | بحث/AI answers | CTA داخل الصفحة | روابط لأدوات | → Diagnostic | اقتباسات/أسئلة العملاء | organic → tool_started |
| Revenue Leakage Calculator | عضوي + شراكات | email | تسلسل تسرّب | → Diagnostic | تقديرات مجهّلة | tool_completed → booked |
| Proof Gap Audit | عضوي | email | تسلسل إثبات | → Command Sprint | فجوات شائعة → محتوى | tool_completed → checkout |
| LinkedIn (يدوي فقط) | منشورات المؤسس | DM يدوي/رابط | محادثة يدوية | → Diagnostic | case snippets | post → profile_clicks |
| Partner/Referral | شركاء (وكالات/استشارات) | one-pager + رابط شريك | onboarding شريك | → Command Sprint | proof مشترك | referrals → paid sprint |

> **محرّمات النمو:** لا scraping، لا WhatsApp بارد آلي، لا أتمتة LinkedIn. كل أصل يوجّه إلى Score/Diagnostic/Command Sprint.

### Answer Library (GEO) — الصفحات
`/ar/answers/what-is-ai-business-operating-system` · `crm-vs-business-os` · `what-is-command-sprint` · `what-is-proof-register` · `approval-first-ai` · `revenue-leakage` · `proof-gap` · `ai-governance-for-saudi-companies`

شكل كل صفحة: **Question → Short Answer → Detailed Answer → Example → Dealix Approach → CTA**.
- structured data حيث يناسب (Google: structured data يوضّح معنى الصفحة).
- AR-first + EN عبر hreflang (Google لديه توثيق للصفحات المحلية/المترجمة).

---

## 8. Delivery Map (Command Sprint — 7 أيام)

أي عميل يدفع يدخل تلقائيًا في:
```
customers/<slug>/   (نسخة من customers/_template/)
  00_intake.md
  01_company_intelligence.md
  02_diagnostic_summary.md
  03_command_sprint_scope.md
  04_revenue_map.md
  05_proof_register.md
  06_approval_register.md
  07_next_action_board.md
  08_executive_command_brief.md
  09_delivery_log.md
  10_proof_pack.md
  11_upsell_recommendation.md
```

**حقول إلزامية في كل ملف (Acceptance):** `source · analysis · assumption · confidence · recommendation · approval_required · next_action · owner · due_date`.

| اليوم | المخرج | مدخلات العميل المطلوبة | Checkpoint |
|---|---|---|---|
| 0 | intake + scope | بيانات الشركة، الوصول للمصادر | موافقة على النطاق |
| 1–2 | company intelligence + diagnostic summary | مصادر البيانات | — |
| 3 | revenue map | تأكيد افتراضات | approval |
| 4 | proof register | — | — |
| 5 | approval register + next action board | أولويات تنفيذية | approval |
| 6 | executive command brief | — | — |
| 7 | **Proof Pack** + upsell recommendation | — | تسليم + موافقة upsell |

**Upsell path:** Command Sprint → Data-to-Revenue Pack → Managed OS.
**محرّمات التسليم:** لا مشروع بلا Proof Pack، لا بلا Capital Asset، لا إرسال خارجي بلا موافقة.

---

## 9. Governance Map

| External action | Approval class | Allowed / Forbidden | Required log | Required evidence | Human approval point |
|---|---|---|---|---|---|
| إرسال بريد لعميل | Gated | مسموح بعد موافقة؛ ممنوع auto-send | governance log | النص + المرسل إليه | المؤسس |
| منشور LinkedIn | Gated | يدوي فقط؛ ممنوع آلي | growth log | المسودة | المؤسس |
| WhatsApp | Gated | يدوي ودافئ فقط؛ ممنوع بارد/آلي | governance log | السياق | المؤسس |
| نشر صفحة عامة | Gated | بعد claims+positioning checks | CI log | تقرير الفحص | المؤسس (merge) |
| ادعاء/claim جديد | Gated | فقط إذا في Claims Register بمصدر | claims log | المصدر | المؤسس |
| تحصيل مبلغ | Gated | بعد scope معتمد | payment log | الفاتورة/الموافقة | المؤسس |
| Free actions | Free | بحث، تحليل، صياغة مسودات، تحديث وثائق داخلية | — | — | — |

مرجع: `os/06_APPROVAL_GATES.yml` (12 بوابة محمية + 10 أفعال حرة).

---

## 10. Analytics & Metrics

**Event names (الطبقة الموحّدة):**
```
page_view, cta_click,
business_os_score_started, business_os_score_completed,
tool_started, tool_completed,
diagnostic_clicked, diagnostic_booked,
command_sprint_clicked, command_sprint_cta_clicked,
checkout_started, sprint_checkout_started, payment_completed, sprint_paid,
intake_submitted, delivery_started, proof_pack_delivered,
upsell_offered, upsell_clicked, managed_os_closed, referral_requested
```

**ملفات الطبقة (تُنشأ في PR 4/5/7):**
- `data/analytics/events.schema.json`
- `data/growth/growth_metrics.jsonl`
- `reports/growth/weekly_growth_brief.md`
- `reports/launch/launch_readiness.md`

تصميمها يسمح لاحقًا بربط PostHog أو أي analytics دون إعادة تفكير.

---

## 11. Security & CI (PR 7)

GitHub Actions launch gates:
- **least privilege:** `permissions: contents: read` افتراضيًا؛ رفع الصلاحية فقط للـ job المحتاج.
- لا صلاحيات write إلا عند الحاجة.
- لا طباعة أسرار في الـ logs (الإخفاء غير مضمون دائمًا — لا تطبعها أصلًا).
- لا حقن سياق GitHub غير موثوق مباشرة في سكربتات shell — مرّره عبر `env:` واستخدمه مقتبسًا.
- **Checkers:** positioning (لا اختزال لـ CRM/Revenue) · unsafe-claims (لا ضمانات/ادعاءات بلا مصدر) · growth-routing (كل أصل يوجّه لـ Score/Diagnostic/Sprint) · launch-readiness.

> مرجع توصيات GitHub: مبدأ أقل صلاحية لـ `GITHUB_TOKEN`، وعدم ضمان إخفاء الأسرار في الـ logs، وتقليل صلاحيات الـ workflows.

---

## 12. Brand Asset System (PR 2)

ملف: `docs/00_platform_truth/VISUAL_IDENTITY_SYSTEM.md` — يغطي:
Logo usage · Color system · Typography scale · Spacing scale · Icon style · Illustration style · Dark mode rules · Arabic typography rules · English typography rules · Do/Don't examples · Slide deck direction · Social post template direction.

---

## 13. Sales / Pitch Kit (PR 2–3، يُكمل في PR 6)

ملفات تحت `sales/`:
- `sales/COMMAND_SPRINT_ONE_PAGER.md`
- `sales/DIAGNOSTIC_SCRIPT.md`
- `sales/OBJECTION_LIBRARY.md`
- `sales/PARTNER_ONE_PAGER.md`
- `sales/PROPOSAL_TEMPLATE.md`
- `sales/FOLLOW_UP_SEQUENCE.md`

الهدف: كل lead من الموقع → مكالمة، كل مكالمة → عرض، كل عرض → تسليم.

---

## 14. الإصدارات: 7 / 30 / 90 يوم

### ⚡ Fastest 7-Day Sellable Version
> **السؤال:** ما أصغر نسخة من Dealix يمكن بيعها خلال 7 أيام دون إضعاف رؤية الـ Business OS؟

1. Homepage قوية
2. Command Sprint page
3. Pricing ladder
4. Start / Diagnostic page
5. Business OS Score (spec أو v1)
6. Command Sprint Delivery OS (`customers/_template/`)
7. Proof Pack Template
8. Claims Register
9. Human Approval Policy
10. First 30 target plan (قائمة أهداف يدوية دافئة)

→ يكفي لاستقبال أول عميل دافع، بإثبات وحوكمة، دون موقع متضخّم.

### 🚀 Strongest 30-Day Launch Version
- PR 1–5 مكتملة + 3 أدوات مجانية حيّة + Answer Library (8 صفحات) + nurture + partner one-pager.
- 3–5 Proof Packs حقيقية.
- CI gates (PR 7) فعّالة.
- هدف: 1–3 Command Sprints مدفوعة + pipeline لـ Managed OS.

### 🏔️ Strongest 90-Day Scale Version
- Managed OS عملاء (MRR).
- Data-to-Revenue Pack + Custom AI Setup كمسارات upsell.
- محتوى GEO يتوسّع + شراكات تُحيل.
- هدف مرجعي (من `os/`/pm): ~8–15K SAR MRR + 30–40K SAR one-time تراكمي بنهاية اليوم 90.

---

## 15. Top 25 Risks (Risk Register)

| # | الخطر | الأثر | الاحتمال | التخفيف | Owner |
|---|---|---|---|---|---|
| 1 | الموقع يصير عام جدًا | عالي | متوسط | Messaging House | Brand Director |
| 2 | claims مبالغ فيها | عالي | عالي | Claims Register + checker | Governance |
| 3 | build يفشل | عالي | متوسط | PR verification | QA |
| 4 | كثرة الصفحات تؤخّر الإطلاق | متوسط | عالي | 7-day sellable version | CEO |
| 5 | free tools تأخذ وقتًا | متوسط | عالي | specs أولًا ثم v1 | Growth |
| 6 | اختزال Dealix لـ CRM | عالي | متوسط | positioning checker | Brand |
| 7 | Command Sprint غير قابل للتسليم في 7 أيام | عالي | متوسط | scope مجمّد + template | Delivery |
| 8 | سعر 499 يُضعف الإشارة | متوسط | متوسط | تأطير "تأسيسي محدود" | CEO |
| 9 | لا proof حقيقي عند الإطلاق | عالي | متوسط | أول 3 sprints بسعر تأسيسي مقابل proof | CEO |
| 10 | فعل خارجي بلا موافقة | عالي | منخفض | approval gates + governance command | Governance |
| 11 | تسريب PII في logs | عالي | منخفض | non-negotiable #6 + اختبارات | Engineer |
| 12 | اعتماد على scraping/spam | عالي | منخفض | محرّمات + رفض | Governance |
| 13 | CI بصلاحيات زائدة | متوسط | متوسط | least-privilege | Engineer |
| 14 | حقن سياق غير موثوق في CI | عالي | منخفض | env-passing مقتبس | Engineer |
| 15 | تشتّت المؤسس بين الطبقات | متوسط | عالي | Execution Board + daily review | CEO |
| 16 | hreflang/i18n خاطئ | متوسط | متوسط | فحص + توثيق Google | Engineer |
| 17 | nurture يبدو spammy | متوسط | متوسط | No-Spam Policy | Governance |
| 18 | upsell مبكر يضر الثقة | متوسط | متوسط | upsell بعد proof فقط | Delivery |
| 19 | تغيّر الخطة كل جلسة | متوسط | عالي | Plan Freeze v1 | CEO |
| 20 | غياب أداة تتبّع | متوسط | متوسط | events.schema.json مبكرًا | Growth |
| 21 | اعتماد على موديول مستقبلي كأنه live | عالي | متوسط | Module Status Map | Brand |
| 22 | تأخر قرارات المؤسس | عالي | عالي | Founder Decision List | CEO |
| 23 | تكلفة الوقت على Custom AI مبكرًا | متوسط | متوسط | تأجيل لـ 90-day | CEO |
| 24 | شراكات بلا حوكمة | متوسط | منخفض | Partner one-pager + سجل | Governance |
| 25 | فقدان الذاكرة بين الجلسات | متوسط | متوسط | os/ memory schemas + ledgers | PM |

## 16. Top 25 Founder Decisions

> القرارات الاستراتيجية التي **يجب** أن يعتمدها المؤسس قبل التنفيذ (وإلا اختار Claude نيابةً — وهذا غير مرغوب).

**القرارات الحرجة الخمسة (تُحسم أولًا):**
1. **Primary CTA wording:** (a) Start Command Sprint · (b) Get Business OS Score · (c) Book Diagnostic
2. **First ICP:** (a) وكالات B2B · (b) استشارات/تدريب · (c) خدمات IT
3. **First price:** (a) 499 SAR founding sprint · (b) 1,500 SAR founding sprint · (c) 3,000 SAR setup
4. **Visual style:** (a) dark command center · (b) light enterprise · (c) hybrid
5. **Free tool priority:** (a) Business OS Score · (b) Revenue Leakage Calculator · (c) Proof Gap Audit

**بقية القرارات (6–25):** 6. لغة الإطلاق الأساسية (AR/EN) · 7. اسم النطاق/الـ subdomain للأدوات · 8. عدد الـ Proof Packs قبل رفع السعر · 9. سقف عملاء Command Sprint التأسيسي · 10. سياسة استرجاع المبلغ · 11. بوابة الدفع (Moyasar sandbox→live) · 12. أداة analytics (PostHog؟) · 13. أداة CRM (HubSpot؟) · 14. أداة الحجز (Calendly؟) · 15. هل ننشر Answer Library قبل الموقع؟ · 16. سياسة الشراكة/العمولة · 17. حدّ المحتوى الأسبوعي · 18. معيار "Done" للأداة المجانية · 19. مستوى تفصيل Proof Pack المُشارَك · 20. سياسة الـ case study (موافقة العميل) · 21. حدّ الـ Managed OS الأول · 22. تسعير Data-to-Revenue Pack النهائي · 23. متى نفعّل Custom AI · 24. سياسة الـ SLA للـ Managed OS · 25. معيار Go-Live النهائي (انظر Go/No-Go).

---

## 17. Definition of Done (لكل PR)

- **PR 1:** CLAUDE.md موجود · agents موجودة · skills/commands موجودة · لا كود مصدري مُلمَس.
- **PR 2:** brand identity · visual identity · messaging house · product family map · module status map · Dealix غير مختزل لـ CRM/Revenue.
- **PR 3:** Homepage · Command Sprint · Pricing · Start مُنفّذة · `npm run build` ينجح · لا ادعاءات مضمونة · CTA واحد لكل صفحة.
- **PR 4:** 3 أدوات مخطّطة/منفّذة · كل أداة تُخرج score + gaps + CTA.
- **PR 5:** growth docs · SEO/GEO plan · content factory · nurture · partner/referral · metrics.
- **PR 6:** delivery template · customer folder template · Proof Pack · Claims Register · Human Approval Policy · No-Spam Policy.
- **PR 7:** CI gate · positioning checker · growth checker · launch readiness checker · GitHub Actions least-privilege.

---

## 18. الخطوة التالية بالضبط (Next Prompt to Implement PR 2)

> PR 1 منفّذ في هذا الـ commit. بعد موافقة المؤسس على التجميد، الـ prompt التالي:

```
نفّذ PR 2 فقط من DEALIX_FULL_COMPANY_LAUNCH_BLUEPRINT.
أنشئ:
- docs/00_platform_truth/VISUAL_IDENTITY_SYSTEM.md
- docs/00_platform_truth/MESSAGING_HOUSE.md
- docs/00_platform_truth/PRODUCT_FAMILY_MAP.md
- docs/00_platform_truth/MODULE_STATUS_MAP.md
قواعد: Dealix = Saudi AI Business OS (ليس CRM/Revenue only). AR-first/EN-ready.
لا كود مصدري. التزم بالـ acceptance والـ DoD لـ PR 2.
انتهِ بـ: ماذا يراجع المؤسس قبل الموافقة.
```

---

## 19. Plan Freeze

```
هذه الخطة مجمّدة كـ v1.
لا يتغيّر تسلسل الـ PRs إلا عند ظهور blocker.
عند التنفيذ، اتبع الـ blueprint المجمّد.
أي انحراف يتطلّب موافقة المؤسس أولًا.
```

**في انتظار موافقة المؤسس قبل تنفيذ PR 2.**
