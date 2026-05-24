# Founder-Led Sales Architecture — معمار البيع تحت قيادة المؤسس

> الهدف: قبول ≥ 5 Sprints + 1 Retainer خلال 90 يوماً، بدون scraping ولا cold automation.
> العقد: كل خطوة لها مدخَل واضح، حاجز حوكمة، ومُخرَج قابل للتدقيق.
> المراجع المرتبطة: [Master Holistic Plan](../transformation/MASTER_HOLISTIC_EXECUTION_PLAN_AR.md) + [AI Layers Doctrine Card](../transformation/AI_LAYERS_DOCTRINE_CARD_AR.md) + [Sprint Engine Playbook](../03_commercial_mvp/SPRINT_ENGINE_PLAYBOOK_AR.md).

## 1) الـ Funnel (المراحل الست)

| # | المرحلة | مدخل | مخرج | KPI |
|---|---|---|---|---|
| 1 | Warm-list Outreach | قائمة المؤسس (لا scraping) | drafts معتمَدة | ≥ 20 drafts بنهاية يوم 7 |
| 2 | Inbound + Diagnostic | استمارة `/dealix-diagnostic` | تقرير صفحتين | ≥ 8 diagnostics بنهاية يوم 30 |
| 3 | Qualification (8Q) | `sales_os.qualification.qualify(...)` | ACCEPT / DIAGNOSTIC_ONLY / REJECT | ≥ 50% ACCEPT rate |
| 4 | Proposal | `sales_os.proposal_renderer.render_proposal(...)` | عرض ثنائي اللغة | ≥ 5 proposals مرسَلة |
| 5 | Sprint Delivery | [Sprint Engine](../03_commercial_mvp/SPRINT_ENGINE_PLAYBOOK_AR.md) | Proof Pack + Capital Asset | ≥ 5 sprints مكتمَلة |
| 6 | Retainer / Upsell | `adoption_os.retainer_readiness.evaluate(...)` | اشتراك شهري | ≥ 1 retainer active |

## 2) الـ AI Layers في معمار البيع

| المرحلة | الطبقة | كيف تُستَخدَم |
|---|---|---|
| Warm-list | `growth_signals` | ترتيب الـ signals من إدخال المؤسس |
| Inbound | `lead_scoring` | تقييم استمارة الـ diagnostic |
| Qualification | `account_scoring` + `compliance_reasoning` | tier + PDPL check قبل التشخيص |
| Proposal | `content_generation` + `proof_curation` | bilingual draft + proof artifacts |
| Sprint | كل الطبقات | راجع Sprint Engine |
| Retainer | `customer_health` + `executive_intelligence` | درجة الصحة + grade |

## 3) Outreach Draft Production Loop (Founder-Led)

```
1. المؤسس يضيف 5-10 names إلى data/warm_list.csv (لا scraping).
2. `python scripts/warm_list_outreach.py --generate-drafts --count 5` ينتج drafts.
3. كل draft يمر بـ:
   - `governance_os.draft_gate.audit_draft_text(...)`
   - `claim_safety.audit_claim_safety(...)`
   - `ai_layers.content_generation.run(ctx)` لـ AR + EN
4. الـ drafts يدخلون `approval_center` queue.
5. المؤسس يراجع + يوافق + يرسل يدوياً.
```

## 4) Qualification Scorecard (8 سؤال)

```python
from auto_client_acquisition.sales_os.qualification import qualify

decision = qualify(
    pain_clear=True,           # العميل وصف ألم محدد
    owner_present=True,        # في الاجتماع شخص يقرِّر
    data_available=True,       # عنده CSV / CRM يستطيع تصديره
    accepts_governance=True,   # موافق على Source Passport + Approval gates
    has_budget=True,           # 499 SAR متوفر
    wants_safe_methods=True,   # لا يطلب scraping / cold spam / guaranteed sales
    proof_path_visible=True,   # نتفق على نوع Proof
    retainer_path_visible=True,# نناقش الاستمرار بعد Sprint
)
# decision in {ACCEPT, DIAGNOSTIC_ONLY, REFRAME, REJECT, REFER_OUT}
```

**القاعدة:** إذا `wants_safe_methods=False` → REJECT مع بديل آمن.

## 5) Proposal Architecture

```python
from auto_client_acquisition.sales_os.proposal_renderer import render_proposal, ProposalContext

ctx = ProposalContext(
    customer_handle="acme",
    offer_rung=1,  # Sprint
    price_sar=499,
    proof_score_target=70,
    capital_asset_min=1,
    governance_clauses=[
        "Source Passport required before AI use",
        "Approval Center for any external send",
        "No scraping / cold automation",
        "Proof Pack delivered at handoff",
    ],
    locale="bilingual",
)
proposal = render_proposal(ctx)
# proposal.body contains AR + EN parallel sections
```

## 6) Doctrine Refusals (قوالب رفض)

عند طلب عميل scraping / cold WhatsApp / LinkedIn automation / guaranteed sales:

```
شكراً [الاسم] — Dealix لا تقدِّم [scraping / cold WhatsApp automation / guaranteed sales].
السبب: نلتزم بـ PDPL + سياسات Dealix الـ 11 غير قابلة للتفاوض.
البديل الآمن: [draft-only outputs / consent-based outreach / evidenced opportunities].
هل تحب أصيغ لك الطرح البديل؟
```

## 7) Pipeline Hygiene (يومي)

- [ ] `approval_center` queue ≤ 24h age.
- [ ] `friction_log` آخر 14 يوم — صفر severity=high بلا قرار.
- [ ] `value_os.monthly_report` يُولَّد آخر كل شهر.
- [ ] `capital_os.list_assets` — كل sprint مكتمل له ≥ 1 asset.

## 8) Weekly Sales Review (60 دقيقة، الأحد)

1. (10د) فتح: عدد warm-list drafts + inbound + diagnostics + proposals + paid sprints.
2. (15د) Pipeline review — أين كل lead.
3. (10د) friction sweep + decisions.
4. (15د) AI Layers signals — `executive_intelligence` grade.
5. (10د) قرار: نسرِّع أم نتوقَّف عن البيع لتحسين Engine.

## 9) Founder Daily Cadence (25 دقيقة)

- (5د) فحص `approval_center` queue.
- (10د) draft مراجعة + إرسال.
- (5د) friction sweep.
- (5د) inbound replies.

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
