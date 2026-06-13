import type { Metadata } from "next";
import CustomRequestForm from "../../../components/CustomRequestForm";
import { VALUE_DISCLAIMER } from "../../../lib/offerings";

export const metadata: Metadata = {
  title: "حلول مخصّصة — وش تبي نسوّي",
  description:
    "اوصف تحدّيك وراح نصمّم لك حلّاً مخصّصاً لتشغيل الإيراد بالذكاء الاصطناعي لشركتك السعودية — بأسلوب الموافقة أولاً. لا scraping، لا إرسال آلي، لا نتائج مضمونة.",
  alternates: { canonical: "/ar/custom", languages: { "ar-SA": "/ar/custom", "en-US": "/custom" } },
};

const STEPS = [
  ["١", "تصف التحدّي", "قل لنا وش تبي تبني أو تصلح — بكلامك أنت."],
  ["٢", "نحدّد النطاق، approval-first", "نحوّله إلى workflow محوكم. لا يُرسل أو يُشحن أي شيء خارجي بدون موافقتك."],
  ["٣", "تحصل على خطوة تالية واضحة", "تشخيص مجاني، أو Command Sprint، أو خطة شهرية — بأدلة لا وعود."],
];

export default function ArabicCustomPage() {
  return (
    <main dir="rtl" className="min-h-screen bg-[#06111f] text-white">
      <header className="mx-auto flex max-w-5xl items-center justify-between px-6 py-5">
        <a href="/ar" className="text-lg font-black text-white">Dealix</a>
        <nav className="flex items-center gap-5 text-sm text-slate-400">
          <a href="/ar/services" className="hover:text-white">الخدمات</a>
          <a href="/custom" className="hover:text-white">English</a>
        </nav>
      </header>

      <section className="mx-auto max-w-5xl px-6 pt-10 pb-8 md:pt-14">
        <p className="mb-5 inline-flex rounded-full border border-cyan-300/30 px-4 py-2 text-sm text-cyan-100">
          Custom AI · approval-first
        </p>
        <h1 className="max-w-3xl text-4xl font-black leading-[1.15] md:text-5xl">
          قل لنا وش تبي نسوّي.
        </h1>
        <p className="mt-6 max-w-2xl text-lg leading-9 text-slate-300">
          ما لقيت الخدمة المناسبة تماماً؟ اوصف تحدّيك وراح نصمّم لك حلّاً مخصّصاً بنفس المبدأ:
          الذكاء الاصطناعي يكتب ويحلّل، وأنت توافق وترسل.
        </p>
      </section>

      <section className="mx-auto max-w-5xl px-6 pb-6">
        <div className="grid gap-4 md:grid-cols-3">
          {STEPS.map(([n, title, body]) => (
            <div key={n} className="rounded-3xl border border-white/10 bg-white/[0.03] p-6">
              <p className="text-sm font-black text-cyan-300">{n}</p>
              <h3 className="mt-2 text-base font-black text-slate-100">{title}</h3>
              <p className="mt-2 text-sm leading-7 text-slate-400">{body}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto max-w-2xl px-6 pb-20 pt-6">
        <CustomRequestForm locale="ar" />
        <p className="mt-8 text-center text-xs text-slate-500">{VALUE_DISCLAIMER}</p>
      </section>
    </main>
  );
}
