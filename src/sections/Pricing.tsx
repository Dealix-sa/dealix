import { CheckCircle2, Star } from "lucide-react";

const plans = [
  {
    name: "Diagnostic Sprint",
    price: "5,000",
    period: "مرة واحدة",
    description:
      "تشخيص تشغيلي وتجاري خلال أيام قليلة لفهم أين تتعطل المتابعة وأين تتسرب الفرص.",
    features: [
      "Revenue leakage map",
      "Booking and follow-up audit",
      "Founder action plan",
      "WhatsApp workflow recommendations",
      "Decision and risk summary",
    ],
    highlighted: false,
  },
  {
    name: "Command Room Build",
    price: "15,000",
    period: "تنفيذ تأسيسي",
    description:
      "بناء الأساس التشغيلي: Command Room + Booking + WhatsApp drafts + Brain ledgers.",
    features: [
      "Revenue command room setup",
      "Approval workflow",
      "Official WhatsApp integration path",
      "Founder dashboard and reports",
      "Safety defaults enabled",
    ],
    highlighted: true,
  },
  {
    name: "Monthly Operating Partner",
    price: "8,000+",
    period: "شهريًا",
    description:
      "تشغيل مستمر للمؤسس والفريق: مراجعة أسبوعية، تحسين الرسائل، وتحديث القرارات والمخاطر.",
    features: [
      "Weekly operating review",
      "Draft and approval cadence",
      "Ongoing optimization",
      "Proof packs and scorecards",
      "Governance and compliance review",
    ],
    highlighted: false,
  },
];

export default function Pricing() {
  return (
    <section id="pricing" className="bg-[#F0F9F8] py-20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mx-auto mb-16 max-w-3xl text-center">
          <span className="text-sm font-semibold uppercase tracking-wide text-[#15807A]">
            Pricing
          </span>
          <h2 className="mt-2 text-3xl font-bold text-[#0A1F1E] sm:text-4xl">
            تسعير مبني على التنفيذ لا على الوعود
          </h2>
          <p className="mt-4 text-lg leading-8 text-[#4A6B69]">
            نبدأ بتشخيص أو بناء تأسيسي، ثم ننتقل إلى تشغيل شهري إذا كان هناك
            fit واضح. لا إرسال حي افتراضيًا، ولا ادعاءات ROI غير مثبتة.
          </p>
        </div>

        <div className="grid gap-6 lg:grid-cols-3">
          {plans.map((plan) => (
            <div
              key={plan.name}
              className={`relative rounded-3xl p-6 ${
                plan.highlighted
                  ? "scale-[1.02] bg-[#0A1F1E] text-white shadow-xl"
                  : "border border-[#E8F4F3] bg-white"
              }`}
            >
              {plan.highlighted && (
                <div className="absolute -top-3 right-5 flex items-center gap-1 rounded-full bg-[#15807A] px-3 py-1 text-xs font-bold text-white">
                  <Star className="h-3 w-3" />
                  المسار الأنسب لمعظم العملاء
                </div>
              )}

              <div className="mb-5">
                <h3
                  className={`text-xl font-bold ${
                    plan.highlighted ? "text-white" : "text-[#0A1F1E]"
                  }`}
                >
                  {plan.name}
                </h3>
                <p
                  className={`mt-2 text-sm leading-7 ${
                    plan.highlighted ? "text-[#B7D2D0]" : "text-[#4A6B69]"
                  }`}
                >
                  {plan.description}
                </p>
              </div>

              <div className="mb-6">
                <div className="flex items-end gap-2">
                  <span
                    className={`text-4xl font-bold ${
                      plan.highlighted ? "text-white" : "text-[#0A1F1E]"
                    }`}
                  >
                    {plan.price}
                  </span>
                  <span
                    className={`pb-1 text-sm ${
                      plan.highlighted ? "text-[#B7D2D0]" : "text-[#4A6B69]"
                    }`}
                  >
                    ر.س
                  </span>
                </div>
                <p
                  className={`mt-1 text-sm ${
                    plan.highlighted ? "text-[#B7D2D0]" : "text-[#4A6B69]"
                  }`}
                >
                  {plan.period}
                </p>
              </div>

              <ul className="mb-6 space-y-3">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-start gap-2">
                    <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-[#15807A]" />
                    <span
                      className={`text-sm ${
                        plan.highlighted ? "text-[#E8F4F3]" : "text-[#4A6B69]"
                      }`}
                    >
                      {feature}
                    </span>
                  </li>
                ))}
              </ul>

              <a
                href="/book-call"
                className={`inline-flex w-full items-center justify-center rounded-xl py-3 text-sm font-semibold transition-colors ${
                  plan.highlighted
                    ? "bg-[#15807A] text-white hover:bg-[#0F5F5A]"
                    : "border border-[#15807A] text-[#15807A] hover:bg-[#15807A] hover:text-white"
                }`}
              >
                احجز مكالمة مناسبة لهذا المسار
              </a>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}