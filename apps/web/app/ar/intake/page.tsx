import LeadForm from "@/components/LeadForm";
import WhatsAppCTA from "@/components/WhatsAppCTA";
import { BOOKING_URL } from "@/lib/contact";

export const metadata = {
  title: "Dealix Intake — ابدأ تشخيصك التحولي",
  description:
    "أرسل بيانات شركتك لبدء التشخيص التحولي مع Dealix. نراجع ونتواصل خلال 24 ساعة.",
};

const WA_INTAKE_MESSAGE = `السلام عليكم،
اسم الشركة: [اسم شركتك]
القطاع: [قطاعك]
المدينة: [مدينتك]
الموظفون: [عدد تقريبي]
أكبر مشكلة الآن: [وصف مختصر]
الميزانية التقريبية: [أقل من 10k / 10-25k / 25-75k / 75k+]
أريد أبدأ بـ Diagnostic Sprint`;

const channels = [
  {
    icon: "📋",
    title: "استمارة مفصلة",
    desc: "للشركات التي تفضل إرسال المعلومات بشكل منظم قبل المحادثة.",
    action: "اعبّئ الاستمارة",
    style: "border border-white/20 hover:bg-white/10",
    href: "#form",
    external: false,
  },
  {
    icon: "📞",
    title: "مكالمة مباشرة",
    desc: "نحدد موعد قصير (20 دقيقة) نأخذ فيه كل البيانات بشكل تفاعلي.",
    action: "احجز موعد",
    style: "border border-white/20 hover:bg-white/10",
    href: BOOKING_URL,
    external: true,
  },
];

const steps = [
  { num: "1", title: "أرسل البيانات", desc: "عبر أي قناة تفضلها — واتساب أو الاستمارة" },
  { num: "2", title: "نراجع خلال 24 ساعة", desc: "نقرأ المعلومات ونحضر التشخيص المبدئي" },
  { num: "3", title: "نتواصل معك", desc: "نحدد موعد Zoom لعرض التشخيص والخطوات" },
  { num: "4", title: "تبدأ الرحلة", desc: "إذا اتفقنا، نبدأ Sprint الرسمي خلال 24 ساعة" },
];

const requiredFields = [
  { group: "الشركة", fields: ["اسم الشركة", "القطاع", "المدينة", "عدد الموظفين تقريباً"] },
  {
    group: "التشغيل الحالي",
    fields: [
      "من أين تأتي الاستفسارات؟",
      "كم استفسار أسبوعياً تقريباً؟",
      "هل يوجد CRM؟",
      "هل توجد تقارير للإدارة؟",
    ],
  },
  {
    group: "المشكلة والهدف",
    fields: [
      "أكبر مشكلة تشغيلية الآن",
      "هدف 30 يوم",
      "الميزانية التقريبية",
    ],
  },
];

