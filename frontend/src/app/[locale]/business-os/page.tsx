import type { Metadata } from "next";
import { BusinessOsLanding } from "@/components/gtm/launch/BusinessOsLanding";
import { buildFunnelMetadata } from "@/lib/gtmMetadata";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  return buildFunnelMetadata(locale, "business-os");
}

export default function BusinessOsPage() {
  return <BusinessOsLanding />;
}
