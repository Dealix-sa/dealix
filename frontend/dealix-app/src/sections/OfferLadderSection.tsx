import { Check, Star, Crown, Gem, Building } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface Props {
  lang: 'ar' | 'en';
}

const t = {
  ar: {
    label: 'الأسعار',
    title: 'سلم عروض',
    titleHighlight: 'Dealix',
    tiers: [
      {
        icon: Star,
        name: 'التشخيص المجاني',
        price: '0',
        period: 'ريال',
        desc: 'تقييم 30 نقطة + تقرير AI',
        features: ['تشخيص شامل لأعمالك', 'تقرير AI مفصل', 'تحديد فرص النمو', '30 دقيقة استشارة'],
        cta: 'ابدأ التشخيص',
        featured: false,
      },
      {
        icon: Gem,
        name: 'البايلوت المدفوع',
        price: '2,500',
        period: 'ريال',
        desc: '7 أيام تنفيذ + تقرير أسبوعي',
        features: ['كل ما في التشخيص', '7 أيام بايلوت كامل', 'تقرير أسبوعي', 'دعم مخصص', 'ضمان استرداد 14 يوم'],
        cta: 'ابدأ البايلوت',
        featured: true,
      },
      {
        icon: Crown,
        name: 'غرفة القيادة',
        price: '4,900',
        period: 'ريال/شهر',
        desc: 'منصة Dealix كاملة + دعم',
        features: ['كل ما في البايلوت', 'منصة كاملة', 'دعم شهري مستمر', 'تحديثات مجانية', 'تقارير متقدمة', 'API كامل'],
        cta: 'اشترك الآن',
        featured: false,
      },
      {
        icon: Building,
        name: 'المؤسسي',
        price: 'مخصص',
        period: '',
        desc: 'أنظمة مخصصة للمؤسسات',
        features: ['كل ما في غرفة القيادة', 'تطوير مخصص', 'تكامل كامل', 'دعم مؤسسي 24/7', 'SLA مضمون', 'مدير حساب مخصص'],
        cta: 'تواصل معنا',
        featured: false,
      },
    ],
  },
  en: {
    label: 'Pricing',
    title: 'Dealix',
    titleHighlight: 'Offer Ladder',
    tiers: [
      {
        icon: Star,
        name: 'Free Diagnostic',
        price: '0',
        period: 'SAR',
        desc: '30-point assessment + AI report',
        features: ['Comprehensive business diagnosis', 'Detailed AI report', 'Growth opportunity identification', '30-minute consultation'],
        cta: 'Start Diagnostic',
        featured: false,
      },
      {
        icon: Gem,
        name: 'Paid Pilot',
        price: '2,500',
        period: 'SAR',
        desc: '7-day execution + weekly report',
        features: ['Everything in Diagnostic', 'Full 7-day pilot', 'Weekly report', 'Dedicated support', '14-day refund guarantee'],
        cta: 'Start Pilot',
        featured: true,
      },
      {
        icon: Crown,
        name: 'Command Center',
        price: '4,900',
        period: 'SAR/month',
        desc: 'Full Dealix platform + support',
        features: ['Everything in Pilot', 'Full platform access', 'Monthly continuous support', 'Free updates', 'Advanced reports', 'Full API access'],
        cta: 'Subscribe Now',
        featured: false,
      },
      {
        icon: Building,
        name: 'Enterprise',
        price: 'Custom',
        period: '',
        desc: 'Custom systems for enterprises',
        features: ['Everything in Command Center', 'Custom development', 'Full integration', '24/7 enterprise support', 'Guaranteed SLA', 'Dedicated account manager'],
        cta: 'Contact Us',
        featured: false,
      },
    ],
  },
};

export default function OfferLadderSection({ lang }: Props) {
  const text = t[lang];

  return (
    <section id="pricing" className="py-24 bg-dealix-warm-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <span className="inline-block px-4 py-1.5 text-sm font-medium text-dealix-emerald bg-dealix-emerald/10 rounded-full mb-4">
            {text.label}
          </span>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-display font-bold text-dealix-charcoal">
            {text.title} <span className="text-dealix-emerald">{text.titleHighlight}</span>
          </h2>
        </div>

        {/* Tiers */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {text.tiers.map((tier, i) => {
            const Icon = tier.icon;
            return (
              <div
                key={i}
                className={`relative rounded-2xl p-6 transition-all hover:-translate-y-1 ${
                  tier.featured
                    ? 'bg-dealix-charcoal text-white shadow-2xl scale-105 lg:scale-110 border-2 border-dealix-gold'
                    : 'bg-white border border-gray-100 hover:border-dealix-emerald/30 shadow-sm hover:shadow-lg'
                }`}
              >
                {/* Featured badge */}
                {tier.featured && (
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-4 py-1 bg-gold-gradient text-dealix-charcoal text-xs font-bold rounded-full">
                    {lang === 'ar' ? 'الأكثر شيوعاً' : 'Most Popular'}
                  </div>
                )}

                {/* Icon */}
                <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-4 ${
                  tier.featured ? 'bg-dealix-gold/20' : 'bg-dealix-emerald/10'
                }`}>
                  <Icon className={`w-6 h-6 ${tier.featured ? 'text-dealix-gold' : 'text-dealix-emerald'}`} />
                </div>

                {/* Name */}
                <h3 className={`text-lg font-display font-bold mb-1 ${
                  tier.featured ? 'text-white' : 'text-dealix-charcoal'
                }`}>
                  {tier.name}
                </h3>

                {/* Price */}
                <div className="mb-3">
                  <span className={`text-3xl font-display font-bold ${
                    tier.featured ? 'text-dealix-gold' : 'text-dealix-emerald'
                  }`}>
                    {tier.price}
                  </span>
                  {tier.period && (
                    <span className={`text-sm ml-1 ${
                      tier.featured ? 'text-white/60' : 'text-dealix-gray'
                    }`}>
                      {tier.period}
                    </span>
                  )}
                </div>

                {/* Desc */}
                <p className={`text-sm mb-4 ${tier.featured ? 'text-white/60' : 'text-dealix-gray'}`}>
                  {tier.desc}
                </p>

                {/* Features */}
                <ul className="space-y-2 mb-6">
                  {tier.features.map((feature, j) => (
                    <li key={j} className="flex items-start gap-2 text-sm">
                      <Check className={`w-4 h-4 mt-0.5 shrink-0 ${
                        tier.featured ? 'text-dealix-gold' : 'text-dealix-emerald'
                      }`} />
                      <span className={tier.featured ? 'text-white/80' : 'text-dealix-charcoal'}>
                        {feature}
                      </span>
                    </li>
                  ))}
                </ul>

                {/* CTA */}
                <Button
                  className={`w-full ${
                    tier.featured
                      ? 'bg-gold-gradient text-dealix-charcoal hover:opacity-90'
                      : 'bg-dealix-emerald hover:bg-dealix-forest text-white'
                  }`}
                >
                  {tier.cta}
                </Button>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
