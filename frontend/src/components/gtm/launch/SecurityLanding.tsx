"use client";

import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";
import {
  LaunchHero,
  Section,
  CardGrid,
  CtaBand,
  Faq,
  Disclosure,
  type Card,
} from "@/components/gtm/launch/kit";

const PILLARS: Card[] = [
  { icon: "✅", title: { ar: "موافقة أولاً", en: "Approval-first" }, body: { ar: "لا إجراء خارجي مواجه للعميل بدون موافقة بشرية موثّقة من المؤسس.", en: "No customer-facing external action without a logged founder approval." } },
  { icon: "📋", title: { ar: "audit log كامل", en: "Full audit log" }, body: { ar: "كل قرار وموافقة وإرسال مسجّل ومرتبط بدليل.", en: "Every decision, approval and send is recorded and tied to evidence." } },
  { icon: "🔒", title: { ar: "PDPL أصيل", en: "PDPL-native" }, body: { ar: "حماية البيانات مبنية في الأساس، لا مضافة لاحقًا.", en: "Data protection built in from the ground up, not bolted on." } },
  { icon: "🚫", title: { ar: "لا تواصل بارد آلي", en: "No cold automation" }, body: { ar: "لا واتساب بارد، لا أتمتة تواصل، لا scraping خلف تسجيل دخول.", en: "No cold WhatsApp, no outreach automation, no scraping behind logins." } },
  { icon: "🧾", title: { ar: "ZATCA جاهز", en: "ZATCA-aware" }, body: { ar: "مهيّأ لمتطلبات الفوترة الإلكترونية السعودية.", en: "Aware of Saudi e-invoicing requirements." } },
  { icon: "📑", title: { ar: "لا ادعاء بلا دليل", en: "No claim without evidence" }, body: { ar: "كل ادعاء عن القيمة مربوط بمستوى تحقّق أو بصياغة آمنة.", en: "Every value claim is tied to a verification tier or safe wording." } },
];

const FAQ = [
  { q: { ar: "هل يمكن لـ Dealix إرسال رسائل دون علمي؟", en: "Can Dealix send messages without my knowledge?" }, a: { ar: "لا. لا إرسال خارجي تلقائي في أي بيئة. كل تواصل خارجي يتطلب موافقتك الموثّقة.", en: "No. No automated external send in any environment. Every external message requires your logged approval." } },
  { q: { ar: "هل تجمعون بيانات من خلف تسجيل الدخول؟", en: "Do you scrape data from behind logins?" }, a: { ar: "لا. لا scraping خلف تسجيل دخول. نعمل بمصادر معلنة وببيانات تشاركها أنت ضمن جواز مصدر.", en: "No. No scraping behind logins. We work with public sources and data you share under a source passport." } },
  { q: { ar: "من يملك قراري النهائي؟", en: "Who holds the final decision?" }, a: { ar: "أنت. الذكاء يستكشف ويوصي، والمسارات الحتمية تنفّذ، والإنسان يوافق على كل التزام خارجي حرج.", en: "You do. AI explores and recommends, deterministic workflows execute, and a human approves every critical external commitment." } },
];

export function SecurityLanding() {
  return (
    <PublicGtmShell>
      <LaunchHero
        eyebrow={{ ar: "الأمان والثقة والحوكمة", en: "Security, Trust & Governance" }}
        title={{ ar: "محكوم بالموافقة،", en: "Approval-first," }}
        titleAccent={{ ar: "مبنيّ على الدليل", en: "evidence-built" }}
        subtitle={{ ar: "Dealix يضع الحوكمة قبل السرعة. لا إرسال خارجي تلقائي، ولا ادعاء بلا دليل، والإنسان يوافق دائمًا.", en: "Dealix puts governance before speed. No automated external send, no claim without evidence, and a human always approves." }}
        primary={{ label: { ar: "ابدأ التشخيص", en: "Run the diagnostic" }, href: "/dealix-diagnostic" }}
        secondary={{ label: { ar: "احسب Business OS Score", en: "Get Business OS Score" }, href: "/business-os-score" }}
      />

      <Section
        eyebrow={{ ar: "ركائز الثقة", en: "Trust pillars" }}
        title={{ ar: "كيف نحمي شركتك وعملاءك", en: "How we protect you and your customers" }}
      >
        <CardGrid items={PILLARS} cols={3} />
      </Section>

      <Section tone="deep" eyebrow={{ ar: "أسئلة شائعة", en: "FAQ" }} title={{ ar: "أسئلة الأمان", en: "Security questions" }}>
        <Faq items={FAQ} />
      </Section>

      <CtaBand
        title={{ ar: "ابدأ بثقة", en: "Start with confidence" }}
        subtitle={{ ar: "تشخيص محكوم بالدليل — أنت تملك كل قرار.", en: "An evidence-governed diagnostic — you own every decision." }}
        cta={{ label: { ar: "ابدأ التشخيص", en: "Run the diagnostic" }, href: "/dealix-diagnostic" }}
      />
      <Disclosure />
    </PublicGtmShell>
  );
}
