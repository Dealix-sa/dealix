import type { Metadata } from "next";
import { PublicFunnelLayout } from "@/components/gtm/PublicFunnelLayout";
import { ToolRunner } from "@/components/wave3/tools/ToolRunner";
import { businessOsScore } from "@/content/wave3/tools/businessOsScore";
import { buildWave3Metadata } from "@/lib/gtmMetadata";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  return buildWave3Metadata(
    locale,
    "/tools/business-os-score",
    "Business OS Score — قِس وضوح تشغيل أعمالك",
    "Business OS Score — Measure how clearly your business runs",
    "خمسة أسئلة سريعة تعطيك نتيجة وأهم 3 فجوات وخطوتك التالية. استرشادي وآمن.",
    "Five quick questions giving you a score, your top 3 gaps, and your next step. Indicative and safe.",
  );
}

export default function BusinessOsScorePage() {
  return (
    <PublicFunnelLayout>
      <ToolRunner tool={businessOsScore} source="tool_business_os_score" />
    </PublicFunnelLayout>
  );
}
