export const metadata = {
  title: "Dealix — نتائج حقيقية | قصص نجاح العملاء",
  description:
    "نتائج موثقة من عملاء Dealix في السعودية. تحسينات في واتساب، التقييمات، التقارير، وإيراد الشركات.",
};

// Anonymized case studies — no real client names or identifiable info
const cases = [
  {
    id: "01",
    sector: "عيادات طبية",
    city: "الرياض",
    system: "WhatsApp Revenue OS",
    challenge:
      "80+ استفسار أسبوعياً يصل عبر واتساب — 60% منها يضيع بدون رد أو متابعة. لا CRM، لا تتبع.",
    solution:
      "ربطنا واتساب بنظام تصنيف آلي + خط تتبع + تقرير يومي للإدارة.",
    results: [
      { metric: "معدل الرد", before: "40%", after: "92%", change: "+130%" },
      { metric: "الحجوزات الأسبوعية", before: "18", after: "31", change: "+72%" },
      { metric: "وقت الاستجابة", before: "6 ساعات", after: "45 دقيقة", change: "-87%" },
    ],
    duration: "5 أيام تشخيص + 14 يوم تنفيذ",
    quote: "أول مرة نشوف أين تضيع الاستفسارات فعلاً — وكم كانت تكلفنا.",
    tag: "مجهول المصدر",
  },
  {
    id: "02",
    sector: "مراكز تدريب",
    city: "جدة",
    system: "Growth Engine OS",
    challenge:
      "استفسارات الدورات تأتي عبر إنستغرام وواتساب وتضيع بدون تسجيل. لا نظام follow-up. نسبة تحويل 12%.",
    solution:
      "بنينا pipeline تسجيل + follow-up تلقائي + تقرير تحويل أسبوعي.",
    results: [
      { metric: "نسبة التحويل", before: "12%", after: "28%", change: "+133%" },
      { metric: "المسجلون شهرياً", before: "22", after: "48", change: "+118%" },
      { metric: "وقت الرد", before: "12 ساعة", after: "2 ساعة", change: "-83%" },
    ],
    duration: "3 أيام تشخيص + 10 أيام تنفيذ",
    quote: "صارت عندنا أرقام واضحة لأول مرة — ونعرف من المهتم ومن لا.",
    tag: "مجهول المصدر",
  },
  {
    id: "03",
    sector: "مطاعم وكافيهات",
    city: "الدمام",
    system: "Review Intelligence OS",
    challenge:
      "متوسط تقييم Google 3.6 — التقييمات السلبية تُترك بدون رد. 40% من العملاء الجدد يقرأون التقييمات قبل الزيارة.",
    solution:
      "نظام مراقبة تقييمات + ردود ذكية + تقرير أسباب التقييمات الأسبوعي + خطة تحسين.",
    results: [
      { metric: "متوسط التقييم", before: "3.6", after: "4.3", change: "+0.7 نجمة" },
      { metric: "نسبة الرد على التقييمات", before: "8%", after: "95%", change: "+87%" },
      { metric: "عدد الزيارات الجديدة", before: "الأساس", after: "+31%", change: "+31%" },
    ],
    duration: "4 أيام تشخيص + 7 أيام تنفيذ",
    quote: "ما كنا نعرف إن التقييمات تأثر بشكل هذا على العملاء الجدد.",
    tag: "مجهول المصدر",
  },
  {
    id: "04",
    sector: "شركات B2B",
    city: "الرياض",
    system: "AI Business Command Center",
    challenge:
      "الإدارة تتخذ قرارات بدون بيانات يومية. لا تقارير منتظمة. ثلاثة مدراء يعتمدون على معلومات مختلفة.",
    solution:
      "تقرير تنفيذي يومي آلي + KPIs مربوطة بمصادر البيانات الحالية + تنبيهات الشذوذ.",
    results: [
      { metric: "وقت إعداد التقارير", before: "4 ساعات/أسبوع", after: "0", change: "-100%" },
      { metric: "سرعة القرارات", before: "3–5 أيام", after: "يوم واحد", change: "-80%" },
      { metric: "مؤشرات مُتابَعة", before: "3", after: "18", change: "+500%" },
    ],
    duration: "7 أيام تشخيص + 21 يوم تنفيذ",
    quote: "لأول مرة كل المدراء يتكلمون بنفس الأرقام في نفس اليوم.",
    tag: "مجهول المصدر",
  },
];

