"use client";

import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";
import {
  LaunchHero,
  Section,
  CardGrid,
  CtaBand,
  PillRow,
  Disclosure,
  type Card,
} from "@/components/gtm/launch/kit";

const LAYERS: Card[] = [
  { icon: "💰", title: { ar: "Revenue OS", en: "Revenue OS" }, body: { ar: "خريطة الإيراد، كشف التسرّب، الفرص المُثبتة. الإسفين الأول.", en: "Revenue map, leakage detection, evidenced opportunities. The first wedge." }, status: "BETA" },
  { icon: "📑", title: { ar: "Proof OS", en: "Proof OS" }, body: { ar: "حزمة إثبات من 14 قسمًا، كل قيمة بمستوى تحقّق.", en: "A 14-section proof pack, every value with a verification tier." }, status: "BETA" },
  { icon: "⚖️", title: { ar: "Governance OS", en: "Governance OS" }, body: { ar: "موافقة أولاً، سجل موافقات، audit log كامل.", en: "Approval-first, approval register, full audit log." }, status: "BETA" },
  { icon: "🗄️", title: { ar: "Data OS", en: "Data OS" }, body: { ar: "جواز مصدر، جودة بيانات مُقاسة، حدود استخدام واضحة.", en: "Source passport, measured data quality, clear usage limits." }, status: "BETA" },
  { icon: "🚚", title: { ar: "Delivery", en: "Delivery" }, body: { ar: "إيقاع تسليم يربط القرار بالتنفيذ بالأثر.", en: "A delivery rhythm linking decision to execution to impact." }, status: "BETA" },
  { icon: "🧭", title: { ar: "Command / Founder OS", en: "Command / Founder OS" }, body: { ar: "موجز قيادي يومي وأسبوعي للقرار.", en: "Daily and weekly executive command brief." }, status: "BETA" },
];

export function PlatformLanding() {
  return (
    <PublicGtmShell>
      <LaunchHero
        eyebrow={{ ar: "المنصة", en: "The platform" }}
        title={{ ar: "طبقات نظام تشغيل واحد،", en: "The layers of one OS," }}
        titleAccent={{ ar: "محكومة بالدليل", en: "evidence-governed" }}
        subtitle={{ ar: "ست طبقات تشتغل معًا كنظام تشغيل أعمال واحد — تبدأ من Revenue OS وتتوسّع بعد الإثبات.", en: "Six layers that work as one Business OS — starting with Revenue OS and expanding only after proof." }}
        primary={{ label: { ar: "احسب Business OS Score", en: "Get Business OS Score" }, href: "/business-os-score" }}
        secondary={{ label: { ar: "اعرف عن نظام التشغيل", en: "About the OS" }, href: "/business-os" }}
      />

      <Section
        eyebrow={{ ar: "الطبقات", en: "The layers" }}
        title={{ ar: "نظام واحد، ست طبقات", en: "One system, six layers" }}
      >
        <CardGrid items={LAYERS} cols={3} />
      </Section>

      <Section tone="deep" title={{ ar: "مبادئ التشغيل", en: "Operating principles" }}>
        <PillRow
          items={[
            { ar: "الذكاء يستكشف ويحلّل ويوصي", en: "AI explores, analyzes, recommends" },
            { ar: "المسارات الحتمية تنفّذ", en: "Deterministic workflows execute" },
            { ar: "الإنسان يوافق على الالتزامات الخارجية", en: "Humans approve external commitments" },
          ]}
        />
      </Section>

      <CtaBand
        title={{ ar: "ابدأ بقياس جاهزيتك", en: "Start by measuring readiness" }}
        cta={{ label: { ar: "احسب Business OS Score", en: "Get Business OS Score" }, href: "/business-os-score" }}
      />
      <Disclosure />
    </PublicGtmShell>
  );
}
