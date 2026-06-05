"use client";

import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";
import {
  LaunchHero,
  Section,
  CardGrid,
  StepList,
  CtaBand,
  Faq,
  PillRow,
  Disclosure,
  type Card,
} from "@/components/gtm/launch/kit";

const MODULES: Card[] = [
  { icon: "🛰️", title: { ar: "ذكاء سوق مختصر", en: "Market Intelligence Lite" }, body: { ar: "قراءة موجزة لسوقك ومنافسيك وإشاراتك — مصادر معلنة فقط، لا scraping خلف تسجيل دخول.", en: "A concise read of your market, competitors and signals — public sources only, no scraping behind logins." } },
  { icon: "🗺️", title: { ar: "خريطة الإيراد", en: "Revenue Map" }, body: { ar: "أين يدخل الإيراد، وأين يتسرّب، وأين الفرص — مبنية على بياناتك أنت.", en: "Where revenue enters, where it leaks, where the opportunities are — built from your own data." } },
  { icon: "📑", title: { ar: "سجل الإثبات", en: "Proof Register" }, body: { ar: "كل ادعاء مربوط بدليل ومستوى تحقّق. لا قيمة بلا إثبات.", en: "Every claim tied to evidence and a verification tier. No value without proof." } },
  { icon: "🧭", title: { ar: "الموجز القيادي", en: "Executive Command Brief" }, body: { ar: "صفحة واحدة للقيادة: ماذا يحدث، وماذا يجب أن يحدث، ولماذا.", en: "One page for leadership: what's happening, what should happen next, and why." } },
  { icon: "✅", title: { ar: "سجل الموافقات", en: "Approval Register" }, body: { ar: "كل إجراء خارجي يمرّ بموافقة بشرية موثّقة قبل التنفيذ.", en: "Every external action passes a logged human approval before it runs." } },
  { icon: "📋", title: { ar: "لوحة الإجراء التالي", en: "Next Action Board" }, body: { ar: "قائمة أولويات قابلة للتنفيذ — من يفعل ماذا ومتى.", en: "An actionable priority board — who does what, by when." } },
  { icon: "🚚", title: { ar: "تسليم مختصر", en: "Delivery Lite" }, body: { ar: "إيقاع تسليم خفيف يربط القرار بالتنفيذ وبالأثر.", en: "A lightweight delivery rhythm linking decision to execution to impact." } },
  { icon: "📈", title: { ar: "توصية التوسّع", en: "Upsell Recommendation" }, body: { ar: "ما الطبقة التالية المناسبة — فقط بعد أن يثبت الإسفين قيمته.", en: "The right next layer — only after the wedge has proven its value." } },
];

const STEPS = [
  { title: { ar: "الجلسة الافتتاحية والوصول الآمن", en: "Kickoff & secure access" }, body: { ar: "نتفق على النطاق والأهداف، ونستلم البيانات عبر مسار آمن ومحكوم. لا وصول خارج النطاق المتفق عليه.", en: "We agree scope and goals, and receive data over a secure, governed path. No access beyond the agreed scope." } },
  { title: { ar: "البناء: من البيانات إلى الخريطة", en: "Build: data to map" }, body: { ar: "نحوّل البيانات المبعثرة إلى خريطة إيراد وسجل إثبات — مع توثيق كل افتراض.", en: "We turn scattered data into a revenue map and proof register — documenting every assumption." } },
  { title: { ar: "الموجز والموافقات", en: "Brief & approvals" }, body: { ar: "نعرض الموجز القيادي وسجل الموافقات؛ المؤسس يوافق على ما يُنفّذ خارجيًا.", en: "We present the executive brief and approval register; the founder approves anything externally executed." } },
  { title: { ar: "التسليم والخطوة التالية", en: "Handover & next step" }, body: { ar: "تستلم حزمة كاملة + لوحة إجراء + توصية توسّع مبنية على الإثبات.", en: "You receive a full pack + action board + an evidence-based expansion recommendation." } },
];

