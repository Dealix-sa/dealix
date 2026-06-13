# Dealix Command Sprint — Private Launch Offer / عرض الإطلاق الخاص

> A founder-led, custom engagement for the private-launch phase. It is **distinct**
> from the self-serve productized plans (`/api/v1/pricing/plans`) and from the
> rung-0 **Free Diagnostic (0 SAR)**. It maps onto the existing service catalog
> (esp. `docs/26_service_catalog/REVENUE_INTELLIGENCE_SPRINT_SERVICE.md`).
>
> ⚠️ **Pricing note:** the price below is the founder's stated private-launch price.
> No committed price in `docs/30_pricing/` contradicts it (those files are
> scope/role stubs). Reconcile this into `docs/30_pricing/SPRINT_PRICING.md`
> and the 5-plan pricing map before any public pricing page uses it.

---

## 1. One-line offer / السطر الواحد

**EN:** Dealix turns scattered follow-up, offers, and revenue decisions into an
**approval-first** AI revenue-operating workflow — with human approvals, execution
evidence, and an executive view of where opportunities leak — in **10 working days**.

**AR:** نحوّل فوضى المتابعة والعروض والقرار التجاري إلى نظام تشغيل إيرادات مدعوم
بالذكاء الاصطناعي بأسلوب **الموافقة أولًا** — مع موافقات بشرية، أدلة تنفيذ،
وتقارير إدارية تبيّن أين تضيع الفرص — خلال **10 أيام عمل**.

---

## 2. Target client (ICP) / العميل المستهدف

B2B service companies in Saudi Arabia with: inconsistent sales follow-up · unclear
or unmeasured offers · missed opportunities · no executive revenue view · scattered
WhatsApp/email operations · a need for proof, control, and measurable next actions.

See `docs/29_sales_os/ICP_SCORECARD.md` to qualify before proposing.

---

## 3. Price & timeline / السعر والمدة

- **Price:** **7,500–15,000 SAR** (first private-launch clients).
- **Timeline:** **10 working days.**
- Price band reflects scope/risk per `docs/30_pricing/PRICING_ARCHITECTURE.md`
  ("price logic tied to risk"). Final number set per qualified scope.

---

## 4. Deliverables / المخرجات

1. Business intake + current workflow map.
2. Lead & follow-up audit (where opportunities leak).
3. Offer/proposal audit.
4. WhatsApp/email response map (manual + approval-first — **no cold automation**).
5. Executive dashboard prototype (revenue-leakage view).
6. Approval-first AI workflow (drafts → human approves → execute).
7. Dry-run AI assistant (no live external action without approval).
8. **Proof Pack** (bilingual, evidence-backed) — see `scripts/dealix_proof_pack.py`.
9. CEO brief.
10. Retainer proposal (path to Monthly RevOps / Governance OS).

Deliverables reuse the existing catalog — they do not invent new doctrine.

---

## 5. Rules & exclusions (non-negotiable) / القواعد والاستثناءات

- ❌ No guaranteed-revenue claims. النتائج التقديرية ليست نتائج مضمونة.
- ❌ No cold WhatsApp automation (`docs/29_sales_os/OBJECTION_NO_WHATSAPP_AUTOMATION.md`).
- ❌ No scraping without a lawful basis (`OBJECTION_NO_SCRAPING.md`).
- ❌ No autonomous live payment or external commitment without founder/client approval.
- ✅ AI drafts, analyzes, recommends; **humans approve**; every sensitive action is gated.

These mirror `dealix/registers/no_overclaim.yaml` and the service exclusions in
`docs/26_service_catalog/SERVICE_EXCLUSIONS.md`.

---

## 6. Success criteria / معايير النجاح

- Client can see **where** revenue leaks.
- Client receives a usable approval-first operating workflow.
- Client receives an evidence-backed Proof Pack.
- Client has a clear next step into a monthly retainer.

---

## 7. 5-minute demo flow / مخطط العرض في 5 دقائق

1. **Problem:** companies lose revenue to lost follow-up, weak offers, and no clear
   next action — not (only) missing tools.
2. **Dealix:** an AI revenue-operating system that analyzes, prioritizes, recommends,
   and documents — while sensitive execution stays **human-approved**.
3. **In 10 days:** map the workflow → expose leaks → tidy follow-up → sharpen the
   offer → build a dashboard prototype → produce a Proof Pack → hand the CEO a clear
   decision.
4. **What we never claim:** guaranteed revenue; no message sent without approval; no
   data pulled without lawful basis; no live payment without approval.
5. **Next step:** start a Command Sprint at the private-launch price, then decide on a
   monthly retainer.

Use with `docs/29_sales_os/DISCOVERY_CALL_SCRIPT.md` and the objection library.

---

## 8. First-contact message — MANUAL USE ONLY / رسالة أولى — يدوية فقط

> ⚠️ **Manual, approval-first.** This template is for a human to send after a warm
> intro. It is **not** wired to any automation and **must not** be sent by the
> system. No cold outreach.

```text
السلام عليكم أستاذ/أستاذة [الاسم]،

أنا [الاسم] من Dealix. نحوّل فوضى المتابعة والعروض والقرار التجاري داخل الشركات
إلى نظام تشغيل واضح مدعوم بالذكاء الاصطناعي — بطريقة approval-first بحيث لا يُرسل
أو يُنفّذ أي شيء حساس بدون موافقة.

عندنا عرض Private Launch اسمه Dealix Command Sprint: خلال 10 أيام نراجع تدفق الفرص
والمتابعة والعروض، ونبني Proof Pack ونظام تشغيل أولي يوضّح أين تضيع الفرص وما
الخطوة التالية.

هل يناسبك اتصال قصير 20 دقيقة هذا الأسبوع؟
```

---

## 9. Related assets / أصول ذات صلة

- Proposals: `docs/29_sales_os/PROPOSAL_TEMPLATE_REVENUE_INTELLIGENCE.md`
- Qualification: `docs/29_sales_os/QUALIFICATION_DECISION_TREE.md`
- Objection handling: `docs/29_sales_os/OBJECTION_*.md`
- Prospect tracking: `docs/ops/pipeline_tracker.csv` (use the existing list — do not
  start a new blank one)
- Launch decision: `docs/ops/OFFICIAL_PRIVATE_LAUNCH_DECISION.md`

_Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة._
