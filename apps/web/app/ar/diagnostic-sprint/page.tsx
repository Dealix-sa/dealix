export const metadata = {
  title: "Dealix Diagnostic Sprint — تشخيص تحولي مدفوع",
  description:
    "تشخيص مدفوع خلال 3-7 أيام لاكتشاف أين تضيع الفرص وما أول نظام يجب بناؤه.",
};

const outputs = [
  "خريطة سير العمل الحالية",
  "نقاط تسرب الإيراد والمتابعة",
  "تحليل أولويات الشركة",
  "نموذج KPI قابل للقياس",
  "اقتراح أول نظام مناسب",
  "عرض تنفيذ واضح للمرحلة التالية",
];

export default function DiagnosticSprintPage() {
  return (
    <main dir="rtl" className="min-h-screen bg-[#06111f] text-white">
      <section className="mx-auto max-w-5xl px-6 py-20">
        <p className="mb-5 inline-flex rounded-full border border-emerald-300/30 px-4 py-2 text-sm text-emerald-100">
          البداية الصحيحة قبل أي بناء مخصص
        </p>

        <h1 className="text-4xl font-black leading-[1.15] md:text-7xl">
          Transformation Diagnostic Sprint
        </h1>

        <p className="mt-7 text-xl leading-9 text-slate-300">
          خلال 3-7 أيام نكشف أين تضيع الفرص داخل الشركة، ونحدد أول نظام يجب بناؤه
          قبل أي التزام كبير أو مشروع مفتوح النطاق.
        </p>

        <div className="mt-10 grid gap-5 md:grid-cols-3">
          <div className="rounded-3xl border border-white/10 bg-white/[0.04] p-6">
            <p className="text-sm text-slate-400">السعر</p>
            <h2 className="mt-2 text-2xl font-black">7,500–25,000 ريال</h2>
          </div>
          <div className="rounded-3xl border border-white/10 bg-white/[0.04] p-6">
            <p className="text-sm text-slate-400">المدة</p>
            <h2 className="mt-2 text-2xl font-black">3–7 أيام</h2>
          </div>
          <div className="rounded-3xl border border-white/10 bg-white/[0.04] p-6">
            <p className="text-sm text-slate-400">الناتج</p>
            <h2 className="mt-2 text-2xl font-black">Blueprint تنفيذي</h2>
          </div>
        </div>

        <a href="/ar" className="mt-10 inline-flex rounded-2xl bg-emerald-400 px-8 py-4 text-lg font-black text-[#06111f] hover:bg-emerald-300">
          اطلب التشخيص الآن
        </a>
      </section>

      <section className="border-y border-white/5 bg-white/[0.02] py-16">
        <div className="mx-auto max-w-5xl px-6">
          <h2 className="text-3xl font-black">مخرجات التشخيص</h2>
          <div className="mt-8 grid gap-3 md:grid-cols-2">
            {outputs.map((item) => (
              <div key={item} className="rounded-2xl border border-white/10 bg-white/[0.04] px-5 py-4">
                ✅ {item}
              </div>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}
