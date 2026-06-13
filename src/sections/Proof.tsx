import { TrendingUp, TrendingDown, AlertTriangle } from 'lucide-react'

const stats = [
  {
    icon: TrendingDown,
    value: '37%',
    label: 'من العملاء المحتملين لم يتم متابعتهم بعد أول رد',
    source: 'تحليل Dealix لـ 20 وكالة',
    type: 'negative',
  },
  {
    icon: AlertTriangle,
    value: '4.2 ساعة',
    label: 'متوسط وقت الرد في B2B السعودي',
    source: 'أفضل المعايير: 15 دقيقة',
    type: 'warning',
  },
  {
    icon: TrendingUp,
    value: '15 دقيقة',
    label: 'SLA المتابعة الموصى به بعد أول استفسار',
    source: 'تجربة Dealix مع العملاء',
    type: 'positive',
  },
  {
    icon: TrendingUp,
    value: '80%+',
    label: 'نسبة المتابعة المستهدفة لتحسين التحويل',
    source: 'هندف شهري في نظام P2',
    type: 'positive',
  },
]

const proofExamples = [
  {
    text: 'اكتشفنا أن 37% من العملاء المحتملين لم يتم متابعتهم بعد أول رد. أكبر تسرب كان بين الاستفسار والعرض. التوصية: SLA متابعة خلال أول 15 دقيقة + رسالتين متابعة خلال 72 ساعة.',
    sector: 'وكالة تسويق',
    anonymous: true,
  },
  {
    text: 'شركة التدريب كانت تستقبل 200+ استفسار واتساب شهرياً لكن نسبة التحويل أقل من 10%. بعد تطبيق نظام المتابعة التلقائي، ارتفعت النسبة لـ 28% خلال 30 يوم.',
    sector: 'شركة تدريب',
    anonymous: true,
  },
]

export default function Proof() {
  return (
    <section className="py-20 bg-[#0A1F1E]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <span className="text-[#15807A] text-sm font-semibold tracking-wide uppercase">الأدلة</span>
          <h2 className="text-3xl sm:text-4xl font-bold text-white mt-2 mb-4">
            أرقام تكشف الحقيقة
          </h2>
          <p className="text-[#8CB3B0] text-lg max-w-2xl mx-auto">
            هذه ليست نظريات — هذه أرقام حقيقية من تحليلاتنا لشركات سعودية
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
          {stats.map((stat) => (
            <div
              key={stat.value}
              className="bg-[#0F2E2C] rounded-2xl p-6 border border-[#15807A]/10 hover:border-[#15807A]/30 transition-all"
            >
              <stat.icon className={`w-8 h-8 mb-4 ${
                stat.type === 'negative' ? 'text-red-400' :
                stat.type === 'warning' ? 'text-yellow-400' :
                'text-[#15807A]'
              }`} />
              <div className="text-3xl font-bold text-white mb-2">{stat.value}</div>
              <div className="text-[#E8F4F3] text-sm mb-2">{stat.label}</div>
              <div className="text-[#8CB3B0] text-xs">{stat.source}</div>
            </div>
          ))}
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {proofExamples.map((example, index) => (
            <div
              key={index}
              className="bg-[#0F2E2C] rounded-2xl p-6 border border-[#15807A]/10"
            >
              <div className="flex items-center gap-2 mb-4">
                <span className="bg-[#15807A]/20 text-[#15807A] text-xs font-bold px-2 py-1 rounded">
                  {example.sector}
                </span>
                {example.anonymous && (
                  <span className="bg-[#1A1A1A] text-[#8CB3B0] text-xs px-2 py-1 rounded">
                    مجهول
                  </span>
                )}
              </div>
              <p className="text-[#E8F4F3] leading-relaxed">{example.text}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
