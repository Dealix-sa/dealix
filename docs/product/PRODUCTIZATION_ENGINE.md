---
title: Productization Engine
owner: Founder (Bassam)
status: active
last_review: 2026-05-23
---

# Productization Engine — محرك المُنتجة

## Purpose
Define the ladder that converts manual delivery into reusable templates, automated workflows, and eventually a SaaS surface. The engine prevents premature platform-building.

## The Productization Rule (verbatim)
- 3 manual successes = document
- 5 successes = template
- 10 successes = automate
- Repeated customer request = SaaS candidate

## Definitions
| Rung | Meaning | Output |
|---|---|---|
| Manual | Founder or analyst delivers by hand each time | Delivery log entry, proof pack |
| Document | Repeatable steps captured in markdown SOP | `docs/delivery/*.md` SOP |
| Template | Inputs/outputs parameterized; Jinja or sheet | `templates/*.md.j2` or sheet |
| Automate | Script or pipeline runs the template with human gate | Internal CLI or job |
| SaaS candidate | External users would self-serve | Discovery doc + paid pilot |

## Rules
- A rung cannot be skipped. Automating before templating creates fragile code.
- A SaaS candidate requires ≥3 unrelated customers asking unprompted.
- Every rung-up needs a logged success count (delivery ledger).
- Before automation, a human-in-the-loop gate is mandatory per `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md`.

## Evidence per rung-up
| From → To | Evidence required |
|---|---|
| Manual → Document | 3 distinct successful deliveries with proof packs |
| Document → Template | 5 successes with consistent inputs/outputs |
| Template → Automate | 10 successes; failure modes catalogued; rollback plan |
| Automate → SaaS | ≥3 unsolicited customer requests; pricing tested |

## Operations
- Founder reviews delivery ledger weekly for rung-up triggers.
- New rung-up logged in `BUILD_DEFER_KILL.md` with date and evidence link.
- SaaS candidates do not enter active build until validation per `docs/sales/QUALIFICATION_ENGINE.md`.

## Owner & cadence
- Owner: Founder.
- Cadence: weekly trigger check; monthly portfolio review.

## Cross-links
- [`PRODUCTIZATION_COMMAND_CENTER.md`](PRODUCTIZATION_COMMAND_CENTER.md)
- [`BUILD_DEFER_KILL.md`](BUILD_DEFER_KILL.md)
- [`NO_OVERBUILD_POLICY.md`](NO_OVERBUILD_POLICY.md)

---

## القسم العربي

**قاعدة المُنتجة:**
- 3 نجاحات يدوية = توثيق
- 5 نجاحات = قالب
- 10 نجاحات = أتمتة
- طلب عميل متكرر = مُرشّح SaaS

**القواعد:** لا تُتجاوز درجة، لا أتمتة قبل القالب، الحارس البشري إلزامي قبل الأتمتة، مُرشّح SaaS يحتاج ثلاثة عملاء غير مرتبطين يطلبون بدون تلميح.

**المالك:** المؤسس. **الإيقاع:** فحص أسبوعي للمحفّزات.
