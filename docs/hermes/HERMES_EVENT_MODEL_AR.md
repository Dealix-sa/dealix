# نموذج الأحداث في Hermes — Event Model

> المرجع: §27 (16 نوع حدث + Event Object) + مثال §36 (وكالة تطلب AI white-label).

---

## لماذا نموذج أحداث؟

Hermes ليس monolith. هو **bus + router**. كل ما يحدث في Dealix يُنشَر كحدث (event) على ناقل مركزي، ثم يوزَّعه Hermes على المُستهلكين المُصرَّح لهم وفق قواعد السيادة والحوكمة.

ميزة هذا التصميم:
- **قابلية تدقيق كاملة**: لا فعل بدون حدث، ولا حدث بدون توقيع زمني وسلسلة سببية.
- **تطور مستقل**: أي وحدة جديدة تُضاف بمجرد الاشتراك في الأحداث المعنية.
- **بوابات حوكمة**: Hermes يستطيع رفض حدث قبل توزيعه إن خرق سياسة.

---

## الـ 16 نوع حدث

| # | اسم الحدث | متى يُطلق | المُصدِر | المُستهلِك الافتراضي | مستوى السيادة |
|---|---|---|---|---|---|
| 1 | `signal.captured` | عند التقاط أي إشارة من قناة خارجية | Channel adapters | Opportunity engine | Internal |
| 2 | `signal.classified` | بعد تصنيف الإشارة (نوع/مصدر/أولوية) | Classifier agent | Routing layer | Internal |
| 3 | `opportunity.created` | عند تأهيل إشارة كفرصة | Opportunity engine | Decision queue | Internal |
| 4 | `opportunity.qualified` | بعد فحص ICP/ميزانية/توقيت | Qualification agent | Sovereign / Decision queue | Internal → Sovereign إن > حد المالية |
| 5 | `decision.requested` | عند الحاجة لقرار بشري | Hermes | Sovereign Workspace / Internal | حسب النوع |
| 6 | `decision.recorded` | بعد تسجيل القرار في Decision Journal | Decision API | كل من يحتاج تتبّع | Sovereign-readable |
| 7 | `execution.started` | بدء وكيل أو إجراء | Agent runtime | Trust Workspace | Internal |
| 8 | `execution.completed` | انتهاء التنفيذ بنجاح | Agent runtime | Outcome ledger | Internal |
| 9 | `execution.failed` | فشل تنفيذ أو خرق سياسة | Agent runtime / Guardrail | Trust + Sovereign | Sovereign-alert |
| 10 | `trust.evidence_pack_built` | بناء حزمة دليل (راجع [EVIDENCE_PACK_AR.md](EVIDENCE_PACK_AR.md)) | Evidence builder | Customer / Sovereign | Customer-visible |
| 11 | `outcome.measured` | قياس Estimated/Observed/Verified | Value ledger | Money Engine | Internal |
| 12 | `asset.created` | تحويل نتيجة متكررة إلى أصل | Asset registry | Capital OS | Internal |
| 13 | `asset.reused` | إعادة استخدام أصل في صفقة جديدة | Any consumer | Capital OS | Internal |
| 14 | `scale.decided` | قرار توسيع أصل/منتج/قطاع | Sovereign | كل الـ workspaces | Sovereign |
| 15 | `kill.decided` | قرار إنهاء أصل/منتج/قطاع | Sovereign | كل الـ workspaces | Sovereign |
| 16 | `governance.alert` | تنبيه حوكمة (تجاوز/خرق/خطر) | Guardrails | Sovereign + Trust | Sovereign |

> ملاحظة: مستوى السيادة الافتراضي يُحدِّد من يستطيع قراءة الحدث، لا من ينتجه. القراءة تخضع لقاعدة Workspaces (راجع [WORKSPACES_OVERVIEW_AR.md](WORKSPACES_OVERVIEW_AR.md)).

---

## Event Object — الشكل القياسي

كل حدث يلتزم بهذا الشكل:

```json
{
  "event_id": "evt_01HXYZ...",
  "event_type": "opportunity.qualified",
  "timestamp": "2026-05-24T09:14:22Z",
  "actor": {
    "kind": "agent | human | system",
    "id": "agent.qualifier.v3"
  },
  "subject": {
    "kind": "signal | opportunity | decision | asset | ...",
    "id": "opp_8841"
  },
  "context": {
    "workspace": "internal",
    "vertical": "agency_whitelabel",
    "source_event": "evt_01HXYW..."
  },
  "payload": { },
  "sovereignty_level": "internal",
  "evidence_refs": ["ev_pack_771"],
  "trace_id": "trc_01HX...",
  "version": "1.0"
}
```

