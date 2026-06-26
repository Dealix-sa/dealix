import Link from "next/link";

export const metadata = {
  title: "Revenue OS — Dealix",
  description: "Revenue operating system dashboard — monthly targets and breakdown.",
};

const OFFER_TIERS = [
  {
    tier: "Free Diagnostic",
    tierAr: "التشخيص المجاني",
    price: "0 SAR",
    mtdCount: 0,
    mtdRevenue: 0,
    note: "Lead magnet — 30 min",
  },
  {
    tier: "Micro Sprint",
    tierAr: "سبرينت مصغر",
    price: "499 SAR",
    mtdCount: 0,
    mtdRevenue: 0,
    note: "Quick win proof",
  },
  {
    tier: "Data Pack",
    tierAr: "حزمة البيانات",
    price: "1,500 SAR",
    mtdCount: 0,
    mtdRevenue: 0,
    note: "One-time data asset",
  },
  {
    tier: "Managed Ops",
    tierAr: "عمليات مُدارة",
    price: "2,999–4,999 SAR/mo",
    mtdCount: 0,
    mtdRevenue: 0,
    note: "Monthly retainer",
  },
  {
    tier: "Diagnostic Sprint",
    tierAr: "سبرينت التشخيص",
    price: "7,500–25,000 SAR",
    mtdCount: 0,
    mtdRevenue: 0,
    note: "Primary paid entry — 3–7 days",
  },
];

const MONTHLY_TARGET = 50000;
const CURRENT_REVENUE = 0;
const DAYS_REMAINING = 30;

const ACTIONS = [
  { labelAr: "أضف أول عميل في CRM", label: "Add first client to CRM", href: "/crm" },
  { labelAr: "ابدأ خط المبيعات", label: "Start the sales pipeline", href: "/pipeline" },
  { labelAr: "أنشئ أول عرض تجاري", label: "Create first proposal", href: "/quotes" },
  { labelAr: "تتبع الصفقات", label: "Track deals", href: "/deals" },
];

export default function RevenueOSPage() {
  const progressPercent = MONTHLY_TARGET > 0
    ? Math.round((CURRENT_REVENUE / MONTHLY_TARGET) * 100)
    : 0;

  return (
    <main className="min-h-screen bg-[#070A12] text-white" dir="rtl">
      <div className="mx-auto max-w-5xl px-6 py-12">
        {/* Header */}
        <header className="mb-10">
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/70 font-mono">
            Revenue OS · نظام الإيرادات
          </p>
          <h1 className="mt-3 text-3xl font-semibold">لوحة الإيرادات الشهرية</h1>
          <p className="mt-2 text-sm text-white/50">
            Day Zero — لا توجد إيرادات بعد. ابدأ بأول صفقة.
          </p>
        </header>

        {/* Top metrics */}
        <div className="mb-8 grid grid-cols-1 gap-4 md:grid-cols-3">
          <div className="rounded-xl border border-amber-300/20 bg-amber-300/5 p-5">
            <p className="text-xs font-mono text-white/40">MONTHLY TARGET · الهدف الشهري</p>
            <p className="mt-2 text-3xl font-bold text-amber-300">
              {MONTHLY_TARGET.toLocaleString()} SAR
            </p>
          </div>
          <div className="rounded-xl border border-white/10 bg-white/5 p-5">
            <p className="text-xs font-mono text-white/40">CURRENT MTD · الإيرادات حتى الآن</p>
            <p className="mt-2 text-3xl font-bold text-white/90">
              {CURRENT_REVENUE.toLocaleString()} SAR
            </p>
          </div>
          <div className="rounded-xl border border-white/10 bg-white/5 p-5">
            <p className="text-xs font-mono text-white/40">DAYS REMAINING · الأيام المتبقية</p>
            <p className="mt-2 text-3xl font-bold text-white/90">{DAYS_REMAINING}</p>
          </div>
        </div>

        {/* Progress bar */}
        <div className="mb-10 rounded-xl border border-white/10 bg-white/5 p-5">
          <div className="flex justify-between mb-2">
            <p className="text-xs text-white/50 font-mono">PROGRESS TO TARGET</p>
            <p className="text-xs font-mono text-amber-300">{progressPercent}%</p>
          </div>
          <div className="h-2 rounded-full bg-white/10">
            <div
              className="h-full rounded-full bg-amber-300/60 transition-all"
              style={{ width: `${progressPercent}%` }}
            />
          </div>
          <p className="mt-2 text-[10px] text-white/25 font-mono">
            {CURRENT_REVENUE.toLocaleString()} / {MONTHLY_TARGET.toLocaleString()} SAR
          </p>
        </div>

        {/* Revenue breakdown by offer tier */}
        <div className="mb-10">
          <h2 className="text-sm font-medium text-white/60 mb-4 font-mono uppercase tracking-widest">
            Revenue by Offer Tier · توزيع الإيرادات حسب العرض
          </h2>
          <div className="space-y-3">
            {OFFER_TIERS.map((tier) => (
              <div
                key={tier.tier}
                className="rounded-xl border border-white/10 bg-white/5 p-4 flex items-center justify-between"
              >
                <div>
                  <p className="text-sm font-medium text-white/80">{tier.tierAr}</p>
                  <p className="text-[11px] text-white/30">{tier.tier} · {tier.note}</p>
                </div>
                <div className="text-right">
                  <p className="text-sm font-mono text-white/60">{tier.price}</p>
                  <p className="text-[10px] text-white/25 mt-0.5">
                    {tier.mtdCount} deals · {tier.mtdRevenue.toLocaleString()} SAR MTD
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* MTD chart (text-based) */}
        <div className="mb-10 rounded-xl border border-white/10 bg-white/5 p-5">
          <p className="text-xs font-mono text-white/40 mb-4 uppercase tracking-widest">
            MTD Revenue Chart · الإيرادات الشهرية
          </p>
          <div className="space-y-2">
            {["W1", "W2", "W3", "W4"].map((week) => (
              <div key={week} className="flex items-center gap-3">
                <span className="w-6 text-[10px] font-mono text-white/30">{week}</span>
                <div className="flex-1 h-5 rounded bg-white/5 border border-white/10 overflow-hidden">
                  <div className="h-full bg-amber-300/0 w-0" />
                </div>
                <span className="w-16 text-right text-[10px] font-mono text-white/20">0 SAR</span>
              </div>
            ))}
          </div>
          <p className="mt-3 text-[10px] text-white/20 font-mono text-center">
            NO DATA YET · ابدأ بأول صفقة
          </p>
        </div>

        {/* Action items */}
        <div className="mb-6">
          <h2 className="text-sm font-medium text-white/60 mb-4 font-mono uppercase tracking-widest">
            Action Items · الإجراءات المطلوبة
          </h2>
          <div className="space-y-2">
            {ACTIONS.map((action) => (
              <Link
                key={action.href}
                href={action.href}
                className="flex items-center justify-between rounded-xl border border-white/10 bg-white/5 px-4 py-3 hover:bg-white/10 hover:border-white/20 transition-colors group"
              >
                <div>
                  <p className="text-sm text-white/80 group-hover:text-white">{action.labelAr}</p>
                  <p className="text-[10px] text-white/30">{action.label}</p>
                </div>
                <span className="text-white/20 group-hover:text-amber-300 text-xs">&larr;</span>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}
