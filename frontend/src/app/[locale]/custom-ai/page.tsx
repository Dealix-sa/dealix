import type { Metadata } from "next";
import { CustomAiPage } from "@/components/gtm/CustomAiPage";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "AI مخصص لعملياتك — Dealix" : "Custom AI for your operations — Dealix",
    description: isAr
      ? "قل لنا ماذا تريد أن نبني — تطوير AI مخصص بنطاق موقّع وموافقة بشرية وProof Pack ختامي. من 5,000 إلى 25,000 ر.س."
      : "Tell us what you want us to build — bespoke AI with signed scope, human approval, and a final Proof Pack. From 5,000 to 25,000 SAR.",
    alternates: { canonical: `https://dealix.me/${locale}/custom-ai` },
  };
}

export default function CustomAiRoute() {
  return <CustomAiPage />;
}
