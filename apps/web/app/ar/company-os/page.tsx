export const metadata = {
  title: "Dealix Company OS — ماكينة تشغيل الشركة اليومية",
  description:
    "نظام Dealix الداخلي لتوليد leads، عروض، drafts، proposals، CRM، وتقارير يومية.",
};

const loops = [
  "Production check",
  "Google Maps lead generation",
  "Daily offer generation",
  "Weakness analysis",
  "WhatsApp / Email drafts",
  "Proposal stubs",
  "CRM pipeline update",
  "Founder daily report",
];

export default function CompanyOSPage() {
  return (
    <main dir="rtl" className="min-h-screen bg-[#06111f] text-white">
      <section className="mx-auto max-w-6xl px-6 py-20">
        <p className="mb-5 inline-flex rounded-full border border-violet-300/30 px-4 py-2 text-sm text-violet-100">
          Company Operating System
        </p>

        <h1 className="max-w-5xl text-4xl font-black leading-[1.15] md:text-7xl">
          ماكينة يومية تولّد فرص، رسائل، عروض، وتقارير — قبل أن يبدأ اليوم.
        </h1>

        <p className="mt-7 max-w-3xl text-xl leading-9 text-slate-300">
          Dealix يشغّل نظاماً يومياً يبحث عن شركات، يحلل نقاط ضعفها، يجهز drafts،
          يقترح العرض المناسب، ويبني proposal stub للمراجعة والإرسال.
        </p>

        <div className="mt-10 grid gap-4 md:grid-cols-4">
          {loops.map((loop) => (
            <div key={loop} className="rounded-2xl border border-white/10 bg-white/[0.04] p-5 text-sm text-slate-200">
              {loop}
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
