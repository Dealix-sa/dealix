import { AppLayout } from "@/components/layout/AppLayout";
import { WhatsAppClientOsPanel } from "@/components/whatsapp/WhatsAppClientOsPanel";
import { WhatsAppOpsTabs } from "@/components/whatsapp/WhatsAppOpsTabs";

interface Props {
  params: Promise<{ locale: string }>;
}

export default async function OpsWhatsAppSessionsPage({ params }: Props) {
  const { locale } = await params;
  const isAr = locale === "ar";

  return (
    <AppLayout
      title={isAr ? "جلسات واتساب" : "WhatsApp sessions"}
      subtitle={isAr ? "الجلسات المحوكمة ومراحلها" : "Governed sessions and their stages"}
    >
      <WhatsAppOpsTabs locale={locale} active="/sessions" />
      <WhatsAppClientOsPanel view="sessions" locale={locale} />
    </AppLayout>
  );
}
