export default function Page() {
  return (
    <main dir="rtl" className="min-h-screen bg-[#070b12] text-white px-6 py-16">
      <section className="mx-auto max-w-5xl space-y-8">
        <p className="text-sm text-cyan-300">Dealix Solutions</p>
        <h1 className="text-4xl font-bold">Dealix للخدمات المهنية B2B</h1>
        <p className="text-xl text-slate-300">Pipeline واضح للعلاقات، العروض، والمتابعة في المبيعات الاستشارية.</p>
        <div className="grid gap-4 md:grid-cols-3">
          <div className="rounded-3xl border border-white/10 bg-white/5 p-6"><h2 className="text-xl font-bold">التقاط الفرص</h2><p className="mt-3 text-slate-300">تنظيم أول تواصل وتحويله إلى lead واضح.</p></div>
          <div className="rounded-3xl border border-white/10 bg-white/5 p-6"><h2 className="text-xl font-bold">متابعة منظمة</h2><p className="mt-3 text-slate-300">next action لكل فرصة بدل الاعتماد على الذاكرة.</p></div>
          <div className="rounded-3xl border border-white/10 bg-white/5 p-6"><h2 className="text-xl font-bold">تقرير أسبوعي</h2><p className="mt-3 text-slate-300">قياس الردود والعروض والفرص الضائعة.</p></div>
        </div>
        <a href="/ar/diagnostic" className="inline-block rounded-2xl bg-cyan-400 px-6 py-3 font-bold text-slate-950">اطلب تشخيص Dealix</a>
      </section>
    </main>
  );
}
