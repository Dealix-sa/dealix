const industries = [
  ['العقار', 'تأهيل الاستفسارات، متابعة العملاء، العروض، وتقارير الفرص.'],
  ['التدريب والاستشارات', 'إدارة leads من الحملات، تذكير، عروض، ومتابعة التسجيل.'],
  ['العيادات والخدمات الصحية', 'تنظيم الاستفسارات والمواعيد مع مراعاة الخصوصية.'],
  ['وكالات التسويق', 'تحويل الحملات إلى pipeline واضح وتقارير قيمة للعميل.'],
  ['التجارة الإلكترونية', 'تحليل الاستفسارات، المرتجعات، وتذاكر العملاء.'],
  ['B2B Services', 'متابعة عروض طويلة، لجان شراء، وقرارات متعددة الأطراف.'],
];
export default function IndustriesPage() {
  return <main className="mx-auto max-w-6xl px-6 py-20" dir="rtl">
    <p className="text-sm uppercase tracking-[0.3em] text-emerald-500">Industries</p>
    <h1 className="mt-4 text-4xl font-bold">قطاعات نبدأ منها لأن الألم واضح</h1>
    <div className="mt-10 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
      {industries.map(([name, desc]) => <section key={name} className="rounded-3xl border p-6">
        <h2 className="text-2xl font-semibold">{name}</h2>
        <p className="mt-3 text-neutral-600">{desc}</p>
      </section>)}
    </div>
  </main>;
}
