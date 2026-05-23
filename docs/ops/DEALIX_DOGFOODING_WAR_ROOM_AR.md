# Dealix Dogfooding — غرفة إيراد داخلية

**الغرض:** تشغيل نفس مسار War Room + Evidence على معالم الشركة (ليس عملاء خارجيين فقط).

---

## المصادر

| أصل | مسار |
|-----|------|
| أهداف داخلية | [dealix_internal_war_room_seed.csv](../commercial/operations/targeting/dealix_internal_war_room_seed.csv) |
| مخرجات JSON | `data/dealix_dogfooding_war_room.json` |
| سكربت | `py -3 scripts/founder_dogfooding_war_room_sync.py` |

---

## إيقاع

1. **صباحاً** — مع `run_founder_commercial_day` راجع المعالم الداخلية في `/ops/war-room` أو JSON.
2. **بعد كل معلم** — سطر في [evidence_events_tracker.csv](../commercial/operations/evidence_events_tracker.csv) (`company=Dealix: ...`).
3. **أسبوعياً** — نفس scorecard وقرار أسبوعي؛ `supports_phase` في قرار الأسبوع يوجّه مرحلة MASTER.

---

## قواعد

- لا أرقام إيراد مخترعة — KPI من import فقط.
- لا إرسال خارجي — المعالم الداخلية `channel=manual|github`.
- anti-waste قبل أي حملة Dealix العامة.

---

*مرتبط بمهام J1–J6 في [FOUNDER_MAX_OPS_BACKLOG_AR.md](FOUNDER_MAX_OPS_BACKLOG_AR.md)*

---

## Document Standard Compliance

## Purpose
Defines this operating document's role inside Dealix Company OS.

## Owner
Sami (Founder). Reassign to the responsible operator when one is named.

## Review Cadence
Weekly until stable, then monthly.

## Inputs
- Relevant company data and signals.
- Founder decisions and customer evidence.

## Outputs
- Operating guidance, decisions, or templates produced by this document.
- Evidence captured for verification.

## Rules
- Must support revenue, delivery, trust, learning, or founder leverage.
- Must not introduce unsupported claims.
- Must preserve public/private boundaries.

## Metrics
- Completion status of the actions this document drives.
- Impact on revenue, delivery, trust, or founder leverage.

## Evidence
- Linked workflow, file, test output, customer interaction, or decision log.

## Last Reviewed
2026-05-23
