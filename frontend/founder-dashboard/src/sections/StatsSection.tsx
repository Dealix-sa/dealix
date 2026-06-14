import { TrendingUp, Shield, Zap, Globe } from 'lucide-react';

interface Props {
  lang: 'ar' | 'en';
}

const t = {
  ar: {
    stats: [
      { icon: TrendingUp, value: '2,587', label: 'ملف بايثون', desc: 'بنية برمجية متكاملة' },
      { icon: Shield, value: '60', label: 'خط CI/CD', desc: 'تكامل ونشر مستمر' },
      { icon: Zap, value: '172', label: 'نقطة API', desc: 'واجهات برمجية شاملة' },
      { icon: Globe, value: '563', label: 'اختبار', desc: 'تغطية شاملة للجودة' },
    ],
  },
  en: {
    stats: [
      { icon: TrendingUp, value: '2,587', label: 'Python Files', desc: 'Integrated codebase' },
      { icon: Shield, value: '60', label: 'CI/CD Lines', desc: 'Continuous integration' },
      { icon: Zap, value: '172', label: 'API Endpoints', desc: 'Comprehensive interfaces' },
      { icon: Globe, value: '563', label: 'Tests', desc: 'Full quality coverage' },
    ],
  },
};

export default function StatsSection({ lang }: Props) {
  const text = t[lang];

  return (
    <section className="relative py-16 bg-dealix-charcoal overflow-hidden">
      {/* Decorative pattern */}
      <div className="absolute inset-0 opacity-5">
        <img src="/brand/pattern-dark.jpg" alt="" className="w-full h-full object-cover" />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
          {text.stats.map((stat, i) => {
            const Icon = stat.icon;
            return (
              <div
                key={i}
                className="text-center p-6 rounded-xl bg-white/5 backdrop-blur-sm border border-white/10 hover:border-dealix-gold/30 transition-all hover:-translate-y-1"
              >
                <Icon className="w-8 h-8 text-dealix-gold mx-auto mb-4" />
                <div className="text-3xl sm:text-4xl font-display font-bold text-white mb-1">
                  {stat.value}
                </div>
                <div className="text-sm font-medium text-dealix-light-gold mb-1">
                  {stat.label}
                </div>
                <div className="text-xs text-white/40">{stat.desc}</div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
