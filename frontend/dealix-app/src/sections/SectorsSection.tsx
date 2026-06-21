import { Building2, HeartPulse, ShoppingCart, Cpu, Factory, Plane } from 'lucide-react';

interface Props {
  lang: 'ar' | 'en';
}

const t = {
  ar: {
    label: 'القطاعات المستهدفة',
    title: 'حلول مخصصة لـ',
    titleHighlight: 'كل قطاع',
    desc: 'نقدم حلولاً مخصصة تلبي احتياجات كل قطاع في السوق السعودي',
    cta: 'اطلب عرض استهدافي',
    sectors: [
      { icon: Building2, name: 'العقارات والمقاولات', desc: 'إدارة المشاريع، مبيعات الوحدات، تحليل السوق العقاري' },
      { icon: HeartPulse, name: 'الرعاية الصحية', desc: 'إدارة المرضى، المواعيد، التأمين، والامتثال الصحي' },
      { icon: ShoppingCart, name: 'التجارة والتجزئة', desc: 'إدارة المخزون، تجربة العملاء، التحليلات التنبؤية' },
      { icon: Cpu, name: 'التقنية والبرمجيات', desc: 'إدارة المشاريع التقنية، اشتراكات SaaS، دعم العملاء' },
      { icon: Factory, name: 'الصناعة والتصنيع', desc: 'سلاسل الإمداد، الجودة، التخطيط الإنتاجي' },
      { icon: Plane, name: 'السياحة والضيافة', desc: 'إدارة الحجوزات، تجربة الزوار، التسويق الذكي' },
    ],
  },
  en: {
    label: 'Target Sectors',
    title: 'Tailored Solutions for',
    titleHighlight: 'Every Sector',
    desc: 'We offer customized solutions that meet the needs of every sector in the Saudi market',
    cta: 'Request Sector Pitch',
    sectors: [
      { icon: Building2, name: 'Real Estate & Construction', desc: 'Project management, unit sales, real estate market analysis' },
      { icon: HeartPulse, name: 'Healthcare', desc: 'Patient management, appointments, insurance, health compliance' },
      { icon: ShoppingCart, name: 'Retail & Commerce', desc: 'Inventory management, customer experience, predictive analytics' },
      { icon: Cpu, name: 'Technology & Software', desc: 'Tech project management, SaaS subscriptions, customer support' },
      { icon: Factory, name: 'Manufacturing', desc: 'Supply chains, quality control, production planning' },
      { icon: Plane, name: 'Tourism & Hospitality', desc: 'Booking management, visitor experience, smart marketing' },
    ],
  },
};

export default function SectorsSection({ lang }: Props) {
  const text = t[lang];

  return (
    <section id="sectors" className="py-24 bg-dealix-cream relative overflow-hidden">
      {/* Decorative */}
      <div className="absolute top-0 right-0 w-96 h-96 bg-dealix-emerald/5 rounded-full -translate-y-1/2 translate-x-1/2" />
      <div className="absolute bottom-0 left-0 w-64 h-64 bg-dealix-gold/5 rounded-full translate-y-1/2 -translate-x-1/2" />

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <span className="inline-block px-4 py-1.5 text-sm font-medium text-dealix-gold bg-dealix-gold/10 rounded-full mb-4">
            {text.label}
          </span>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-display font-bold text-dealix-charcoal mb-4">
            {text.title} <span className="text-dealix-emerald">{text.titleHighlight}</span>
          </h2>
          <p className="max-w-2xl mx-auto text-lg text-dealix-gray">{text.desc}</p>
        </div>

        {/* Sectors Grid */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {text.sectors.map((sector, i) => {
            const Icon = sector.icon;
            return (
              <div
                key={i}
                className="group relative p-6 rounded-xl bg-white border border-gray-100 hover:border-dealix-emerald/30 shadow-sm hover:shadow-lg transition-all duration-300 cursor-pointer overflow-hidden"
              >
                {/* Hover accent */}
                <div className="absolute top-0 left-0 w-1 h-full bg-dealix-emerald scale-y-0 group-hover:scale-y-100 transition-transform duration-300 origin-top" />

                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 rounded-lg bg-dealix-emerald/10 flex items-center justify-center shrink-0 group-hover:bg-dealix-emerald transition-colors">
                    <Icon className="w-6 h-6 text-dealix-emerald group-hover:text-white transition-colors" />
                  </div>
                  <div>
                    <h3 className="text-lg font-display font-bold text-dealix-charcoal mb-1 group-hover:text-dealix-emerald transition-colors">
                      {sector.name}
                    </h3>
                    <p className="text-sm text-dealix-gray leading-relaxed">{sector.desc}</p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
