import { ArrowLeft, MessageCircle, Phone } from "lucide-react";

const sessionAgenda = [
  "فهم نموذج الإيرادات الحالي ومسار الحجز أو المتابعة",
  "تحديد أين يتعطل العمل بين lead وreply وmeeting وproposal",
  "تقدير المسار الأنسب: Sprint أو Build أو Monthly Operating Partner",
  "توضيح حدود البيانات، الحوكمة، وقنوات الإرسال الرسمية",
];

export default function CTA() {
  return (
    <section id="cta" className="bg-[#F0F9F8] py-20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="relative overflow-hidden rounded-3xl bg-[#0A1F1E] p-8 sm:p-12 lg:p-16">
          <div className="absolute -left-10 -top-10 h-64 w-64 rounded-full bg-[#15807A] opacity-10 blur-3xl" />
          <div className="absolute -bottom-16 -right-8 h-80 w-80 rounded-full bg-[#15807A] opacity-10 blur-3xl" />

          <div className="relative grid items-center gap-12 lg:grid-cols-2">
            <div>
              <h2 className="text-3xl font-bold text-white sm:text-4xl">
                إذا كان لديك leads ومحادثات وقرارات متأخرة،
                <br />
                فهذه هي المكالمة الصحيحة للبدء.
              </h2>
              <p className="mt-5 text-lg leading-8 text-[#B7D2D0]">
                مكالمة تشخيص قصيرة نحدد فيها ما إذا كان Dealix مناسبًا
                لمرحلتك الحالية، وما هو النظام الذي يجب بناؤه أولًا داخل الشركة.
              </p>

              <div className="mt-8 flex flex-col gap-4 sm:flex-row">
                <a
                  href="/book-call"
                  className="inline-flex items-center justify-center gap-2 rounded-xl bg-[#15807A] px-8 py-4 text-lg font-semibold text-white transition-colors hover:bg-[#0F5F5A]"
                >
                  <Phone className="h-5 w-5" />
                  احجز مكالمة التشخيص
                  <ArrowLeft className="h-5 w-5" />
                </a>
                <a
                  href="/command-room"
                  className="inline-flex items-center justify-center gap-2 rounded-xl border border-[#15807A]/40 px-8 py-4 text-lg font-medium text-[#E8F4F3] transition-colors hover:bg-[#15807A]/10"
                >
                  <MessageCircle className="h-5 w-5" />
                  شاهد الواجهة التشغيلية
                </a>
              </div>

              <div className="mt-8 flex flex-wrap gap-3 text-sm text-[#B7D2D0]">
                <span className="rounded-full bg-white/5 px-4 py-2">
                  بدون التزام طويل
                </span>
                <span className="rounded-full bg-white/5 px-4 py-2">
                  بدون live send افتراضي
                </span>
                <span className="rounded-full bg-white/5 px-4 py-2">
                  مناسب للمؤسس أو الفريق التجاري
                </span>
              </div>
            </div>

            <div className="rounded-3xl border border-[#15807A]/20 bg-[#0F2E2C] p-6">
              <h3 className="text-xl font-bold text-white">
                ماذا سنغطي في الجلسة؟
              </h3>
              <div className="mt-5 space-y-3">
                {sessionAgenda.map((item, index) => (
                  <div
                    key={item}
                    className="flex items-start gap-3 rounded-2xl bg-white/5 p-3"
                  >
                    <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-[#15807A]/20 text-sm font-bold text-[#15807A]">
                      {index + 1}
                    </div>
                    <p className="text-sm leading-7 text-[#E8F4F3]">{item}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}