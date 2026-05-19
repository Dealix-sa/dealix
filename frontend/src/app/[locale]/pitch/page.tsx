import type { Metadata } from "next";
import { PitchDeck } from "@/components/pitch/PitchDeck";
import type { Lang, PitchContent } from "@/components/pitch/types";
import contentJson from "@/content/pitch/pitch-content.json";

const content = contentJson as unknown as PitchContent;

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({
  params,
}: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  const title = isAr
    ? "Dealix — العرض التقديمي للمبيعات"
    : "Dealix — Sales Pitch Deck";
  const description = isAr
    ? "لماذا Dealix مهم: المشكلة، السوق، المقارنات، الرسوم البيانية، وحساب العائد — بالعربية والإنجليزية."
    : "Why Dealix matters: the problem, the market, comparisons, charts and ROI — in Arabic and English.";
  return {
    title,
    description,
    openGraph: {
      title,
      description,
      locale: isAr ? "ar_SA" : "en_US",
      type: "website",
    },
  };
}

export default async function PitchPage({ params }: PageProps) {
  const { locale } = await params;
  const lang: Lang = locale === "en" ? "en" : "ar";
  return <PitchDeck content={content} lang={lang} />;
}
