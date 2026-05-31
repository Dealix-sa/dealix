import type { Metadata } from "next";
import { ServicesSprintPanelDynamic } from "@/components/services/ServicesSprintPanelDynamic";
import { buildServicesMetadata } from "@/lib/gtmMetadata";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  return buildServicesMetadata(locale);
}

export default async function ServicesHubPage({ params }: Props) {
  const { locale } = await params;
  return <ServicesSprintPanelDynamic locale={locale} />;
}
