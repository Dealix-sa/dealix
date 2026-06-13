export default function CaseStudiesPage() {
  return <main className="mx-auto max-w-5xl px-6 py-20" dir="rtl">
    <p className="text-sm uppercase tracking-[0.3em] text-emerald-500">Proof</p>
    <h1 className="mt-4 text-4xl font-bold">دراسات حالة Dealix</h1>
    <p className="mt-4 text-neutral-600">ابدأ بنشر دراسات حالة بدون أسرار عملاء: المشكلة، العملية القديمة، النظام الجديد، وما تغير تشغيليًا.</p>
    <section className="mt-10 rounded-3xl border p-8">
      <h2 className="text-2xl font-semibold">قالب دراسة حالة</h2>
      <ol className="mt-5 list-decimal space-y-3 pr-6 text-neutral-700">
        <li>الوضع قبل Dealix.</li>
        <li>أين كانت الفرص تضيع؟</li>
        <li>ما workflow الذي بُني؟</li>
        <li>ما المؤشرات قبل/بعد؟</li>
        <li>ما القرار التالي؟</li>
      </ol>
    </section>
  </main>;
}
