import Link from "next/link";

export const metadata = {
  title: "Pipeline — Dealix",
  description: "Visual sales pipeline by stage — Day Zero state.",
};

const STAGES = [
  { id: "discover", labelAr: "الاكتشاف", label: "Discover" },
  { id: "qualify", labelAr: "التأهيل", label: "Qualify" },
  { id: "outreach", labelAr: "التواصل", label: "Outreach" },
  { id: "meeting", labelAr: "الاجتماع", label: "Meeting" },
  { id: "proposal", labelAr: "العرض", label: "Proposal" },
  { id: "close", labelAr: "الإغلاق", label: "Close" },
];

const STATS = [
  { labelAr: "إجمالي الفرص", label: "Total Opportunities", value: "0" },
  { labelAr: "القيمة التقديرية", label: "Estimated Value", value: "SAR 0" },
  { labelAr: "معدل التحويل", label: "Conversion Rate", value: "—" },
  { labelAr: "متوسط دورة المبيعات", label: "Avg Sales Cycle", value: "—" },
];

export default function PipelinePage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white" dir="rtl">
      <div className="mx-auto max-w-7xl px-6 py-12">
        {/* Header */}
        <header className="mb-10">
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/70 font-mono">
            Pipeline · خط المبيعات
          </p>
          <h1 className="mt-3 text-3xl font-semibold">
            من الاكتشاف إلى الإغلاق
          </h1>
          <p className="mt-2 text-sm text-white/50">
            Day Zero — لا توجد فرص بعد. ابدأ بإضافة عملاء محتملين من{" "}
            <Link href="/lead-engine" className="text-amber-300 hover:underline">
              محرك العملاء
            </Link>
            .
          </p>
        </header>

        {/* Stats bar */}
        <div className="mb-10 grid grid-cols-2 gap-3 md:grid-cols-4">
          {STATS.map((s) => (
            <div
              key={s.label}
              className="rounded-xl border border-white/10 bg-white/5 px-4 py-4"
            >
              <p className="text-xs text-white/40 font-mono">{s.label}</p>
              <p className="mt-1 text-xl font-semibold text-amber-300">{s.value}</p>
              <p className="text-xs text-white/60">{s.labelAr}</p>
            </div>
          ))}
        </div>

        {/* Pipeline columns */}
        <div className="grid gap-3 md:grid-cols-6">
          {STAGES.map((stage, idx) => (
            <div
              key={stage.id}
              className="rounded-xl border border-white/10 bg-white/5 p-4 flex flex-col"
            >
              <div className="flex items-center justify-between mb-3">
                <span className="text-[10px] font-mono text-white/30">
                  {String(idx + 1).padStart(2, "0")}
                </span>
                <span className="text-[10px] font-mono text-white/20 bg-white/10 rounded px-1.5 py-0.5">
                  0
                </span>
              </div>
              <p className="text-sm font-medium text-white/80">{stage.labelAr}</p>
              <p className="text-[10px] text-white/30 mb-4">{stage.label}</p>
              <div className="flex-1 rounded-lg border border-dashed border-white/10 flex items-center justify-center py-8">
                <p className="text-[10px] text-white/20 text-center">
                  لا يوجد
                  <br />
                  nothing here
                </p>
              </div>
              <p className="mt-3 text-[10px] text-white/20 font-mono text-center">
                SAR 0
              </p>
            </div>
          ))}
        </div>

        {/* Quick links */}
        <div className="mt-10 flex flex-wrap gap-3">
          <Link
            href="/lead-engine"
            className="rounded-lg border border-amber-300/30 bg-amber-300/10 px-4 py-2 text-sm text-amber-300 hover:bg-amber-300/20 transition-colors"
          >
            + أضف عميل محتمل — Lead Engine
          </Link>
          <Link
            href="/deals"
            className="rounded-lg border border-white/10 bg-white/5 px-4 py-2 text-sm text-white/60 hover:text-white hover:bg-white/10 transition-colors"
          >
            عرض الصفقات — Deals
          </Link>
          <Link
            href="/crm"
            className="rounded-lg border border-white/10 bg-white/5 px-4 py-2 text-sm text-white/60 hover:text-white hover:bg-white/10 transition-colors"
          >
            إدارة العملاء — CRM
          </Link>
        </div>
      </div>
    </main>
  );
}
