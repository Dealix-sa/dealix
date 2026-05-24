# Sprint Engine Playbook — كتيب تشغيل Revenue Intelligence Sprint

> العقد: تسليم Sprint بقيمة 499 SAR خلال 7 أيام، بأقل من 5 ساعات من وقت المؤسس، مع Proof Pack score ≥ 70 + capital asset ≥ 1.
> العقد التشغيلي الموازي: [AI Layers Doctrine Card](../transformation/AI_LAYERS_DOCTRINE_CARD_AR.md) + [Master Holistic Execution Plan](../transformation/MASTER_HOLISTIC_EXECUTION_PLAN_AR.md).

## 1) الجدول الزمني (Day 1 → Day 7)

| اليوم | المهمة | الـ AI Layer المستخدَم | المُخرَج | وقت المؤسس |
|---|---|---|---|---|
| 1 | Kickoff + Source Passport | — | `SourcePassport` validated | 45د |
| 2 | Data import + DQ score | — | `dq_score` ≥ 70 | 30د |
| 3 | Top 10 Account scoring | `account_scoring` | 10 accounts ranked + reasons | 45د |
| 4 | Bilingual drafts | `content_generation` + `compliance_reasoning` | 5 drafts + governance decisions | 60د |
| 5 | Proof Pack assembly | `proof_curation` + `decision_passport` | 14-section ProofPack + score | 60د |
| 6 | Handoff + founder review | `executive_intelligence` | Pack + recommendations | 30د |
| 7 | Capital asset + Retainer eligibility | `customer_health` + `growth_signals` | Asset registered + retainer decision | 30د |

**إجمالي وقت المؤسس:** 5 ساعات بالضبط — متى زاد عن ذلك بعد العميل الخامس → نوقف بيع جديد ونحسِّن الـ Engine.

## 2) Pre-flight (قبل Day 1)

- [ ] العميل دفع 50% (250 SAR) عبر Moyasar live mode.
- [ ] `tests/test_doctrine_guardrails.py` PASS.
- [ ] `curl $PROD/api/v1/ai-layers/` يعود 200.
- [ ] `Source Passport` template جاهز للعميل (`docs/14_trust_os/source_passport_template.md`).

## 3) Day-by-Day Detail

### Day 1 — Kickoff
1. مكالمة 30 دقيقة مع العميل.
2. تعبئة `SourcePassport` (source_id, owner, allowed_use, contains_pii, sensitivity, retention_policy, ai_access_allowed, external_use_allowed).
3. `auto_client_acquisition.data_os.validate(passport)` → إذا False BLOCK + اطلب التصحيح.
4. أرسل email تأكيد عبر `email/transactional.send_transactional(kind='sprint_kickoff', ...)`.

### Day 2 — Data + DQ
1. العميل يرسل CSV / CRM export.
2. `data_os.preview(file)` → عرض أول 10 صفوف + المخطط.
3. `data_os.compute_dq(...)` → إذا < 70 المؤسس يراجع.

### Day 3 — Account Scoring
```python
from auto_client_acquisition.ai_layers import LayerContext, run_layer

for account in top_10_accounts:
    ctx = LayerContext(
        customer_id=customer_id,
        payload={
            "account_name": account["name"],
            "icp_signals": account["icp"],
            "readiness_signals": account["readiness"],
            "estimated_acv_sar": account["acv"],
        },
        source_refs=(account["source_ref"],),
    )
    result = run_layer("account_scoring", ctx)
    # store result.output for the Proof Pack.
```

### Day 4 — Drafts
```python
ctx = LayerContext(
    customer_id=customer_id,
    payload={"topic": "Revenue Sprint", "audience": "fintech", "cta": "Reply by Sunday."},
    source_refs=("founder://sprint/001",),
    external_action_requested=False,  # المؤسس يراجع قبل الإرسال
)
draft = run_layer("content_generation", ctx)
# draft.governance_decision == "DRAFT_ONLY"
```

### Day 5 — Proof Pack
1. `proof_os.assemble(engagement_id, customer_id, source_passport, dq_score, value_events, governance_events, ...)`.
2. الحد الأدنى: 14 sections + score ≥ 70.
3. إذا < 70 → نراجع Day 3-4 ونعيد.

### Day 6 — Handoff
1. مكالمة 30 دقيقة، شاشة مشترَكة، شرح كل قسم.
2. العميل يدفع الـ 50% الباقي (250 SAR).
3. `value_os.add_event(tier='observed', ...)` عن النواتج المَلحوظة.

### Day 7 — Capital + Retainer
1. اختر أصل قابل للإعادة (scoring_rule / draft_template / governance_rule / proof_example / sector_insight).
2. `capital_os.add_asset(asset_type=..., source_engagement_id=..., reusability_notes=...)`.
3. `adoption_os.retainer_readiness.evaluate(customer_id)` → إذا eligible قدِّم 2,999 SAR/mo.

## 4) Governance Gates (لا تُتجاوز)

- [ ] كل draft مرَّ على `governance_os.decide(action='generate_draft', ...)`.
- [ ] كل external send (لا يحدث في Sprint عادةً) مرَّ بـ `approval_center`.
- [ ] كل value event له `tier` صحيح (لا auto-promote).
- [ ] Proof Pack له ≥ 14 sections.
- [ ] Capital asset مسجَّل قبل إغلاق Sprint.

## 5) Friction Discipline

كل تدخُّل بشري → `friction_log.emit(customer_id, kind=..., severity=..., notes=sanitized)`.

أمثلة:
- DQ score < 70 → kind=`data_quality`, severity=`medium`.
- العميل لم يرد على email لأكثر من 48h → kind=`response_latency`, severity=`low`.
- claim_safety blocked draft → kind=`content_safety`, severity=`high`.

## 6) Exit Criteria

Sprint يُعتبر مكتملاً عند:
- ✅ Proof Pack score ≥ 70.
- ✅ ≥ 1 Capital Asset مسجَّل.
- ✅ كل القيود الإلزامية على governance_decision موثَّقة.
- ✅ الـ 50% الباقي مدفوع.
- ✅ Retainer decision موَثَّق (مقبول / مؤجَّل / مرفوض).

## 7) After-action

- يومان لاحقاً: إرسال QBR summary (case-safe) للعميل.
- أسبوع لاحق: إذا qualifying → عرض Managed Ops 2,999 SAR/mo.

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
