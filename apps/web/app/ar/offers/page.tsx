export const metadata = {
  title: "Dealix — عروض وأسعار | AI Business Transformation",
  description:
    "سلم عروض Dealix الكامل: من تشخيص مجاني إلى نظام مؤسسي مخصص. كل عرض مصمم لمرحلة مختلفة من نضج شركتك.",
};

const offers = [
  {
    tier: "1",
    name: "Free Diagnostic",
    nameAr: "التشخيص المجاني",
    price: "مجاني",
    duration: "30 دقيقة",
    badge: "نقطة البداية",
    badgeColor: "border-slate-400/40 text-slate-300",
    highlight: false,
    description:
      "محادثة سريعة نحدد فيها أين تضيع الفرص في شركتك وما أول خطوة منطقية.",
    outputs: [
      "تحديد 3 نقاط تسرب رئيسية",
      "توصية بأول نظام مناسب",
      "وضوح هل Diagnostic Sprint مناسب أم لا",
    ],
    cta: "احجز محادثة مجانية",
    ctaHref: "/ar/intake",
    ctaStyle: "border border-white/20 hover:bg-white/10",
  },
  {
    tier: "2",
    name: "Micro Sprint",
    nameAr: "سبرنت سريع",
    price: "499 ريال",
    duration: "1–2 يوم",
    badge: "إثبات الكفاءة",
    badgeColor: "border-blue-400/40 text-blue-300",
    highlight: false,
    description:
      "نثبت قدرتنا بحل واحد سريع وملموس. مخرج حقيقي في يومين بسعر منخفض.",
    outputs: [
      "حل تشغيلي واحد مُنجز",
      "توثيق الحل وطريقة الاستخدام",
      "تقرير مبدئي بفرص إضافية",
    ],
    cta: "ابدأ Micro Sprint",
    ctaHref: "/ar/intake",
    ctaStyle: "border border-blue-400/40 text-blue-200 hover:bg-blue-400/10",
  },
  {
    tier: "3",
    name: "Data Intelligence Pack",
    nameAr: "حزمة بيانات",
    price: "1,500 ريال",
    duration: "2–3 أيام",
    badge: "أصل بيانات",
    badgeColor: "border-purple-400/40 text-purple-300",
    highlight: false,
    description:
      "نبني لك قاعدة بيانات عملاء مؤهلة، مصنفة، وجاهزة للتواصل.",
    outputs: [
      "قاعدة بيانات عملاء محتملين (100+ سجل)",
      "تصنيف حسب القطاع والأولوية",
      "تقرير جودة البيانات",
      "خريطة التواصل الأولى",
    ],
    cta: "احصل على حزمة البيانات",
    ctaHref: "/ar/intake",
    ctaStyle: "border border-purple-400/40 text-purple-200 hover:bg-purple-400/10",
  },
  {
    tier: "4",
    name: "Managed AI Operations",
    nameAr: "تشغيل AI شهري",
    price: "2,999–4,999 ريال/شهر",
    duration: "شهري مستمر",
    badge: "علاقة مستمرة",
    badgeColor: "border-amber-400/40 text-amber-300",
    highlight: false,
    description:
      "نشغّل نظام AI يومياً ونسلمك تقرير أسبوعي بالنتائج والتوصيات.",
    outputs: [
      "تقرير أسبوعي بالأداء والتوصيات",
      "تحديثات مستمرة على النظام",
      "دعم واتساب مباشر",
      "مراجعة شهرية مع المؤسس",
    ],
    cta: "ابدأ الإدارة الشهرية",
    ctaHref: "/ar/intake",
    ctaStyle: "border border-amber-400/40 text-amber-200 hover:bg-amber-400/10",
  },
  {
    tier: "5",
    name: "Transformation Diagnostic Sprint",
    nameAr: "تشخيص تحولي مدفوع",
    price: "7,500–25,000 ريال",
    duration: "3–7 أيام",
    badge: "نقطة الدخول الرئيسية",
    badgeColor: "border-cyan-300/60 text-cyan-200",
    highlight: true,
    description:
      "نكتشف أين يتسرب إيرادك ونبني لك خارطة الحل قبل أي التزام كبير.",
    outputs: [
      "Workflow Map — خريطة العمليات الحالية",
      "Leakage Map — أين يتسرب الإيراد وكم يكلف",
      "KPI Model — الأرقام التي يجب متابعتها",
      "First System Recommendation — أول نظام يستحق البناء",
      "Implementation Quote — السعر والجدول الزمني",
      "14-Day Pilot Plan — كيف تبدأ خلال أسبوعين",
    ],
    cta: "ابدأ التشخيص الآن",
    ctaHref: "/ar/diagnostic-sprint",
    ctaStyle: "bg-cyan-400 text-[#06111f] hover:bg-cyan-300 font-black",
  },
  {
    tier: "6",
    name: "Custom Enterprise System",
    nameAr: "نظام مؤسسي مخصص",
    price: "25,000–100,000+ ريال",
    duration: "4–12 أسبوع",
    badge: "للمؤسسات",
    badgeColor: "border-rose-400/40 text-rose-300",
    highlight: false,
    description:
      "نظام AI مبني خصيصاً لعمليات شركتك، مدمج مع فريقك وأدواتك الحالية.",
    outputs: [
      "تحليل العمليات الكامل",
      "تصميم النظام المخصص",
      "بناء وتكامل كامل",
      "تدريب الفريق",
      "دعم 90 يوم بعد الإطلاق",
      "توثيق كامل وتسليم الملكية",
    ],
    cta: "ناقش مشروعك",
    ctaHref: "/ar/intake",
    ctaStyle: "border border-rose-400/40 text-rose-200 hover:bg-rose-400/10",
  },
];

