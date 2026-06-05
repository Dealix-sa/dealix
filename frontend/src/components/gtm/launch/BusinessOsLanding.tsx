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

const QUESTIONS: Card[] = [
  { icon: "👁️", title: { ar: "ماذا يحدث؟", en: "What is happening?" }, body: { ar: "صورة واحدة موحّدة بدل واتساب وإكسل واجتماعات مبعثرة.", en: "One unified picture instead of scattered WhatsApp, Excel and meetings." } },
  { icon: "➡️", title: { ar: "ماذا يجب أن يحدث؟", en: "What should happen next?" }, body: { ar: "أولويات واضحة مبنية على الدليل، لا على الانطباع.", en: "Clear, evidence-based priorities — not gut feel." } },
  { icon: "✅", title: { ar: "من يوافق؟", en: "Who approves?" }, body: { ar: "كل التزام خارجي يمرّ بموافقة بشرية موثّقة.", en: "Every external commitment passes a logged human approval." } },
  { icon: "📑", title: { ar: "ما الدليل؟", en: "What is the evidence?" }, body: { ar: "كل قرار مربوط بسجل إثبات ومستوى تحقّق.", en: "Every decision tied to a proof register and verification tier." } },
  { icon: "📋", title: { ar: "ما الإجراء التالي؟", en: "What is the next action?" }, body: { ar: "لوحة إجراء تالٍ: من يفعل ماذا ومتى.", en: "A next-action board: who does what, by when." } },
];

const LAYERS: Card[] = [
  { icon: "💰", title: { ar: "Revenue OS", en: "Revenue OS" }, body: { ar: "خريطة الإيراد وكشف التسرّب والفرص. الإسفين الأول.", en: "Revenue map, leakage detection and opportunities. The first wedge." }, tag: { ar: "نقطة البداية", en: "Entry point" }, status: "BETA" },
  { icon: "📑", title: { ar: "Proof OS", en: "Proof OS" }, body: { ar: "كل ادعاء بدليل ومستوى تحقّق. لا قيمة بلا إثبات.", en: "Every claim with evidence and a tier. No value without proof." }, status: "BETA" },
  { icon: "⚖️", title: { ar: "Governance OS", en: "Governance OS" }, body: { ar: "موافقة أولاً، audit log كامل، حدود واضحة.", en: "Approval-first, full audit log, clear boundaries." }, status: "BETA" },
  { icon: "🗄️", title: { ar: "Data OS", en: "Data OS" }, body: { ar: "بيانات محكومة بجواز مصدر وجودة مُقاسة.", en: "Data governed by a source passport and measured quality." }, status: "BETA" },
  { icon: "🚚", title: { ar: "Delivery", en: "Delivery" }, body: { ar: "ربط القرار بالتنفيذ بالأثر في إيقاع واحد.", en: "Linking decision to execution to impact in one rhythm." }, status: "BETA" },
  { icon: "🧭", title: { ar: "Command / Founder OS", en: "Command / Founder OS" }, body: { ar: "موجز قيادي يومي وأسبوعي لاتخاذ القرار.", en: "Daily and weekly executive brief for decision-making." }, status: "BETA" },
  { icon: "🏢", title: { ar: "Enterprise OS", en: "Enterprise OS" }, body: { ar: "توسّع مؤسسي متعدد الفرق والوحدات.", en: "Enterprise expansion across teams and units." }, status: "FUTURE" },
  { icon: "🤝", title: { ar: "Partner OS", en: "Partner OS" }, body: { ar: "توزيع عبر شبكة شركاء محكومة.", en: "Distribution through a governed partner network." }, status: "FUTURE" },
];

