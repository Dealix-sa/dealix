import type { Metadata } from "next";
import { BusinessOsScoreTool } from "@/components/gtm/launch/BusinessOsScoreTool";
import { buildFunnelMetadata } from "@/lib/gtmMetadata";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  return buildFunnelMetadata(locale, "business-os-score");
}

export default function BusinessOsScorePage() {
  return <BusinessOsScoreTool />;
}
