export default function PricingPage() {
  const plans = [
    ['Growth Diagnostic', 'Free / Symbolic', 'تشخيص تسرب الفرص، متابعة، واتساب، عروض، وتقرير أولي.'],
    ['Pilot Build', '499–2,500 SAR', 'تنفيذ workflow واحد خلال 7–14 يوم مع تقرير Before/After.'],
    ['Revenue OS Setup', '4,500–18,000 SAR', 'بناء نظام تشغيل مبيعات/عمليات كامل حسب حجم الشركة.'],
    ['Managed Growth OS', '2,500–15,000 SAR / month', 'تشغيل وتحسين ومتابعة أسبوعية مستمرة.'],
    ['Custom AI Systems', 'Custom', 'أنظمة مخصصة للقطاعات والبيانات الداخلية والعمليات المعقدة.'],
  ];
  return <main className="mx-auto max-w-6xl px-6 py-20" dir="rtl">
    <p className="text-sm uppercase tracking-[0.3em] text-emerald-500">Pricing</p>
    <h1 className="mt-4 text-4xl font-bold">تسعير واضح يبدأ بإثبات القيمة</h1>
    <p className="mt-4 max-w-3xl text-lg text-neutral-600">نبدأ صغيرًا: تشخيص، Pilot، ثم توسع إذا ظهرت قيمة تشغيلية قابلة للقياس.</p>
    <div className="mt-10 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
      {plans.map(([name, price, desc]) => <section key={name} className="rounded-3xl border p-6 shadow-sm">
        <h2 className="text-2xl font-semibold">{name}</h2>
        <p className="mt-3 text-emerald-600 font-bold">{price}</p>
        <p className="mt-4 text-neutral-600">{desc}</p>
        <a className="mt-6 inline-block rounded-full bg-black px-5 py-3 text-white" href="/contact">ابدأ التشخيص</a>
      </section>)}
    </div>
    <p className="mt-8 text-sm text-neutral-500">لا نقدم ضمانات إيراد رقمية. نقيس التحسن التشغيلي ونبني على البيانات الفعلية.</p>
  </main>;
}
