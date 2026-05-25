# Growth Experiments — تجارب النمو المحوكمة

> Section 41. ExperimentCard schema، 10 أنواع تجارب، قاعدة المتغيّر الواحد، وثلاثة أمثلة محلولة.
> Module path: `dealix/growth_os/experiments/`

---

## مقدّمة — Introduction

التجربة في Dealix ليست A/B test على زر. هي قرار محدود الوقت بإطار قبول/رفض واضح، يُوثَّق في `ExperimentCard`، ويُغذّي Growth Learning Loop.

An experiment at Dealix is a time-boxed decision with an explicit accept/reject frame — documented, attributed, and fed back to the playbook.

---

## قاعدة المتغيّر الواحد — One-Variable-at-a-Time

> **متغيّر واحد فقط لكل تجربة.** إن غيّرت السعر، لا تغيّر القناة. إن غيّرت الرسالة، لا تغيّر العرض.

السبب: بدون عزل المتغيّر، النتيجة لا تُعَلِّمنا شيئاً. تُصبح vibes، لا data.

---

## ExperimentCard Schema

```json
{
  "experiment_id": "EXP-2026-0017",
  "title": "Price test: Governance Snapshot 5K vs 8K",
  "hypothesis": "رفع السعر من 5K إلى 8K ر.س لن يخفّض close_rate أكثر من 20%.",
  "experiment_type": "price_point",
  "variable_under_test": "price",
  "control": {"price_sar": 5000},
  "treatment": {"price_sar": 8000},
  "constants": [
    "offer_scope",
    "channel = abm_direct",
    "icp = agencies",
    "message_template_version = v3"
  ],
  "sample_target": 12,
  "duration_days": 21,
  "success_criteria": {
    "primary": "close_rate_drop_pct <= 20",
    "secondary": "median_proposal_to_signature_days <= 10"
  },
  "decision_rule": "if primary passes → adopt treatment; else → keep control or reprice",
  "status": "running",
  "started_at": "2026-05-10",
  "owner": "founder",
  "results": null,
  "decision": null,
  "learning_entry_id": null,
  "disclosures": [
    "Small sample; results are directional not statistical."
  ]
}
```

---

## أنواع التجارب العشرة — The 10 Experiment Types

| # | النوع | المتغيّر | مثال |
|---|---|---|---|
| 1 | Message Angle | زاوية الرسالة | "Compliance angle" vs "Revenue angle" |
| 2 | Price Point | السعر | 5K vs 8K |
| 3 | Channel | قناة الوصول | LinkedIn DM vs email |
| 4 | Offer Scope | نطاق العرض | Snapshot vs Snapshot + Pilot |
| 5 | ICP | شريحة العميل | Agencies vs B2B SMB |
| 6 | CTA Wording | نص الـ CTA | "احجز" vs "اطّلع" |
| 7 | Landing Page Layout | بنية الصفحة | Long-form vs scannable |
| 8 | Proof Asset | نوع الدليل | ProofPack PDF vs interactive demo |
| 9 | Cadence | تردّد المتابعة | 3 رسائل/14 يوم vs 5/14 |
| 10 | Partner Motion | حركة الشريك | direct vs partner-led |

---

## بوّابات التجربة — Experiment Gates

1. **G1 — Hypothesis Clarity.** هل الفرضية قابلة للدحض؟
2. **G2 — Single Variable.** هل المتغيّر معزول؟
3. **G3 — Sample Realism.** هل الـ sample قابل للوصول خلال المدّة؟
4. **G4 — Decision Rule.** هل قاعدة القرار مكتوبة قبل البدء؟
5. **G5 — Constitution Check.** لا يخالف رفضًا موثَّقًا.

---

## ثلاثة أمثلة محلولة — Three Worked Examples

### Example A — Message Angle

- **Hypothesis.** "Compliance angle" يولّد reply_rate أعلى من "Revenue angle" بـ ≥ 5 نقاط مئويّة في وكالات الرياض.
- **Variable.** زاوية الرسالة فقط.
- **Constants.** السعر، القناة (LinkedIn DM), ICP، الـ CTA.
- **Sample.** 20 رسالة × زاوية = 40 رسالة.
- **Duration.** 14 يوم.
- **Decision Rule.** اعتمد الفائز إن الفرق ≥ 5pp ولم تنخفض meeting_rate.
- **Outcome (placeholder).** `<TBD: founder fill>`.

### Example B — Price Point

- **Hypothesis.** 8K لا يُسقط close_rate أكثر من 20% مقارنة بـ 5K.
- **Variable.** السعر فقط.
- **Constants.** scope، channel، ICP، message.
- **Sample.** 12 محادثة بيع.
- **Duration.** 21 يوم.
- **Decision Rule.** إن النتيجة pass → ادفع للسعر الأعلى. إن fail → جرّب bundling.
- **Outcome (placeholder).** `<TBD>`.

### Example C — Channel

- **Hypothesis.** Partner-referred leads يغلقون بسرعة meeting→signature ≤ 7 يوم مقابل ≤ 14 لـ ABM direct.
- **Variable.** القناة فقط.
- **Constants.** offer, price, ICP, message frame.
- **Sample.** 10 صفقات لكل قناة.
- **Duration.** 60 يوم.
- **Decision Rule.** إن partner ≤ 7 يوم بنفس margin → زِد نسبة العمولة وادفع للنمو عبر الشركاء.
- **Outcome (placeholder).** `<TBD>`.

---

## بعد التجربة — Post-Experiment

كل تجربة تنتج `LearningEntry`:

```json
{
  "learning_id": "LRN-2026-0017",
  "experiment_id": "EXP-2026-0017",
  "decision": "adopt_treatment | keep_control | run_again | kill",
  "playbook_updates": ["OfferCard.OFF-GOV-SNAP-001.price = 8000"],
  "next_experiment_id": "EXP-2026-0018"
}
```

---

## How to verify

```bash
bash scripts/growth_os_master_verify.sh
```

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
