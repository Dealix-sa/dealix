import { AppLayout } from "@/components/layout/AppLayout";
import { WhatsAppClientOsPanel } from "@/components/whatsapp/WhatsAppClientOsPanel";
import { WhatsAppOpsTabs } from "@/components/whatsapp/WhatsAppOpsTabs";

interface Props {
  params: Promise<{ locale: string }>;
}

export default async function OpsWhatsAppPage({ params }: Props) {
  const { locale } = await params;
  const isAr = locale === "ar";

  return (
    <AppLayout
      title={isAr ? "WhatsApp Client OS" : "WhatsApp Client OS"}
      subtitle={isAr ? "تجربة العميل المحوكمة على واتساب" : "Governed client WhatsApp experience"}
    >
      <WhatsAppOpsTabs locale={locale} active="" />
      <WhatsAppClientOsPanel view="overview" locale={locale} />
    </AppLayout>
  );
}
