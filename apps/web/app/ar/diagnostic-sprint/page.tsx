export const metadata = {
  title: "Dealix Diagnostic Sprint — تشخيص تحولي مدفوع | 7,500–25,000 ريال",
  description:
    "خلال 3–7 أيام نكشف أين يتسرب إيرادك ونبني خارطة الحل الكاملة. Workflow Map + Leakage Map + KPI Model + Implementation Quote + 14-Day Plan.",
};

const outputs = [
  {
    num: "01",
    title: "Workflow Map",
    titleAr: "خريطة العمليات",
    desc: "كيف تسير عملياتك فعلاً — كل خطوة من الاستفسار حتى الإغلاق أو التسليم.",
  },
  {
    num: "02",
    title: "Leakage Map",
    titleAr: "خريطة التسرب",
    desc: "أين يتسرب الإيراد، كم يكلفك كل نقطة تسرب شهرياً، وما أسباب التسرب.",
  },
  {
    num: "03",
    title: "KPI Model",
    titleAr: "نموذج الأداء",
    desc: "الأرقام التي يجب أن تتابعها يومياً لتعرف إن الشركة تتقدم أم تتراجع.",
  },
  {
    num: "04",
    title: "First System Recommendation",
    titleAr: "توصية أول نظام",
    desc: "أي نظام يحل أكبر مشكلة أولاً — مع تفسير لماذا هذا النظام وليس غيره.",
  },
  {
    num: "05",
    title: "Implementation Quote",
    titleAr: "عرض التنفيذ",
    desc: "كم يكلف بناء النظام الموصى به، ما الجدول الزمني، وما يشمله وما لا يشمله.",
  },
  {
    num: "06",
    title: "14-Day Pilot Plan",
    titleAr: "خطة التجريب",
    desc: "كيف تبدأ تجريب النظام خلال أسبوعين بدون مخاطرة كبيرة.",
  },
];

const process = [
  {
    day: "اليوم 1–2",
    title: "Discovery",
    steps: [
      "جلسة Zoom (90 دقيقة) مع المؤسس أو الفريق",
      "جمع المستندات والبيانات الموجودة",
      "ملء استمارة الـ Intake الكاملة",
      "مراجعة الأدوات والعمليات الحالية",
    ],
  },
  {
    day: "اليوم 3–5",
    title: "Analysis",
    steps: [
      "بناء Workflow Map الكامل",
      "رسم Leakage Map مع الأرقام التقديرية",
      "تصميم KPI Model المناسب للقطاع",
      "تقييم الخيارات التقنية للحل",
    ],
  },
  {
    day: "اليوم 6–7",
    title: "Delivery",
    steps: [
      "جلسة Zoom لعرض النتائج (60 دقيقة)",
      "تسليم المستندات الست كاملة",
      "نقاش التوصيات والأسئلة",
      "تقديم Implementation Quote إذا طُلب",
    ],
  },
];

const pricing = [
  {
    size: "شركة صغيرة",
    employees: "أقل من 20 موظف",
    price: "7,500 SAR",
    includes: ["التشخيص الكامل", "3 مستندات رئيسية", "جلستان Zoom"],
  },
  {
    size: "شركة متوسطة",
    employees: "20–100 موظف",
    price: "12,500 SAR",
    includes: ["التشخيص الكامل", "6 مستندات كاملة", "3 جلسات Zoom", "خطة 14 يوم"],
    featured: true,
  },
  {
    size: "شركة كبيرة",
    employees: "100+ موظف أو متعدد الفروع",
    price: "25,000 SAR",
    includes: ["التشخيص الكامل بعمق", "6 مستندات + ملاحق", "4 جلسات Zoom", "مراجعة مع الإدارة العليا"],
  },
];

