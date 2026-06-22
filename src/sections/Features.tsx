import {
  BarChart3,
  Brain,
  FileCheck,
  MessageSquareMore,
  Shield,
} from "lucide-react";

const systems = [
  {
    icon: BarChart3,
    title: "Revenue Command Room OS",
    description:
      "لوحة يومية تعرض pipeline، الـ drafts، المتابعات المتأخرة، والقرارات التي يجب أن يتخذها المؤسس اليوم.",
    bullets: ["pipeline health", "approval queue", "founder actions"],
  },
  {
    icon: MessageSquareMore,
    title: "WhatsApp Follow-up OS",
    description:
      "قناة WhatsApp رسمية عبر Cloud API مع templates، webhooks، inbox، وحالة إرسال قابلة للتتبع.",
    bullets: ["official API", "draft_only default", "status lifecycle"],
  },
  {
    icon: Brain,
    title: "Company Brain OS",
    description:
      "طبقة قرار تشغيلي تجمع signals، decisions، risks، وopportunities داخل نظام واحد واضح.",
    bullets: ["signals", "decision discipline", "risk register"],
  },
  {
    icon: Shield,
    title: "AI Trust & Compliance OS",
    description:
      "ضوابط AI قابلة للبيع للمؤسسات: human review، تقليل بيانات، سجلات تشغيل، ووثائق امتثال قابلة للمراجعة.",
    bullets: ["PDPL-aware", "manual approval", "audit-friendly"],
  },
  {
    icon: FileCheck,
    title: "Client Delivery OS",
    description:
      "من intake إلى diagnosis إلى blueprint ثم proof pack، بحيث يتحول كل عميل إلى مسار تسليم متكرر وواضح.",
    bullets: ["intake", "blueprint", "proof pack"],
  },
];

export default function Features() {
  return (
    <section id="systems" className="bg-white py-20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mx-auto mb-16 max-w-3xl text-center">
          <span className="text-sm font-semibold uppercase tracking-wide text-[#15807A]">
            Core Systems
          </span>
          <h2 className="mt-2 text-3xl font-bold text-[#0A1F1E] sm:text-4xl">
            خمسة أنظمة تشغيل بدل أداة واحدة معزولة
          </h2>
          <p className="mt-4 text-lg leading-8 text-[#4A6B69]">
            Dealix لا يضيف طبقة شكلية فوق عملك الحالي. هو يعيد تنظيم التشغيل
            التجاري والتشغيلي حتى تصبح المبيعات، المتابعة، القرار، والحوكمة
            ضمن نظام يومي واحد.
          </p>
        </div>

        <div className="grid gap-8 md:grid-cols-2 xl:grid-cols-5">
          {systems.map((system) => (
            <div
              key={system.title}
              className="rounded-3xl border border-[#E8F4F3] bg-white p-6 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:border-[#15807A]/30 hover:shadow-lg"
            >
              <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-2xl bg-[#E8F4F3]">
                <system.icon className="h-6 w-6 text-[#15807A]" />
              </div>

              <h3 className="text-lg font-bold text-[#0A1F1E]">
                {system.title}
              </h3>
              <p className="mt-3 min-h-[96px] text-sm leading-7 text-[#4A6B69]">
                {system.description}
              </p>

              <div className="mt-5 flex flex-wrap gap-2">
                {system.bullets.map((bullet) => (
                  <span
                    key={bullet}
                    className="rounded-full bg-[#F0F9F8] px-3 py-1 text-xs text-[#15807A]"
                  >
                    {bullet}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}