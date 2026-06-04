// Shared content for the Dealix commercial launch pages (AR + EN).
// Trust-first, approval-first. No blind automation. Human-in-the-loop.

export const SITE_URL =
  process.env.NEXT_PUBLIC_SITE_URL ?? "https://dealix.me";

export const HERO = {
  en: {
    title: "Dealix — AI Revenue & Operations OS for Saudi and GCC B2B companies",
    subtitle:
      "AI drafts, ranks, and recommends. You review, approve, and send manually. The system never sends on its own.",
  },
  ar: {
    title:
      "Dealix — نظام تشغيل الإيرادات والعمليات بالذكاء الاصطناعي للشركات السعودية والخليجية",
    subtitle:
      "الذكاء الاصطناعي يصيغ ويرتّب ويوصي. أنت تراجع وتعتمد وترسل يدويًا. النظام لا يرسل من تلقاء نفسه.",
  },
};

export const PRINCIPLES = [
  { en: "Trust-first", ar: "الثقة أولاً" },
  { en: "Approval-first", ar: "الاعتماد أولاً" },
  { en: "No blind automation", ar: "لا أتمتة عمياء" },
  { en: "Human-in-the-loop", ar: "الإنسان في الحلقة" },
];

export type Cta = { id: string; en: string; ar: string; href: string };

export const CTAS: Cta[] = [
  { id: "audit", en: "Request AI Workflow Audit", ar: "اطلب تدقيق سير العمل", href: "/contact" },
  { id: "diagnostic", en: "Book Diagnostic", ar: "احجز جلسة تشخيص", href: "/contact" },
  { id: "pilot", en: "Start Pilot", ar: "ابدأ تجربة", href: "/contact" },
];

export type Vertical = {
  slug: string;
  en: string;
  ar: string;
  painEn: string;
  painAr: string;
};

export const VERTICALS: Vertical[] = [
  {
    slug: "facilities-management",
    en: "Facilities Management & Maintenance",
    ar: "إدارة المرافق والصيانة",
    painEn: "Work-order triage, faster dispatch, and cross-site reporting.",
    painAr: "فرز أوامر العمل وتسريع الإرسال وتقارير المواقع.",
  },
  {
    slug: "contracting-project-controls",
    en: "Contracting & Project Controls",
    ar: "المقاولات وضبط المشاريع",
    painEn: "Tender preparation, progress and cost reporting, submittal review.",
    painAr: "إعداد العطاءات وتقارير التقدم والتكلفة ومراجعة المستندات.",
  },
  {
    slug: "real-estate-property-ops",
    en: "Real Estate & Property Operations",
    ar: "العقار وعمليات إدارة الأملاك",
    painEn: "Listing lead response, tenant requests, renewals and collections.",
    painAr: "الرد على العملاء وطلبات المستأجرين والتجديد والتحصيل.",
  },
  {
    slug: "legal-professional-services",
    en: "Legal & Professional Services",
    ar: "الخدمات القانونية والمهنية",
    painEn: "Client intake and triage, first-draft documents, matter reporting. Privacy-first.",
    painAr: "استقبال العملاء وفرزهم والمسودات الأولى وتقارير القضايا. الخصوصية أولاً.",
  },
  {
    slug: "consulting-training-b2b",
    en: "Consulting, Training & B2B Services",
    ar: "الاستشارات والتدريب وخدمات الأعمال",
    painEn: "Proposal and SOW turnaround, warm-lead follow-up, client reporting.",
    painAr: "إنجاز العروض ونطاقات العمل ومتابعة العملاء وتقارير العملاء.",
  },
];

export type Offer = {
  en: string;
  ar: string;
  price: string;
};

export const OFFERS: Offer[] = [
  { en: "AI Workflow Audit", ar: "تدقيق سير العمل بالذكاء الاصطناعي", price: "499–2,500 SAR" },
  { en: "Paid Pilot", ar: "تجربة مدفوعة", price: "5,000–25,000 SAR" },
  { en: "Department OS", ar: "نظام تشغيل القسم", price: "25,000–150,000 SAR" },
  { en: "Monthly Retainer", ar: "اشتراك شهري", price: "3,000–25,000 SAR / month" },
  { en: "Enterprise Custom OS", ar: "نظام تشغيل مؤسسي مخصص", price: "150,000+ SAR" },
];

export const PROBLEM = {
  en: "Saudi and GCC B2B teams lose hours to manual outreach, slow proposals, and fragmented reporting — while blind automation creates real compliance and reputation risk.",
  ar: "تفقد فرق الأعمال في السعودية والخليج ساعات في التواصل اليدوي والعروض البطيئة والتقارير المبعثرة — بينما تخلق الأتمتة العمياء مخاطر امتثال وسمعة حقيقية.",
};

export const SOLUTION = {
  en: "Dealix is an AI revenue & operations OS. It drafts, ranks, and recommends the work; your team reviews and approves every step; sending stays manual and human-controlled.",
  ar: "Dealix نظام تشغيل للإيرادات والعمليات بالذكاء الاصطناعي. يصيغ ويرتّب ويوصي بالعمل؛ ويراجع فريقك ويعتمد كل خطوة؛ ويبقى الإرسال يدويًا تحت تحكم بشري.",
};

export function orgJsonLd() {
  return {
    "@context": "https://schema.org",
    "@type": "Organization",
    name: "Dealix",
    url: SITE_URL,
    description: HERO.en.subtitle,
    areaServed: ["SA", "AE", "QA", "KW", "BH", "OM"],
  };
}

export function websiteJsonLd() {
  return {
    "@context": "https://schema.org",
    "@type": "WebSite",
    name: "Dealix",
    url: SITE_URL,
    inLanguage: ["ar", "en"],
  };
}

export function serviceJsonLd() {
  return {
    "@context": "https://schema.org",
    "@type": "Service",
    serviceType: "AI Revenue & Operations OS",
    provider: { "@type": "Organization", name: "Dealix", url: SITE_URL },
    areaServed: "Saudi Arabia and GCC",
  };
}

export function breadcrumbJsonLd(items: { name: string; path: string }[]) {
  return {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: items.map((it, i) => ({
      "@type": "ListItem",
      position: i + 1,
      name: it.name,
      item: `${SITE_URL}${it.path}`,
    })),
  };
}

export function faqJsonLd(qa: { q: string; a: string }[]) {
  return {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: qa.map((x) => ({
      "@type": "Question",
      name: x.q,
      acceptedAnswer: { "@type": "Answer", text: x.a },
    })),
  };
}
