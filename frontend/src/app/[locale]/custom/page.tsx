import type { Metadata } from "next";
import { PublicFunnelLayout } from "@/components/gtm/PublicFunnelLayout";
import { CustomSolutionForm } from "@/components/forms/CustomSolutionForm";
import { buildFunnelMetadata } from "@/lib/gtmMetadata";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  return buildFunnelMetadata(locale, "custom");
}

export default function CustomSolutionPage() {
  return (
    <PublicFunnelLayout>
      <CustomSolutionForm />
    </PublicFunnelLayout>
  );
}