const PAIN: Card[] = [
  { icon: "💬", title: { ar: "واتساب لا ينتهي", en: "Endless WhatsApp" }, body: { ar: "قرارات وصفقات مدفونة في محادثات لا يجدها أحد لاحقًا.", en: "Decisions and deals buried in chats no one can find later." } },
  { icon: "📊", title: { ar: "إكسل متناثر", en: "Scattered Excel" }, body: { ar: "نسخ متعددة، أرقام متضاربة، لا مصدر واحد للحقيقة.", en: "Many copies, conflicting numbers, no single source of truth." } },
  { icon: "🗣️", title: { ar: "اجتماعات بلا أثر", en: "Meetings without trace" }, body: { ar: "قرارات تُتخذ وتُنسى، ولا أحد يعرف الإجراء التالي.", en: "Decisions made then forgotten, with no clear next action." } },
];

export function BusinessOsLanding() {
  return (
    <PublicGtmShell>
      <LaunchHero
        eyebrow={{ ar: "نظام تشغيل الأعمال", en: "The Business Operating System" }}
        title={{ ar: "شغّل شركتك بإيقاع واحد", en: "Run your company on one" }}
        titleAccent={{ ar: "بالذكاء الاصطناعي", en: "operating rhythm" }}
        subtitle={{ ar: "Dealix ليس مجرد CRM أو شات بوت أو وكالة. إنه نظام تشغيل أعمال سعودي بالذكاء الاصطناعي — وRevenue OS هو أول إسفين فيه.", en: "Dealix is not just a CRM, chatbot, or agency. It is a Saudi AI Business Operating System — and Revenue OS is its first wedge." }}
        primary={{ label: { ar: "احسب Business OS Score", en: "Get Business OS Score" }, href: "/business-os-score" }}
        secondary={{ label: { ar: "ابدأ Command Sprint", en: "Start Command Sprint" }, href: "/command-sprint" }}
      />

      <Section
        eyebrow={{ ar: "المشكلة", en: "The problem" }}
        title={{ ar: "العمل مبعثر، والقرار بطيء", en: "Work is scattered, decisions are slow" }}
      >
        <CardGrid items={PAIN} cols={3} />
      </Section>

      <Section
        tone="deep"
        eyebrow={{ ar: "الحل", en: "The solution" }}
        title={{ ar: "خمسة أسئلة، إجابة واحدة محكومة", en: "Five questions, one governed answer" }}
        subtitle={{ ar: "نظام التشغيل يجيب باستمرار على الأسئلة الخمسة التي تدير بها شركتك.", en: "The OS continuously answers the five questions you run your company by." }}
      >
        <CardGrid items={QUESTIONS} cols={3} />
      </Section>

      <Section
        eyebrow={{ ar: "الطبقات", en: "The layers" }}
        title={{ ar: "نظام واحد منظّم في طبقات", en: "One system organized in layers" }}
        subtitle={{ ar: "الطبقات ليست منتجات منفصلة تُشترى بالقطعة عند الإطلاق — إنها طريقة تنظيم نظام تشغيل واحد.", en: "Layers are not separate products to buy à la carte at launch — they are how one OS is organized." }}
      >
        <CardGrid items={LAYERS} cols={4} />
      </Section>

      <Section tone="deep" title={{ ar: "محكوم بالدليل والموافقة", en: "Evidence-governed, approval-first" }}>
        <PillRow
          items={[
            { ar: "PDPL أصيل", en: "PDPL-native" },
            { ar: "ZATCA جاهز", en: "ZATCA-aware" },
            { ar: "audit log كامل", en: "Full audit log" },
            { ar: "لا إرسال خارجي تلقائي", en: "No automated external send" },
            { ar: "لا إثبات مزيّف", en: "No fake proof" },
          ]}
        />
      </Section>

      <CtaBand
        title={{ ar: "ابدأ بقياس جاهزيتك", en: "Start by measuring your readiness" }}
        subtitle={{ ar: "احسب Business OS Score المجاني في دقيقتين، ثم اختر خطوتك التالية.", en: "Get your free Business OS Score in two minutes, then choose your next step." }}
        cta={{ label: { ar: "احسب Business OS Score", en: "Get Business OS Score" }, href: "/business-os-score" }}
      />
      <Disclosure />
    </PublicGtmShell>
  );
}
