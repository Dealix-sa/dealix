import { redirect } from "next/navigation";

interface OfferPageProps {
  params: Promise<{ locale: string }>;
}

/**
 * Legacy standalone offer page (previously listed a conflicting 9,500 SAR
 * price). The canonical, single-source offer ladder now lives on /services
 * and /pricing (mirroring service_catalog/registry.py). Redirect to avoid a
 * divergent pricing surface.
 */
export default async function LeadIntelligenceSprintOfferPage({ params }: OfferPageProps) {
  const { locale } = await params;
  redirect(`/${locale}/services`);
}
