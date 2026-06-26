import { getLocale } from "next-intl/server";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";

interface PolicySection {
  icon: string;
  headingAr: string;
  headingEn: string;
  bulletsAr: string[];
  bulletsEn: string[];
  docHref?: string;
  docLabelAr?: string;
  docLabelEn?: string;
}

const SECTIONS: PolicySection[] = [
  {
    icon: "shield",
    headingAr: "الامتثال لنظام PDPL",
    headingEn: "PDPL Compliance",
    bulletsAr: [
      "تُعالج البيانات الشخصية وفق نظام حماية البيانات الشخصية السعودي (PDPL).",
      "لا تُشارك البيانات مع أطراف ثالثة بدون موافقة صريحة من صاحبها.",
      "يحق لكل عميل طلب الاطلاع على بياناته أو حذفها في أي وقت.",
    ],
    bulletsEn: [
      "Personal data is processed under Saudi Arabia's Personal Data Protection Law (PDPL).",
      "Data is not shared with third parties without explicit consent from the data subject.",
      "Every client may request access to or deletion of their data at any time.",
    ],
    docHref: "/docs/pdpl-policy.pdf",
    docLabelAr: "سياسة PDPL الكاملة",
    docLabelEn: "Full PDPL policy",
  },
  {
    icon: "minimize",
    headingAr: "تقليص البيانات",
    headingEn: "Data Minimization",
    bulletsAr: [
      "نجمع فقط البيانات الضرورية لتقديم الخدمة المطلوبة.",
      "لا يتم تخزين البيانات الحساسة بعد انتهاء الغرض منها.",
      "تُحدَّد فترة الاحتفاظ بالبيانات بوضوح في كل عقد.",
    ],
    bulletsEn: [
      "We collect only the data necessary to deliver the requested service.",
      "Sensitive data is not retained after its purpose is fulfilled.",
      "Retention periods are stated explicitly in each engagement contract.",
    ],
  },
  {
    icon: "gate",
    headingAr: "بوابات الاعتماد البشري",
    headingEn: "Human Approval Gates",
    bulletsAr: [
      "لا إجراء خارجي بلا اعتماد المؤسس — رسائل، عروض، أو فواتير.",
      "جميع مخرجات الذكاء الاصطناعي تمر عبر مراجعة بشرية قبل الإرسال.",
      "قائمة الانتظار للموافقة متاحة دائماً للمراجعة الداخلية.",
    ],
    bulletsEn: [
      "No external action without founder approval — messages, proposals, or invoices.",
      "All AI outputs pass through human review before delivery.",
      "The approval queue is always available for internal audit.",
    ],
    docHref: "/docs/approval-gate-policy.pdf",
    docLabelAr: "سياسة بوابات الاعتماد",
    docLabelEn: "Approval gate policy",
  },
  {
    icon: "ai",
    headingAr: "سياسة استخدام الذكاء الاصطناعي",
    headingEn: "AI Usage Policy",
    bulletsAr: [
      "لا يُستخدم الذكاء الاصطناعي لتقديم ادعاءات مضمونة أو وعود بنتائج محددة.",
      "لا يتم تشغيل أتمتة على قنوات خارجية (واتساب، لينكدإن) بدون إذن صريح.",
      "تُوثَّق جميع قرارات الذكاء الاصطناعي مع السياق الذي بُني عليه القرار.",
    ],
    bulletsEn: [
      "AI is not used to make guaranteed claims or promise specific outcomes.",
      "No automation runs on external channels (WhatsApp, LinkedIn) without explicit permission.",
      "All AI decisions are logged with the context on which the decision was based.",
    ],
    docHref: "/docs/ai-usage-policy.pdf",
    docLabelAr: "سياسة استخدام الذكاء الاصطناعي",
    docLabelEn: "AI usage policy",
  },
];

const ICON_MAP: Record<string, string> = {
  shield: "[S]",
  minimize: "[M]",
  gate: "[G]",
  ai: "[A]",
};

export default async function TrustCenterPage() {
  const locale = await getLocale();
  const isAr = locale === "ar";
  const dir = isAr ? "rtl" : "ltr";

  return (
    <PublicGtmShell compactNav>
      <div dir={dir} className="mx-auto max-w-4xl px-6 py-12">
        <div className="mb-10">
          <h1 className="text-3xl md:text-4xl font-bold tracking-tight text-foreground">
            {isAr ? "مركز الثقة والحوكمة" : "Trust & Governance Center"}
          </h1>
          <p className="mt-2 text-lg text-muted-foreground max-w-2xl">
            {isAr
              ? "كيف نحمي بياناتك، ونحكم استخدام الذكاء الاصطناعي، ونضمن الرقابة البشرية في كل خطوة."
              : "How we protect your data, govern AI usage, and ensure human oversight at every step."}
          </p>
        </div>

        {/* Prominent approval gate notice */}
        <div className="mb-8 rounded-xl border border-[#D4AF37]/50 bg-[#D4AF37]/5 p-5">
          <p className="text-center font-semibold text-[#D4AF37] text-base">
            {isAr
              ? "لا إجراء خارجي بلا اعتماد المؤسس / No external action without founder approval"
              : "No external action without founder approval / لا إجراء خارجي بلا اعتماد المؤسس"}
          </p>
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          {SECTIONS.map((section) => (
            <div
              key={section.headingEn}
              className="rounded-xl border border-border bg-card p-6"
            >
              <div className="flex items-center gap-3 mb-4">
                <span className="text-2xl font-mono text-[#D4AF37]" aria-hidden>
                  {ICON_MAP[section.icon]}
                </span>
                <h2 className="text-base font-semibold text-foreground">
                  {isAr ? section.headingAr : section.headingEn}
                  {" / "}
                  <span className="text-muted-foreground text-sm font-normal">
                    {isAr ? section.headingEn : section.headingAr}
                  </span>
                </h2>
              </div>
              <ul className="space-y-2">
                {(isAr ? section.bulletsAr : section.bulletsEn).map(
                  (bullet, i) => (
                    <li
                      key={i}
                      className="flex items-start gap-2 text-sm text-muted-foreground"
                    >
                      <span className="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-[#10b981]" />
                      {bullet}
                    </li>
                  )
                )}
              </ul>
              {section.docHref && (
                <div className="mt-4">
                  <a
                    href={section.docHref}
                    className="text-xs text-[#D4AF37] underline hover:no-underline"
                  >
                    {isAr ? section.docLabelAr : section.docLabelEn}
                  </a>
                </div>
              )}
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
