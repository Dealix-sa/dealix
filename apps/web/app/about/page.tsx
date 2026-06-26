import Link from "next/link";

export const metadata = {
  title: "من نحن — Dealix | About Us",
  description:
    "Dealix is Saudi Arabia's first AI Business Transformation company — we build operating systems for B2B growth.",
};

const WHY = [
  {
    icon: "⚡",
    ar: "سرعة لا مثيل لها",
    en: "Unmatched Speed",
    desc: "نبني ونشغّل خلال أيام، لا أشهر.",
  },
  {
    icon: "🔍",
    ar: "شفافية كاملة",
    en: "Full Transparency",
    desc: "كل قرار، كل نتيجة، كل رقم — مكشوف أمامك.",
  },
  {
    icon: "📊",
    ar: "نتائج قابلة للقياس",
    en: "Measurable Outcomes",
    desc: "لا وعود فضفاضة — مؤشرات واضحة من اليوم الأول.",
  },
];

export default function AboutPage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-4xl px-6 py-20">

        {/* Hero */}
        <header className="text-center">
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">من نحن · About</p>
          <h1 className="mt-4 text-4xl font-bold leading-tight">
            نحوّل الشركات السعودية
            <br />
            بالذكاء الاصطناعي
          </h1>
          <p className="mt-4 text-sm text-white/60 max-w-xl mx-auto leading-relaxed">
            Dealix هي أول شركة سعودية متخصصة في بناء أنظمة تشغيل ذكاء اصطناعي للشركات B2B — من
            إدارة الإيرادات إلى خدمة العملاء إلى النمو التجاري.
          </p>
          <p className="mt-2 text-xs text-white/40">
            Dealix is Saudi Arabia's first AI Business Transformation company, building AI operating
            systems for B2B growth.
          </p>
        </header>

        {/* Mission */}
        <section className="mt-16 rounded-2xl border border-white/10 bg-white/[0.03] p-8">
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80 mb-4">رسالتنا · Mission</p>
          <p className="text-lg font-medium leading-relaxed">
            نعتقد أن كل شركة سعودية تستحق أنظمة تشغيل ذكية تعمل على مدار الساعة — بدون تعقيد، بدون
            تكلفة ضخمة، وبنتائج يمكن قياسها.
          </p>
          <p className="mt-3 text-sm text-white/50">
            We believe every Saudi B2B company deserves intelligent operating systems that run 24/7 —
            without complexity, without bloat, with results you can measure.
          </p>
        </section>

        {/* Why Dealix */}
        <section className="mt-12">
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80 mb-6">لماذا Dealix؟</p>
          <div className="grid gap-4 sm:grid-cols-3">
            {WHY.map((w) => (
              <div
                key={w.ar}
                className="rounded-2xl border border-white/10 bg-white/[0.03] p-6 text-center"
              >
                <span className="text-3xl">{w.icon}</span>
                <p className="mt-3 font-semibold">{w.ar}</p>
                <p className="text-xs text-white/40 mb-2">{w.en}</p>
                <p className="text-sm text-white/60">{w.desc}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Disclaimer */}
        <p className="mt-10 text-xs text-white/30 text-center">
          القيمة التقديرية ليست قيمة مُتحقَّقة · Estimated value is not Verified value
        </p>

        {/* CTA */}
        <div className="mt-12 flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
          <Link
            href="/pricing"
            className="rounded-lg bg-amber-300 px-6 py-3 text-sm font-semibold text-black hover:bg-amber-200 transition-colors"
          >
            عروضنا وأسعارنا
          </Link>
          <Link
            href="/book"
            className="rounded-lg border border-white/20 px-6 py-3 text-sm font-semibold text-white hover:border-white/40 transition-colors"
          >
            احجز تشخيصاً مجانياً
          </Link>
        </div>
      </div>
    </main>
  );
}
