import {
  ArrowLeft,
  BarChart3,
  BrainCircuit,
  MessageSquareMore,
  ShieldCheck,
} from "lucide-react";

const operatingLayers = [
  {
    label: "Revenue Command Room",
    value: "Pipeline + drafts + follow-ups",
  },
  {
    label: "WhatsApp Official Flow",
    value: "Cloud API + approval + webhook",
  },
  {
    label: "Company Brain",
    value: "Signals + decisions + risks",
  },
];

export default function Hero() {
  return (
    <section className="relative overflow-hidden bg-[#0A1F1E] pb-20 pt-32">
      <div className="absolute inset-0 opacity-10">
        <div className="absolute right-20 top-24 h-72 w-72 rounded-full bg-[#15807A] blur-3xl" />
        <div className="absolute bottom-10 left-10 h-96 w-96 rounded-full bg-[#15807A] blur-3xl" />
      </div>

      <div className="relative mx-auto grid max-w-7xl gap-12 px-4 sm:px-6 lg:grid-cols-2 lg:px-8">
        <div>
          <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-[#15807A]/30 bg-[#15807A]/15 px-4 py-2">
            <span className="h-2 w-2 rounded-full bg-[#15807A]" />
            <span className="text-sm text-[#E8F4F3]">
              Founder-led operating system with safety-by-default workflows
            </span>
          </div>

          <h1 className="max-w-3xl text-4xl font-bold leading-tight text-white sm:text-5xl lg:text-6xl">
            Dealix يبني
            <span className="text-[#15807A]"> AI Operating Systems </span>
            للشركات السعودية B2B
          </h1>

          <p className="mt-6 max-w-2xl text-lg leading-8 text-[#B7D2D0]">
            بدل chatbot إضافي أو CRM جديد، Dealix يربط بين الإيرادات،
            WhatsApp، قرارات الإدارة، والحوكمة في نظام تشغيل يومي يمكن
            للمؤسس وفريقه استخدامه بثقة.
          </p>

          <div className="mt-8 flex flex-col gap-4 sm:flex-row">
            <a
              href="/book-call"
              className="inline-flex items-center justify-center gap-2 rounded-xl bg-[#15807A] px-8 py-4 text-lg font-semibold text-white transition-all hover:scale-[1.02] hover:bg-[#0F5F5A]"
            >
              احجز تشخيصًا تشغيليًا
              <ArrowLeft className="h-5 w-5" />
            </a>
            <a
              href="/command-room"
              className="inline-flex items-center justify-center gap-2 rounded-xl border border-[#15807A]/40 px-8 py-4 text-lg font-medium text-[#E8F4F3] transition-colors hover:bg-[#15807A]/10"
            >
              افتح Command Room
            </a>
          </div>

          <div className="mt-10 grid grid-cols-1 gap-4 sm:grid-cols-3">
            <div className="rounded-2xl border border-[#15807A]/15 bg-white/5 p-4">
              <p className="text-2xl font-bold text-white">5 أنظمة</p>
              <p className="mt-1 text-sm text-[#B7D2D0]">
                Revenue + Brain + WhatsApp + Trust + Delivery
              </p>
            </div>
            <div className="rounded-2xl border border-[#15807A]/15 bg-white/5 p-4">
              <p className="text-2xl font-bold text-white">draft_only</p>
              <p className="mt-1 text-sm text-[#B7D2D0]">
                لا إرسال حي افتراضيًا بدون موافقة بشرية
              </p>
            </div>
            <div className="rounded-2xl border border-[#15807A]/15 bg-white/5 p-4">
              <p className="text-2xl font-bold text-white">PDPL-ready</p>
              <p className="mt-1 text-sm text-[#B7D2D0]">
                تقليل بيانات وسجل أحداث ومراجعة بشرية
              </p>
            </div>
          </div>
        </div>

        <div className="hidden lg:block">
          <div className="rounded-3xl border border-[#15807A]/20 bg-[#0F2E2C] p-6 shadow-2xl">
            <div className="mb-5 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="h-3 w-3 rounded-full bg-red-500" />
                <div className="h-3 w-3 rounded-full bg-yellow-500" />
                <div className="h-3 w-3 rounded-full bg-green-500" />
              </div>
              <span className="text-xs font-medium text-[#8CB3B0]">
                Daily Founder View
              </span>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div className="rounded-2xl border border-[#15807A]/10 bg-[#0A1F1E] p-4">
                <div className="mb-3 flex items-center gap-2 text-[#B7D2D0]">
                  <BarChart3 className="h-4 w-4 text-[#15807A]" />
                  <span className="text-sm">Revenue Room</span>
                </div>
                <p className="text-2xl font-bold text-white">12</p>
                <p className="mt-1 text-xs text-[#8CB3B0]">
                  فرص نشطة تحتاج قرارات ومتابعات
                </p>
              </div>

              <div className="rounded-2xl border border-[#15807A]/10 bg-[#0A1F1E] p-4">
                <div className="mb-3 flex items-center gap-2 text-[#B7D2D0]">
                  <MessageSquareMore className="h-4 w-4 text-[#15807A]" />
                  <span className="text-sm">WhatsApp</span>
                </div>
                <p className="text-2xl font-bold text-white">7</p>
                <p className="mt-1 text-xs text-[#8CB3B0]">
                  رسائل pending بانتظار review أو approval
                </p>
              </div>

              <div className="rounded-2xl border border-[#15807A]/10 bg-[#0A1F1E] p-4">
                <div className="mb-3 flex items-center gap-2 text-[#B7D2D0]">
                  <BrainCircuit className="h-4 w-4 text-[#15807A]" />
                  <span className="text-sm">Brain OS</span>
                </div>
                <p className="text-2xl font-bold text-white">5</p>
                <p className="mt-1 text-xs text-[#8CB3B0]">
                  قرارات ومخاطر وفرص تحتاج owner واضح
                </p>
              </div>

              <div className="rounded-2xl border border-[#15807A]/10 bg-[#0A1F1E] p-4">
                <div className="mb-3 flex items-center gap-2 text-[#B7D2D0]">
                  <ShieldCheck className="h-4 w-4 text-[#15807A]" />
                  <span className="text-sm">Trust Layer</span>
                </div>
                <p className="text-2xl font-bold text-white">Safe</p>
                <p className="mt-1 text-xs text-[#8CB3B0]">
                  outbound approvals + audit trail + dry run defaults
                </p>
              </div>
            </div>

            <div className="mt-5 rounded-2xl border border-[#15807A]/10 bg-[#0A1F1E] p-4">
              <p className="mb-3 text-sm font-semibold text-white">
                طبقات التشغيل داخل Dealix
              </p>
              <div className="space-y-3">
                {operatingLayers.map((item) => (
                  <div
                    key={item.label}
                    className="flex items-center justify-between rounded-xl bg-white/5 px-3 py-2"
                  >
                    <span className="text-sm text-white">{item.label}</span>
                    <span className="text-xs text-[#8CB3B0]">{item.value}</span>
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