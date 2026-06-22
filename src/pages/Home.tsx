import CTA from "../sections/CTA";
import Features from "../sections/Features";
import Footer from "../sections/Footer";
import Hero from "../sections/Hero";
import Pricing from "../sections/Pricing";

export default function Home() {
  return (
    <div className="min-h-screen bg-white" dir="rtl">
      <nav className="fixed inset-x-0 top-0 z-50 border-b border-[#E8F4F3] bg-white/90 backdrop-blur-md">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
          <a href="/" className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#15807A]">
              <span className="text-sm font-bold text-white">D</span>
            </div>
            <div>
              <p className="text-lg font-bold text-[#0A1F1E]">Dealix</p>
              <p className="text-[11px] text-[#4A6B69]">
                AI Operating Systems for Saudi B2B
              </p>
            </div>
          </a>

          <div className="hidden items-center gap-7 md:flex">
            <a
              href="#systems"
              className="text-sm text-[#4A6B69] transition-colors hover:text-[#15807A]"
            >
              الأنظمة
            </a>
            <a
              href="#pricing"
              className="text-sm text-[#4A6B69] transition-colors hover:text-[#15807A]"
            >
              الأسعار
            </a>
            <a
              href="/command-room"
              className="text-sm text-[#4A6B69] transition-colors hover:text-[#15807A]"
            >
              Command Room
            </a>
            <a
              href="/brain"
              className="text-sm text-[#4A6B69] transition-colors hover:text-[#15807A]"
            >
              Brain OS
            </a>
          </div>

          <a
            href="/book-call"
            className="rounded-xl bg-[#15807A] px-5 py-2 text-sm font-medium text-white transition-colors hover:bg-[#0F5F5A]"
          >
            احجز تشخيصًا
          </a>
        </div>
      </nav>

      <main>
        <Hero />
        <Features />
        <Pricing />
        <CTA />
      </main>

      <Footer />
    </div>
  );
}