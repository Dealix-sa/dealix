# Dealix Sovereign OS — Hermes Universal Kernel

> هذا التوثيق يلخص الكود الفعلي تحت `dealix/hermes/` ويربطه بفقرات الخطة (111–140).
> الكود هو المرجع. أي تعارض → الكود يفوز.

## القاعدة الذهبية

كل شيء يمر في نفس الأنبوب:

```
Signal → Opportunity → Decision → Execution → Outcome → Asset
```

لا يوجد module يعمل خارج هذا النمط. الـ `payload` يحمل المحتوى الخاص بكل مجال (money, partner, customer, …) لكن البنية واحدة.

## خريطة الموديولات (مطابقة لفقرة 111)

| Module | المسار | المسؤولية |
| --- | --- | --- |
| Core | `dealix/hermes/core/` | الأنبوب العام + scoring + scale/kill + events |
| Sovereignty | `dealix/hermes/sovereignty/` | S0..S5، classifier، kill switch، sovereign memory، decision journal، capital |
| Trust | `dealix/hermes/trust/` | registries، permission matrix، approvals، guardrails، evidence، audit، MCP gateway، incidents، risk |
| Money | `dealix/hermes/money/` | cash scout، revenue hunter، proposal factory، pricing، followups، invoice، dashboard |
| Products | `dealix/hermes/products/` | offer builder، library، landing pages، experiments، packaging، tiers، scale/kill |
| Partners | `dealix/hermes/partners/` | scout، fit score، pitch، onboarding، revenue share، performance، risk |
| Intelligence | `dealix/hermes/intelligence/` | market radar، sector radar، tender radar، competitor watch، trend→offer، reports، open data |
| Training | `dealix/hermes/training/` | workshops، materials، enablement، certifications، prompt packs |
| Customer | `dealix/hermes/customer/` | onboarding، health score، value report، renewal، upsell، churn، case studies |
| Ventures | `dealix/hermes/ventures/` | vertical launcher، portfolio، kill/scale، micro products، acquisition scout |
| API | `dealix/hermes/api/` | capability gateway، developer docs، rate limit |
| Marketplace | `dealix/hermes/marketplace/` | listings، ratings |
| Audit | `dealix/hermes/audit/` | No-Orphan auditor، Red Flag detector (129/132) |
| Kernel | `dealix/hermes/kernel.py` | الـ facade الذي يربط كل ما سبق |

## مستويات السيادة (S0..S5) — فقرة 113

| Level | المعنى | السلوك في الكود |
| --- | --- | --- |
| S0 | Auto Safe | يسمح تلقائيًا (summarize, classify) |
| S1 | Internal | يسمح تلقائيًا (drafts, internal tasks) |
| S2 | Sami Approval | يضع طلبًا في `ApprovalCenter` ولا ينفذ |
| S3 | Sovereign Memo | يحتاج memo + موافقة سامي يدويًا |
| S4 | Sovereign Only | الـ kernel يرفض التنفيذ التلقائي بالكامل |
| S5 | Never Autonomous | يُحظر دائمًا (wire_transfer, sign_contract) |

التطبيق:
- `dealix/hermes/sovereignty/classifier.py`
- `dealix/hermes/sovereignty/approval_rules.py`

## قواعد لا يجوز كسرها (Trust + No-Orphan)

- **No agent without KPI** → `AgentRegistry.register` يرفض البطاقة الفارغة.
- **No tool without owner** → `ToolRegistry.register` يرفض البطاقة بلا owner.
- **High-risk tool ⇒ requires_approval** → يُفرض عند التسجيل.
- **No execution without outcome** → `NoOrphanAudit` يكشف الـ executions المكتملة بدون outcome.
- **Customer without value report** → يظهر red flag بعد 35 يومًا.
- **Partner without performance review** → يظهر red flag بعد 30 يومًا.
- **No marketplace publish بدون سامي** → `Marketplace.publish` ترفض أي approver آخر.
- **No SAR movement بدون سامي** → `CapitalLedger.disburse` ترفض الجميع عدا `sami`.

## مثال تشغيل سريع

```python
from dealix.hermes.kernel import HermesKernel
from dealix.hermes.core.schemas import Signal, Opportunity, Decision
from dealix.hermes.core.scoring import ScoreInputs
from dealix.hermes.sovereignty.levels import SovereigntyLevel

k = HermesKernel()
sig = k.signals.receive(Signal.make(source="email", domain="money", summary="lead"))
opp = k.opportunities.add(Opportunity.make(signal_id=sig.id, domain="money", title="Pilot"))
k.scorer.score(opp, ScoreInputs(cash_speed=0.7, close_probability=0.5,
                                 deal_value_sar=80_000, strategic_value=0.6, risk=0.2))
k.opportunities.mark_scored(opp.id); k.opportunities.queue(opp.id)

dec = Decision.make(opportunity_id=opp.id, action="draft_proposal",
                    sovereignty_level=SovereigntyLevel.S1_INTERNAL,
                    rationale="Draft pilot pack")
k.decisions.file(dec, domain="money")   # S1 → auto-approved
```

## تشغيل الاختبارات

اختبارات Hermes معزولة عن الـ conftest العام (الذي يحمّل قاعدة بيانات + LLM).
تشغيلها مستقلًا:

```bash
python -m pytest tests/hermes -q -o addopts="" --confcutdir=tests/hermes
```

## المنتجات الثلاثة الرئيسية (فقرة 138)

تجدها في `dealix/hermes/products/flagship.py`:

1. **Revenue Hunter Pilot** — 14,900 SAR / أسبوعين.
2. **AI Trust Kit** — 49,000 SAR / 4 أسابيع.
3. **Agency White-label Kit** — 29,000 SAR / 3 أسابيع.

كل عرض جاهز للتسجيل عبر `OfferBuilder.draft(...)`.
