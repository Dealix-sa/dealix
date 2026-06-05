import type { Metadata } from "next";
import { SecurityLanding } from "@/components/gtm/launch/SecurityLanding";
import { buildFunnelMetadata } from "@/lib/gtmMetadata";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  return buildFunnelMetadata(locale, "security");
}

export default function SecurityPage() {
  return <SecurityLanding />;
}
