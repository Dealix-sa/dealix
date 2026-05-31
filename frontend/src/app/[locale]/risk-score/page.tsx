import type { Metadata } from "next";
import { PublicFunnelLayout } from "@/components/gtm/PublicFunnelLayout";
import { DiagnosticFunnel } from "@/components/gtm/DiagnosticFunnel";
import { buildFunnelMetadata } from "@/lib/gtmMetadata";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  return buildFunnelMetadata(locale, "risk-score");
}

export default function RiskScorePage() {
  return (
    <PublicFunnelLayout>
      <DiagnosticFunnel />
    </PublicFunnelLayout>
  );
}
