# Claims Register — سجل الادعاءات

**Status: INTERNAL**

> Purpose — الغرض: the register of every claim Dealix may make, each mapped to claim text (AR+EN), required evidence, safe wording, and status (approved/forbidden). Includes the forbidden→approved rewrite table and the no-overclaim rules. Grounded in `auto_client_acquisition/governance_os/` (`claim_safety`, `draft_gate`, `forbidden_actions`, `approval_matrix`). Cross-link: [HUMAN_APPROVAL_POLICY.md](./HUMAN_APPROVAL_POLICY.md), [../04_delivery/PROOF_PACK_TEMPLATE.md](../04_delivery/PROOF_PACK_TEMPLATE.md), [../05_founder/LAUNCH_GO_NO_GO.md](../05_founder/LAUNCH_GO_NO_GO.md).

سجل لكل ادعاء قد تطرحه دِيلِكس، مُربَط بنصّ الادعاء (عربي+إنجليزي)، والدليل المطلوب، والصياغة الآمنة، والحالة (معتمد/محظور). مُؤسَّس على وحدة الحوكمة البرمجية التي تفحص المسودات وتحجب الادعاءات غير الآمنة.

---

## How a claim is governed — كيف يُحكَم الادعاء

Every customer-facing line passes a deterministic scan (`claim_safety.audit_claim_safety`) before a human approves it:

- A **forbidden claim** (guarantees, fake proof) → **BLOCK**. — ادعاء محظور (ضمانات، إثبات مزيّف) ← حجب.
- A **forbidden operational term** (scraping, auto-send, cold WhatsApp) → **DRAFT_ONLY**, routed to review. — مصطلح تشغيلي محظور ← مسودة فقط، يُحوَّل للمراجعة.
- Clean text → **ALLOW**, but a human still approves customer-facing copy. — نص نظيف ← يُسمَح، مع بقاء الاعتماد البشري.

The scan is a shallow guardrail. It never replaces human approval; it only catches the obvious before a human looks.

الفحص حارس سطحي لا يحلّ محل الاعتماد البشري؛ يلتقط الواضح قبل أن ينظر الإنسان.

---

## No-overclaim rules — قواعد عدم المبالغة

1. No claim without evidence or safe wording. — لا ادعاء بلا دليل أو صياغة آمنة.
2. No revenue, ROI, or sales stated as fact. Use estimated / observed / verified / client_confirmed with the source. — لا إيراد أو عائد كحقيقة.
3. No guarantees. Replace with "evidenced opportunities" / "فرص مُثبتة بأدلة".
4. No fake proof, no invented testimonials. — لا إثبات مزيّف.
5. No public case study without customer approval. — لا دراسة حالة عامة دون اعتماد العميل.
6. No confidential third-party metrics — aggregated patterns and methodology only. — أنماط مُجمَّعة ومنهجية فقط.

---

## Claim entries — قيود الادعاءات

Each entry: claim text (AR+EN), evidence required, safe wording, status.

| # | Claim (EN / AR) | Evidence required | Safe wording | Status |
|---|---|---|---|---|
| C1 | "Dealix is a Saudi-first AI Business Operating System" / "دِيلِكس نظام تشغيل أعمال بالذكاء الاصطناعي سعودي-أولاً" | product scope docs | as written; positioning, not outcome | approved |
| C2 | "The Command Sprint delivers 8 modules" / "سبرنت القيادة يسلّم ٨ وحدات" | delivery OS playbook | name the 8 modules | approved |
| C3 | "We surface evidenced revenue opportunities" / "نُبرز فرص إيرادات مُثبتة بأدلة" | Proof Register entries with tiers | keep "evidenced," keep tiers | approved |
| C4 | "We guarantee X SAR in new sales" / "نضمن مبيعات بقيمة كذا" | none possible | replace — see rewrite table | forbidden |
| C5 | "Proven ROI for every client" / "عائد مُثبت لكل عميل" | none possible | "observed value where evidenced" | forbidden |
| C6 | "We send outreach on your behalf automatically" / "نرسل نيابةً عنك تلقائياً" | n/a — violates no-auto-send | replace — see rewrite table | forbidden |
| C7 | "Estimated dormant-value opportunity of X SAR" / "فرصة قيمة خاملة تقديرية بقيمة كذا" | Revenue Map + tier=estimated | keep "estimated" label | approved |
| C8 | "Verified value of X SAR" / "قيمة مُتحقَّقة بقيمة كذا" | `source_ref` / `confirmation_ref` | only with reference; else estimated | approved (conditional) |
| C9 | "We use scraped data to find leads" / "نستخدم بيانات مستخلَصة" | n/a — forbidden operation | replace — see rewrite table | forbidden |
| C10 | "Client confirmed X SAR realized" / "أكّد العميل تحقّق كذا" | `confirmation_ref` + customer approval | tier=client_confirmed only | approved (conditional) |

---

## Forbidden → approved rewrite table — جدول إعادة الصياغة

| Forbidden — محظور | Approved rewrite — البديل المعتمد |
|---|---|
| "guaranteed sales" / "نضمن مبيعات" | "evidenced opportunities" / "فرص مُثبتة بأدلة" |
| "guaranteed ROI" / "نضمن العائد" | "observed value where evidenced" / "قيمة مُلاحَظة حيث توفّر الدليل" |
| "proven results" (no source) / "نتائج مُثبتة" | "estimated, pending verification" / "تقديرية بانتظار التحقّق" |
| "we auto-send for you" / "نرسل تلقائياً نيابةً عنك" | "we prepare approval-ready drafts; you approve before any send" / "نُجهّز مسودات للاعتماد، وأنت تعتمد قبل أي إرسال" |
| "scraped leads" / "عملاء مستخلَصون" | "client-provided and lawfully sourced data" / "بيانات يقدّمها العميل بمصدر نظامي" |
| "we run cold WhatsApp campaigns" / "حملات واتساب باردة" | "approved, consented channels only" / "قنوات معتمدة وبموافقة فقط" |

---

## Status taxonomy for claims — تصنيف حالة الادعاء

- **approved** — may be used as written. — يُستخدَم كما هو.
- **approved (conditional)** — only with the named evidence/reference. — فقط بالدليل المُسمّى.
- **forbidden** — must be rewritten via the table; the scan blocks it. — يُعاد صياغته؛ الفحص يحجبه.

Any new claim not in this register defaults to forbidden until reviewed and added. The register is reviewed in [../05_founder/WEEKLY_BOARD_REVIEW.md](../05_founder/WEEKLY_BOARD_REVIEW.md).

أي ادعاء جديد غير مُدرَج يُعَدّ محظوراً حتى يُراجَع ويُضاف.

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
