import { useState, useEffect } from 'react';
import { Menu, X } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface NavbarProps {
  lang: 'ar' | 'en';
  setLang: (lang: 'ar' | 'en') => void;
}

const t = {
  ar: {
    nav: ['الرئيسية', 'المميزات', 'القطاعات', 'كيف يعمل', 'الأسعار', 'ابدأ الآن'],
    start: 'ابدأ الآن',
  },
  en: {
    nav: ['Home', 'Features', 'Sectors', 'How It Works', 'Pricing', 'Get Started'],
    start: 'Get Started',
  },
};

const navLinks = ['#hero', '#features', '#sectors', '#howitworks', '#pricing', '#cta'];

export default function Navbar({ lang, setLang }: NavbarProps) {
  const [isScrolled, setIsScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 50);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const text = t[lang];

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        isScrolled
          ? 'bg-dealix-charcoal/95 backdrop-blur-md shadow-lg'
          : 'bg-transparent'
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 lg:h-20">
          {/* Logo */}
          <a href="#hero" className="flex items-center gap-2 shrink-0">
            <img
              src="/brand/dealix-logo-primary.png"
              alt="Dealix"
              className="h-8 w-auto brightness-0 invert"
            />
            <span className="text-white font-display font-bold text-xl tracking-wide">
              Dealix
            </span>
          </a>

          {/* Desktop Nav */}
          <div className="hidden lg:flex items-center gap-1">
            {text.nav.slice(0, -1).map((item, i) => (
              <a
                key={i}
                href={navLinks[i]}
                className="px-3 py-2 text-sm text-white/70 hover:text-dealix-gold transition-colors duration-200"
              >
                {item}
              </a>
            ))}
          </div>

          {/* Actions */}
          <div className="hidden lg:flex items-center gap-3">
            <button
              onClick={() => setLang(lang === 'ar' ? 'en' : 'ar')}
              className="px-3 py-1.5 text-sm text-white/70 hover:text-dealix-gold border border-white/20 rounded-md hover:border-dealix-gold/50 transition-all"
            >
              {lang === 'ar' ? 'EN' : 'AR'}
            </button>
            <Button
              className="bg-dealix-emerald hover:bg-dealix-forest text-white px-5"
            >
              {text.start}
            </Button>
          </div>

          {/* Mobile Toggle */}
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="lg:hidden p-2 text-white"
          >
            {mobileOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {mobileOpen && (
        <div className="lg:hidden bg-dealix-charcoal/98 backdrop-blur-md border-t border-white/10">
          <div className="px-4 py-4 space-y-2">
            {text.nav.slice(0, -1).map((item, i) => (
              <a
                key={i}
                href={navLinks[i]}
                onClick={() => setMobileOpen(false)}
                className="block px-3 py-2 text-white/80 hover:text-dealix-gold"
              >
                {item}
              </a>
            ))}
            <div className="pt-3 border-t border-white/10 flex items-center gap-3">
              <button
                onClick={() => setLang(lang === 'ar' ? 'en' : 'ar')}
                className="px-3 py-1.5 text-sm text-white/70 border border-white/20 rounded-md"
              >
                {lang === 'ar' ? 'EN' : 'AR'}
              </button>
              <Button className="bg-dealix-emerald hover:bg-dealix-forest text-white flex-1">
                {text.start}
              </Button>
            </div>
          </div>
        </div>
      )}
    </nav>
  );
}
