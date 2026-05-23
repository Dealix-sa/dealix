# Dealix — Autonomous Enterprise OS

Status: v1
Owner: Founder

## 1. Definition — التعريف

The Autonomous Enterprise OS is the set of software, policies, agents, evals, and runbooks that allows Dealix to operate as a full enterprise with a founder-in-the-loop instead of a department-in-the-loop.

نظام تشغيل المؤسسة الذاتي هو مجموعة البرمجيات والسياسات والوكلاء والاختبارات والإجراءات التي تتيح لـDealix أن تعمل كمؤسسة كاملة بمؤسس في الحلقة بدلاً من قسم كامل.

## 2. Autonomy We Allow — الاستقلالية المسموح بها

- Reading public/licensed signals about Saudi B2B accounts.
- Drafting messages, briefs, proposals, scorecards.
- Detecting risks, anomalies, renewal signals.
- Composing daily founder briefings.
- Compiling evidence from worker outputs.

## 3. Autonomy We Forbid — الاستقلالية الممنوعة

- Sending anything externally.
- Publishing proof or marketing content.
- Committing to pricing, contracts, payment terms.
- Modifying policy, registry, kill switches.
- Releasing any agent without a green eval gate.

## 4. The Six Subsystems — الأنظمة الستة

1. Intelligence — collects and structures signals.
2. Revenue — drafts and queues outreach, proposals, follow-ups.
3. Trust — enforces policy and class system at runtime.
4. Finance — tracks cost, margin, AI spend; reads only.
5. Runtime — worker mesh and orchestrator that executes scheduled jobs.
6. Control Plane — exposes everything to the founder console and APIs.

## 5. Single-Operator Mode — وضع المشغّل الواحد

The OS is designed so the founder can:
- See the entire company state on one screen.
- Approve or reject the day's queue.
- Trip kill switches without engineering help.
- Read the audit log filtered by class, agent, or date.

## 6. Scale-Out Mode — وضع التوسع

When a CSM or AE is added:
- Same console, scoped permissions.
- Owners assigned per agent.
- Approvals delegated by class (A1 auto, A2 owner, A3 founder).
- Audit per-user, per-action.

## 7. Operating Cadence — الإيقاع التشغيلي

| Cadence | Output |
|---|---|
| Continuous | Worker mesh, agent runs, audit log |
| Hourly | Control plane refresh |
| Daily | Founder briefing, approvals queue, eval status |
| Weekly | Scorecard, risk register, DORA metrics |
| Monthly | Maturity review, eval corpus growth, cost review |

## 8. Resilience — الصمود

- Every agent has a kill switch.
- Every worker has a heartbeat and a freshness SLO.
- Every external dependency has a fallback path.
- Postgres has primary mode; CSV shadow exists as the last-line audit trail.

## 9. The Promise — الوعد

The Autonomous Enterprise OS is not "AI replaces the founder."
It is "AI lets one founder run the disciplined operating company that would otherwise require a department." Every external action still requires the founder. Every claim still requires evidence.

## 10. References — مراجع

- `docs/company/DEALIX_SOVEREIGN_AI_OPERATING_COMPANY.md`
- `docs/architecture/AI_NATIVE_COMPANY_ARCHITECTURE.md`
- `docs/runtime/ULTIMATE_WORKER_MESH.md`
- `docs/control_plane/DEALIX_CONTROL_PLANE.md`
