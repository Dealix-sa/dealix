import Link from "next/link";
import { getLocale } from "next-intl/server";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";

interface Rung {
  id: string;
  titleAr: string;
  titleEn: string;
  priceAr: string;
  priceEn: string;
  descAr: string;
  descEn: string;
  ctaAr: string;
  ctaEn: string;
  href: (locale: string) => string;
  highlight?: boolean;
}

const RUNGS: Rung[] = [
  {
    id: "rung0",
    titleAr: "تشخيص العمليات المجاني",
    titleEn: "Free AI Ops Diagnostic",
    priceAr: "مجاني",
    priceEn: "0 SAR",
    descAr: "جلسة ٣٠ دقيقة لمراجعة فجوات العمليات وتحديد أولويات التحسين.",
    descEn: "30-minute session to review ops gaps and identify improvement priorities.",
    ctaAr: "احجز التشخيص",
    ctaEn: "Book diagnostic",
    href: (locale) => `/${locale}/book-call`,
  },
  {
    id: "rung1",
    titleAr: "سبرينت استخبارات الإيراد – ٧ أيام",
    titleEn: "7-Day Revenue Intelligence Sprint",
    priceAr: "٤٩٩ ريال",
    priceEn: "499 SAR",
    descAr: "خطة إيراد قابلة للتنفيذ خلال أسبوع، مبنية على بيانات فعلية من عملك.",
    descEn: "An actionable revenue plan in one week, built on your actual business data.",
    ctaAr: "ابدأ السبرينت",
    ctaEn: "Start sprint",
    href: (locale) => `/${locale}/book-call`,
  },
  {
    id: "rung2",
    titleAr: "حزمة البيانات للإيراد",
    titleEn: "Data-to-Revenue Pack",
    priceAr: "١٬٥٠٠ ريال (مرة واحدة)",
    priceEn: "1,500 SAR (one-time)",
    descAr: "أصول بيانات منظّمة وجاهزة للاستخدام في اتخاذ القرار والتوسع.",
    descEn: "Structured data assets ready for decision-making and growth.",
    ctaAr: "اطلب الحزمة",
    ctaEn: "Request pack",
    href: (locale) => `/${locale}/book-call`,
  },
  {
    id: "rung3",
    titleAr: "إدارة العمليات الإيرادية",
    titleEn: "Managed Revenue Ops",
    priceAr: "٢٬٩٩٩ – ٤٬٩٩٩ ريال / شهر",
    priceEn: "2,999–4,999 SAR / mo",
    descAr: "إدارة مستمرة لمسارات الإيراد، التقارير، والتحسين الدوري.",
    descEn: "Ongoing management of revenue pipelines, reporting, and periodic optimization.",
    ctaAr: "تحدث معنا",
    ctaEn: "Talk to us",
    href: (locale) => `/${locale}/book-call`,
    highlight: true,
  },
  {
    id: "rung4",
    titleAr: "إعداد نظام ذكاء اصطناعي مخصص",
    titleEn: "Custom AI Service Setup",
    priceAr: "٥٬٠٠٠ – ٢٥٬٠٠٠ ريال + ١٬٠٠٠ ريال / شهر",
    priceEn: "5,000–25,000 SAR + 1,000 SAR / mo",
    descAr: "نظام ذكاء اصطناعي مصمم لقطاعك وبياناتك، مع إدارة شهرية مستمرة.",
    descEn: "AI system designed for your sector and data, with ongoing monthly management.",
    ctaAr: "قدّم طلبك",
    ctaEn: "Submit request",
    href: (locale) => `/${locale}/custom-ai`,
  },
  {
    id: "enterprise",
    titleAr: "مراجعة حوكمة الذكاء الاصطناعي",
    titleEn: "AI Governance Review",
    priceAr: "٢٥٬٠٠٠ – ٥٠٬٠٠٠ ريال",
    priceEn: "25,000–50,000 SAR",
    descAr: "تقييم شامل لحوكمة البيانات والذكاء الاصطناعي للمؤسسات الكبيرة.",
    descEn: "Comprehensive data and AI governance assessment for large enterprises.",
    ctaAr: "تواصل مباشرة",
    ctaEn: "Contact directly",
    href: (locale) => `/${locale}/book-call`,
  },
];

export default async function PricingPage() {
  const locale = await getLocale();
  const isAr = locale === "ar";
  const dir = isAr ? "rtl" : "ltr";

  return (
    <PublicGtmShell compactNav>
      <div dir={dir} className="mx-auto max-w-5xl px-6 py-12">
        <div className="mb-10 text-center">
          <h1 className="text-3xl md:text-4xl font-bold tracking-tight text-foreground">
            {isAr ? "الأسعار والخدمات" : "Pricing & Services"}
          </h1>
          <p className="mt-2 text-lg text-muted-foreground max-w-2xl mx-auto">
            {isAr
              ? "سلّم خدمات واضح — ابدأ من حيث يناسبك، وتقدّم بحسب نتائجك الفعلية."
              : "A clear service ladder — start where it fits, advance based on your actual results."}
          </p>
          <p className="mt-2 text-sm text-muted-foreground">
            {isAr
              ? "لا ضمانات على النتائج. القيم المذكورة تقديرية."
              : "No guaranteed outcomes. Values shown are estimates."}
          </p>
        </div>

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {RUNGS.map((rung) => (
            <div
              key={rung.id}
              className={`flex flex-col rounded-xl border p-6 ${
                rung.highlight
                  ? "border-[#D4AF37]/60 bg-[#D4AF37]/5"
                  : "border-border bg-card"
              }`}
            >
              {rung.highlight && (
                <span className="mb-3 inline-block self-start rounded-full bg-[#D4AF37]/20 px-2.5 py-0.5 text-xs font-semibold text-[#D4AF37]">
                  {isAr ? "الأكثر طلباً" : "Most requested"}
                </span>
              )}
              <h2 className="text-base font-semibold text-foreground">
                {isAr ? rung.titleAr : rung.titleEn}
              </h2>
              <p className="mt-1 text-xl font-bold text-[#D4AF37]">
                {isAr ? rung.priceAr : rung.priceEn}
              </p>
              <p className="mt-2 text-sm text-muted-foreground flex-1">
                {isAr ? rung.descAr : rung.descEn}
              </p>
              <div className="mt-4">
                <Link
                  href={rung.href(locale)}
                  className="inline-flex w-full items-center justify-center rounded-lg bg-[#001F3F] px-4 py-2 text-sm font-medium text-white hover:bg-[#001F3F]/80 transition-colors"
                >
                  {isAr ? rung.ctaAr : rung.ctaEn}
                </Link>
              </div>
            </div>
          ))}
        </div>

        <p className="mt-10 text-center text-xs text-muted-foreground border-t border-border pt-4">
          {isAr
            ? "القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value"
            : "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة"}
        </p>
      </div>
    </PublicGtmShell>
  );
}
