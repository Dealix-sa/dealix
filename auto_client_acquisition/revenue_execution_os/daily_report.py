"""Daily report composer — the single founder-facing distribution report.

Renders Markdown from the stores + engines. Read-only: composing a report
never sends, charges, or mutates anything. Every customer-facing report ends
with the bilingual estimated-value disclaimer.
"""

from __future__ import annotations

from datetime import UTC, datetime

from auto_client_acquisition.revenue_execution_os import stores
from auto_client_acquisition.revenue_execution_os.draft_quality import review_drafts
from auto_client_acquisition.revenue_execution_os.followup_engine import build_followup_queue
from auto_client_acquisition.revenue_execution_os.metrics import daily_metrics, weekly_metrics
from auto_client_acquisition.revenue_execution_os.models import (
    OPEN_DRAFT_STATUSES,
    PaymentHandoffStatus,
    ProposalStatus,
)
from auto_client_acquisition.revenue_execution_os.payment_handoff import handoff_is_ready
from auto_client_acquisition.revenue_execution_os.proof_pack_factory import proof_pack_meets_bar
from auto_client_acquisition.revenue_execution_os.sectors import rank_sectors
from auto_client_acquisition.revenue_execution_os.win_loss import weekly_learning

DISCLAIMER = "> القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value."


def _h(title: str) -> str:
    return f"\n## {title}\n"


def render_daily_report(now: datetime | None = None) -> str:
    now = now or datetime.now(UTC)
    today = now.date().isoformat()
    lines: list[str] = [
        f"# تقرير التصريف اليومي — {today}",
        "",
        "نظام تنفيذ الإيراد (Revenue Execution OS) — موافقة أولًا، بدون إرسال خارجي.",
    ]

    # 1) Top sector
    ranked = rank_sectors()[:3]
    lines.append(_h("القطاع الأفضل اليوم"))
    if ranked:
        lines.append("| الترتيب | القطاع | النقاط | أول عرض مدفوع |")
        lines.append("|---|---|---:|---|")
        for i, s in enumerate(ranked, 1):
            lines.append(f"| {i} | {s.name_ar} | {s.total} | {s.first_paid_offer} |")
    else:
        lines.append("لا توجد قطاعات مُعرّفة بعد — راجع data/distribution/sectors.yaml.")

    # 2) Pending drafts
    drafts = stores.DRAFTS.list(limit=100_000)
    open_drafts = [d for d in drafts if d.status in OPEN_DRAFT_STATUSES]
    lines.append(_h(f"مسودات بانتظار الموافقة ({len(open_drafts)})"))
    if open_drafts:
        lines.append("| المعرّف | النوع | القناة | قرار الحوكمة | ملاحظات |")
        lines.append("|---|---|---|---|---|")
        for d in open_drafts[:10]:
            issues = ", ".join(d.issues) if d.issues else "—"
            lines.append(
                f"| {d.draft_id} | {d.draft_type} | {d.channel} | {d.governance_decision} | {issues} |"
            )
    else:
        lines.append("لا مسودات مفتوحة — ولّد دفعة عبر API أو generate_drafts.")

    # 3) Due follow-ups
    queue = build_followup_queue(now=now)
    lines.append(_h(f"متابعات مستحقة ({len(queue)})"))
    if queue:
        lines.append("| المتلقّي (prospect) | السبب | النوع المقترح |")
        lines.append("|---|---|---|")
        for f in queue[:10]:
            lines.append(f"| {f.prospect_id} | {f.reason} | {f.suggested_draft_type} |")
    else:
        lines.append("لا متابعات مستحقة اليوم.")

    # 4) Proposals
    proposals = stores.PROPOSALS.list(limit=100_000)
    open_props = [
        p
        for p in proposals
        if p.status
        in (ProposalStatus.PENDING_APPROVAL, ProposalStatus.SENT, ProposalStatus.APPROVED)
    ]
    lines.append(_h(f"عروض مفتوحة ({len(open_props)})"))
    for p in open_props[:10]:
        lines.append(f"- {p.proposal_id} — {p.offer_key} — {p.price_label} — {p.status}")
    if not open_props:
        lines.append("لا عروض مفتوحة.")

    # 5) Proof packs
    packs = stores.PROOF_PACKS.list(limit=100_000)
    ready_packs = [p for p in packs if proof_pack_meets_bar(p)]
    lines.append(_h(f"حِزَم الإثبات ({len(packs)} — منها {len(ready_packs)} تتجاوز عتبة ٧٠)"))
    for p in packs[:10]:
        flag = "✓" if proof_pack_meets_bar(p) else "—"
        lines.append(f"- {p.proof_pack_id} — score={p.score} — L{p.evidence_level} — bar:{flag}")
    if not packs:
        lines.append("لا حِزَم إثبات بعد.")

    # 6) Payment handoffs
    handoffs = stores.PAYMENT_HANDOFFS.list(limit=100_000)
    ready = [h for h in handoffs if handoff_is_ready(h) and h.status != PaymentHandoffStatus.PAID]
    lines.append(_h(f"تسليمات الدفع الجاهزة ({len(ready)})"))
    for h in ready[:10]:
        lines.append(f"- {h.handoff_id} — {h.offer_key} — {h.amount_label} — {h.status}")
    blocked = [h for h in handoffs if not handoff_is_ready(h)]
    if blocked:
        lines.append(
            f"\nتسليمات محجوبة بانتظار شروط ({len(blocked)}): تحتاج موافقة عرض/سعر/نطاق/شروط/مؤسس."
        )
    if not handoffs:
        lines.append("لا تسليمات دفع بعد.")

    # 7) Renewals
    renewals = [r for r in stores.RENEWALS.list(limit=100_000) if r.status == "open"]
    lines.append(_h(f"فرص التجديد ({len(renewals)})"))
    for r in renewals[:10]:
        lines.append(
            f"- {r.customer_id} — {r.current_offer_key} → {r.next_offer_key} — {r.trigger}"
        )
    if not renewals:
        lines.append("لا فرص تجديد مفتوحة.")

    # 8) Win/loss weekly learning
    learning = weekly_learning(now=now)
    lines.append(_h("تعلّم الأسبوع (Win/Loss)"))
    lines.append(
        f"- مغلق: {learning['won']} ربح / {learning['lost']} خسارة — معدل الإغلاق {learning['close_rate']}"
    )
    lines.append(
        f"- أفضل قطاع: {learning['best_sector']} · أفضل قناة: {learning['best_channel']} · أفضل عرض: {learning['best_offer']}"
    )
    if learning["top_objections"]:
        lines.append(f"- أبرز الاعتراضات: {', '.join(str(o) for o in learning['top_objections'])}")

    # 9) Quality + metrics
    quality = review_drafts(open_drafts)
    dm = daily_metrics(now=now)
    wm = weekly_metrics(now=now)
    lines.append(_h("المقاييس"))
    lines.append(
        f"- اليوم: مسودات مُولّدة {dm['drafts_generated']} · مفتوحة {dm['drafts_open']} · متابعات مستحقة {dm['followups_due']} · عروض {dm['proposals_generated']}"
    )
    lines.append(
        f"- الأسبوع: معدل الموافقة {wm['approval_rate']} · معدل الرد {wm['reply_rate']} · معدل الإغلاق {wm['close_rate']} · قيمة خط الأنابيب التقديرية {wm['pipeline_value_estimated_sar']} ريال"
    )
    lines.append(
        f"- جودة المسودات المفتوحة: {quality.passed}/{quality.total} اجتازت (معدل {quality.pass_rate})"
    )

    # 10) Daily decision
    lines.append(_h("قرارك اليوم"))
    lines.append("- [ ] راجع المسودات المفتوحة: وافق / عدّل / ارفض.")
    lines.append("- [ ] انسخ المعتمدة وأرسلها يدويًا عبر القناة المناسبة.")
    lines.append("- [ ] نفّذ المتابعات المستحقة.")
    lines.append("- [ ] ولّد عرضًا/حزمة إثبات لأي فرصة جادة.")
    lines.append("- [ ] جهّز تسليم دفع واحدًا إن اكتملت الشروط.")

    lines.append("")
    lines.append(DISCLAIMER)
    return "\n".join(lines)


