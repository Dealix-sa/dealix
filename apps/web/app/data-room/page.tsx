import Link from "next/link";

export const metadata = {
  title: "Data Room — Dealix",
  description: "Company data room — governance and documentation hub.",
};

const BUSINESS_DOCS = [
  { title: "Company Overview", titleAr: "نظرة عامة على الشركة", desc: "One paragraph on what Dealix does", status: "draft" },
  { title: "Market Thesis", titleAr: "أطروحة السوق", desc: "Why now, why Saudi, why Dealix", status: "draft" },
  { title: "Product Architecture", titleAr: "هيكل المنتج", desc: "Layers, components, integrations", status: "draft" },
  { title: "Commercial Model", titleAr: "النموذج التجاري", desc: "Seven offers and unit economics", status: "draft" },
];

const COMPLIANCE_DOCS = [
  { title: "PDPL Compliance Policy", titleAr: "سياسة الامتثال لحماية البيانات", status: "active" },
  { title: "No Auto-Send Policy", titleAr: "سياسة عدم الإرسال التلقائي", status: "active" },
  { title: "AI Output Review Policy", titleAr: "سياسة مراجعة مخرجات الذكاء الاصطناعي", status: "active" },
  { title: "Founder Approval Gate", titleAr: "بوابة موافقة المؤسس", status: "active" },
];

export default function DataRoomPage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white" dir="rtl">
      <div className="mx-auto max-w-5xl px-6 py-12">
        {/* Header */}
        <header className="mb-10">
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/70 font-mono">
            Data Room · غرفة البيانات
          </p>
          <h1 className="mt-3 text-3xl font-semibold">مركز الحوكمة والتوثيق</h1>
          <p className="mt-2 text-sm text-white/50">
            Governance and documentation hub — all numbers are placeholders until replaced by real data.
          </p>
        </header>

        {/* PDPL compliance badge */}
        <div className="mb-10 flex flex-wrap gap-3">
          <div className="flex items-center gap-2 rounded-full border border-emerald-400/20 bg-emerald-400/5 px-4 py-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400" />
            <span className="text-xs text-emerald-300 font-mono">PDPL-COMPLIANT</span>
          </div>
          <div className="flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2">
            <span className="w-2 h-2 rounded-full bg-amber-400" />
            <span className="text-xs text-white/50 font-mono">NO AUTO-SEND</span>
          </div>
          <div className="flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2">
            <span className="w-2 h-2 rounded-full bg-white/40" />
            <span className="text-xs text-white/50 font-mono">FOUNDER APPROVAL REQUIRED</span>
          </div>
        </div>

        {/* Business Documents */}
        <section className="mb-10">
          <h2 className="text-sm font-medium text-white/60 mb-4 font-mono uppercase tracking-widest">
            Business Documents · وثائق الأعمال
          </h2>
          <div className="grid gap-3 md:grid-cols-2">
            {BUSINESS_DOCS.map((doc) => (
              <div
                key={doc.title}
                className="rounded-xl border border-white/10 bg-white/5 p-5"
              >
                <div className="flex items-start justify-between mb-2">
                  <p className="font-medium text-white/80">{doc.titleAr}</p>
                  <span className="text-[10px] font-mono text-white/25 bg-white/5 border border-white/10 rounded px-2 py-0.5">
                    {doc.status}
                  </span>
                </div>
                <p className="text-[11px] text-white/30">{doc.title}</p>
                <p className="mt-2 text-xs text-white/40">{doc.desc}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Contracts */}
        <section className="mb-10">
          <h2 className="text-sm font-medium text-white/60 mb-4 font-mono uppercase tracking-widest">
            Contracts · العقود
          </h2>
          <div className="rounded-xl border border-dashed border-white/10 bg-white/5 p-8 text-center">
            <p className="text-2xl font-bold text-white/20">0</p>
            <p className="text-xs text-white/30 mt-1">لا توجد عقود بعد · NO CONTRACTS YET</p>
            <p className="text-[10px] text-white/20 mt-2 font-mono">
              Contracts added after first signed deal
            </p>
          </div>
        </section>

        {/* Client Files */}
        <section className="mb-10">
          <h2 className="text-sm font-medium text-white/60 mb-4 font-mono uppercase tracking-widest">
            Client Files · ملفات العملاء
          </h2>
          <div className="rounded-xl border border-dashed border-white/10 bg-white/5 p-8 text-center">
            <p className="text-2xl font-bold text-white/20">0</p>
            <p className="text-xs text-white/30 mt-1">لا توجد ملفات بعد · NO CLIENT FILES YET</p>
            <p className="text-[10px] text-white/20 mt-2 font-mono">
              Client files added after first project starts
            </p>
          </div>
        </section>

        {/* Compliance Docs */}
        <section className="mb-10">
          <h2 className="text-sm font-medium text-white/60 mb-4 font-mono uppercase tracking-widest">
            Compliance Docs · وثائق الامتثال
          </h2>
          <div className="space-y-2">
            {COMPLIANCE_DOCS.map((doc) => (
              <div
                key={doc.title}
                className="flex items-center justify-between rounded-xl border border-white/10 bg-white/5 px-4 py-3"
              >
                <div>
                  <p className="text-sm text-white/80">{doc.titleAr}</p>
                  <p className="text-[10px] text-white/30">{doc.title}</p>
                </div>
                <span className="flex items-center gap-1.5 text-[10px] font-mono text-emerald-300">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                  {doc.status}
                </span>
              </div>
            ))}
          </div>
        </section>

        {/* Quick links */}
        <div className="flex flex-wrap gap-3">
          <Link
            href="/legal"
            className="rounded-lg border border-white/10 bg-white/5 px-4 py-2 text-sm text-white/60 hover:text-white hover:bg-white/10 transition-colors"
          >
            القانونية — Legal
          </Link>
          <Link
            href="/proof-vault"
            className="rounded-lg border border-white/10 bg-white/5 px-4 py-2 text-sm text-white/60 hover:text-white hover:bg-white/10 transition-colors"
          >
            خزانة الإثبات — Proof Vault
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
