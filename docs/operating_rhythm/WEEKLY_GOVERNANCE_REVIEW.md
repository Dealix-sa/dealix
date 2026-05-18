# Weekly Governance Review — المراجعة الأسبوعية للحوكمة والدكترين

<!-- Owner: Founder | Cadence: weekly, inside the Weekly Operating Meeting (§5) | ~5 min -->
<!-- Arabic primary · English secondary -->

> الوكلاء و«الذكاء الظِّل» مخاطر تشغيلية حقيقية. Dealix تحتاج **تسجيلًا، مراقبة، وإيقافًا مركزيًا** للوكلاء ومخرجاتهم.
> هذه قائمة فحص يمكن للمؤسس تشغيلها حرفيًا كل أسبوع.
>
> AI agents and "shadow AI" are real operational risk. This is a runnable weekly checklist; it feeds item 5 of the [Weekly Operating Meeting](WEEKLY_OPERATING_MEETING.md).

---

## 1. قائمة الفحص — Checklist (tick every week)

| # | السؤال / Question | ✅ / ⚠️ / ❌ |
|---|-------------------|-------------|
| 1 | كل تشغيلات الذكاء (AI runs) هذا الأسبوع مُسجّلة؟ / All AI runs logged? | |
| 2 | كل المخرجات (outputs) لها governance status؟ / Every output has a governance status? | |
| 3 | ظهرت أي PII flags؟ تمّت معالجتها وتنقيتها (redact)؟ / Any PII flags — handled & redacted? | |
| 4 | رُفض أي claim غير مدعوم؟ / Any unsupported claim rejected? | |
| 5 | طلب أي عميل automation ممنوعة (cold outreach/scraping)؟ / Client asked for prohibited automation? | |
| 6 | طلب أي وكيل صلاحية أعلى من المسموح في MVP؟ / Any agent requested elevated autonomy? | |
| 7 | خرجت أي رسالة خارجية بلا موافقة (approval-first)؟ / Any external send without approval? | |
| 8 | ظهرت أي صياغة «نضمن / guaranteed»؟ / Any "نضمن"/"guaranteed" wording surfaced? | |
| 9 | وقع أي حادث (incident)؟ / Any incident this week? | |
| 10 | friction log أظهر `governance_block` متكرر؟ / Recurring `governance_block` in friction log? | |

---

## 2. قرارات صارمة — Hard rules (no discretion)

| الملاحظة / Finding | القرار / Decision |
|--------------------|-------------------|
| Output بلا governance status | **فشل QA** — يُصلَح قبل التسليم / QA fail — fix before delivery |
| إجراء خارجي بلا موافقة / external action without approval | **حادث** — مسار incident response / treated as incident |
| Agent autonomy > 3 في MVP | **حظر فوري** / immediate block |
| Claim غير مدعوم / unsupported claim | إزالة + إضافة **قاعدة/اختبار جديد** / remove + add new rule/test |
| صياغة ضمان («نضمن»/"guaranteed") | إعادة صياغة فورية — ممنوع دكترينيًا / rewrite — doctrine violation |
| PII في ملخص proof / PII in proof summary | تنقية (`redact_text`) قبل أي مشاركة / redact before any share |

> **مبدأ الدكترين:** بلا outreach بارد · بلا proof مزيّف · بلا وعود مضمونة · الموافقة أولًا.
> **Doctrine:** no cold outreach · no fake proof · no guaranteed claims · approval-first.

---

## 3. المخرج الأسبوعي — Weekly output (into the meeting)

سجّل في محضر الاجتماع الأسبوعي:

- [ ] **1 risk reduced** — مخاطرة حوكمة واحدة خُفّضت هذا الأسبوع (إجراء ملموس).
- [ ] أي بند ❌ يصبح **commitment** بمالك وتاريخ.
- [ ] أي حادث يُوثَّق في `docs/ops/INCIDENT_RUNBOOK.md`.

---

## 4. الكود والمراجع — Code & references

- `auto_client_acquisition/operating_rhythm_os/governance_review.py`
- `auto_client_acquisition/friction_log/` — مصدر `governance_block` events
- `standards_os/agent_control_standard.py` · `compliance_trust_os/` · `llm_gateway_v10/`
- مسار الحوادث / incidents: [`../ops/INCIDENT_RUNBOOK.md`](../ops/INCIDENT_RUNBOOK.md)
</content>
