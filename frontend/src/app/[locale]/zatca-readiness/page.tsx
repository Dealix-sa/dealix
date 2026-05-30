import type { Metadata } from "next";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";
import { ZatcaReadinessQuiz } from "@/components/gtm/ZatcaReadinessQuiz";

type PageProps = { params: Promise<{ locale: string }> };

const SITE = "https://dealix.me";

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  const title = isAr
    ? "هل شركتك جاهزة لـ ZATCA الموجة ٢٤؟ — Dealix"
    : "Is your company ready for ZATCA Wave 24? — Dealix";
  const description = isAr
    ? "موجة ZATCA ٢٤ إلزامية بحلول ٣٠ يونيو ٢٠٢٦ لأي شركة تجاوزت ٣٧٥٬٠٠٠ ريال. خذ الاختبار في ٦٠ ثانية واعرف وضعك."
    : "ZATCA Wave 24 is mandatory by June 30, 2026 for any company exceeding 375,000 SAR. Take the 60-second readiness check.";
  const url = `${SITE}/${locale}/zatca-readiness`;
  const OG = [{ url: `${SITE}/brand/og-dealix.svg`, width: 1200, height: 630, alt: "Dealix" }];
  return {
    title,
    description,
    openGraph: { title, description, url, images: OG },
    alternates: { canonical: url },
  };
}

export default async function ZatcaReadinessPage({ params }: PageProps) {
  const { locale } = await params;
  return (
    <PublicGtmShell compactNav>
      <ZatcaReadinessQuiz locale={locale} />
    </PublicGtmShell>
  );
}
