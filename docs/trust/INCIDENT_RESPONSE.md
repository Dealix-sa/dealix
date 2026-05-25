---
title: Incident Response
owner: Founder
status: active
last_review: 2026-05-23
---

# Incident Response — الاستجابة للحوادث

## Purpose

A clear, rehearsed loop for when something goes wrong: detect, contain, notify, recover, learn. Slow response is its own incident.

## Severity tiers

| Tier | Definition | Examples | Response SLA |
|---|---|---|---|
| SEV-1 | Client data exposed; regulator-touching | PII leaked to public repo; SDAIA inquiry mishandled. | Founder paged immediately; contain within 1h. |
| SEV-2 | Material delivery failure or scope breach | Lead table sent with unredacted phones; agent acted outside autonomy. | Contain within 4h; notify client within 24h. |
| SEV-3 | Internal control failure with no external exposure | Schema validation skipped on a batch. | Contain within 1 business day. |
| SEV-4 | Near-miss caught by control | Pre-commit hook blocked a leak before push. | Logged, reviewed weekly. |

## The loop

1. **Detect.** Anyone notices; opens `dealix-ops-private/incidents/INC-YYYY-NNN.md` with tier and one-line summary.
2. **Contain.** Stop the bleeding: pause agent, revoke link, withdraw post, freeze repo if needed.
3. **Notify.** SEV-1 to founder + Trust Lead within 15 minutes. SEV-2 to client within 24h using the approved comms template (below). SEV-3/4 logged.
4. **Recover.** Restore correct state. For data exposure, follow PDPL-aware steps in [docs/02_saudi_positioning/PDPL_AWARE_LANGUAGE.md](../02_saudi_positioning/PDPL_AWARE_LANGUAGE.md).
5. **Learn.** Within 5 business days, write the postmortem: timeline, root cause, control that failed, control change committed.

## Client comms template (SEV-2)

```
Subject — Notice regarding [deliverable name]

We identified an issue with [brief, non-defensive description]. Status: contained.

What happened: [one sentence].
What we have done: [actions taken].
What we will do next: [recovery step + date].
What we ask of you: [optional; only if relevant].

We will share a written postmortem within 5 business days.
```

AR version stored alongside in `dealix-ops-private/incidents/templates/`.

## What never happens during an incident

- No blame language toward an individual in public artifacts.
- No claim of full root-cause analysis before evidence is gathered.
- No private incident details discussed on public channels.

## Evidence

- Incident file with timeline.
- Postmortem with control change.
- Updated control entry in [TRUST_CONTROL_SYSTEM.md](./TRUST_CONTROL_SYSTEM.md) if applicable.

## Cross-links

- [TRUST_CONTROL_SYSTEM.md](./TRUST_CONTROL_SYSTEM.md)
- [AUTONOMY_POLICY.md](./AUTONOMY_POLICY.md) — agent kill switch.
- [AUDIT_POLICY.md](./AUDIT_POLICY.md)

## Owner & cadence

- Founder. Tabletop exercise quarterly.

## AR — ملخّص

دورة الاستجابة: اكتشف، احتواء، إبلاغ، تعافٍ، تعلّم. أربعة مستويات خطورة بمواعيد محدّدة. كل حادثة تخلق ملفًا ومراجعة لاحقة وتغييرًا في الضوابط إن لزم. الإبلاغ بصياغة معتمدة لا دفاعية. القيمة التقديرية ليست قيمة مُتحقَّقة.