الحقول الإلزامية: `event_id`, `event_type`, `timestamp`, `actor`, `subject`, `sovereignty_level`. باقي الحقول اختيارية لكن مُوصى بها.

---

## مثال مُفصَّل — وكالة تطلب AI white-label (§36 مثال 1)

السيناريو: وكالة سعودية ترسل استفسارًا عبر نموذج موقع Dealix يطلب فيه white-label لـ AI agent يُعرَض لعملائها. التتبع الكامل لسلسلة الأحداث:

```json
[
  {
    "event_id": "evt_001",
    "event_type": "signal.captured",
    "timestamp": "2026-05-24T08:02:11Z",
    "actor": {"kind": "system", "id": "channel.web_form"},
    "subject": {"kind": "signal", "id": "sig_4421"},
    "payload": {"source": "web_form", "raw": "agency asking about white-label"},
    "sovereignty_level": "internal"
  },
  {
    "event_id": "evt_002",
    "event_type": "signal.classified",
    "actor": {"kind": "agent", "id": "agent.classifier.v2"},
    "subject": {"kind": "signal", "id": "sig_4421"},
    "payload": {"category": "partner_inquiry", "vertical": "agency_whitelabel", "priority": "high"}
  },
  {
    "event_id": "evt_003",
    "event_type": "opportunity.created",
    "actor": {"kind": "system", "id": "opportunity.engine"},
    "subject": {"kind": "opportunity", "id": "opp_8841"},
    "context": {"source_event": "evt_002"}
  },
  {
    "event_id": "evt_004",
    "event_type": "opportunity.qualified",
    "actor": {"kind": "agent", "id": "agent.qualifier.v3"},
    "subject": {"kind": "opportunity", "id": "opp_8841"},
    "payload": {"icp_match": true, "budget_band": "TBD", "fit_score": 0.82}
  },
  {
    "event_id": "evt_005",
    "event_type": "decision.requested",
    "actor": {"kind": "system", "id": "hermes"},
    "subject": {"kind": "opportunity", "id": "opp_8841"},
    "payload": {"decision_type": "partner_admission", "required_level": "sovereign"},
    "sovereignty_level": "sovereign"
  },
  {
    "event_id": "evt_006",
    "event_type": "decision.recorded",
    "actor": {"kind": "human", "id": "sami"},
    "subject": {"kind": "decision", "id": "dec_2210"},
    "payload": {"outcome": "approved_pilot", "rationale_ref": "journal_dec_2210"}
  },
  {
    "event_id": "evt_007",
    "event_type": "execution.started",
    "actor": {"kind": "agent", "id": "agent.partner_onboarding.v1"},
    "subject": {"kind": "opportunity", "id": "opp_8841"}
  },
  {
    "event_id": "evt_008",
    "event_type": "trust.evidence_pack_built",
    "actor": {"kind": "system", "id": "evidence.builder"},
    "subject": {"kind": "opportunity", "id": "opp_8841"},
    "evidence_refs": ["ev_pack_904"]
  },
  {
    "event_id": "evt_009",
    "event_type": "execution.completed",
    "actor": {"kind": "agent", "id": "agent.partner_onboarding.v1"},
    "subject": {"kind": "opportunity", "id": "opp_8841"},
    "payload": {"partner_workspace_id": "pw_55"}
  },
  {
    "event_id": "evt_010",
    "event_type": "outcome.measured",
    "actor": {"kind": "system", "id": "value.ledger"},
    "subject": {"kind": "opportunity", "id": "opp_8841"},
    "payload": {"estimated_value": "TBD", "observed_value": "TBD"}
  },
  {
    "event_id": "evt_011",
    "event_type": "asset.created",
    "actor": {"kind": "system", "id": "asset.registry"},
    "subject": {"kind": "asset", "id": "asset_whitelabel_kit_v2"},
    "payload": {"asset_type": "playbook+template", "reusable": true}
  }
]
```

في هذا المثال، إشارة واحدة من نموذج ويب تتحول عبر 11 حدثًا إلى أصل قابل لإعادة الاستخدام مع شركاء آخرين دون تكلفة هامشية إضافية.

---

## English Summary

- Hermes is an event bus with 16 canonical event types covering the full Signal-to-Asset loop.
- Every event follows a single schema with mandatory fields (id, type, timestamp, actor, subject, sovereignty level) and optional fields for context, payload, and evidence refs.
- Sovereignty level on each event controls who can read it; the workspace isolation rules in `WORKSPACES_OVERVIEW_AR.md` enforce distribution.
- The worked example traces an agency white-label inquiry across 11 events from `signal.captured` to `asset.created`, showing how one signal becomes a reusable asset.
- Event payloads keep estimated/observed value as "TBD" rather than fabricating numbers.
