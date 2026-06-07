import type { Metadata } from "next";
import { buildFunnelMetadata } from "@/lib/gtmMetadata";
import { AppLayout } from "@/components/layout/AppLayout";
import { TrustCenter } from "@/components/trust/TrustCenter";

type TrustCenterPageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: TrustCenterPageProps): Promise<Metadata> {
  const { locale } = await params;
  return buildFunnelMetadata(locale, "trust-center");
}

export default async function TrustCenterPage({ params }: TrustCenterPageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";

  return (
    <AppLayout
      title={isAr ? "مركز الثقة" : "Trust Center"}
      subtitle={
        isAr
          ? "شهادات الامتثال وسياسات الأمان"
          : "Compliance certificates and security policies"
      }
    >
      <TrustCenter />
    </AppLayout>
  );
}
