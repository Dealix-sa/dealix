export const metadata = {
  title: "Dealix Demo | تجربة مباشرة",
  description: "شاهد كيف يحول Dealix بيانات المبيعات والمتابعات إلى Revenue OS عملي خلال دقائق.",
};

const cards = [
  {
    title: "Revenue Intelligence Sprint",
    text: "تشخيص سريع يوضح أين تضيع الفرص، من أول 20 فرصة تستحق المتابعة، وما الرسائل المناسبة لكل شريحة.",
  },
  {
    title: "AI Sales Ops Assistant",
    text: "طبقة تشغيل أسبوعية تنتج أولويات المتابعة، مسودات الرسائل، تحضير الاجتماعات، وملخص الاعتراضات.",
  },
  {
    title: "Executive Command Center",
    text: "غرفة قيادة للمؤسس تعرض الإيراد، الفرص، المخاطر، القرارات، وProof Packs في مكان واحد.",
  },
];

export default function ArabicDemoPage() {
  return (
    <main dir="rtl" className="min-h-screen bg-[#06111f] px-6 py-16 text-white">
      <section className="mx-auto max-w-6xl">
        <p className="mb-4 inline-flex rounded-full border border-cyan-300/30 px-4 py-2 text-sm text-cyan-100">
          تجربة Dealix المباشرة
        </p>
        <h1 className="max-w-4xl text-4xl font-black leading-tight md:text-6xl">
          شاهد Dealix يحول فوضى المتابعات والفرص إلى نظام إيراد واضح.
        </h1>
        <p className="mt-6 max-w-3xl text-lg leading-8 text-slate-300">
          هذه الصفحة مخصصة للعرض أمام العملاء: تبدأ بـ P1 لتشخيص الإيراد، ثم تتحول إلى P2 للتشغيل الشهري، ثم P3 لغرفة القيادة التنفيذية.
        </p>

        <div className="mt-10 grid gap-5 md:grid-cols-3">
          {cards.map((card) => (
            <article key={card.title} className="rounded-3xl border border-white/10 bg-white/[0.06] p-6 shadow-2xl">
              <h2 className="text-xl font-bold text-cyan-100">{card.title}</h2>
              <p className="mt-4 leading-7 text-slate-300">{card.text}</p>
            </article>
          ))}
        </div>

        <section className="mt-12 rounded-3xl border border-emerald-300/20 bg-emerald-400/10 p-8">
          <h2 className="text-2xl font-black text-emerald-100">سيناريو البيع الآن</h2>
          <ol className="mt-5 space-y-3 text-slate-200">
            <li>1. افتح هذه الصفحة في أول دقيقة من المكالمة.</li>
            <li>2. اشرح أن البداية ليست SaaS كبير، بل Proof Pack خلال 5 إلى 7 أيام.</li>
            <li>3. اعرض P1 فقط: Revenue Intelligence Sprint.</li>
            <li>4. بعد إثبات القيمة، اعرض P2 كتشغيل شهري.</li>
            <li>5. اعرض P3 فقط إذا كان صاحب القرار يريد لوحة قيادة تنفيذية.</li>
          </ol>
        </section>

        <div className="mt-10 flex flex-wrap gap-4">
          <a className="rounded-2xl bg-cyan-300 px-6 py-3 font-bold text-slate-950" href="/revenue-os">
            افتح Revenue OS
          </a>
          <a className="rounded-2xl border border-white/20 px-6 py-3 font-bold text-white" href="/go-to-market">
            افتح Go-To-Market
          </a>
          <a className="rounded-2xl border border-white/20 px-6 py-3 font-bold text-white" href="/ar/zatca-readiness">
            فحص جاهزية ZATCA
          </a>
        </div>
      </section>
    </main>
  );
}
