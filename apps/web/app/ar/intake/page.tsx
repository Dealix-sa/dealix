export const metadata = {
  title: "Dealix Intake — بيانات التشخيص",
  description: "أرسل بيانات شركتك لبدء التشخيص التحولي مع Dealix.",
};

const fields = [
  "اسم الشركة",
  "القطاع",
  "المدينة",
  "عدد الفروع",
  "اسم المسؤول",
  "رقم واتساب",
  "البريد الإلكتروني",
  "الموقع أو حسابات التواصل",
  "مصدر الاستفسارات الحالي",
  "عدد الاستفسارات أسبوعياً",
  "هل يوجد CRM؟",
  "هل توجد تقارير للإدارة؟",
  "أكبر مشكلة تشغيلية",
  "هدف 30 يوم",
  "الميزانية التقريبية",
];

export default function IntakePage() {
  return (
    <main dir="rtl" className="min-h-screen bg-[#06111f] text-white">
      <section className="mx-auto max-w-5xl px-6 py-20">
        <p className="mb-5 inline-flex rounded-full border border-cyan-300/30 px-4 py-2 text-sm text-cyan-100">
          Dealix Intake
        </p>

        <h1 className="text-4xl font-black leading-[1.15] md:text-6xl">
          ابدأ تشخيص شركتك ببيانات واضحة.
        </h1>

        <p className="mt-7 max-w-3xl text-xl leading-9 text-slate-300">
          حتى نبني النظام الصحيح، نحتاج نفهم أين تأتي الاستفسارات، أين تضيع المتابعة،
          هل توجد تقارير، وما أول هدف تريد تحقيقه خلال 30 يوم.
        </p>

        <div className="mt-10 rounded-3xl border border-white/10 bg-white/[0.04] p-6">
          <h2 className="text-2xl font-black">البيانات المطلوبة</h2>
          <div className="mt-6 grid gap-3 md:grid-cols-2">
            {fields.map((field) => (
              <div key={field} className="rounded-2xl border border-white/10 bg-white/[0.04] px-4 py-3">
                {field}
              </div>
            ))}
          </div>
        </div>

        <div className="mt-10 grid gap-4 md:grid-cols-2">
          <a
            href="/ar/diagnostic-sprint"
            className="rounded-2xl bg-cyan-400 px-8 py-4 text-center text-lg font-black text-[#06111f] hover:bg-cyan-300"
          >
            اعرف مخرجات التشخيص
          </a>
          <a
            href="/ar/transformation"
            className="rounded-2xl border border-white/20 px-8 py-4 text-center text-lg font-semibold hover:bg-white/10"
          >
            شاهد أنظمة Dealix
          </a>
        </div>

        <p className="mt-8 text-sm leading-7 text-slate-400">
          يمكن إرسال هذه البيانات عبر واتساب أو نموذج Intake. بعد المراجعة، نحدد هل البداية
          المناسبة Diagnostic Sprint أو نظام تشغيل مباشر.
        </p>
      </section>
    </main>
  );
}
