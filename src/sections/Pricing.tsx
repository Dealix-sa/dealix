import { CheckCircle2, Star } from 'lucide-react'

const plans = [
  {
    name: 'P1 — Revenue Intelligence Sprint',
    price: '2,500',
    originalPrice: '5,000',
    period: 'لمرة واحدة',
    description: 'اكتشاف سريع لوين تضيع فرصك + خطة 30 يوم',
    features: [
      'Revenue Leakage Map',
      'Lead Response Audit',
      'Follow-up Gap Report',
      'Offer Quality Review',
      'Objection Map',
      '30-Day Revenue Plan',
      'CEO Brief',
      'P2 Upgrade Proposal',
    ],
    cta: 'ابدأ الآن',
    highlighted: true,
  },
  {
    name: 'P2 Small — AI Sales Ops',
    price: '3,000',
    period: '/شهر',
    description: 'تشغيل أسبوعي للفرق الصغيرة',
    features: [
      'Weekly War Room',
      'Pipeline tracking',
      'Message optimization',
      'Monthly CEO report',
      'SLA review',
      'Team training (2 hrs/month)',
    ],
    cta: 'تواصل معنا',
    highlighted: false,
  },
  {
    name: 'P2 Medium — AI Sales Ops',
    price: '8,000',
    period: '/شهر',
    description: 'تشغيل كامل للفرق المتوسطة',
    features: [
      'Weekly War Room',
      'Pipeline tracking + optimization',
      'Message optimization + A/B testing',
      'Objection Intelligence',
      'Weekly team training',
      'Monthly CEO report + ROI review',
      'Proof Pack generation',
    ],
    cta: 'تواصل معنا',
    highlighted: false,
  },
  {
    name: 'P2 Enterprise',
    price: '20,000',
    period: '/شهر',
    description: 'نظام كامل للمؤسسات الكبيرة',
    features: [
      'Daily War Room support',
      'Full Revenue OS implementation',
      'Custom AI governance setup',
      'Dedicated success manager',
      'Unlimited team training',
      'Weekly executive briefing',
      'Quarterly business review',
      'Priority support',
    ],
    cta: 'تواصل معنا',
    highlighted: false,
  },
]

export default function Pricing() {
  return (
    <section id="pricing" className="py-20 bg-[#F0F9F8]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <span className="text-[#15807A] text-sm font-semibold tracking-wide uppercase">الأسعار</span>
          <h2 className="text-3xl sm:text-4xl font-bold text-[#0A1F1E] mt-2 mb-4">
            ابدأ بالـ Sprint وانتقل للتشغيل الشهري
          </h2>
          <p className="text-[#4A6B69] text-lg max-w-2xl mx-auto">
            لا يوجد التزام طويل — ابدأ بـ Sprint 5 أيام وإذا أعجبتك النتيجة، ننتقل للتشغيل المستمر
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {plans.map((plan) => (
            <div
              key={plan.name}
              className={`relative rounded-2xl p-6 ${
                plan.highlighted
                  ? 'bg-[#0A1F1E] text-white shadow-xl scale-105 lg:scale-110'
                  : 'bg-white border border-[#E8F4F3]'
              }`}
            >
              {plan.highlighted && (
                <div className="absolute -top-3 right-4 bg-[#15807A] text-white text-xs font-bold px-3 py-1 rounded-full flex items-center gap-1">
                  <Star className="w-3 h-3" />
                  الأكثر طلباً
                </div>
              )}

              <div className="mb-4">
                <h3 className={`text-lg font-bold ${plan.highlighted ? 'text-white' : 'text-[#0A1F1E]'}`}>
                  {plan.name}
                </h3>
                <p className={`text-sm mt-1 ${plan.highlighted ? 'text-[#8CB3B0]' : 'text-[#4A6B69]'}`}>
                  {plan.description}
                </p>
              </div>

              <div className="mb-6">
                <div className="flex items-baseline gap-2">
                  <span className={`text-3xl font-bold ${plan.highlighted ? 'text-white' : 'text-[#0A1F1E]'}`}>
                    {plan.price}
                  </span>
                  <span className={`text-sm ${plan.highlighted ? 'text-[#8CB3B0]' : 'text-[#4A6B69]'}`}>
                    ر.س
                  </span>
                  {plan.originalPrice && (
                    <span className={`text-sm line-through ${plan.highlighted ? 'text-[#8CB3B0]' : 'text-[#8CB3B0]'}`}>
                      {plan.originalPrice}
                    </span>
                  )}
                </div>
                <span className={`text-sm ${plan.highlighted ? 'text-[#8CB3B0]' : 'text-[#4A6B69]'}`}>
                  {plan.period}
                </span>
              </div>

              <ul className="space-y-2 mb-6">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-start gap-2">
                    <CheckCircle2 className={`w-4 h-4 shrink-0 mt-0.5 ${plan.highlighted ? 'text-[#15807A]' : 'text-[#15807A]'}`} />
                    <span className={`text-sm ${plan.highlighted ? 'text-[#E8F4F3]' : 'text-[#4A6B69]'}`}>
                      {feature}
                    </span>
                  </li>
                ))}
              </ul>

              <button
                className={`w-full py-3 rounded-xl font-semibold text-sm transition-all ${
                  plan.highlighted
                    ? 'bg-[#15807A] text-white hover:bg-[#0F5F5A]'
                    : 'border border-[#15807A] text-[#15807A] hover:bg-[#15807A] hover:text-white'
                }`}
              >
                {plan.cta}
              </button>
            </div>
          ))}
        </div>

        <div className="mt-12 text-center">
          <p className="text-[#4A6B69] text-sm">
            الأسعار الأولية — تخفيض 50% للـ Sprint للعملاء الأوائل
          </p>
        </div>
      </div>
    </section>
  )
}
