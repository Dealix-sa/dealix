import type { Metadata } from "next";
import { PublicFunnelLayout } from "@/components/gtm/PublicFunnelLayout";
import { CustomAiBuildLanding } from "@/components/gtm/CustomAiBuildLanding";
import { buildFunnelMetadata } from "@/lib/gtmMetadata";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  return buildFunnelMetadata(locale, "build");
}

export default function BuildPage() {
  return (
    <PublicFunnelLayout>
      <CustomAiBuildLanding />
    </PublicFunnelLayout>
  );
}
