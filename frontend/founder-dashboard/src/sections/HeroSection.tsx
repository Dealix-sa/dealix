import { Button } from '@/components/ui/button';
import { ArrowDown, Sparkles } from 'lucide-react';

interface HeroProps {
  lang: 'ar' | 'en';
}

const t = {
  ar: {
    badge: 'نظام تشغيل الإيرادات بالذكاء الاصطناعي',
    headline: 'حوّل أعمالك السعودية بـ',
    headlineHighlight: 'قوة الذكاء الاصطناعي',
    subheadline:
      'Dealix هو النظام الأول في السعودية لإدارة الإيرادات والنمو والثقة — مدعوم بالذكاء الاصطناعي ومتوافق مع PDPL وZATCA',
    ctaPrimary: 'احصل على تشخيص مجاني',
    ctaSecondary: 'شاهد كيف يعمل',
    stats: [
      { value: '500+', label: 'اختبار تلقائي' },
      { value: '172', label: 'نقطة API' },
      { value: '100%', label: 'متوافق مع PDPL' },
    ],
  },
  en: {
    badge: 'AI Revenue Operating System',
    headline: 'Transform Your Saudi Business with',
    headlineHighlight: 'AI-Powered Intelligence',
    subheadline:
      'Dealix is Saudi Arabia\'s first Revenue, Growth & Trust Operating System — AI-driven, PDPL & ZATCA compliant',
    ctaPrimary: 'Get Free Diagnostic',
    ctaSecondary: 'See How It Works',
    stats: [
      { value: '500+', label: 'Automated Tests' },
      { value: '172', label: 'API Endpoints' },
      { value: '100%', label: 'PDPL Compliant' },
    ],
  },
};

export default function HeroSection({ lang }: HeroProps) {
  const text = t[lang];

  return (
    <section
      id="hero"
      className="relative min-h-screen flex items-center justify-center overflow-hidden"
    >
      {/* Background */}
      <div className="absolute inset-0">
        <img
          src="/brand/hero-bg-dark.jpg"
          alt=""
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-dealix-charcoal/70 via-dealix-charcoal/50 to-dealix-charcoal/90" />
      </div>

      {/* Content */}
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-32 text-center">
        {/* Badge */}
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 backdrop-blur-sm border border-dealix-gold/30 mb-8">
          <Sparkles className="w-4 h-4 text-dealix-gold" />
          <span className="text-sm text-dealix-light-gold font-medium">
            {text.badge}
          </span>
        </div>

        {/* Headline */}
        <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-display font-bold text-white leading-tight mb-6">
          {text.headline}
          <br />
          <span className="text-gradient-gold">{text.headlineHighlight}</span>
        </h1>

        {/* Subheadline */}
        <p className="max-w-3xl mx-auto text-lg sm:text-xl text-white/70 leading-relaxed mb-10">
          {text.subheadline}
        </p>

        {/* CTAs */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
          <Button
            size="lg"
            className="bg-dealix-emerald hover:bg-dealix-forest text-white px-8 py-6 text-lg shadow-glow-emerald transition-all hover:scale-105"
          >
            {text.ctaPrimary}
          </Button>
          <Button
            size="lg"
            variant="outline"
            className="border-dealix-gold/50 text-dealix-gold hover:bg-dealix-gold/10 px-8 py-6 text-lg"
            onClick={() => document.getElementById('howitworks')?.scrollIntoView()}
          >
            {text.ctaSecondary}
          </Button>
        </div>

        {/* Stats */}
        <div className="flex flex-wrap items-center justify-center gap-8 sm:gap-16">
          {text.stats.map((stat, i) => (
            <div key={i} className="text-center">
              <div className="text-3xl sm:text-4xl font-display font-bold text-dealix-gold mb-1">
                {stat.value}
              </div>
              <div className="text-sm text-white/50">{stat.label}</div>
            </div>
          ))}
        </div>

        {/* Scroll indicator */}
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
          <ArrowDown className="w-6 h-6 text-white/30" />
        </div>
      </div>
    </section>
  );
}
