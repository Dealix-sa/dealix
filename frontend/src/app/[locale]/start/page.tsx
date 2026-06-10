import type { Metadata } from "next";
import { PublicFunnelLayout } from "@/components/gtm/PublicFunnelLayout";
import { StartDiagnosticForm } from "@/components/wave3/StartDiagnosticForm";
import { buildWave3Metadata } from "@/lib/gtmMetadata";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  return buildWave3Metadata(
    locale,
    "/start",
    "ابدأ التشخيص — Dealix",
    "Start your diagnostic — Dealix",
    "أرسل تشخيصاً مختصراً وسنتواصل معك يدوياً لنرى هل يناسبك Command Sprint. بدون إرسال تلقائي.",
    "Submit a short diagnostic and we'll reach out manually to see if a Command Sprint fits. No auto-send.",
  );
}

export default function Start() {
  return (
    <PublicFunnelLayout>
      <StartDiagnosticForm />
    </PublicFunnelLayout>
  );
}
