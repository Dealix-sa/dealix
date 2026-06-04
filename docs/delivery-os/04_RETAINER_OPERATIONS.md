# Retainer Operations — تشغيل الاشتراك الشهري

The Retainer tier (SAR 3,000–25,000 / month). Ongoing operation, tuning, and reporting for a delivered Pilot or Department OS. The Retainer keeps a governed system running well; it is not a vague "support" line. Background on the path: [03_commercial_mvp/RETAINER_PATH.md](../03_commercial_mvp/RETAINER_PATH.md).

الاشتراك الشهري تشغيل وضبط وتقارير مستمرة لنظام مُسلَّم. هو تشغيل مُحوكَم، لا بند دعم غامض.

## Inputs — المدخلات

- A signed retainer scope with a defined monthly deliverable and review cadence.
- A delivered Pilot or Department OS as the operating base.
- Current data sources under a maintained Source Passport.
- A named client owner for the monthly review.

## Outputs — المخرجات

- Operated review loops: drafts generated, ranked, and routed to client/founder review every cycle.
- A monthly client success report. See [05_CLIENT_SUCCESS_REPORTING.md](05_CLIENT_SUCCESS_REPORTING.md).
- Policy and prompt updates as the workflow evolves, logged in the registry.
- A running value ledger with Estimated/Observed/Verified labeling.

## Timeline — الجدول الزمني

- Monthly cycle with a fixed review cadence (default: weekly internal, monthly client report).
- Minimum term and notice period stated in the scope.
- Quarterly business review with the client owner.

## Acceptance criteria — معايير القبول

Each cycle is delivered when: the agreed review loops ran; the monthly report is approved and sent; policy/prompt changes are logged; and the value ledger is updated. A missed cadence is a service issue, logged and addressed.

## Human approval boundary — حدود الموافقة البشرية

Unchanged from build: AI drafts, ranks, recommends; humans approve; the system never sends externally. Any new outreach segment requires fresh, per-batch client approval before the client sends manually.

## Security boundary — حدود الأمان

Access stays least-privilege. Source Passports are reviewed each quarter. Retention and deletion run on schedule per [04_data_os/DATA_RETENTION_POLICY.md](../04_data_os/DATA_RETENTION_POLICY.md). Any scope or data change is re-approved before it takes effect.

## Handover — التسليم

Retainers are continuous, so "handover" means: clean monthly artifacts, a current configuration export, and — at offboarding — a full transfer pack so the client can operate or migrate without lock-in. Template: [06_HANDOVER_TEMPLATE.md](06_HANDOVER_TEMPLATE.md).

## Upsell path — مسار الترقية

Retainer → expanded Retainer (more workflows, higher tier) or Retainer → new Department OS (build the next department, then operate it). Expansion is proposed at quarterly reviews with evidenced patterns. See [07_EXPANSION_PLAYBOOK.md](07_EXPANSION_PLAYBOOK.md).

## Retainer trigger — مُحفِّز الاشتراك الشهري

Not applicable inbound — this is the retainer. The relevant trigger here is the renewal/expansion trigger: when observed value justifies a higher tier or an added workflow, it is proposed honestly, never auto-escalated.

## Client success metrics — مقاييس نجاح العميل

- Cadence adherence (cycles delivered on time).
- Review yield and cycle time, trended month over month.
- Observed and Verified value accumulated in the ledger.
- Renewal and expansion (tracked, never promised).
- Safety violations and compliance rejections (target: trending down).

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