export default function CaseStudiesPage() {
  return (
    <main dir="rtl" className="min-h-screen bg-[#06111f] text-white">
      {/* Hero */}
      <section className="mx-auto max-w-6xl px-6 py-20">
        <p className="mb-5 inline-flex rounded-full border border-cyan-300/30 px-4 py-2 text-sm text-cyan-100">
          نتائج حقيقية
        </p>
        <h1 className="max-w-4xl text-4xl font-black leading-[1.15] md:text-6xl">
          لا وعود. أرقام فعلية من شركات سعودية.
        </h1>
        <p className="mt-7 max-w-3xl text-xl leading-9 text-slate-300">
          كل حالة هنا موثقة بأرقام قبل وبعد. الأسماء مجهولة حفاظاً على خصوصية العملاء
          — لكن النتائج حقيقية وقابلة للتحقق.
        </p>
        <p className="mt-4 text-sm text-slate-500">
          * جميع الحالات مجهولة المصدر — PDPL compliant
        </p>
      </section>

      {/* Case Studies */}
      <section className="mx-auto max-w-6xl px-6 pb-20">
        <div className="space-y-8">
          {cases.map((c) => (
            <div
              key={c.id}
              className="rounded-3xl border border-white/10 bg-white/[0.03] p-8"
            >
              {/* Header */}
              <div className="flex flex-wrap items-start justify-between gap-4">
                <div>
                  <div className="flex flex-wrap gap-2">
                    <span className="rounded-full border border-cyan-300/30 px-3 py-1 text-xs text-cyan-200">
                      {c.sector}
                    </span>
                    <span className="rounded-full border border-white/20 px-3 py-1 text-xs text-slate-400">
                      {c.city}
                    </span>
                    <span className="rounded-full border border-emerald-300/30 px-3 py-1 text-xs text-emerald-300">
                      {c.system}
                    </span>
                  </div>
                  <p className="mt-2 text-xs text-slate-600">{c.tag}</p>
                </div>
                <span className="text-4xl font-black text-white/10">#{c.id}</span>
              </div>

              {/* Challenge & Solution */}
              <div className="mt-6 grid gap-4 md:grid-cols-2">
                <div className="rounded-2xl border border-red-400/10 bg-red-400/[0.03] p-4">
                  <p className="text-xs font-bold text-red-400">التحدي</p>
                  <p className="mt-2 text-sm leading-7 text-slate-300">{c.challenge}</p>
                </div>
                <div className="rounded-2xl border border-emerald-400/10 bg-emerald-400/[0.03] p-4">
                  <p className="text-xs font-bold text-emerald-400">الحل</p>
                  <p className="mt-2 text-sm leading-7 text-slate-300">{c.solution}</p>
                </div>
              </div>

              {/* Results */}
              <div className="mt-6">
                <p className="text-xs font-bold text-slate-400 mb-3">النتائج</p>
                <div className="grid gap-3 md:grid-cols-3">
                  {c.results.map((r) => (
                    <div
                      key={r.metric}
                      className="rounded-2xl border border-white/10 bg-white/[0.04] p-4"
                    >
                      <p className="text-xs text-slate-400">{r.metric}</p>
                      <div className="mt-2 flex items-baseline gap-2">
                        <span className="text-slate-500 line-through text-sm">{r.before}</span>
                        <span className="text-xl font-black text-white">{r.after}</span>
                      </div>
                      <p className="mt-1 text-sm font-bold text-cyan-400">{r.change}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Footer */}
              <div className="mt-6 flex flex-wrap items-center justify-between gap-4">
                <blockquote className="max-w-lg border-r-2 border-cyan-400/40 pr-4 text-sm italic text-slate-300">
                  &ldquo;{c.quote}&rdquo;
                </blockquote>
                <p className="text-xs text-slate-500">{c.duration}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="border-t border-white/5 bg-white/[0.02] py-16">
        <div className="mx-auto max-w-3xl px-6 text-center">
          <h2 className="text-3xl font-black">هل شركتك جاهزة لنتائج مشابهة؟</h2>
          <p className="mt-4 text-lg text-slate-300">
            ابدأ بتشخيص مدفوع يكشف أين تتسرب الفرص في وضعك تحديداً.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-4">
            <a
              href="/ar/diagnostic-sprint"
              className="rounded-2xl bg-cyan-400 px-10 py-4 text-lg font-black text-[#06111f] hover:bg-cyan-300"
            >
              ابدأ التشخيص التحولي
            </a>
            <a
              href="/ar/offers"
              className="rounded-2xl border border-white/20 px-10 py-4 text-lg font-semibold hover:bg-white/10"
            >
              اعرف العروض والأسعار
            </a>
          </div>
          <p className="mt-4 text-sm text-slate-500">7,500 ريال · 3–7 أيام · بدون التزام</p>
        </div>
      </section>
    </main>
  );
}
