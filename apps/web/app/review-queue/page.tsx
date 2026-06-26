import Link from "next/link";

export const metadata = {
  title: "Review Queue — Dealix",
  description: "Approval queue for drafts pending human review before any external action.",
};

const QUEUE_SECTIONS = [
  {
    id: "outreach-drafts",
    labelAr: "مسودات التواصل",
    label: "Outreach Drafts",
    descAr: "رسائل WhatsApp والبريد الإلكتروني المعلقة",
    desc: "Pending WhatsApp and email messages",
    count: 0,
  },
  {
    id: "proposals",
    labelAr: "العروض التجارية",
    label: "Proposals",
    descAr: "عروض الأسعار وعقود العملاء",
    desc: "Price quotes and client contracts",
    count: 0,
  },
  {
    id: "ai-outputs",
    labelAr: "مخرجات الذكاء الاصطناعي",
    label: "AI Outputs",
    descAr: "نصوص وتحليلات تحتاج مراجعة بشرية",
    desc: "Generated text and analysis requiring human review",
    count: 0,
  },
];

export default function ReviewQueuePage() {
  const totalPending = QUEUE_SECTIONS.reduce((sum, s) => sum + s.count, 0);

  return (
    <main className="min-h-screen bg-[#070A12] text-white" dir="rtl">
      <div className="mx-auto max-w-4xl px-6 py-12">
        {/* Header */}
        <header className="mb-10">
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/70 font-mono">
            Review Queue · طابور المراجعة
          </p>
          <h1 className="mt-3 text-3xl font-semibold">
            كل إجراء خارجي يحتاج موافقة المؤسس
          </h1>
          <p className="mt-2 text-sm text-white/50">
            Every external action requires founder approval — no auto-send, no exceptions.
          </p>
        </header>

        {/* Queue empty status */}
        <div className="mb-10 rounded-xl border border-emerald-400/20 bg-emerald-400/5 px-6 py-5 flex items-center gap-4">
          <span className="w-3 h-3 rounded-full bg-emerald-400 flex-shrink-0" />
          <div>
            <p className="font-medium text-emerald-300 text-sm">
              QUEUE EMPTY · لا توجد مسودات معلقة
            </p>
            <p className="text-xs text-white/40 mt-0.5">
              {totalPending} items pending · All clear
            </p>
          </div>
        </div>

        {/* Queue sections */}
        <div className="space-y-4">
          {QUEUE_SECTIONS.map((section) => (
            <div
              key={section.id}
              className="rounded-xl border border-white/10 bg-white/5 p-5"
            >
              <div className="flex items-center justify-between mb-4">
                <div>
                  <p className="font-medium text-white/90">{section.labelAr}</p>
                  <p className="text-[11px] text-white/30">{section.label}</p>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-[10px] font-mono text-white/30 bg-white/5 border border-white/10 rounded px-2 py-0.5">
                    {section.count} pending
                  </span>
                  <span className="w-2 h-2 rounded-full bg-emerald-400" />
                </div>
              </div>
              <p className="text-xs text-white/40 mb-3">{section.descAr}</p>
              <div className="rounded-lg border border-dashed border-white/10 py-8 text-center">
                <p className="text-[10px] text-white/20 font-mono">
                  EMPTY · لا يوجد
                </p>
              </div>
            </div>
          ))}
        </div>

        {/* Safety reminder */}
        <div className="mt-8 rounded-xl border border-amber-300/20 bg-amber-300/5 p-5">
          <p className="text-sm font-medium text-amber-200 mb-2">
            تذكير الأمان — Safety Reminder
          </p>
          <ul className="space-y-1.5 text-xs text-white/50">
            <li>· Every external message (WhatsApp, email, LinkedIn) requires explicit founder approval</li>
            <li>· Never send automatically — approve manually with scripts/approve_outreach_draft.py</li>
            <li>· Proposals and invoices must be reviewed before delivery</li>
            <li>· AI outputs are drafts only until human-reviewed</li>
          </ul>
        </div>

        {/* Quick links */}
        <div className="mt-6 flex flex-wrap gap-3">
          <Link
            href="/outreach-lab"
            className="rounded-lg border border-white/10 bg-white/5 px-4 py-2 text-sm text-white/60 hover:text-white hover:bg-white/10 transition-colors"
          >
            مختبر التواصل — Outreach Lab
          </Link>
          <Link
            href="/approvals"
            className="rounded-lg border border-white/10 bg-white/5 px-4 py-2 text-sm text-white/60 hover:text-white hover:bg-white/10 transition-colors"
          >
            الموافقات — Approvals
          </Link>
          <Link
            href="/safety"
            className="rounded-lg border border-white/10 bg-white/5 px-4 py-2 text-sm text-white/60 hover:text-white hover:bg-white/10 transition-colors"
          >
            الأمان — Safety
          </Link>
        </div>
      </div>
    </main>
  );
}