export default function OffersPage() {
  return (
    <main dir="rtl" className="min-h-screen bg-[#06111f] text-white">
      {/* Hero */}
      <section className="mx-auto max-w-6xl px-6 py-20">
        <p className="mb-5 inline-flex rounded-full border border-cyan-300/30 px-4 py-2 text-sm text-cyan-100">
          عروض Dealix
        </p>
        <h1 className="max-w-4xl text-4xl font-black leading-[1.15] md:text-6xl">
          ابدأ من أي مستوى. اتطور بالخطوة الصحيحة.
        </h1>
        <p className="mt-7 max-w-3xl text-xl leading-9 text-slate-300">
          كل عرض مصمم لمرحلة مختلفة من نضج شركتك. لا تلتزم بمشروع كبير قبل أن تعرف أين تقف.
          البداية الأذكى دائماً بتشخيص.
        </p>
      </section>

      {/* Offers Grid */}
      <section className="mx-auto max-w-6xl px-6 pb-20">
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {offers.map((offer) => (
            <div
              key={offer.tier}
              className={`relative flex flex-col rounded-3xl border p-6 ${
                offer.highlight
                  ? "border-cyan-400/50 bg-cyan-400/[0.06] ring-1 ring-cyan-400/30"
                  : "border-white/10 bg-white/[0.03]"
              }`}
            >
              {offer.highlight && (
                <div className="absolute -top-3 right-6">
                  <span className="rounded-full bg-cyan-400 px-3 py-1 text-xs font-black text-[#06111f]">
                    الأكثر طلباً
                  </span>
                </div>
              )}

              <div className="flex items-start justify-between">
                <span
                  className={`rounded-full border px-3 py-1 text-xs ${offer.badgeColor}`}
                >
                  {offer.badge}
                </span>
                <span className="text-sm text-slate-500">#{offer.tier}</span>
              </div>

              <h2 className="mt-4 text-2xl font-black">{offer.name}</h2>
              <p className="text-sm text-slate-400">{offer.nameAr}</p>

              <div className="mt-4 flex items-baseline gap-2">
                <span className="text-3xl font-black text-white">{offer.price}</span>
              </div>
              <p className="mt-1 text-sm text-slate-400">{offer.duration}</p>

              <p className="mt-4 text-sm leading-7 text-slate-300">
                {offer.description}
              </p>

              <ul className="mt-4 flex-1 space-y-2">
                {offer.outputs.map((output) => (
                  <li key={output} className="flex gap-2 text-sm text-slate-300">
                    <span className="mt-0.5 text-cyan-400">✓</span>
                    <span>{output}</span>
                  </li>
                ))}
              </ul>

              <a
                href={offer.ctaHref}
                className={`mt-6 block rounded-2xl px-6 py-3 text-center text-sm font-bold transition-colors ${offer.ctaStyle}`}
              >
                {offer.cta}
              </a>
            </div>
          ))}
        </div>
      </section>

      {/* Trust signals */}
      <section className="border-t border-white/5 bg-white/[0.02] py-16">
        <div className="mx-auto max-w-5xl px-6 text-center">
          <h2 className="text-2xl font-black">ضمانات التشغيل</h2>
          <div className="mt-8 grid gap-4 text-sm md:grid-cols-4">
            {[
              { icon: "🛡️", text: "PDPL-native — بياناتك محمية" },
              { icon: "✋", text: "موافقة أولاً — لا أتمتة بدون إذنك" },
              { icon: "📅", text: "3–7 أيام — نتائج سريعة" },
              { icon: "🇸🇦", text: "سعودي أولاً — نفهم السوق المحلي" },
            ].map((item) => (
              <div
                key={item.text}
                className="rounded-2xl border border-white/10 bg-white/[0.03] p-4"
              >
                <p className="text-2xl">{item.icon}</p>
                <p className="mt-2 text-slate-300">{item.text}</p>
              </div>
            ))}
          </div>

          <div className="mt-12">
            <a
              href="/ar/diagnostic-sprint"
              className="rounded-2xl bg-cyan-400 px-10 py-4 text-lg font-black text-[#06111f] hover:bg-cyan-300"
            >
              ابدأ بتشخيص تحولي مدفوع
            </a>
            <p className="mt-3 text-sm text-slate-500">
              7,500 ريال · 3–7 أيام · بدون التزام بالتنفيذ بعده
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}
