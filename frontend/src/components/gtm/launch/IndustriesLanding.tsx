"use client";

import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";
import {
  LaunchHero,
  Section,
  CardGrid,
  CtaBand,
  Disclosure,
  type Card,
} from "@/components/gtm/launch/kit";

const SECTORS: Card[] = [
  { icon: "🏗️", title: { ar: "المقاولات والإنشاء", en: "Construction" }, body: { ar: "عروض ومشاريع ومستخلصات مبعثرة — نوحّدها في خريطة إيراد محكومة وجاهزية ZATCA.", en: "Scattered bids, projects and invoices — unified into a governed revenue map and ZATCA readiness." } },
  { icon: "💼", title: { ar: "الخدمات المهنية", en: "Professional services" }, body: { ar: "ساعات وعقود ومتابعات — ربطها بالإيراد والإثبات والإجراء التالي.", en: "Hours, contracts and follow-ups — tied to revenue, proof and next actions." } },
  { icon: "💻", title: { ar: "التقنية والبرمجيات", en: "Technology & SaaS" }, body: { ar: "خط أنابيب وتجديدات وتوسّع — إيقاع تشغيل واحد محكوم بالدليل.", en: "Pipeline, renewals and expansion — one evidence-governed operating rhythm." } },
  { icon: "📦", title: { ar: "التجارة والتوزيع", en: "Trade & distribution" }, body: { ar: "طلبات وعملاء وذمم — ذاكرة عميل محكومة بدل واتساب وإكسل.", en: "Orders, accounts and receivables — governed client memory instead of WhatsApp and Excel." } },
  { icon: "🏥", title: { ar: "الرعاية والعيادات", en: "Healthcare & clinics" }, body: { ar: "إحالات ومتابعات وامتثال — قرارات بدليل وخصوصية PDPL أصيلة.", en: "Referrals, follow-ups and compliance — evidence-based decisions, PDPL-native privacy." } },
  { icon: "🛡️", title: { ar: "قطاعك غير مذكور؟", en: "Sector not listed?" }, body: { ar: "نظام التشغيل قطاعي-محايد. ابدأ بـ Business OS Score ونرسم خريطتك.", en: "The OS is sector-agnostic. Start with a Business OS Score and we map your case." } },
];

export function IndustriesLanding() {
  return (
    <PublicGtmShell>
      <LaunchHero
        eyebrow={{ ar: "القطاعات", en: "Industries" }}
        title={{ ar: "نظام تشغيل مهيّأ", en: "An OS tuned for" }}
        titleAccent={{ ar: "لقطاعات السعودية", en: "Saudi sectors" }}
        subtitle={{ ar: "نفس الإيقاع، مهيّأ لواقع كل قطاع B2B سعودي — مع PDPL وZATCA في الصميم.", en: "The same rhythm, tuned to each Saudi B2B sector's reality — with PDPL and ZATCA at the core." }}
        primary={{ label: { ar: "احسب Business OS Score", en: "Get Business OS Score" }, href: "/business-os-score" }}
      />

      <Section
        eyebrow={{ ar: "أمثلة قطاعية", en: "Sector examples" }}
        title={{ ar: "كيف يبدو الإيقاع في قطاعك", en: "What the rhythm looks like in your sector" }}
        subtitle={{ ar: "أمثلة توضيحية لكيفية تطبيق نظام التشغيل — تُخصَّص على بيانات شركتك.", en: "Illustrative examples of how the OS applies — tailored to your company's data." }}
      >
        <CardGrid items={SECTORS} cols={3} />
      </Section>

      <CtaBand
        title={{ ar: "اعرف أين تقف شركتك", en: "See where your company stands" }}
        cta={{ label: { ar: "احسب Business OS Score", en: "Get Business OS Score" }, href: "/business-os-score" }}
      />
      <Disclosure />
    </PublicGtmShell>
  );
}