def render_draft_quality_report(now: datetime | None = None) -> str:
    drafts = stores.DRAFTS.list(limit=100_000)
    prospects = {p.prospect_id: p for p in stores.PROSPECTS.list(limit=100_000)}
    report = review_drafts(drafts, prospects)
    lines = [
        "# مراجعة جودة المسودات — Draft Quality Review",
        "",
        f"الإجمالي: {report.total} · اجتاز: {report.passed} · أخفق: {report.failed} · المعدل: {report.pass_rate}",
        "",
        "| المعرّف | النتيجة | اجتاز | الأسباب |",
        "|---|---:|---|---|",
    ]
    for r in report.results[:200]:
        reasons = "; ".join(r.reasons) if r.reasons else "—"
        lines.append(f"| {r.draft_id} | {r.score} | {'نعم' if r.passed else 'لا'} | {reasons} |")
    if not report.results:
        lines.append("| — | — | — | لا مسودات بعد |")
    lines.append("")
    lines.append(DISCLAIMER)
    return "\n".join(lines)


def render_followup_queue_report(now: datetime | None = None) -> str:
    queue = build_followup_queue(now=now)
    lines = [
        "# قائمة المتابعات المستحقة — Follow-up Queue",
        "",
        f"الإجمالي المستحق: {len(queue)}",
        "",
        "| prospect | السبب | النوع المقترح | القناة |",
        "|---|---|---|---|",
    ]
    for f in queue:
        lines.append(f"| {f.prospect_id} | {f.reason} | {f.suggested_draft_type} | {f.channel} |")
    if not queue:
        lines.append("| — | — | — | لا متابعات مستحقة |")
    lines.append("")
    lines.append(DISCLAIMER)
    return "\n".join(lines)


def render_metrics_report(now: datetime | None = None) -> str:
    dm = daily_metrics(now=now)
    wm = weekly_metrics(now=now)
    lines = ["# مقاييس التصريف — Distribution Metrics", "", "## اليومية"]
    for k, v in dm.items():
        lines.append(f"- {k}: {v}")
    lines.append("\n## الأسبوعية")
    for k, v in wm.items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append(DISCLAIMER)
    return "\n".join(lines)


def render_win_loss_report(now: datetime | None = None) -> str:
    learning = weekly_learning(now=now)
    lines = ["# تعلّم الربح/الخسارة — Win/Loss Learning", ""]
    for k, v in learning.items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append(DISCLAIMER)
    return "\n".join(lines)


__all__ = [
    "DISCLAIMER",
    "render_daily_report",
    "render_draft_quality_report",
    "render_followup_queue_report",
    "render_metrics_report",
    "render_win_loss_report",
]
