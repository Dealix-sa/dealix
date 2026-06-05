import type { Metadata } from "next";
import { MarketingShell } from "@/components/wave3/MarketingShell";
import { PlatformPage } from "@/components/wave3/PlatformPage";
import { buildWave3Metadata } from "@/lib/gtmMetadata";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  return buildWave3Metadata(
    locale,
    "/platform",
    "المنصة — نظام تشغيل أعمال بالذكاء الاصطناعي",
    "Platform — AI Business Operating System",
    "طبقات تشغيل واحدة: Revenue, Proof, Governance, Delivery, Market Intelligence. تبدأ من Command Sprint.",
    "One set of operating layers: Revenue, Proof, Governance, Delivery, Market Intelligence. You start with a Command Sprint.",
  );
}

export default async function Platform({ params }: PageProps) {
  const { locale } = await params;
  return (
    <MarketingShell locale={locale}>
      <PlatformPage locale={locale} />
    </MarketingShell>
  );
}
