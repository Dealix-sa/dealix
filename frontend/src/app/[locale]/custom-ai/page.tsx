import type { Metadata } from "next";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";
import { CustomAiRequestForm } from "@/components/gtm/CustomAiRequestForm";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr
      ? "مشروع AI مخصّص — Dealix | قل لنا ماذا نبني"
      : "Custom AI Project — Dealix | Tell us what to build",
    description: isAr
      ? "تطوير AI مخصّص لعملياتك بـ Scope موقَّع وموافقة بشرية على كل خطوة وProof Pack ختامي. 5,000–25,000 ر.س. PDPL أصيل، لا scraping."
      : "Bespoke AI development for your operations — signed Scope, human approval at every step, final Proof Pack. 5,000–25,000 SAR. PDPL-native, no scraping.",
    alternates: { canonical: `https://dealix.me/${locale}/custom-ai` },
    openGraph: {
      title: isAr ? "مشروع AI مخصّص — Dealix" : "Custom AI Project — Dealix",
      description: isAr
        ? "قل لنا ماذا تريد أن نبني — نحوّله إلى نظام AI موثّق بموافقة وProof Pack."
        : "Tell us what you want built — we turn it into a governed AI system with approval and a Proof Pack.",
      url: `https://dealix.me/${locale}/custom-ai`,
      images: [{ url: "https://dealix.me/brand/og-dealix.svg", width: 1200, height: 630, alt: "Dealix Custom AI Project" }],
    },
  };
}

export default function CustomAiPage() {
  return (
    <PublicGtmShell compactNav>
      <div className="mx-auto max-w-5xl px-6 py-12">
        <CustomAiRequestForm />
      </div>
    </PublicGtmShell>
  );
}