export default function IntakePage() {
  return (
    <main dir="rtl" className="min-h-screen bg-[#06111f] text-white">
      {/* Hero */}
      <section className="mx-auto max-w-5xl px-6 py-20">
        <p className="mb-5 inline-flex rounded-full border border-cyan-300/30 px-4 py-2 text-sm text-cyan-100">
          البداية هنا
        </p>
        <h1 className="text-4xl font-black leading-[1.15] md:text-6xl">
          أرسل بيانات شركتك.
          <br />
          <span className="text-cyan-400">نراجع ونتواصل خلال 24 ساعة.</span>
        </h1>
        <p className="mt-7 max-w-3xl text-xl leading-9 text-slate-300">
          لا التزامات، لا دفع مسبق. فقط محادثة نفهم فيها وضعك ونحدد هل نقدر نساعدك.
        </p>
      </section>

      {/* Channels */}
      <section className="mx-auto max-w-5xl px-6 pb-16">
        <h2 className="text-2xl font-black mb-6">اختر طريقة التواصل</h2>
        <div className="grid gap-4 md:grid-cols-3">
          <div className="flex flex-col rounded-3xl border border-emerald-400/20 bg-emerald-400/[0.04] p-6">
            <p className="text-3xl">💬</p>
            <h3 className="mt-4 text-lg font-black">واتساب مباشر</h3>
            <p className="mt-2 flex-1 text-sm leading-7 text-slate-300">
              الأسرع. تواصل مع المؤسس مباشرة وسنأخذ البيانات خلال محادثة قصيرة.
            </p>
            <WhatsAppCTA
              message={WA_INTAKE_MESSAGE}
              label="راسل على واتساب"
              fallbackSubject="بدء تشخيص مع Dealix"
              className="mt-5 block rounded-2xl bg-emerald-500 px-6 py-3 text-center text-sm font-bold text-white transition-colors hover:bg-emerald-400"
            />
          </div>
          {channels.map((ch) => (
            <div
              key={ch.title}
              className="flex flex-col rounded-3xl border border-white/10 bg-white/[0.03] p-6"
            >
              <p className="text-3xl">{ch.icon}</p>
              <h3 className="mt-4 text-lg font-black">{ch.title}</h3>
              <p className="mt-2 flex-1 text-sm leading-7 text-slate-300">{ch.desc}</p>
              <a
                href={ch.href}
                {...(ch.external
                  ? { target: "_blank", rel: "noopener noreferrer" }
                  : {})}
                className={`mt-5 block rounded-2xl px-6 py-3 text-center text-sm font-bold transition-colors ${ch.style}`}
              >
                {ch.action}
              </a>
            </div>
          ))}
        </div>
      </section>

      {/* What happens next */}
      <section className="border-y border-white/5 bg-white/[0.02] py-16">
        <div className="mx-auto max-w-5xl px-6">
          <h2 className="text-2xl font-black">ماذا يحدث بعد إرسال البيانات؟</h2>
          <div className="mt-8 grid gap-4 md:grid-cols-4">
            {steps.map((s) => (
              <div key={s.num} className="rounded-3xl border border-white/10 bg-white/[0.03] p-5">
                <p className="text-3xl font-black text-cyan-400">{s.num}</p>
                <h3 className="mt-3 font-bold">{s.title}</h3>
                <p className="mt-2 text-sm leading-7 text-slate-400">{s.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Required info */}
      <section className="mx-auto max-w-5xl px-6 py-16">
        <h2 className="text-2xl font-black">ما المعلومات التي نحتاجها؟</h2>
        <p className="mt-3 text-slate-400">
          لا تحتاج تجهيز كل شيء — أرسل ما تعرفه والباقي نحدده في المحادثة.
        </p>
        <div className="mt-8 grid gap-4 md:grid-cols-3">
          {requiredFields.map((group) => (
            <div
              key={group.group}
              className="rounded-3xl border border-white/10 bg-white/[0.03] p-5"
            >
              <h3 className="font-black text-cyan-400">{group.group}</h3>
              <ul className="mt-4 space-y-2">
                {group.fields.map((f) => (
                  <li key={f} className="flex gap-2 text-sm text-slate-300">
                    <span className="text-slate-500">·</span>
                    <span>{f}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="mt-6 rounded-3xl border border-white/10 bg-white/[0.02] p-4 text-sm text-slate-400">
          <span className="font-bold text-emerald-400">ملاحظة: </span>
          لا نطلب بيانات مالية حساسة، عقوداً، أو أي معلومات سرية في هذه المرحلة.
          البيانات تُستخدم فقط للتشخيص المبدئي. PDPL-compliant.
        </div>
      </section>

      {/* Lead form + direct CTA */}
      <section className="border-t border-white/5 bg-white/[0.02] py-16" id="form">
        <div className="mx-auto max-w-3xl px-6 text-center">
          <h2 className="text-3xl font-black">ابدأ الآن</h2>
          <p className="mt-4 text-lg text-slate-300">
            اعبّئ الاستمارة ونتواصل معك خلال 24 ساعة:
          </p>

          <div className="mt-8 rounded-3xl border border-white/10 bg-white/[0.03] p-6 md:p-8 text-right">
            <LeadForm />
          </div>

          <p className="mt-10 text-lg text-slate-300">
            أو أرسل رسالة واتساب بهذه المعلومات:
          </p>

          <div
            className="mt-6 rounded-3xl border border-emerald-400/20 bg-emerald-400/[0.04] p-6 text-right"
            dir="rtl"
          >
            <p className="text-sm font-bold text-emerald-400 mb-4">نسخ وأرسل على واتساب</p>
            <pre className="whitespace-pre-wrap text-sm leading-8 text-slate-300 font-sans">
{WA_INTAKE_MESSAGE}
            </pre>
            <div className="mt-5 text-center">
              <WhatsAppCTA
                message={WA_INTAKE_MESSAGE}
                label="أرسل مباشرة على واتساب"
                fallbackSubject="بدء تشخيص مع Dealix"
                className="inline-block rounded-2xl bg-emerald-500 px-8 py-3 text-sm font-bold text-white hover:bg-emerald-400"
              />
            </div>
          </div>

          <div className="mt-8 flex flex-wrap justify-center gap-4">
            <a
              href="/ar/diagnostic-sprint"
              className="rounded-2xl border border-white/20 px-8 py-4 font-semibold hover:bg-white/10"
            >
              اعرف مخرجات التشخيص
            </a>
            <a
              href="/ar/trust"
              className="rounded-2xl border border-white/20 px-8 py-4 font-semibold hover:bg-white/10"
            >
              كيف نحمي بياناتك؟
            </a>
          </div>
        </div>
      </section>
    </main>
  );
}
