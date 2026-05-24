import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { OpsMandARadar } from "@/components/gtm/OpsMandARadar";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function OpsMandAPage({ params }: PageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "nav" });

  return (
    <AppLayout
      title={locale === "ar" ? "رادار الاستحواذ والاندماج" : "M&A Radar"}
      subtitle={locale === "ar" ? "تقييم الشركات المستهدفة وصياغة خطابات النوايا" : "Evaluate targets & draft Letters of Intent"}
    >
      <OpsMandARadar />
    </AppLayout>
  );
}
