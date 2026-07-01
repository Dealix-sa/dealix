import LeadForm from "@/components/LeadForm";
import WhatsAppCTA from "@/components/WhatsAppCTA";
import { BOOKING_URL, CONTACT_EMAIL, mailtoLink } from "@/lib/contact";

export const metadata = {
  title: "Dealix — تواصل معنا",
  description:
    "تواصل مع Dealix عبر واتساب أو البريد أو الاستمارة. نراجع ونرد خلال 24 ساعة.",
};

const channels = [
  {
    icon: "💬",
    title: "واتساب",
    desc: "الأسرع — راسلنا مباشرة وسنكمل التفاصيل في محادثة قصيرة.",
  },
  {
    icon: "📧",
    title: "البريد الإلكتروني",
    desc: "أرسل تفاصيل شركتك ونرد عليك برد مفصّل.",
  },
  {
    icon: "📅",
    title: "احجز موعداً",
    desc: "مكالمة تعريفية قصيرة (20–30 دقيقة) نفهم فيها وضعك.",
  },
];

export default function ContactPage() {
  return (
    <main dir="rtl" className="min-h-screen bg-[#06111f] text-white">
      <section className="mx-auto max-w-5xl px-6 py-20">
        <p className="mb-5 inline-flex rounded-full border border-cyan-300/30 px-4 py-2 text-sm text-cyan-100">
          تواصل معنا
        </p>
        <h1 className="text-4xl font-black leading-[1.15] md:text-6xl">
          نرد خلال <span className="text-cyan-400">24 ساعة</span>.
        </h1>
        <p className="mt-7 max-w-3xl text-xl leading-9 text-slate-300">
          اختر القناة الأنسب لك. البداية دائماً بتشخيص مجاني — لا التزامات ولا دفع مسبق.
        </p>
      </section>

      <section className="mx-auto max-w-5xl px-6 pb-16">
        <div className="grid gap-4 md:grid-cols-3">
          <div className="flex flex-col rounded-3xl border border-emerald-400/20 bg-emerald-400/[0.04] p-6">
            <p className="text-3xl">{channels[0].icon}</p>
            <h2 className="mt-4 text-lg font-black">{channels[0].title}</h2>
            <p className="mt-2 flex-1 text-sm leading-7 text-slate-300">
              {channels[0].desc}
            </p>
            <WhatsAppCTA
              message="السلام عليكم، أريد التواصل مع Dealix بخصوص خدماتكم."
              label="راسلنا على واتساب"
              fallbackSubject="تواصل مع Dealix"
              className="mt-5 block rounded-2xl bg-emerald-500 px-6 py-3 text-center text-sm font-bold text-white hover:bg-emerald-400"
            />
          </div>

          <div className="flex flex-col rounded-3xl border border-white/10 bg-white/[0.03] p-6">
            <p className="text-3xl">{channels[1].icon}</p>
            <h2 className="mt-4 text-lg font-black">{channels[1].title}</h2>
            <p className="mt-2 flex-1 text-sm leading-7 text-slate-300">
              {channels[1].desc}
            </p>
            <a
              href={mailtoLink("تواصل مع Dealix")}
              dir="ltr"
              className="mt-5 block rounded-2xl border border-white/20 px-6 py-3 text-center text-sm font-bold hover:bg-white/10"
            >
              {CONTACT_EMAIL}
            </a>
          </div>

          <div className="flex flex-col rounded-3xl border border-white/10 bg-white/[0.03] p-6">
            <p className="text-3xl">{channels[2].icon}</p>
            <h2 className="mt-4 text-lg font-black">{channels[2].title}</h2>
            <p className="mt-2 flex-1 text-sm leading-7 text-slate-300">
              {channels[2].desc}
            </p>
            <a
              href={BOOKING_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-5 block rounded-2xl border border-cyan-300/30 px-6 py-3 text-center text-sm font-bold text-cyan-100 hover:bg-cyan-400/10"
            >
              احجز موعداً
            </a>
          </div>
        </div>
      </section>

      <section className="border-t border-white/5 bg-white/[0.02] py-16">
        <div className="mx-auto max-w-3xl px-6">
          <h2 className="text-3xl font-black">أو أرسل الاستمارة</h2>
          <p className="mt-3 text-slate-400">
            نراجع المعلومات ونتواصل معك خلال 24 ساعة.
          </p>
          <div className="mt-8">
            <LeadForm />
          </div>
          <p className="mt-8 text-center text-sm text-slate-500">
            تريد تفاصيل أكثر عن البداية؟{" "}
            <a href="/ar/intake" className="text-cyan-300 hover:underline">
              صفحة بدء التشخيص
            </a>
          </p>
        </div>
      </section>
    </main>
  );
}
