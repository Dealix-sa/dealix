import { Mail, MapPin, Phone } from 'lucide-react';

interface Props {
  lang: 'ar' | 'en';
}

const t = {
  ar: {
    company: 'الشركة',
    links: ['عن Dealix', 'الوظائف', 'المدونة', 'الصحافة'],
    product: 'المنتج',
    productLinks: ['المميزات', 'التسعير', 'القطاعات', 'API'],
    resources: 'الموارد',
    resourceLinks: ['التوثيق', 'الدعم', 'الحالة', 'الأمان'],
    legal: 'قانوني',
    legalLinks: ['الخصوصية', 'الشروط', 'PDPL', 'ZATCA'],
    contact: 'تواصل معنا',
    copyright: '© 2025 Dealix. جميع الحقوق محفوظة.',
    tagline: 'نظام تشغيل الإيرادات بالذكاء الاصطناعي',
  },
  en: {
    company: 'Company',
    links: ['About Dealix', 'Careers', 'Blog', 'Press'],
    product: 'Product',
    productLinks: ['Features', 'Pricing', 'Sectors', 'API'],
    resources: 'Resources',
    resourceLinks: ['Documentation', 'Support', 'Status', 'Security'],
    legal: 'Legal',
    legalLinks: ['Privacy', 'Terms', 'PDPL', 'ZATCA'],
    contact: 'Contact Us',
    copyright: '© 2025 Dealix. All rights reserved.',
    tagline: 'AI Revenue Operating System',
  },
};

export default function FooterSection({ lang }: Props) {
  const text = t[lang];

  return (
    <footer className="bg-dealix-charcoal text-white/70 pt-16 pb-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-8 mb-12">
          {/* Brand */}
          <div className="col-span-2 md:col-span-4 lg:col-span-1 mb-4 lg:mb-0">
            <div className="flex items-center gap-2 mb-4">
              <img
                src="/brand/dealix-logo-primary.png"
                alt="Dealix"
                className="h-8 w-auto brightness-0 invert"
              />
              <span className="text-white font-display font-bold text-xl">Dealix</span>
            </div>
            <p className="text-sm text-white/50 mb-4">{text.tagline}</p>
            <div className="space-y-2 text-sm">
              <div className="flex items-center gap-2">
                <Mail className="w-4 h-4 text-dealix-gold" />
                <span>hello@dealix.me</span>
              </div>
              <div className="flex items-center gap-2">
                <Phone className="w-4 h-4 text-dealix-gold" />
                <span>+966 50 000 0000</span>
              </div>
              <div className="flex items-center gap-2">
                <MapPin className="w-4 h-4 text-dealix-gold" />
                <span>Riyadh, Saudi Arabia</span>
              </div>
            </div>
          </div>

          {/* Company */}
          <div>
            <h4 className="text-white font-display font-bold mb-4">{text.company}</h4>
            <ul className="space-y-2 text-sm">
              {text.links.map((link, i) => (
                <li key={i}>
                  <a href="#" className="hover:text-dealix-gold transition-colors">{link}</a>
                </li>
              ))}
            </ul>
          </div>

          {/* Product */}
          <div>
            <h4 className="text-white font-display font-bold mb-4">{text.product}</h4>
            <ul className="space-y-2 text-sm">
              {text.productLinks.map((link, i) => (
                <li key={i}>
                  <a href="#" className="hover:text-dealix-gold transition-colors">{link}</a>
                </li>
              ))}
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h4 className="text-white font-display font-bold mb-4">{text.resources}</h4>
            <ul className="space-y-2 text-sm">
              {text.resourceLinks.map((link, i) => (
                <li key={i}>
                  <a href="#" className="hover:text-dealix-gold transition-colors">{link}</a>
                </li>
              ))}
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h4 className="text-white font-display font-bold mb-4">{text.legal}</h4>
            <ul className="space-y-2 text-sm">
              {text.legalLinks.map((link, i) => (
                <li key={i}>
                  <a href="#" className="hover:text-dealix-gold transition-colors">{link}</a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom */}
        <div className="pt-8 border-t border-white/10 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-sm text-white/40">{text.copyright}</p>
          <div className="flex items-center gap-4">
            <span className="inline-block w-2 h-2 rounded-full bg-green-400 animate-pulse" />
            <span className="text-xs text-white/40">All Systems Operational</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
