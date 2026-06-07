export default function ContactPage() {
  return <main className="mx-auto max-w-4xl px-6 py-20" dir="rtl">
    <p className="text-sm uppercase tracking-[0.3em] text-emerald-500">Contact</p>
    <h1 className="mt-4 text-4xl font-bold">ابدأ Diagnostic مختصر</h1>
    <p className="mt-4 text-neutral-600">أرسل لنا وضع المتابعة الحالي، ونرجع لك بثلاث فرص تحسين واضحة.</p>
    <form className="mt-10 grid gap-4">
      <input className="rounded-2xl border p-4" placeholder="الاسم" />
      <input className="rounded-2xl border p-4" placeholder="الشركة" />
      <input className="rounded-2xl border p-4" placeholder="رقم التواصل أو البريد" />
      <textarea className="rounded-2xl border p-4" rows={6} placeholder="ما أكبر مشكلة عندكم في المتابعة أو العروض؟" />
      <button className="rounded-full bg-black px-6 py-4 text-white">إرسال الطلب</button>
    </form>
  </main>;
}