const FAQ = [
  { q: { ar: "هل تضمنون زيادة الإيراد؟", en: "Do you guarantee revenue growth?" }, a: { ar: "لا. لا نقدّم وعود إيراد مضمونة. نقدّم فرصًا مُثبتة بأدلة وقرارات أوضح وإجراءات تالية محدّدة.", en: "No. We make no guaranteed revenue claims. We deliver evidenced opportunities, clearer decisions, and defined next actions." } },
  { q: { ar: "هل ترسلون رسائل للعملاء نيابة عنا؟", en: "Do you message our customers for us?" }, a: { ar: "لا إرسال خارجي تلقائي. أي تواصل خارجي يتطلب موافقة بشرية موثّقة. لا واتساب بارد ولا أتمتة تواصل.", en: "No automated external send. Any external outreach requires a logged human approval. No cold WhatsApp, no outreach automation." } },
  { q: { ar: "ما الذي أستلمه فعليًا؟", en: "What do I actually receive?" }, a: { ar: "الوحدات الثماني أعلاه كحزمة موثّقة ثنائية اللغة، مع سجل إثبات وموافقات ولوحة إجراء تالية.", en: "The eight modules above as a documented bilingual pack, with a proof register, approvals, and a next-action board." } },
  { q: { ar: "هل بياناتي آمنة؟", en: "Is my data safe?" }, a: { ar: "نعم. PDPL أصيل، audit log كامل، لا scraping، ولا وصول خارج النطاق. راجع صفحة الأمان.", en: "Yes. PDPL-native, full audit log, no scraping, no out-of-scope access. See the Security page." } },
];

export function CommandSprintLanding() {
  return (
    <PublicGtmShell>
      <LaunchHero
        eyebrow={{ ar: "الإسفين التجاري الأول", en: "The first commercial wedge" }}
        status="BETA"
        title={{ ar: "ابدأ نظام تشغيل أعمالك عبر", en: "Start your Business OS with a" }}
        titleAccent={{ ar: "Command Sprint", en: "Command Sprint" }}
        subtitle={{ ar: "ثماني وحدات تحوّل الفوضى إلى إيقاع تشغيل واحد: ذكاء سوق، خريطة إيراد، سجل إثبات، موجز قيادي، موافقات، وإجراء تالٍ — بدليل وبموافقة بشرية.", en: "Eight modules that turn chaos into one operating rhythm: market intelligence, revenue map, proof register, executive brief, approvals, and a next action — evidence-led, human-approved." }}
        primary={{ label: { ar: "ابدأ Command Sprint", en: "Start Command Sprint" }, href: "/start" }}
        secondary={{ label: { ar: "احسب Business OS Score", en: "Get Business OS Score" }, href: "/business-os-score" }}
      />

      <Section
        eyebrow={{ ar: "ما يتضمّنه", en: "What's included" }}
        title={{ ar: "ثماني وحدات في حزمة واحدة", en: "Eight modules in one pack" }}
        subtitle={{ ar: "كل وحدة تجيب على سؤال تشغيلي، وكلها محكومة بالدليل والموافقة.", en: "Each module answers one operating question, all governed by evidence and approval." }}
      >
        <CardGrid items={MODULES} cols={4} />
      </Section>

      <Section
        tone="deep"
        eyebrow={{ ar: "كيف يعمل", en: "How it works" }}
        title={{ ar: "من الفوضى إلى القرار في إيقاع محكوم", en: "From chaos to decision in a governed rhythm" }}
      >
        <div className="mx-auto max-w-3xl">
          <StepList steps={STEPS} />
        </div>
      </Section>

      <Section title={{ ar: "مبنيّ على مبادئ غير قابلة للتفاوض", en: "Built on non-negotiables" }}>
        <PillRow
          items={[
            { ar: "لا إثبات مزيّف", en: "No fake proof" },
            { ar: "لا وعود إيراد مضمونة", en: "No guaranteed revenue" },
            { ar: "لا إرسال خارجي تلقائي", en: "No automated external send" },
            { ar: "لا واتساب بارد", en: "No cold WhatsApp" },
            { ar: "لا scraping", en: "No scraping" },
            { ar: "الإنسان يوافق", en: "Humans approve" },
          ]}
        />
      </Section>

      <Section tone="deep" eyebrow={{ ar: "أسئلة شائعة", en: "FAQ" }} title={{ ar: "قبل أن تبدأ", en: "Before you start" }}>
        <Faq items={FAQ} />
      </Section>

      <CtaBand
        title={{ ar: "جاهز لتشغيل شركتك بإيقاع واحد؟", en: "Ready to run on one rhythm?" }}
        subtitle={{ ar: "ابدأ بـ Command Sprint كأول إسفين، ووسّع فقط بعد أن يثبت قيمته.", en: "Start with the Command Sprint as your first wedge, and expand only after it proves its value." }}
        cta={{ label: { ar: "ابدأ Command Sprint", en: "Start Command Sprint" }, href: "/start" }}
      />
      <Disclosure />
    </PublicGtmShell>
  );
}
