import { Search, FlaskConical, FileCheck, Rocket } from 'lucide-react';

interface Props {
  lang: 'ar' | 'en';
}

const t = {
  ar: {
    label: 'كيف يعمل',
    title: 'رحلة التحول في',
    titleHighlight: '4 خطوات',
    steps: [
      {
        icon: Search,
        num: '01',
        title: 'التشخيص المجاني',
        desc: 'نحلل أعمالك الحالية ونحدد فرص النمو والتحسين خلال 30 دقيقة',
        color: 'bg-dealix-emerald',
      },
      {
        icon: FlaskConical,
        num: '02',
        title: 'البايلوت المدفوع',
        desc: 'اختبار المنصة على أرض الواقع لمدة 7 أيام مع تقارير أسبوعية',
        color: 'bg-dealix-gold',
      },
      {
        icon: FileCheck,
        num: '03',
        title: 'غرفة القيادة',
        desc: 'الاشتراك الشهري الكامل مع الدعم المستمر والتحديثات',
        color: 'bg-dealix-emerald',
      },
      {
        icon: Rocket,
        num: '04',
        title: 'التوسع والنمو',
        desc: 'أنظمة مخصصة ومؤسسية حسب احتياجات عملك المتنامية',
        color: 'bg-dealix-gold',
      },
    ],
  },
  en: {
    label: 'How It Works',
    title: 'Your Transformation Journey in',
    titleHighlight: '4 Steps',
    steps: [
      {
        icon: Search,
        num: '01',
        title: 'Free Diagnostic',
        desc: 'We analyze your current business and identify growth opportunities in 30 minutes',
        color: 'bg-dealix-emerald',
      },
      {
        icon: FlaskConical,
        num: '02',
        title: 'Paid Pilot',
        desc: 'Test the platform in the real world for 7 days with weekly reports',
        color: 'bg-dealix-gold',
      },
      {
        icon: FileCheck,
        num: '03',
        title: 'Command Center',
        desc: 'Full monthly subscription with continuous support and updates',
        color: 'bg-dealix-emerald',
      },
      {
        icon: Rocket,
        num: '04',
        title: 'Scale & Grow',
        desc: 'Custom enterprise systems tailored to your growing business needs',
        color: 'bg-dealix-gold',
      },
    ],
  },
};

export default function HowItWorksSection({ lang }: Props) {
  const text = t[lang];

  return (
    <section id="howitworks" className="py-24 bg-dealix-charcoal relative overflow-hidden">
      {/* Background image */}
      <div className="absolute inset-0 opacity-10">
        <img src="/brand/ai-analytics-visual.jpg" alt="" className="w-full h-full object-cover" />
      </div>
      <div className="absolute inset-0 bg-gradient-to-b from-dealix-charcoal via-dealix-charcoal/95 to-dealix-charcoal" />

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <span className="inline-block px-4 py-1.5 text-sm font-medium text-dealix-gold bg-dealix-gold/10 rounded-full mb-4">
            {text.label}
          </span>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-display font-bold text-white">
            {text.title} <span className="text-gradient-gold">{text.titleHighlight}</span>
          </h2>
        </div>

        {/* Steps */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {text.steps.map((step, i) => {
            const Icon = step.icon;
            return (
              <div key={i} className="relative">
                {/* Connector line */}
                {i < 3 && (
                  <div className="hidden lg:block absolute top-10 left-full w-full h-0.5 bg-gradient-to-r from-dealix-gold/50 to-dealix-emerald/50 z-0" />
                )}

                <div className="relative z-10 p-6 rounded-xl bg-white/5 backdrop-blur-sm border border-white/10 hover:border-dealix-gold/30 transition-all text-center">
                  {/* Number badge */}
                  <div className={`inline-flex items-center justify-center w-14 h-14 rounded-xl ${step.color} mb-4 shadow-lg`}>
                    <Icon className="w-7 h-7 text-white" />
                  </div>

                  <div className="text-4xl font-display font-bold text-dealix-gold/20 mb-2">
                    {step.num}
                  </div>

                  <h3 className="text-lg font-display font-bold text-white mb-2">
                    {step.title}
                  </h3>
                  <p className="text-sm text-white/60 leading-relaxed">{step.desc}</p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
