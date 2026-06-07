type Props = { params: Promise<{ slug: string }> }

export default async function CaseStudyDetailPage({ params }: Props) {
  const { slug } = await params;
  return (
    <main className="min-h-screen bg-[#07111f] text-white px-6 py-20">
      <article className="mx-auto max-w-3xl">
        <p className="uppercase tracking-[0.3em] text-sm opacity-60">Case Study</p>
        <h1 className="text-5xl font-black mt-4">دراسة حالة Dealix</h1>
        <p className="mt-6 opacity-80">Slug: {slug}</p>
        <section className="mt-10 grid gap-6">
          <div><h2 className="text-2xl font-bold">المشكلة</h2><p className="opacity-80">فوضى متابعة وفرص غير موثقة.</p></div>
          <div><h2 className="text-2xl font-bold">التدخل</h2><p className="opacity-80">بناء workflow وتشخيص مؤشرات قياس.</p></div>
          <div><h2 className="text-2xl font-bold">النتيجة</h2><p className="opacity-80">تحسن وضوح الأولويات والمتابعة.</p></div>
        </section>
      </article>
    </main>
  );
}
