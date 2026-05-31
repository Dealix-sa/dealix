import type { Metadata } from "next";
import { PricingPage } from "@/components/gtm/PricingPage";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr
      ? "تسعير Dealix — خمسة مستويات · ابدأ مجاناً"
      : "Dealix Pricing — Five Tiers · Start Free",
    description: isAr
      ? "من التشخيص المجاني إلى مشاريع AI المخصصة. لا upsell قبل Proof Pack مُسلَّم. جميع الأسعار بالريال السعودي."
      : "From free diagnostic to custom AI projects. No upsell before delivered Proof Pack. All prices in SAR.",
    alternates: { canonical: `https://dealix.me/${locale}/pricing` },
  };
}

export default function PricingPageRoute() {
  return <PricingPage />;
}
