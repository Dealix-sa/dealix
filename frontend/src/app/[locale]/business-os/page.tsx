import type { Metadata } from "next";
import { MarketingShell } from "@/components/wave3/MarketingShell";
import { BusinessOsPage } from "@/components/wave3/BusinessOsPage";
import { buildWave3Metadata } from "@/lib/gtmMetadata";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  return buildWave3Metadata(
    locale,
    "/business-os",
    "Business OS — صورة تشغيل واحدة",
    "Business OS — one operating picture",
    "نحوّل ما بداخل أدواتك إلى صورة قرار. دييلكس ليس CRM ولا شات بوت. موافقة أولاً.",
    "We turn what's inside your tools into a decision picture. Dealix is not a CRM or a chatbot. Approval-first.",
  );
}

export default async function BusinessOs({ params }: PageProps) {
  const { locale } = await params;
  return (
    <MarketingShell locale={locale}>
      <BusinessOsPage locale={locale} />
    </MarketingShell>
  );
}
