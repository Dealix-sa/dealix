import type { Metadata } from "next";
import { PlatformLanding } from "@/components/gtm/launch/PlatformLanding";
import { buildFunnelMetadata } from "@/lib/gtmMetadata";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  return buildFunnelMetadata(locale, "platform");
}

export default function PlatformPage() {
  return <PlatformLanding />;
}
