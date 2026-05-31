import type { Metadata } from "next";
import { OnboardingFlow } from "@/components/gtm/OnboardingFlow";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr
      ? "تأهيل العميل — Dealix"
      : "Customer Onboarding — Dealix",
    description: isAr
      ? "ابدأ رحلتك مع Dealix — أكمل إعداد الحساب وأطلق سبرينت ذكاء الإيراد في 4 خطوات."
      : "Start your Dealix journey — complete account setup and launch your Revenue Intelligence Sprint in 4 steps.",
    alternates: { canonical: `https://dealix.me/${locale}/onboarding` },
  };
}

export default function OnboardingPage() {
  return (
    <div className="min-h-screen bg-background flex items-start justify-center py-12 px-4">
      <div className="w-full max-w-2xl">
        {/* Page header */}
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-[var(--dealix-navy)]">
            Dealix
          </h1>
          <p className="text-muted-foreground text-sm mt-2">
            Revenue Intelligence Platform
          </p>
        </div>

        {/* Onboarding wizard */}
        <OnboardingFlow />
      </div>
    </div>
  );
}
