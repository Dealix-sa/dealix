import { Button } from '@/components/ui/button';
import { ArrowRight, Calendar } from 'lucide-react';

interface Props {
  lang: 'ar' | 'en';
}

const t = {
  ar: {
    title: 'ابدأ رحلة تحويل أعمالك',
    subtitle: 'احصل على تشخيص مجاني لأعمالك واكتشف كيف يمكن لـ Dealix أن يضاعف إيراداتك',
    ctaPrimary: 'احجز استشارة مجانية',
    ctaSecondary: 'جرب التشخيص المجاني',
    note: 'لا يوجد التزام. التشخيص مجاني تماماً.',
  },
  en: {
    title: 'Start Your Business Transformation',
    subtitle: 'Get a free diagnostic for your business and discover how Dealix can multiply your revenue',
    ctaPrimary: 'Book a Free Consultation',
    ctaSecondary: 'Try Free Diagnostic',
    note: 'No commitment. The diagnostic is completely free.',
  },
};

export default function CTASection({ lang }: Props) {
  const text = t[lang];

  return (
    <section id="cta" className="py-24 relative overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0">
        <img src="/brand/riyadh-skyline.jpg" alt="" className="w-full h-full object-cover" />
        <div className="absolute inset-0 bg-gradient-to-r from-dealix-charcoal/95 via-dealix-charcoal/90 to-dealix-emerald/80" />
      </div>

      <div className="relative z-10 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 className="text-3xl sm:text-4xl lg:text-5xl font-display font-bold text-white mb-6">
          {text.title}
        </h2>
        <p className="text-lg sm:text-xl text-white/70 mb-10 max-w-2xl mx-auto">
          {text.subtitle}
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-8">
          <Button
            size="lg"
            className="bg-dealix-gold hover:bg-dealix-light-gold text-dealix-charcoal px-8 py-6 text-lg font-bold shadow-glow transition-all hover:scale-105"
          >
            <Calendar className="w-5 h-5 mr-2" />
            {text.ctaPrimary}
          </Button>
          <Button
            size="lg"
            variant="outline"
            className="border-white/30 text-white hover:bg-white/10 px-8 py-6 text-lg"
          >
            {text.ctaSecondary}
            <ArrowRight className="w-5 h-5 ml-2" />
          </Button>
        </div>

        <p className="text-sm text-white/40">{text.note}</p>
      </div>
    </section>
  );
}