const faqs = [
  {
    q: "هل أُلزم بالتنفيذ بعد التشخيص؟",
    a: "لا. التشخيص هو مستند مستقل. يمكنك الاستفادة منه بدون أي التزام بمشروع تالٍ مع Dealix.",
  },
  {
    q: "ماذا لو لم أكن راضياً عن النتائج؟",
    a: "نناقش النتائج معك في جلسة التسليم. إذا كانت هناك نقاط غير واضحة، نُكملها. نهدف لمستند قابل للتنفيذ فعلاً.",
  },
  {
    q: "هل يحتاج التشخيص حضور شخصي؟",
    a: "لا. كل العمل يتم عبر Zoom وتبادل الملفات. مناسب للرياض، جدة، الدمام، وأي مدينة أخرى.",
  },
  {
    q: "ما البيانات التي تحتاجونها؟",
    a: "بيانات تشغيلية عامة: حجم الاستفسارات، الأدوات المستخدمة، عدد الموظفين، وأمثلة من العمليات الحالية. لا بيانات مالية حساسة.",
  },
  {
    q: "هل يمكن تقسيم الدفع؟",
    a: "نعم. 50% عند البدء، 50% عند التسليم. لا رسوم خفية.",
  },
];

export default function DiagnosticSprintPage() {
  return (
    <main dir="rtl" className="min-h-screen bg-[#06111f] text-white">
      {/* Hero */}
      <section className="mx-auto max-w-6xl px-6 py-20">
        <p className="mb-5 inline-flex rounded-full border border-emerald-300/30 px-4 py-2 text-sm text-emerald-100">
          نقطة الدخول الرئيسية لـ Dealix
        </p>
        <h1 className="max-w-5xl text-4xl font-black leading-[1.15] md:text-7xl">
          Transformation Diagnostic Sprint
        </h1>
        <p className="mt-5 max-w-4xl text-2xl font-black text-cyan-400 md:text-4xl">
          خلال 3–7 أيام، نكتشف أين يتسرب إيرادك ونبني خارطة الحل.
        </p>
        <p className="mt-7 max-w-3xl text-xl leading-9 text-slate-300">
          لا نبدأ بمشروع ضخم. نبدأ بتشخيص دقيق يعطيك 6 مستندات قابلة للتنفيذ
          قبل أي التزام كبير.
        </p>

        <div className="mt-10 grid gap-4 md:grid-cols-3">
          {[
            { label: "السعر", value: "7,500–25,000 ريال" },
            { label: "المدة", value: "3–7 أيام" },
            { label: "المخرج", value: "6 مستندات تنفيذية" },
          ].map((item) => (
            <div
              key={item.label}
              className="rounded-3xl border border-white/10 bg-white/[0.04] p-6"
            >
              <p className="text-sm text-slate-400">{item.label}</p>
              <h2 className="mt-2 text-2xl font-black">{item.value}</h2>
            </div>
          ))}
        </div>

        <div className="mt-10 flex flex-wrap gap-4">
          <a
            href="/ar/intake"
            className="rounded-2xl bg-cyan-400 px-10 py-4 text-lg font-black text-[#06111f] hover:bg-cyan-300"
          >
            ابدأ التشخيص الآن
          </a>
          <a
            href="/ar/case-studies"
            className="rounded-2xl border border-white/20 px-10 py-4 text-lg font-semibold hover:bg-white/10"
          >
            شاهد نتائج حقيقية
          </a>
        </div>
      </section>

      {/* Outputs */}
      <section className="border-y border-white/5 bg-white/[0.02] py-16">
        <div className="mx-auto max-w-6xl px-6">
          <h2 className="text-3xl font-black">6 مستندات تحصل عليها</h2>
          <p className="mt-3 text-slate-400">كل مستند مبني على بياناتك الفعلية — لا templates عامة.</p>
          <div className="mt-8 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {outputs.map((o) => (
              <div
                key={o.num}
                className="rounded-3xl border border-white/10 bg-white/[0.04] p-6"
              >
                <span className="text-sm font-black text-cyan-400">{o.num}</span>
                <h3 className="mt-2 text-lg font-black">{o.title}</h3>
                <p className="text-sm text-slate-400">{o.titleAr}</p>
                <p className="mt-3 text-sm leading-7 text-slate-300">{o.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Process */}
      <section className="mx-auto max-w-6xl px-6 py-16">
        <h2 className="text-3xl font-black">كيف يسير العمل؟</h2>
        <div className="mt-8 grid gap-6 md:grid-cols-3">
          {process.map((p) => (
            <div key={p.day} className="rounded-3xl border border-white/10 bg-white/[0.03] p-6">
              <p className="text-sm font-bold text-cyan-400">{p.day}</p>
              <h3 className="mt-2 text-xl font-black">{p.title}</h3>
              <ul className="mt-4 space-y-2">
                {p.steps.map((s) => (
                  <li key={s} className="flex gap-2 text-sm text-slate-300">
                    <span className="mt-0.5 text-emerald-400">→</span>
                    <span>{s}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </section>

      {/* Pricing */}
      <section className="border-y border-white/5 bg-white/[0.02] py-16">
        <div className="mx-auto max-w-5xl px-6">
          <h2 className="text-3xl font-black">الأسعار</h2>
          <p className="mt-3 text-slate-400">السعر يعتمد على حجم الشركة وعمق التشخيص المطلوب.</p>
          <div className="mt-8 grid gap-4 md:grid-cols-3">
            {pricing.map((p) => (
              <div
                key={p.size}
                className={`rounded-3xl border p-6 ${
                  p.featured
                    ? "border-cyan-400/50 bg-cyan-400/[0.06] ring-1 ring-cyan-400/20"
                    : "border-white/10 bg-white/[0.03]"
                }`}
              >
                {p.featured && (
                  <span className="mb-3 inline-block rounded-full bg-cyan-400 px-3 py-1 text-xs font-black text-[#06111f]">
                    الأكثر طلباً
                  </span>
                )}
                <h3 className="text-lg font-black">{p.size}</h3>
                <p className="text-sm text-slate-400">{p.employees}</p>
                <p className="mt-4 text-3xl font-black">{p.price}</p>
                <ul className="mt-4 space-y-2">
                  {p.includes.map((item) => (
                    <li key={item} className="flex gap-2 text-sm text-slate-300">
                      <span className="text-cyan-400">✓</span>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
                <a
                  href="/ar/intake"
                  className={`mt-6 block rounded-2xl px-6 py-3 text-center text-sm font-bold transition-colors ${
                    p.featured
                      ? "bg-cyan-400 text-[#06111f] hover:bg-cyan-300"
                      : "border border-white/20 hover:bg-white/10"
                  }`}
                >
                  ابدأ الآن
                </a>
              </div>
            ))}
          </div>
          <p className="mt-4 text-sm text-slate-500">
            * شروط الدفع: 50% عند البدء — 50% عند التسليم
          </p>
        </div>
      </section>

      {/* FAQ */}
      <section className="mx-auto max-w-4xl px-6 py-16">
        <h2 className="text-3xl font-black">أسئلة شائعة</h2>
        <div className="mt-8 space-y-4">
          {faqs.map((faq) => (
            <div
              key={faq.q}
              className="rounded-3xl border border-white/10 bg-white/[0.03] p-6"
            >
              <h3 className="font-bold text-white">{faq.q}</h3>
              <p className="mt-3 text-sm leading-7 text-slate-300">{faq.a}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="border-t border-white/5 bg-white/[0.02] py-16">
        <div className="mx-auto max-w-3xl px-6 text-center">
          <h2 className="text-3xl font-black">جاهز لتعرف أين يتسرب إيرادك؟</h2>
          <p className="mt-4 text-lg text-slate-300">
            ابدأ بإرسال بيانات شركتك — سنراجعها ونتواصل خلال 24 ساعة.
          </p>
          <div className="mt-8">
            <a
              href="/ar/intake"
              className="rounded-2xl bg-cyan-400 px-12 py-4 text-xl font-black text-[#06111f] hover:bg-cyan-300"
            >
              ابدأ التشخيص التحولي
            </a>
          </div>
          <div className="mt-6 flex flex-wrap justify-center gap-6 text-sm text-slate-500">
            <span>PDPL-native</span>
            <span>·</span>
            <span>Approval-first</span>
            <span>·</span>
            <span>لا التزام بالتنفيذ بعده</span>
          </div>
        </div>
      </section>
    </main>
  );
}
