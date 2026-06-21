import { Brain, Lock, BarChart3, Users, Workflow, MessageSquare } from 'lucide-react';

interface Props {
  lang: 'ar' | 'en';
}

const t = {
  ar: {
    label: 'المميزات',
    title: 'منصة متكاملة لـ',
    titleHighlight: 'نمو أعمالك',
    features: [
      {
        icon: Brain,
        title: 'محرك الإيرادات بالذكاء الاصطناعي',
        desc: 'نظام متكامل يحلل بياناتك ويقدم توصيات ذكية لزيادة الإيرادات وتحسين الأداء',
      },
      {
        icon: Lock,
        title: 'الامتثال لـ PDPL وZATCA',
        desc: 'متوافق بالكامل مع أنظمة حماية البيانات والفوترة الإلكترونية في السعودية',
      },
      {
        icon: BarChart3,
        title: 'تحليلات متقدمة في الوقت الفعلي',
        desc: 'لوحات معلومات تفاعلية تظهر أداء أعمالك مع رؤى قابلة للتنفيذ',
      },
      {
        icon: Users,
        title: 'نظام العملاء والـ CRM',
        desc: 'إدارة العملاء المحتملين والفرص مع تتبع ذكي لرحلة العميل',
      },
      {
        icon: Workflow,
        title: 'أتمتة العمليات التجارية',
        desc: 'أتمتة سير العمل والمهام المتكررة لتوفير الوقت وزيادة الكفاءة',
      },
      {
        icon: MessageSquare,
        title: 'تواصل ذكي متعدد القنوات',
        desc: 'تواصل مع عملائك عبر WhatsApp والبريد والمزيد — كلها من منصة واحدة',
      },
    ],
  },
  en: {
    label: 'Features',
    title: 'All-in-One Platform for',
    titleHighlight: 'Business Growth',
    features: [
      {
        icon: Brain,
        title: 'AI Revenue Engine',
        desc: 'Integrated system that analyzes your data and provides intelligent recommendations to increase revenue',
      },
      {
        icon: Lock,
        title: 'PDPL & ZATCA Compliant',
        desc: 'Fully compliant with Saudi data protection laws and e-invoicing regulations',
      },
      {
        icon: BarChart3,
        title: 'Real-Time Advanced Analytics',
        desc: 'Interactive dashboards showing your business performance with actionable insights',
      },
      {
        icon: Users,
        title: 'CRM & Lead Management',
        desc: 'Smart lead and opportunity management with intelligent customer journey tracking',
      },
      {
        icon: Workflow,
        title: 'Business Process Automation',
        desc: 'Automate workflows and repetitive tasks to save time and increase efficiency',
      },
      {
        icon: MessageSquare,
        title: 'Smart Multi-Channel Communication',
        desc: 'Engage customers via WhatsApp, email, and more — all from one platform',
      },
    ],
  },
};

export default function FeaturesSection({ lang }: Props) {
  const text = t[lang];

  return (
    <section id="features" className="py-24 bg-dealix-warm-white">
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

        {/* Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {text.features.map((feature, i) => {
            const Icon = feature.icon;
            return (
              <div
                key={i}
                className="group p-8 rounded-2xl bg-white border border-gray-100 hover:border-dealix-emerald/30 shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-1"
              >
                <div className="w-14 h-14 rounded-xl bg-dealix-emerald/10 flex items-center justify-center mb-6 group-hover:bg-dealix-emerald group-hover:shadow-glow-emerald transition-all duration-300">
                  <Icon className="w-7 h-7 text-dealix-emerald group-hover:text-white transition-colors" />
                </div>
                <h3 className="text-xl font-display font-bold text-dealix-charcoal mb-3">
                  {feature.title}
                </h3>
                <p className="text-dealix-gray leading-relaxed">{feature.desc}</p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
