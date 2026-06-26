import Link from "next/link";

export const metadata = {
  title: "Proof Vault — Dealix",
  description: "Before/after evidence store for client projects.",
};

const CATEGORIES = [
  {
    id: "before-after",
    labelAr: "تقارير قبل/بعد",
    label: "Before / After Reports",
    descAr: "مقارنة الأداء قبل وبعد التدخل",
    desc: "Performance comparison before and after intervention",
    count: 0,
  },
  {
    id: "decision-logs",
    labelAr: "سجلات القرارات",
    label: "Decision Logs",
    descAr: "توثيق كل قرار مهم اتُخذ في المشروع",
    desc: "Documentation of every key project decision",
    count: 0,
  },
  {
    id: "kpi-improvements",
    labelAr: "تحسينات المؤشرات",
    label: "KPI Improvements",
    descAr: "أرقام قبل وبعد على مؤشرات الأداء الرئيسية",
    desc: "Before/after numbers on key performance indicators",
    count: 0,
  },
  {
    id: "testimonials",
    labelAr: "شهادات العملاء",
    label: "Client Testimonials",
    descAr: "شهادات حقيقية فقط — لا محتوى مزيف",
    desc: "Real testimonials only — no fabricated content",
    count: 0,
  },
];

export default function ProofVaultPage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white" dir="rtl">
      <div className="mx-auto max-w-5xl px-6 py-12">
        {/* Header */}
        <header className="mb-10">
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/70 font-mono">
            Proof Vault · خزانة الإثبات
          </p>
          <h1 className="mt-3 text-3xl font-semibold">الدليل يسبق الادعاء</h1>
          <p className="mt-2 text-sm text-white/50">
            لا يوجد proof بعد — ابدأ بأول مشروع. كل دليل يُرفع يدويًا فقط.
          </p>
        </header>

        {/* Empty state banner */}
        <div className="mb-10 rounded-xl border border-dashed border-amber-300/20 bg-amber-300/5 px-6 py-8 text-center">
          <p className="text-lg font-medium text-amber-200">
            لا يوجد proof بعد — ابدأ بأول مشروع
          </p>
          <p className="mt-1 text-sm text-white/40">
            NO PROOF YET · Start with your first client project
          </p>
          <div className="mt-4">
            <Link
              href="/app/client-delivery"
              className="inline-block rounded-lg border border-amber-300/30 bg-amber-300/10 px-5 py-2 text-sm text-amber-300 hover:bg-amber-300/20 transition-colors"
            >
              ابدأ مشروع — Client Delivery
            </Link>
          </div>
        </div>

        {/* Categories */}
        <div className="grid gap-4 md:grid-cols-2">
          {CATEGORIES.map((cat) => (
            <div
              key={cat.id}
              className="rounded-xl border border-white/10 bg-white/5 p-5"
            >
              <div className="flex items-start justify-between">
                <div>
                  <p className="font-medium text-white/90">{cat.labelAr}</p>
                  <p className="text-[11px] text-white/30 mt-0.5">{cat.label}</p>
                </div>
                <span className="rounded-full border border-white/10 bg-white/10 px-2 py-0.5 text-xs font-mono text-white/40">
                  {cat.count}
                </span>
              </div>
              <p className="mt-3 text-xs text-white/50">{cat.descAr}</p>
              <p className="text-[10px] text-white/25">{cat.desc}</p>
              <div className="mt-4 rounded-lg border border-dashed border-white/10 py-6 text-center">
                <p className="text-[10px] text-white/20">فارغ · EMPTY</p>
              </div>
            </div>
          ))}
        </div>

        {/* Upload instructions */}
        <div className="mt-8 rounded-xl border border-white/10 bg-white/5 p-5">
          <p className="text-sm font-medium text-white/80 mb-2">
            كيفية إضافة الأدلة — Upload Instructions
          </p>
          <ul className="space-y-2 text-xs text-white/50">
            <li>· أكمل المشروع مع العميل أولًا</li>
            <li>· وثّق النتائج بأرقام حقيقية فقط</li>
            <li>· احصل على موافقة المؤسس قبل النشر</li>
            <li>· لا يوجد رفع تلقائي — كل شيء يدوي</li>
          </ul>
          <p className="mt-3 text-[10px] text-white/25 font-mono">
            No auto-upload · Manual process only · Founder approval required before publishing
          </p>
        </div>
      </div>
    </main>
  );
}
