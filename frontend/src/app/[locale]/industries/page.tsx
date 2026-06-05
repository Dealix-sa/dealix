import type { Metadata } from "next";
import { IndustriesLanding } from "@/components/gtm/launch/IndustriesLanding";
import { buildFunnelMetadata } from "@/lib/gtmMetadata";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  return buildFunnelMetadata(locale, "industries");
}

export default function IndustriesPage() {
  return <IndustriesLanding />;
}
