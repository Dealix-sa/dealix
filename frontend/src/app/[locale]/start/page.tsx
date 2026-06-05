import type { Metadata } from "next";
import { StartHub } from "@/components/gtm/launch/StartHub";
import { buildFunnelMetadata } from "@/lib/gtmMetadata";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  return buildFunnelMetadata(locale, "start");
}

export default function StartPage() {
  return <StartHub />;
}
