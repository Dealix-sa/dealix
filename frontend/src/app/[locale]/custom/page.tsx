import type { Metadata } from "next";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";
import { CustomSolutionForm } from "@/components/gtm/CustomSolutionForm";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr
      ? "حلول AI مخصّصة — Dealix"
      : "Custom AI Solutions — Dealix",
    description: isAr
      ? "أنظمة ذكاء اصطناعي agentic مخصّصة لقطاعك: الصيانة، المشاريع، المعرفة السيادية، الإيرادات والحوكمة. صف حالتك ونبنيها."
      : "Bespoke agentic AI systems for your sector: maintenance, projects, sovereign knowledge, revenue and governance. Describe your case and we build it.",
    alternates: { canonical: `https://dealix.me/${locale}/custom` },
  };
}

export default async function CustomPage({ params }: PageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";

  return (
    <PublicGtmShell compactNav>
      <div className="mx-auto max-w-5xl px-6 py-12" dir={isAr ? "rtl" : "ltr"}>
        {/* Hero */}
        <header className="rounded-2xl bg-gradient-to-br from-[#001F3F] to-[#0a2040] text-white p-8 md:p-10 mb-12">
          <p className="inline-block rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30 px-3 py-1 text-xs mb-4">
            {isAr ? "حلول مخصّصة — Dealix" : "Custom Solutions — Dealix"}
          </p>
          <h1 className="text-3xl md:text-4xl font-bold leading-tight">
            {isAr
              ? "عندك حالة مخصّصة؟ نصمّمها ونبنيها لك"
              : "Have a custom case? We design & build it for you"}
          </h1>
          <p className="mt-4 text-white/70 max-w-2xl leading-relaxed">
            {isAr
              ? "أنظمة AI agentic كاملة مبنية على بياناتك وسير عملك — بحوكمة، امتثال PDPL، وموافقة بشرية في كل خطوة. نبدأ بتدقيق سريع ونتدرّج إلى نظام تشغيل متكامل."
              : "Full agentic AI systems built on your data and workflows — governed, PDPL-compliant, with human approval at every step. We start with a fast audit and scale to a complete operating system."}
          </p>
          <div className="mt-6 grid grid-cols-2 sm:grid-cols-4 gap-3">
            {(isAr
              ? [
                  { v: "7 أيام", l: "تدقيق مبدئي" },
                  { v: "Agentic", l: "وكلاء AI" },
                  { v: "سيادي", l: "بياناتك تبقى لك" },
                  { v: "موافقة", l: "قبل كل خطوة" },
                ]
              : [
                  { v: "7 days", l: "Initial audit" },
                  { v: "Agentic", l: "AI agents" },
                  { v: "Sovereign", l: "Your data stays yours" },
                  { v: "Approval", l: "Before every step" },
                ]
            ).map((m) => (
              <div key={m.l} className="rounded-xl bg-white/5 border border-white/10 p-3 text-center">
                <p className="text-lg font-bold text-amber-300">{m.v}</p>
                <p className="text-xs text-white/50 mt-0.5">{m.l}</p>
              </div>
            ))}
          </div>
        </header>

        <CustomSolutionForm />
      </div>
    </PublicGtmShell>
  );
}
